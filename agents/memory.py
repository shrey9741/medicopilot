"""
Point 4 — Temporal Patient Memory.
Stores and retrieves visit history per patient.
Generates trend analysis so agents can say
'glucose was 195 → 202 → 210 — worsening trend'.
"""
from datetime import datetime
from models.schemas import PatientBundle

# In-memory store (keyed by patient_id)
# In production: replace with Redis or a database
_memory_store: dict[str, list[dict]] = {}


def update_memory(patient: PatientBundle) -> None:
    """Append current visit data to patient's memory log."""
    pid = patient.patient_id
    if pid not in _memory_store:
        _memory_store[pid] = []

    _memory_store[pid].append({
        "timestamp": datetime.utcnow().isoformat(),
        "glucose": patient.recent_vitals.glucose,
        "blood_pressure": patient.recent_vitals.blood_pressure,
        "heart_rate": patient.recent_vitals.heart_rate,
        "bmi": patient.recent_vitals.bmi,
        "conditions": patient.conditions.copy(),
        "medications": patient.medications.copy(),
    })


def load_history(patient_id: str, fhir_history: list) -> None:
    """Seed memory with FHIR historical records (called on first load)."""
    if patient_id not in _memory_store:
        _memory_store[patient_id] = []

    for record in fhir_history:
        _memory_store[patient_id].append({
            "timestamp": record.get("date", "unknown"),
            "glucose": record.get("glucose", 0),
            "blood_pressure": record.get("bp", "unknown"),
            "heart_rate": record.get("hr", 0),
            "note": record.get("note", ""),
        })


def analyze_trends(patient_id: str) -> str:
    """
    Generates a human-readable trend summary from memory.
    Returns empty string if no history.
    """
    records = _memory_store.get(patient_id, [])
    if len(records) < 2:
        return ""

    # Analyze glucose trend
    glucose_values = [r["glucose"] for r in records if r.get("glucose")]
    bp_values = [r["blood_pressure"] for r in records if r.get("blood_pressure") != "unknown"]
    hr_values = [r["heart_rate"] for r in records if r.get("heart_rate")]

    trend_parts = []

    if len(glucose_values) >= 2:
        g_start, g_end = glucose_values[0], glucose_values[-1]
        delta = g_end - g_start
        direction = "worsening" if delta > 10 else ("improving" if delta < -10 else "stable")
        trend_parts.append(
            f"Glucose trend: {' → '.join(str(g) for g in glucose_values)} mg/dL ({direction}, Δ{delta:+d})"
        )

    if len(hr_values) >= 2:
        hr_start, hr_end = hr_values[0], hr_values[-1]
        delta = hr_end - hr_start
        direction = "increasing" if delta > 5 else ("decreasing" if delta < -5 else "stable")
        trend_parts.append(
            f"Heart rate trend: {hr_start} → {hr_end} bpm ({direction})"
        )

    if bp_values:
        trend_parts.append(f"BP across visits: {' → '.join(bp_values)}")

    if not trend_parts:
        return ""

    return "PATIENT MEMORY TRENDS:\n" + "\n".join(f"  - {t}" for t in trend_parts)


def get_full_memory(patient_id: str) -> list[dict]:
    """Returns full memory log for a patient."""
    return _memory_store.get(patient_id, [])
