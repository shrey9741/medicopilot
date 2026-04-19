"""
MediCopilot Orchestrator — the main A2A agent.
Coordinates all sub-agents in sequence, builds reasoning trace,
and returns a complete structured clinical briefing.
"""
import os
from datetime import datetime
from langchain_community.vectorstores import FAISS

from fhir.mock_client import get_patient_bundle, get_patient_history
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
    Returns a complete MediCopilotResponse with all 6 features.
    """
    reasoning_trace: list[ReasoningStep] = []

    # ── Step 1: Fetch FHIR patient data ─────────────────────────────────────

    patient = get_patient_bundle(patient_id)
    fhir_history = get_patient_history(patient_id)

    reasoning_trace.append(ReasoningStep(
        agent="FHIRAgent",
        action=f"Fetched patient bundle for {patient_id}",
        finding=f"{patient.name}, {patient.age}y — {len(patient.conditions)} conditions, {len(patient.medications)} medications"
    ))

    # ── Step 2: Load memory and analyze trends (Point 4) ────────────────────

    load_history(patient_id, fhir_history)
    update_memory(patient)
    memory_trend = analyze_trends(patient_id)

    if memory_trend:
        reasoning_trace.append(ReasoningStep(
            agent="MemoryAgent",
            action=f"Analyzed {len(fhir_history) + 1} historical visit records",
            finding=memory_trend.split("\n")[1] if "\n" in memory_trend else memory_trend
        ))

    # ── Step 3: Vital anomaly detection (Point 9) ───────────────────────────

    anomaly = detect_anomalies(patient)

    if anomaly.triggered:
        reasoning_trace.append(ReasoningStep(
            agent="AnomalyDetector",
            action="Rule-based vital sign analysis (pre-LLM)",
            finding=f"{anomaly.level}: {anomaly.reasons[0]}" + (f" (+{len(anomaly.reasons)-1} more)" if len(anomaly.reasons) > 1 else "")
        ))

    anomaly_summary = "\n".join(anomaly.reasons) if anomaly.triggered else ""

    # ── Step 4: RAG knowledge retrieval ─────────────────────────────────────

    rag_query = f"{' '.join(patient.conditions)} {' '.join(patient.medications[:2])}"
    rag_context = retrieve_context(rag_query, vectorstore, k=4)

    reasoning_trace.append(ReasoningStep(
        agent="RAGAgent",
        action=f"Retrieved relevant medical guidelines from knowledge base",
        finding=f"Found {len(rag_context)} relevant guideline chunks for conditions: {', '.join(patient.conditions[:2])}"
    ))

    # ── Step 5: Diagnosis sub-agent ──────────────────────────────────────────

    diagnoses, next_steps, dx_steps = run_diagnosis_agent(
        patient, rag_context, memory_trend, anomaly_summary
    )
    reasoning_trace.extend(dx_steps)

    # ── Step 6: Drug safety sub-agent ───────────────────────────────────────
    
    drug_rag = retrieve_context(f"drug interactions {' '.join(patient.medications[:3])}", vectorstore, k=2)
    drug_warnings, drug_steps = run_drug_agent(
        patient.medications, patient.conditions, patient.allergies, drug_rag
    )
    reasoning_trace.extend(drug_steps)

    # ── Step 7: Risk scoring sub-agent ──────────────────────────────────────
    risk_rag = retrieve_context(f"cardiovascular risk {patient.age} year old {' '.join(patient.conditions[:2])}", vectorstore, k=2)
    risk_scores, risk_steps = run_risk_agent(patient, risk_rag)
    reasoning_trace.extend(risk_steps)

    # ── Step 8: Second opinion (Point 7) ────────────────────────────────────
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
    drug_alert = f"{len(drug_warnings)} drug interaction(s) flagged." if drug_warnings else "No drug interactions."

    summary = (
        f"{patient.name} ({patient.age}y {patient.gender}) presents with {len(patient.conditions)} active conditions. "
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
