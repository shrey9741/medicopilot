"""
Mock FHIR client — simulates a real FHIR R4 server response.
In production, replace get_patient_bundle() with actual FHIR API calls
using the fhir_token from SHARP context.
"""
from models.schemas import PatientBundle, VitalSigns

MOCK_PATIENTS = {
    "P001": PatientBundle(
        patient_id="P001",
        name="John Doe",
        age=62,
        gender="Male",
        conditions=["Type 2 Diabetes", "Hypertension", "Chronic Kidney Disease Stage 2"],
        medications=["Metformin 500mg", "Lisinopril 10mg", "Atorvastatin 20mg", "Aspirin 81mg"],
        allergies=["Penicillin", "Sulfa drugs"],
        recent_vitals=VitalSigns(
            blood_pressure="148/92",
            heart_rate=88,
            glucose=210,
            bmi=29.4,
            temperature=98.6,
            oxygen_saturation=97
        ),
        last_visit="2025-11-10",
        observations=["Elevated creatinine 1.8 mg/dL", "HbA1c 8.2%", "Microalbuminuria present"]
    ),
    "P002": PatientBundle(
        patient_id="P002",
        name="Sarah Chen",
        age=45,
        gender="Female",
        conditions=["Atrial Fibrillation", "Hypothyroidism", "Obesity"],
        medications=["Warfarin 5mg", "Levothyroxine 100mcg", "Metoprolol 25mg", "Ibuprofen 400mg"],
        allergies=["Latex"],
        recent_vitals=VitalSigns(
            blood_pressure="135/85",
            heart_rate=102,
            glucose=95,
            bmi=33.1,
            temperature=98.2,
            oxygen_saturation=96
        ),
        last_visit="2025-12-01",
        observations=["Irregular rhythm confirmed on ECG", "TSH mildly elevated 5.2", "INR 1.8 (subtherapeutic)"]
    ),
    "P003": PatientBundle(
        patient_id="P003",
        name="Marcus Johnson",
        age=71,
        gender="Male",
        conditions=["COPD", "Heart Failure (EF 35%)", "Type 2 Diabetes", "Depression"],
        medications=["Furosemide 40mg", "Carvedilol 6.25mg", "Metformin 1000mg", "Sertraline 50mg", "Tiotropium inhaler"],
        allergies=["ACE inhibitors (cough)", "NSAIDs"],
        recent_vitals=VitalSigns(
            blood_pressure="155/98",
            heart_rate=95,
            glucose=245,
            bmi=27.2,
            temperature=99.1,
            oxygen_saturation=91
        ),
        last_visit="2025-10-22",
        observations=["Bilateral crackles on auscultation", "2+ pitting edema bilateral ankles", "FEV1/FVC ratio 0.62"]
    ),
}

MOCK_HISTORY = {
    "P001": [
        {"date": "2025-09-01", "glucose": 195, "bp": "145/90", "hr": 84, "note": "Increased Metformin dose"},
        {"date": "2025-10-15", "glucose": 202, "bp": "150/94", "hr": 86, "note": "Added Lisinopril"},
        {"date": "2025-11-10", "glucose": 210, "bp": "148/92", "hr": 88, "note": "Worsening glucose trend"},
    ],
    "P002": [
        {"date": "2025-10-01", "glucose": 90, "bp": "130/82", "hr": 98, "note": "INR borderline"},
        {"date": "2025-12-01", "glucose": 95, "bp": "135/85", "hr": 102, "note": "Rate control suboptimal"},
    ],
    "P003": [
        {"date": "2025-08-10", "glucose": 220, "bp": "150/95", "hr": 90, "note": "SpO2 dropped to 93%"},
        {"date": "2025-09-20", "glucose": 235, "bp": "152/96", "hr": 92, "note": "Edema worsening"},
        {"date": "2025-10-22", "glucose": 245, "bp": "155/98", "hr": 95, "note": "Critical multi-system decline"},
    ],
}


def get_patient_bundle(patient_id: str) -> PatientBundle:
    """
    Fetch patient FHIR bundle.
    In production: calls FHIR server using Authorization: Bearer {fhir_token}
    GET /fhir/R4/Patient/{patient_id}/$everything
    """
    patient = MOCK_PATIENTS.get(patient_id)
    if not patient:
        # Default fallback patient for demo
        return MOCK_PATIENTS["P001"]
    return patient


def get_patient_history(patient_id: str) -> list:
    """Returns timestamped visit history for temporal memory."""
    return MOCK_HISTORY.get(patient_id, [])
