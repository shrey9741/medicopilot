"""
Drug Safety Agent — Sub-agent 2.
Checks medication interactions and returns a severity matrix.
"""
import json
import os
from groq import Groq
from models.schemas import DrugWarning, ReasoningStep

from dotenv import load_dotenv
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def run_drug_agent(
    medications: list[str],
    conditions: list[str],
    allergies: list[str],
    rag_context: list[str]
) -> tuple[list[DrugWarning], list[ReasoningStep]]:
    """
    Returns: (drug_warnings, reasoning_steps)
    """
    rag_text = "\n---\n".join(rag_context)

    prompt = f"""You are a clinical pharmacist. Check the following medication list for dangerous interactions, contraindications, and allergy conflicts.

MEDICATIONS: {', '.join(medications)}
ACTIVE CONDITIONS: {', '.join(conditions)}
KNOWN ALLERGIES: {', '.join(allergies)}

DRUG INTERACTION GUIDELINES:
{rag_text}

Respond ONLY with valid JSON:
{{
  "warnings": [
    {{
      "drug_a": "Drug name 1",
      "drug_b": "Drug name 2 or condition",
      "severity": "critical",
      "recommendation": "Specific clinical action to take"
    }}
  ]
}}

Severity levels: "critical", "major", "moderate", "minor"
- critical: Contraindicated, immediate action needed
- major: Avoid combination, significant clinical risk
- moderate: Monitor closely, may need dose adjustment
- minor: Minimal clinical significance

Check for: drug-drug interactions, drug-disease contraindications, allergy conflicts.
If no interactions found, return {{"warnings": []}}.
Return ONLY the JSON object, no other text."""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=600,
    )

    raw = response.choices[0].message.content.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)

    warnings = [
        DrugWarning(
            drug_a=w["drug_a"],
            drug_b=w["drug_b"],
            severity=w["severity"],
            recommendation=w["recommendation"]
        )
        for w in data.get("warnings", [])
    ]

    critical_count = sum(1 for w in warnings if w.severity in ["critical", "major"])

    reasoning_steps = [
        ReasoningStep(
            agent="DrugSafetyAgent",
            action=f"Checked {len(medications)} medications for interactions + allergy conflicts",
            finding=f"Found {len(warnings)} warnings ({critical_count} critical/major)" if warnings else "No significant drug interactions detected"
        )
    ]

    return warnings, reasoning_steps
