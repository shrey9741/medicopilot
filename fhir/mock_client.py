"""
Mock FHIR client — simulates a real FHIR R4 server response.
In production, replace get_patient_bundle() with actual FHIR API calls
using the fhir_token from SHARP context.
"""
from models.schemas import PatientBundle, VitalSigns

MOCK_PATIENTS = {
    # ── Original Patients ────────────────────────────────────────────────────
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

    # ── Oncology Patients ────────────────────────────────────────────────────
    "P004": PatientBundle(
        patient_id="P004",
        name="Patricia Williams",
        age=54,
        gender="Female",
        conditions=["Stage III Breast Cancer (HER2+)", "Chemotherapy-induced Nausea", "Anemia"],
        medications=["Trastuzumab 6mg/kg IV", "Pertuzumab 420mg IV", "Ondansetron 8mg", "Ferrous Sulfate 325mg", "Dexamethasone 4mg"],
        allergies=["Taxol (hypersensitivity)"],
        recent_vitals=VitalSigns(
            blood_pressure="112/70",
            heart_rate=96,
            glucose=88,
            bmi=22.1,
            temperature=99.4,
            oxygen_saturation=98
        ),
        last_visit="2025-12-10",
        observations=["Hemoglobin 9.2 g/dL", "Neutropenia ANC 1200", "LVEF 58% on recent echo", "CA 15-3 elevated at 48 U/mL"]
    ),
    "P005": PatientBundle(
        patient_id="P005",
        name="Robert Nguyen",
        age=67,
        gender="Male",
        conditions=["Stage IV Non-Small Cell Lung Cancer", "COPD", "Hypertension", "Cachexia"],
        medications=["Pembrolizumab 200mg IV", "Amlodipine 5mg", "Tiotropium inhaler", "Megestrol 160mg", "Morphine SR 30mg"],
        allergies=["Cisplatin (nephrotoxicity)"],
        recent_vitals=VitalSigns(
            blood_pressure="130/82",
            heart_rate=91,
            glucose=102,
            bmi=18.3,
            temperature=98.8,
            oxygen_saturation=93
        ),
        last_visit="2025-11-28",
        observations=["Weight loss 12kg over 3 months", "PD-L1 expression 70%", "CT: stable primary, new adrenal metastasis", "ECOG performance status 2"]
    ),

    # ── Pediatric Patients ───────────────────────────────────────────────────
    "P006": PatientBundle(
        patient_id="P006",
        name="Aiden Patel",
        age=8,
        gender="Male",
        conditions=["Type 1 Diabetes", "Asthma (Moderate Persistent)", "ADHD"],
        medications=["Insulin Glargine 12 units", "Insulin Lispro sliding scale", "Fluticasone 44mcg inhaler", "Albuterol PRN", "Methylphenidate 10mg"],
        allergies=["Amoxicillin (rash)"],
        recent_vitals=VitalSigns(
            blood_pressure="100/65",
            heart_rate=92,
            glucose=185,
            bmi=17.2,
            temperature=98.4,
            oxygen_saturation=98
        ),
        last_visit="2025-12-05",
        observations=["HbA1c 8.9% — suboptimal control", "Peak flow 78% predicted", "Growth percentile 45th", "Recent hypoglycemic episode at school"]
    ),
    "P007": PatientBundle(
        patient_id="P007",
        name="Lily Thompson",
        age=5,
        gender="Female",
        conditions=["Acute Lymphoblastic Leukemia (ALL) — Maintenance Phase", "Immunosuppression", "Failure to Thrive"],
        medications=["Mercaptopurine 50mg/m2", "Methotrexate 20mg/m2 weekly", "Trimethoprim-Sulfamethoxazole (prophylaxis)", "Folic Acid 1mg"],
        allergies=["None known"],
        recent_vitals=VitalSigns(
            blood_pressure="90/58",
            heart_rate=105,
            glucose=78,
            bmi=13.8,
            temperature=100.1,
            oxygen_saturation=99
        ),
        last_visit="2025-12-12",
        observations=["WBC 2.1 (leukopenic)", "Platelets 85,000", "Weight 3rd percentile for age", "Bone marrow remission confirmed at 12 months"]
    ),

    # ── Mental Health Patients ───────────────────────────────────────────────
    "P008": PatientBundle(
        patient_id="P008",
        name="Diana Foster",
        age=34,
        gender="Female",
        conditions=["Bipolar I Disorder", "Generalized Anxiety Disorder", "Hypothyroidism", "Obesity"],
        medications=["Lithium Carbonate 900mg", "Quetiapine 200mg", "Sertraline 100mg", "Levothyroxine 75mcg", "Lorazepam 0.5mg PRN"],
        allergies=["Valproate (hepatotoxicity)"],
        recent_vitals=VitalSigns(
            blood_pressure="128/80",
            heart_rate=78,
            glucose=105,
            bmi=31.4,
            temperature=98.3,
            oxygen_saturation=99
        ),
        last_visit="2025-11-20",
        observations=["Lithium level 0.6 mEq/L (low therapeutic)", "TSH 4.8 (borderline)", "PHQ-9 score 14 (moderate depression)", "Recent manic episode 6 weeks ago"]
    ),
    "P009": PatientBundle(
        patient_id="P009",
        name="Carlos Rivera",
        age=28,
        gender="Male",
        conditions=["Schizophrenia", "Substance Use Disorder (Cannabis)", "Metabolic Syndrome"],
        medications=["Clozapine 300mg", "Metformin 500mg", "Atorvastatin 10mg"],
        allergies=["Haloperidol (severe EPS)", "Risperidone (NMS)"],
        recent_vitals=VitalSigns(
            blood_pressure="138/88",
            heart_rate=88,
            glucose=118,
            bmi=34.2,
            temperature=98.7,
            oxygen_saturation=98
        ),
        last_visit="2025-10-30",
        observations=["ANC 1800 (clozapine monitoring)", "Fasting triglycerides 280 mg/dL", "PANSS score 62 (moderate symptoms)", "Cannabis use 3-4x weekly reported"]
    ),

    # ── Rare / Complex Disease Patients ─────────────────────────────────────
    "P010": PatientBundle(
        patient_id="P010",
        name="Eleanor Voss",
        age=41,
        gender="Female",
        conditions=["Systemic Lupus Erythematosus (SLE)", "Lupus Nephritis Class III", "Antiphospholipid Syndrome", "Anemia of Chronic Disease"],
        medications=["Hydroxychloroquine 400mg", "Mycophenolate Mofetil 1500mg", "Prednisone 10mg", "Warfarin 4mg", "Vitamin D 2000 IU"],
        allergies=["Sulfa drugs", "NSAIDs (renal exacerbation)"],
        recent_vitals=VitalSigns(
            blood_pressure="142/88",
            heart_rate=84,
            glucose=112,
            bmi=23.6,
            temperature=99.2,
            oxygen_saturation=97
        ),
        last_visit="2025-12-08",
        observations=["Proteinuria 1.8g/24hr", "Complement C3 low at 62 mg/dL", "Anti-dsDNA titre rising 1:320", "INR 2.4 (therapeutic)", "Hemoglobin 10.1 g/dL"]
    ),
    "P011": PatientBundle(
        patient_id="P011",
        name="Samuel Okafor",
        age=19,
        gender="Male",
        conditions=["Cystic Fibrosis (F508del homozygous)", "CF-related Diabetes", "Pancreatic Exocrine Insufficiency", "Chronic Pseudomonas Infection"],
        medications=["Elexacaftor/Tezacaftor/Ivacaftor (Trikafta)", "Insulin Aspart sliding scale", "Creon 12000 units with meals", "Tobramycin inhaled", "Azithromycin 250mg"],
        allergies=["Ciprofloxacin (tendinopathy)"],
        recent_vitals=VitalSigns(
            blood_pressure="108/68",
            heart_rate=88,
            glucose=165,
            bmi=19.1,
            temperature=99.6,
            oxygen_saturation=94
        ),
        last_visit="2025-11-15",
        observations=["FEV1 62% predicted — stable post-Trikafta", "Sputum Pseudomonas aeruginosa +ve", "Fecal elastase < 100 mcg/g", "HbA1c 7.8%", "BMI low — nutritional support ongoing"]
    ),
    "P012": PatientBundle(
        patient_id="P012",
        name="Ingrid Larsson",
        age=37,
        gender="Female",
        conditions=["Multiple Sclerosis (Relapsing-Remitting)", "Neurogenic Bladder", "Major Depressive Disorder", "Vitamin D Deficiency"],
        medications=["Natalizumab 300mg IV monthly", "Oxybutynin 5mg", "Duloxetine 60mg", "Vitamin D3 5000 IU", "Baclofen 10mg"],
        allergies=["Interferon beta (severe flu-like reaction)"],
        recent_vitals=VitalSigns(
            blood_pressure="118/74",
            heart_rate=72,
            glucose=88,
            bmi=24.3,
            temperature=98.1,
            oxygen_saturation=99
        ),
        last_visit="2025-12-03",
        observations=["JC virus antibody index 2.8 (high PML risk)", "EDSS score 3.5", "25-OH Vitamin D 18 ng/mL (deficient)", "PHQ-9 score 16 (moderate-severe depression)", "New T2 lesion on MRI — no gadolinium enhancement"]
    ),
    "P013": PatientBundle(
        patient_id="P013",
        name="Theo Blackwood",
        age=52,
        gender="Male",
        conditions=["Amyotrophic Lateral Sclerosis (ALS)", "Respiratory Insufficiency", "Dysphagia", "Insomnia"],
        medications=["Riluzole 50mg", "Edaravone 60mg IV", "Baclofen 20mg", "Melatonin 5mg", "Glycopyrrolate 1mg (secretions)"],
        allergies=["None known"],
        recent_vitals=VitalSigns(
            blood_pressure="122/76",
            heart_rate=78,
            glucose=94,
            bmi=21.8,
            temperature=97.9,
            oxygen_saturation=92
        ),
        last_visit="2025-12-01",
        observations=["FVC 48% predicted — BiPAP initiated", "Dysphagia moderate — PEG tube discussed", "EMG: widespread active denervation", "ALSFRS-R score 28 (moderate-severe)", "Bulbar symptoms progressing"]
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
    "P004": [
        {"date": "2025-10-01", "glucose": 92, "bp": "118/72", "hr": 88, "note": "Cycle 4 chemo — tolerated well"},
        {"date": "2025-11-05", "glucose": 85, "bp": "110/68", "hr": 94, "note": "Hemoglobin dropping, fatigue++"},
        {"date": "2025-12-10", "glucose": 88, "bp": "112/70", "hr": 96, "note": "Neutropenia noted post cycle 6"},
    ],
    "P005": [
        {"date": "2025-09-15", "glucose": 98, "bp": "134/84", "hr": 88, "note": "Started pembrolizumab"},
        {"date": "2025-10-20", "glucose": 100, "bp": "132/82", "hr": 90, "note": "Weight loss accelerating"},
        {"date": "2025-11-28", "glucose": 102, "bp": "130/82", "hr": 91, "note": "New adrenal metastasis on CT"},
    ],
    "P006": [
        {"date": "2025-09-10", "glucose": 172, "bp": "98/62", "hr": 90, "note": "Pump settings adjusted"},
        {"date": "2025-10-25", "glucose": 168, "bp": "100/64", "hr": 91, "note": "Asthma flare — steroid burst"},
        {"date": "2025-12-05", "glucose": 185, "bp": "100/65", "hr": 92, "note": "HbA1c remains elevated"},
    ],
    "P007": [
        {"date": "2025-08-01", "glucose": 82, "bp": "88/56", "hr": 108, "note": "Maintenance chemo started"},
        {"date": "2025-10-10", "glucose": 79, "bp": "90/58", "hr": 106, "note": "ANC nadir — held MTX one week"},
        {"date": "2025-12-12", "glucose": 78, "bp": "90/58", "hr": 105, "note": "Fever — infection screen ordered"},
    ],
    "P008": [
        {"date": "2025-09-05", "glucose": 98, "bp": "124/78", "hr": 76, "note": "Lithium level stable 0.8"},
        {"date": "2025-10-18", "glucose": 102, "bp": "126/80", "hr": 80, "note": "Manic episode — dose adjusted"},
        {"date": "2025-11-20", "glucose": 105, "bp": "128/80", "hr": 78, "note": "Lithium level dropped — non-compliance"},
    ],
    "P009": [
        {"date": "2025-08-15", "glucose": 110, "bp": "136/86", "hr": 86, "note": "ANC monitoring — borderline"},
        {"date": "2025-09-28", "glucose": 114, "bp": "138/88", "hr": 87, "note": "Cannabis use disclosed"},
        {"date": "2025-10-30", "glucose": 118, "bp": "138/88", "hr": 88, "note": "Metabolic syndrome worsening"},
    ],
    "P010": [
        {"date": "2025-09-20", "glucose": 108, "bp": "138/86", "hr": 82, "note": "Proteinuria increasing"},
        {"date": "2025-10-25", "glucose": 110, "bp": "140/88", "hr": 83, "note": "Lupus flare — prednisone increased"},
        {"date": "2025-12-08", "glucose": 112, "bp": "142/88", "hr": 84, "note": "Anti-dsDNA titre rising"},
    ],
    "P011": [
        {"date": "2025-09-01", "glucose": 158, "bp": "110/70", "hr": 86, "note": "Trikafta month 6 — FEV1 improved"},
        {"date": "2025-10-10", "glucose": 162, "bp": "108/68", "hr": 87, "note": "Pseudomonas exacerbation — IV tobra"},
        {"date": "2025-11-15", "glucose": 165, "bp": "108/68", "hr": 88, "note": "BMI still low — dietitian review"},
    ],
    "P012": [
        {"date": "2025-09-15", "glucose": 85, "bp": "116/72", "hr": 70, "note": "MRI stable — no new lesions"},
        {"date": "2025-10-28", "glucose": 87, "bp": "118/74", "hr": 71, "note": "JC antibody index rising"},
        {"date": "2025-12-03", "glucose": 88, "bp": "118/74", "hr": 72, "note": "New T2 lesion — natalizumab review"},
    ],
    "P013": [
        {"date": "2025-09-10", "glucose": 91, "bp": "124/78", "hr": 76, "note": "FVC 58% — monitoring closely"},
        {"date": "2025-10-20", "glucose": 92, "bp": "122/76", "hr": 77, "note": "Dysphagia worsening — SLT referral"},
        {"date": "2025-12-01", "glucose": 94, "bp": "122/76", "hr": 78, "note": "FVC 48% — BiPAP initiated"},
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
        return MOCK_PATIENTS["P001"]
    return patient


def get_patient_history(patient_id: str) -> list:
    """Returns timestamped visit history for temporal memory."""
    return MOCK_HISTORY.get(patient_id, [])#   f o r c e   r e d e p l o y  
 