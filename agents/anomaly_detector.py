"""
Point 9 — Vital Anomaly Detection.
Runs BEFORE any LLM call. Fast, deterministic, rule-based.
Flags critical conditions so the LLM gets pre-warned context.
"""
from models.schemas import PatientBundle, AnomalyFlag


def _parse_bp(bp_str: str) -> tuple[int, int]:
    """Parse '148/92' into (148, 92)."""
    try:
        parts = bp_str.split("/")
        return int(parts[0]), int(parts[1])
    except Exception:
        return 0, 0


def detect_anomalies(patient: PatientBundle) -> AnomalyFlag:
    """
    Rule-based vital anomaly detection.
    Returns an AnomalyFlag with severity level and list of triggered reasons.
    """
    reasons = []
    vitals = patient.recent_vitals
    systolic, diastolic = _parse_bp(vitals.blood_pressure)

    # --- Blood pressure rules ---
    if systolic >= 180 or diastolic >= 120:
        reasons.append(f"HYPERTENSIVE CRISIS: BP {vitals.blood_pressure} (≥180/120)")
    elif systolic >= 160 or diastolic >= 100:
        reasons.append(f"Severely elevated BP: {vitals.blood_pressure}")
    elif systolic >= 140 or diastolic >= 90:
        reasons.append(f"Stage 2 hypertension: {vitals.blood_pressure}")

    # --- Glucose rules ---
    
    if vitals.glucose >= 400:
        reasons.append(f"CRITICAL hyperglycemia: glucose {vitals.glucose} mg/dL (≥400)")
    elif vitals.glucose >= 300:
        reasons.append(f"Severe hyperglycemia: glucose {vitals.glucose} mg/dL")
    elif vitals.glucose >= 200:
        reasons.append(f"Elevated glucose: {vitals.glucose} mg/dL")
    elif vitals.glucose < 70:
        reasons.append(f"HYPOGLYCEMIA: glucose {vitals.glucose} mg/dL (<70)")

    # --- Heart rate rules ---
    if vitals.heart_rate >= 150:
        reasons.append(f"CRITICAL tachycardia: HR {vitals.heart_rate} bpm")
    elif vitals.heart_rate >= 100:
        reasons.append(f"Tachycardia: HR {vitals.heart_rate} bpm")
    elif vitals.heart_rate < 50:
        reasons.append(f"Bradycardia: HR {vitals.heart_rate} bpm")

    # --- Oxygen saturation rules ---
    if vitals.oxygen_saturation is not None:
        if vitals.oxygen_saturation < 90:
            reasons.append(f"CRITICAL hypoxia: SpO2 {vitals.oxygen_saturation}% (<90%)")
        elif vitals.oxygen_saturation < 94:
            reasons.append(f"Low oxygen saturation: SpO2 {vitals.oxygen_saturation}%")

    # --- BMI rules ---
    if vitals.bmi >= 40:
        reasons.append(f"Morbid obesity: BMI {vitals.bmi}")
    elif vitals.bmi < 17:
        reasons.append(f"Severely underweight: BMI {vitals.bmi}")

    # --- Combined danger rules ---
    if systolic >= 140 and vitals.glucose >= 200:
        reasons.append("Combined risk: Uncontrolled BP + elevated glucose — high cardiovascular event risk")

    if "Heart Failure" in " ".join(patient.conditions) and vitals.oxygen_saturation and vitals.oxygen_saturation < 94:
        reasons.append("Heart failure patient with low SpO2 — possible acute decompensation")

    # --- Determine severity level ---
    critical_keywords = ["CRITICAL", "CRISIS", "HYPOGLYCEMIA"]
    is_critical = any(any(kw in r for kw in critical_keywords) for r in reasons)

    if is_critical:
        level = "CRITICAL"
    elif len(reasons) >= 3:
        level = "URGENT"
    elif len(reasons) >= 1:
        level = "WARNING"
    else:
        level = "NORMAL"

    return AnomalyFlag(
        triggered=len(reasons) > 0,
        level=level,
        reasons=reasons
    )
