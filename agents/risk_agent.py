"""
Risk Scoring Agent — Sub-agent 3.
Calculates percentage risk scores for major conditions
with contributing factors and recommendations.
"""
import json
import os
from groq import Groq
from models.schemas import PatientBundle, RiskScore, ReasoningStep

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_risk_agent(
    patient: PatientBundle,
    rag_context: list[str]
) -> tuple[list[RiskScore], list[ReasoningStep]]:
    """
    Returns: (risk_scores, reasoning_steps)
    """
    rag_text = "\n---\n".join(rag_context)

    prompt = f"""You are a clinical risk assessment specialist. Calculate risk scores for this patient.

PATIENT:
- Age: {patient.age}, Gender: {patient.gender}
- Conditions: {', '.join(patient.conditions)}
- Vitals: BP {patient.recent_vitals.blood_pressure}, HR {patient.recent_vitals.heart_rate}, Glucose {patient.recent_vitals.glucose}, BMI {patient.recent_vitals.bmi}
- Observations: {', '.join(patient.observations)}

RISK GUIDELINES:
{rag_text}

Respond ONLY with valid JSON:
{{
  "risk_scores": [
    {{
      "condition": "Cardiovascular Disease (10-year)",
      "score": 72,
      "factors": ["Age 62", "Hypertension BP 148/92", "Diabetes HbA1c 8.2%"],
      "recommendation": "Intensify statin therapy, target LDL <70 mg/dL"
    }}
  ]
}}

Calculate 2-3 risk scores most relevant to this patient's profile.
Score is 0-100 (percentage risk or severity indicator).
List 3-4 specific contributing factors per score.
Return ONLY the JSON object, no other text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=600,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    scores = [
        RiskScore(
            condition=r["condition"],
            score=int(r["score"]),
            factors=r["factors"],
            recommendation=r["recommendation"]
        )
        for r in data.get("risk_scores", [])
    ]

    highest = max(scores, key=lambda x: x.score) if scores else None

    reasoning_steps = [
        ReasoningStep(
            agent="RiskScoringAgent",
            action=f"Computed risk scores using patient vitals, age, conditions, and Framingham/ACC guidelines",
            finding=f"Highest risk: {highest.condition} at {highest.score}%" if highest else "Risk assessment complete"
        )
    ]

    return scores, reasoning_steps
