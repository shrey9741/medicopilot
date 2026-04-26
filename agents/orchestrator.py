"""
MediCopilot Orchestrator — the main A2A agent.
Coordinates all sub-agents in sequence, builds reasoning trace,
and returns a complete structured clinical briefing.
"""
import os
import asyncio
from datetime import datetime
from langchain_community.vectorstores import FAISS

from fhir.mock_client import get_patient_bundle as get_mock_bundle, get_patient_history
from fhir.hapi_client import HAPIFHIRClient
from rag.retriever import retrieve_context
from agents.anomaly_detector import detect_anomalies
from agents.memory import update_memory, load_history, analyze_trends
from agents.diagnosis_agent import run_diagnosis_agent
from agents.drug_agent import run_drug_agent
from agents.risk_agent import run_risk_agent
from agents.second_opinion_agent import run_second_opinion
from agents.soap_generator import generate_soap_note
from models.schemas import MediCopilotResponse, ReasoningStep


def run_medicopilot(
    patient_id: str,
    vectorstore: FAISS,
    sharp_token: str = None
) -> MediCopilotResponse:
    """
    Full orchestration pipeline.
    Tries HAPI FHIR first for real patient data, falls back to mock.
    Returns a complete MediCopilotResponse with all 6 features.
    """
    reasoning_trace: list[ReasoningStep] = []

    # ── Step 1: Fetch FHIR patient data ─────────────────────────────────────

    use_mock = os.getenv("FHIR_USE_MOCK", "false").lower() == "true"
    fhir_source = "mock"

    # Try HAPI FHIR first
    if not use_mock:
        try:
            client = HAPIFHIRClient()
            loop = asyncio.new_event_loop()
            bundle = loop.run_until_complete(client.get_patient_bundle(patient_id))
            fhir_data = client.parse_bundle(bundle, patient_id)
            loop.run_until_complete(client.close())
            loop.close()
            fhir_source = "hapi_fhir"
        except Exception as e:
            fhir_source = "mock"

    # Always use mock patient object for agent pipeline
    # (agents expect the mock Patient dataclass structure)
    patient = get_mock_bundle(patient_id)
    fhir_history = get_patient_history(patient_id)

    # If we got real FHIR data, enrich the mock patient with real conditions/meds
    if fhir_source == "hapi_fhir" and fhir_data:
        try:
            if fhir_data.get("conditions"):
                real_conditions = [
                    c["name"] for c in fhir_data["conditions"]
                    if isinstance(c, dict) and c.get("name")
                ]
                if real_conditions:
                    patient.conditions = real_conditions[:5]

            if fhir_data.get("medications"):
                real_meds = [
                    m["name"] for m in fhir_data["medications"]
                    if isinstance(m, dict) and m.get("name")
                ]
                if real_meds:
                    patient.medications = real_meds[:8]

            if fhir_data.get("patient_name") and fhir_data["patient_name"] != f"FHIR Patient {patient_id}":
                patient.name = fhir_data["patient_name"]

        except Exception:
            pass  # If enrichment fails, continue with mock data

    reasoning_trace.append(ReasoningStep(
        agent="FHIRAgent",
        action=f"Fetched patient bundle for {patient_id} (source: {fhir_source})",
        finding=f"{patient.name}, {patient.age}y — {len(patient.conditions)} conditions, {len(patient.medications)} medications"
    ))

    # ── Step 2: Load memory and analyze trends ───────────────────────────────

    load_history(patient_id, fhir_history)
    update_memory(patient)
    memory_trend = analyze_trends(patient_id)

    if memory_trend:
        reasoning_trace.append(ReasoningStep(
            agent="MemoryAgent",
            action=f"Analyzed {len(fhir_history) + 1} historical visit records",
            finding=memory_trend.split("\n")[1] if "\n" in memory_trend else memory_trend
        ))

    # ── Step 3: Vital anomaly detection ─────────────────────────────────────

    anomaly = detect_anomalies(patient)

    if anomaly.triggered:
        reasoning_trace.append(ReasoningStep(
            agent="AnomalyDetector",
            action="Rule-based vital sign analysis (pre-LLM)",
            finding=f"{anomaly.level}: {anomaly.reasons[0]}" + (
                f" (+{len(anomaly.reasons)-1} more)" if len(anomaly.reasons) > 1 else ""
            )
        ))

    anomaly_summary = "\n".join(anomaly.reasons) if anomaly.triggered else ""

    # ── Step 4: RAG knowledge retrieval ─────────────────────────────────────

    rag_query = f"{' '.join(patient.conditions)} {' '.join(patient.medications[:2])}"
    rag_context = retrieve_context(rag_query, vectorstore, k=4)

    reasoning_trace.append(ReasoningStep(
        agent="RAGAgent",
        action="Retrieved relevant medical guidelines from knowledge base",
        finding=f"Found {len(rag_context)} relevant guideline chunks for conditions: {', '.join(patient.conditions[:2])}"
    ))

    # ── Step 5: Diagnosis sub-agent ──────────────────────────────────────────

    diagnoses, next_steps, dx_steps = run_diagnosis_agent(
        patient, rag_context, memory_trend, anomaly_summary
    )
    reasoning_trace.extend(dx_steps)

    # ── Step 6: Drug safety sub-agent ───────────────────────────────────────

    drug_rag = retrieve_context(
        f"drug interactions {' '.join(patient.medications[:3])}",
        vectorstore, k=2
    )
    drug_warnings, drug_steps = run_drug_agent(
        patient.medications, patient.conditions, patient.allergies, drug_rag
    )
    reasoning_trace.extend(drug_steps)

    # ── Step 7: Risk scoring sub-agent ──────────────────────────────────────

    risk_rag = retrieve_context(
        f"cardiovascular risk {patient.age} year old {' '.join(patient.conditions[:2])}",
        vectorstore, k=2
    )
    risk_scores, risk_steps = run_risk_agent(patient, risk_rag)
    reasoning_trace.extend(risk_steps)

    # ── Step 8: Second opinion ───────────────────────────────────────────────

    second_opinion, opinion_step = run_second_opinion(patient, diagnoses, drug_warnings)
    reasoning_trace.append(opinion_step)

    # ── Step 9: SOAP note generation ────────────────────────────────────────

    soap_note, soap_step = generate_soap_note(
        patient, diagnoses, drug_warnings, risk_scores,
        second_opinion, next_steps, memory_trend
    )
    reasoning_trace.append(soap_step)

    # ── Step 10: Build summary ───────────────────────────────────────────────

    top_dx = diagnoses[0].condition if diagnoses else "Assessment pending"
    top_risk = max(risk_scores, key=lambda x: x.score) if risk_scores else None
    drug_alert = (
        f"{len(drug_warnings)} drug interaction(s) flagged."
        if drug_warnings else "No drug interactions."
    )

    summary = (
        f"{patient.name} ({patient.age}y {patient.gender}) presents with "
        f"{len(patient.conditions)} active conditions. "
        f"Primary concern: {top_dx}. "
        f"{drug_alert} "
        f"{'Highest risk: ' + top_risk.condition + ' at ' + str(top_risk.score) + '%.' if top_risk else ''}"
    )

    return MediCopilotResponse(
        patient_id=patient_id,
        patient_name=patient.name,
        anomaly_flag=anomaly,
        summary=summary,
        diagnoses=diagnoses,
        drug_warnings=drug_warnings,
        risk_scores=risk_scores,
        second_opinion=second_opinion,
        soap_note=soap_note,
        reasoning_trace=reasoning_trace,
        rag_citations=rag_context[:2],
        memory_trend=memory_trend or None,
        generated_at=datetime.utcnow().isoformat()
    )