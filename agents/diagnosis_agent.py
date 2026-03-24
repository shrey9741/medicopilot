"""
Diagnosis Agent — Sub-agent 1.
Generates differential diagnosis (DDx) with confidence scoring,
explainability, and suggested next steps.
"""
import json
import os
from groq import Groq
from models.schemas import PatientBundle, DiagnosisResult, ReasoningStep

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_diagnosis_agent(
    patient: PatientBundle,
    rag_context: list[str],
    memory_trend: str,
    anomaly_summary: str
) -> tuple[list[DiagnosisResult], list[str], list[ReasoningStep]]:
    """
    Returns: (diagnoses, next_steps, reasoning_steps)
    """
    rag_text = "\n---\n".join(rag_context)
    trend_section = f"\nMEMORY TRENDS:\n{memory_trend}" if memory_trend else ""
    anomaly_section = f"\nANOMALY FLAGS:\n{anomaly_summary}" if anomaly_summary else ""

    prompt = f"""You are a senior clinical diagnosis assistant. Analyze the patient data below and generate a differential diagnosis (DDx).

PATIENT DATA:
- Name: {patient.name}, Age: {patient.age}, Gender: {patient.gender}
- Active conditions: {', '.join(patient.conditions)}
- Current medications: {', '.join(patient.medications)}
- Allergies: {', '.join(patient.allergies)}
- Vitals: BP {patient.recent_vitals.blood_pressure}, HR {patient.recent_vitals.heart_rate}, Glucose {patient.recent_vitals.glucose}, BMI {patient.recent_vitals.bmi}, SpO2 {patient.recent_vitals.oxygen_saturation}%
- Observations: {', '.join(patient.observations)}
{trend_section}
{anomaly_section}

RELEVANT MEDICAL GUIDELINES:
{rag_text}

Respond ONLY with valid JSON in this exact format:
{{
  "diagnoses": [
    {{
      "condition": "condition name",
      "reasoning": "brief clinical reasoning citing specific vitals/observations",
      "confidence": 85,
      "tier": "critical"
    }}
  ],
  "next_steps": [
    "Order HbA1c test",
    "Refer to nephrologist"
  ]
}}

Rules:
- List 3-4 diagnoses ranked by confidence (highest first)
- confidence: 0-100 integer
- tier: one of "critical", "high", "moderate", "low"
- reasoning: 1-2 sentences citing specific patient data
- next_steps: 3-5 actionable clinical recommendations
- Return ONLY the JSON object, no other text"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=800,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    diagnoses = [
        DiagnosisResult(
            condition=d["condition"],
            reasoning=d["reasoning"],
            confidence=int(d["confidence"]),
            tier=d["tier"]
        )
        for d in data.get("diagnoses", [])
    ]

    next_steps = data.get("next_steps", [])

    reasoning_steps = [
        ReasoningStep(
            agent="DiagnosisAgent",
            action=f"Analyzed {len(patient.conditions)} conditions + {len(patient.observations)} observations",
            finding=f"Generated {len(diagnoses)}-item DDx. Top: {diagnoses[0].condition} ({diagnoses[0].confidence}% confidence)" if diagnoses else "No diagnoses generated"
        )
    ]

    return diagnoses, next_steps, reasoning_steps
