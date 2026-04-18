"""
SOAP Note Generator.
Converts MediCopilot output into a structured clinical SOAP note
— the exact format doctors use in medical records.
"""
import json
import os
from groq import Groq
from models.schemas import (
    PatientBundle, DiagnosisResult, DrugWarning,
    RiskScore, SecondOpinion, SOAPNote, ReasoningStep
)

from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_soap_note(
    patient: PatientBundle,
    diagnoses: list[DiagnosisResult],
    drug_warnings: list[DrugWarning],
    risk_scores: list[RiskScore],
    second_opinion: SecondOpinion,
    next_steps: list[str],
    memory_trend: str
) -> tuple[SOAPNote, ReasoningStep]:
    """
    Generates a structured SOAP note from all agent outputs.
    Returns: (SOAPNote, ReasoningStep)
    """
    dx_summary = "\n".join(f"- {d.condition} ({d.tier.upper()}, {d.confidence}%)" for d in diagnoses)
    drug_summary = "\n".join(f"- {w.drug_a}+{w.drug_b}: {w.severity}" for w in drug_warnings) or "None"
    risk_summary = "\n".join(f"- {r.condition}: {r.score}%" for r in risk_scores)
    steps_summary = "\n".join(f"- {s}" for s in next_steps)
    trend_section = f"\nTrends: {memory_trend}" if memory_trend else ""

    prompt = f"""Generate a professional clinical SOAP note based on this patient data.

PATIENT: {patient.name}, {patient.age}y {patient.gender}
CHIEF COMPLAINT / VISIT: Routine follow-up / AI-assisted pre-visit assessment

VITALS: BP {patient.recent_vitals.blood_pressure}, HR {patient.recent_vitals.heart_rate} bpm, Glucose {patient.recent_vitals.glucose} mg/dL, BMI {patient.recent_vitals.bmi}, SpO2 {patient.recent_vitals.oxygen_saturation}%
CONDITIONS: {', '.join(patient.conditions)}
MEDICATIONS: {', '.join(patient.medications)}
ALLERGIES: {', '.join(patient.allergies)}
OBSERVATIONS: {', '.join(patient.observations)}
{trend_section}

AI DIFFERENTIAL DIAGNOSIS:
{dx_summary}

DRUG SAFETY:
{drug_summary}

RISK SCORES:
{risk_summary}

SECOND OPINION NOTE:
{second_opinion.final_recommendation}

RECOMMENDED NEXT STEPS:
{steps_summary}

Respond ONLY with valid JSON:
{{
  "subjective": "Patient-reported symptoms and history summary (2-3 sentences)",
  "objective": "Objective clinical findings: vitals, observations, lab values (3-4 sentences)",
  "assessment": "Clinical assessment integrating AI diagnoses and second opinion (3-4 sentences)",
  "plan": "Numbered action plan with specific orders, referrals, and follow-up (4-6 items)"
}}

Write in formal clinical language. Be specific with values.
Return ONLY the JSON object, no other text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=700,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    note = SOAPNote(
        subjective=data.get("subjective", ""),
        objective=data.get("objective", ""),
        assessment=data.get("assessment", ""),
        plan=data.get("plan", "") if isinstance(data.get("plan", ""), str) else "\n".join(data.get("plan", []))
    )

    step = ReasoningStep(
        agent="SOAPNoteGenerator",
        action="Synthesized all agent outputs into structured clinical documentation",
        finding="SOAP note generated — ready for EHR entry"
    )

    return note, step
