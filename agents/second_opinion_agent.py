"""
Point 7 — Second Opinion Mode.
After main diagnosis, this agent plays devil's advocate —
challenges the primary diagnosis and enriches the SOAP note's Assessment.
"""
import json
import os
from groq import Groq
from models.schemas import DiagnosisResult, PatientBundle, SecondOpinion, ReasoningStep

from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_second_opinion(
    patient: PatientBundle,
    primary_diagnoses: list[DiagnosisResult],
    drug_warnings: list,
) -> tuple[SecondOpinion, ReasoningStep]:
    """
    Challenges primary diagnoses and provides a balanced second opinion.
    Returns: (SecondOpinion, ReasoningStep)
    """
    primary_summary = "\n".join(
        f"- {d.condition} ({d.confidence}% confidence): {d.reasoning}"
        for d in primary_diagnoses[:2]
    )

    warning_summary = "\n".join(
        f"- {w.drug_a} + {w.drug_b}: {w.severity} — {w.recommendation}"
        for w in drug_warnings[:3]
    ) if drug_warnings else "None identified"

    prompt = f"""You are a senior attending physician reviewing a clinical AI's assessment. Your role is to challenge the primary diagnosis, identify what might have been missed, and provide a balanced second opinion.

PATIENT: {patient.name}, {patient.age}y {patient.gender}
CONDITIONS: {', '.join(patient.conditions)}
VITALS: BP {patient.recent_vitals.blood_pressure}, HR {patient.recent_vitals.heart_rate}, Glucose {patient.recent_vitals.glucose}, SpO2 {patient.recent_vitals.oxygen_saturation}%
OBSERVATIONS: {', '.join(patient.observations)}

PRIMARY AI DIAGNOSES:
{primary_summary}

DRUG WARNINGS IDENTIFIED:
{warning_summary}

Respond ONLY with valid JSON:
{{
  "challenge": "What the primary assessment may have overlooked or overweighted",
  "counter_evidence": "Specific clinical findings that support an alternative or modified interpretation",
  "final_recommendation": "Balanced final clinical recommendation combining both perspectives"
}}

Be specific. Cite actual vitals and observations. Keep each field to 2-3 sentences.
Return ONLY the JSON object, no other text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
        max_tokens=500,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    opinion = SecondOpinion(
        challenge=data.get("challenge", ""),
        counter_evidence=data.get("counter_evidence", ""),
        final_recommendation=data.get("final_recommendation", "")
    )

    step = ReasoningStep(
        agent="SecondOpinionAgent",
        action="Reviewed primary diagnoses and challenged assumptions",
        finding=f"Identified potential gap: {opinion.challenge[:80]}..."
    )

    return opinion, step
