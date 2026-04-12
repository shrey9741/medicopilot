"""
Mock FHIR client — simulates a real FHIR R4 server response.
13 patients covering diverse clinical scenarios.
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
    "P004": PatientBundle(
        patient_id="P004",
        name="Patricia Williams",
        age=54,
        gender="Female",
        conditions=["Breast Cancer HER2+", "Chemotherapy-induced Neuropathy", "Hypertension"],
        medications=["Trastuzumab", "Pertuzumab", "Docetaxel", "Amlodipine 5mg", "Ondansetron 8mg"],
        allergies=["Taxanes (hypersensitivity)", "Contrast dye"],
        recent_vitals=VitalSigns(
            blood_pressure="142/88",
            heart_rate=76,
            glucose=105,
            bmi=24.8,
            temperature=98.4,
            oxygen_saturation=98
        ),
        last_visit="2025-12-10",
        observations=["Cycle 4 of chemotherapy", "Grade 2 peripheral neuropathy", "LVEF 58% on recent echo", "Neutrophil count 1.8 (mild neutropenia)"]
    ),
    "P005": PatientBundle(
        patient_id="P005",
        name="Robert Nguyen",
        age=67,
        gender="Male",
        conditions=["Lung Cancer Stage IV (NSCLC)", "COPD", "Type 2 Diabetes"],
        medications=["Pembrolizumab", "Metformin 500mg", "Tiotropium inhaler", "Dexamethasone 4mg", "Omeprazole 20mg"],
        allergies=["Platinum compounds"],
        recent_vitals=VitalSigns(
            blood_pressure="128/78",
            heart_rate=82,
            glucose=188,
            bmi=21.3,
            temperature=98.9,
            oxygen_saturation=93
        ),
        last_visit="2025-11-28",
        observations=["Performance status ECOG 2", "Pleural effusion right side", "SpO2 drops to 88% on exertion", "PD-L1 expression 60%"]
    ),
    "P006": PatientBundle(
        patient_id="P006",
        name="Aiden Patel",
        age=8,
        gender="Male",
        conditions=["Type 1 Diabetes", "Asthma", "Celiac Disease"],
        medications=["Insulin Glargine 10 units", "Insulin Lispro sliding scale", "Albuterol inhaler PRN", "Fluticasone inhaler"],
        allergies=["Gluten", "Egg"],
        recent_vitals=VitalSigns(
            blood_pressure="100/65",
            heart_rate=92,
            glucose=285,
            bmi=16.2,
            temperature=98.1,
            oxygen_saturation=99
        ),
        last_visit="2025-12-05",
        observations=["HbA1c 9.1% (poor control)", "Recent DKA episode 3 weeks ago", "Peak flow 78% predicted", "IgA tissue transglutaminase elevated"]
    ),
    "P007": PatientBundle(
        patient_id="P007",
        name="Lily Thompson",
        age=5,
        gender="Female",
        conditions=["Acute Lymphoblastic Leukemia (ALL)", "Anemia", "Febrile Neutropenia"],
        medications=["Vincristine", "Prednisone", "Methotrexate", "6-Mercaptopurine", "Trimethoprim-Sulfamethoxazole"],
        allergies=["Asparaginase"],
        recent_vitals=VitalSigns(
            blood_pressure="95/60",
            heart_rate=118,
            glucose=92,
            bmi=14.8,
            temperature=101.2,
            oxygen_saturation=98
        ),
        last_visit="2025-12-08",
        observations=["ANC 0.4 (severe neutropenia)", "Hemoglobin 7.8 g/dL", "Fever 101.2F — febrile neutropenia protocol", "Day 22 of induction chemotherapy"]
    ),
    "P008": PatientBundle(
        patient_id="P008",
        name="Diana Foster",
        age=34,
        gender="Female",
        conditions=["Bipolar I Disorder", "Generalized Anxiety Disorder", "Hypothyroidism"],
        medications=["Lithium 600mg BID", "Quetiapine 200mg", "Clonazepam 0.5mg", "Levothyroxine 75mcg"],
        allergies=["Valproate (hepatotoxicity)", "Carbamazepine (rash)"],
        recent_vitals=VitalSigns(
            blood_pressure="118/74",
            heart_rate=78,
            glucose=98,
            bmi=26.1,
            temperature=98.3,
            oxygen_saturation=99
        ),
        last_visit="2025-11-20",
        observations=["Lithium level 0.6 mEq/L (low therapeutic)", "TSH 4.8 (mildly elevated)", "PHQ-9 score 12 (moderate depression)", "Mild tremor noted on exam"]
    ),
    "P009": PatientBundle(
        patient_id="P009",
        name="Carlos Rivera",
        age=28,
        gender="Male",
        conditions=["Schizophrenia", "Substance Use Disorder (Cannabis)", "Hypertension"],
        medications=["Risperidone 4mg", "Benztropine 1mg", "Amlodipine 5mg"],
        allergies=["Haloperidol (severe EPS)", "Clozapine (agranulocytosis)"],
        recent_vitals=VitalSigns(
            blood_pressure="138/86",
            heart_rate=84,
            glucose=108,
            bmi=28.9,
            temperature=98.5,
            oxygen_saturation=98
        ),
        last_visit="2025-11-15",
        observations=["Medication adherence poor (missed 3 doses this week)", "Positive symptoms: auditory hallucinations", "Fasting glucose borderline", "Extrapyramidal symptoms mild"]
    ),
    "P010": PatientBundle(
        patient_id="P010",
        name="Eleanor Voss",
        age=41,
        gender="Female",
        conditions=["Systemic Lupus Erythematosus", "Antiphospholipid Syndrome", "Lupus Nephritis Class III"],
        medications=["Hydroxychloroquine 400mg", "Mycophenolate 1500mg BID", "Prednisone 10mg", "Warfarin 7.5mg", "Calcium + Vitamin D"],
        allergies=["NSAIDs (renal flare)", "Sulfa drugs"],
        recent_vitals=VitalSigns(
            blood_pressure="145/92",
            heart_rate=88,
            glucose=112,
            bmi=23.4,
            temperature=99.0,
            oxygen_saturation=97
        ),
        last_visit="2025-12-03",
        observations=["Proteinuria 2.1g/24hr (worsening)", "Complement C3 low 68", "Anti-dsDNA elevated 1:320", "INR 2.1 (therapeutic)", "Malar rash present"]
    ),
    "P011": PatientBundle(
        patient_id="P011",
        name="Samuel Okafor",
        age=19,
        gender="Male",
        conditions=["Cystic Fibrosis (F508del homozygous)", "CF-related Diabetes", "Chronic Pseudomonas Infection"],
        medications=["Elexacaftor/Tezacaftor/Ivacaftor", "Tobramycin inhaled", "Dornase alfa", "Insulin Glargine 8 units", "Azithromycin 500mg 3x/week"],
        allergies=["Ciprofloxacin (tendinopathy)"],
        recent_vitals=VitalSigns(
            blood_pressure="112/70",
            heart_rate=88,
            glucose=195,
            bmi=18.1,
            temperature=98.8,
            oxygen_saturation=94
        ),
        last_visit="2025-11-30",
        observations=["FEV1 58% predicted (decline from 65%)", "Sputum culture: Pseudomonas aeruginosa", "HbA1c 7.8%", "Weight loss 3kg over 3 months"]
    ),
    "P012": PatientBundle(
        patient_id="P012",
        name="Ingrid Larsson",
        age=37,
        gender="Female",
        conditions=["Multiple Sclerosis (Relapsing-Remitting)", "Depression", "Osteoporosis"],
        medications=["Natalizumab 300mg IV monthly", "Sertraline 100mg", "Vitamin D3 2000 IU", "Calcium Carbonate 1200mg", "Baclofen 10mg TID"],
        allergies=["Interferon beta (flu-like reaction)", "Glatiramer acetate (injection site)"],
        recent_vitals=VitalSigns(
            blood_pressure="115/72",
            heart_rate=74,
            glucose=90,
            bmi=22.8,
            temperature=98.2,
            oxygen_saturation=99
        ),
        last_visit="2025-12-01",
        observations=["New T2 lesion on MRI brain", "JC virus antibody index 2.8 (high PML risk)", "EDSS score 3.5", "PHQ-9 score 14 (moderate-severe depression)"]
    ),
    "P013": PatientBundle(
        patient_id="P013",
        name="Theo Blackwood",
        age=52,
        gender="Male",
        conditions=["ALS (Amyotrophic Lateral Sclerosis)", "Dysphagia", "Respiratory Failure (early)"],
        medications=["Riluzole 50mg BID", "Edaravone 60mg IV", "Baclofen 20mg TID", "Glycopyrrolate 1mg TID", "Modafinil 200mg"],
        allergies=["Morphine (hypersensitivity)"],
        recent_vitals=VitalSigns(
            blood_pressure="122/78",
            heart_rate=72,
            glucose=95,
            bmi=20.1,
            temperature=98.0,
            oxygen_saturation=94
        ),
        last_visit="2025-11-25",
        observations=["FVC 62% predicted (declining)", "Bulbar symptoms progressing", "PEG tube placement discussed", "NIV initiated at night", "ALSFRS-R score 32 (moderate disability)"]
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
        {"date": "2025-10-15", "glucose": 98, "bp": "138/85", "hr": 74, "note": "Pre-chemo baseline"},
        {"date": "2025-11-15", "glucose": 102, "bp": "140/87", "hr": 76, "note": "Cycle 3 completed"},
        {"date": "2025-12-10", "glucose": 105, "bp": "142/88", "hr": 76, "note": "Neuropathy grade 2"},
    ],
    "P005": [
        {"date": "2025-09-28", "glucose": 175, "bp": "130/80", "hr": 80, "note": "Immunotherapy started"},
        {"date": "2025-11-28", "glucose": 188, "bp": "128/78", "hr": 82, "note": "Pleural effusion noted"},
    ],
    "P006": [
        {"date": "2025-10-01", "glucose": 240, "bp": "98/62", "hr": 95, "note": "HbA1c 8.8%"},
        {"date": "2025-12-05", "glucose": 285, "bp": "100/65", "hr": 92, "note": "DKA episode 3 weeks prior"},
    ],
    "P007": [
        {"date": "2025-11-01", "glucose": 88, "bp": "92/58", "hr": 112, "note": "Induction day 1"},
        {"date": "2025-12-08", "glucose": 92, "bp": "95/60", "hr": 118, "note": "Febrile neutropenia"},
    ],
    "P008": [
        {"date": "2025-09-20", "glucose": 95, "bp": "115/72", "hr": 76, "note": "Lithium adjusted"},
        {"date": "2025-11-20", "glucose": 98, "bp": "118/74", "hr": 78, "note": "Mild depressive episode"},
    ],
    "P009": [
        {"date": "2025-10-15", "glucose": 104, "bp": "135/84", "hr": 82, "note": "Medication compliance issues"},
        {"date": "2025-11-15", "glucose": 108, "bp": "138/86", "hr": 84, "note": "Positive symptoms persisting"},
    ],
    "P010": [
        {"date": "2025-10-03", "glucose": 108, "bp": "140/90", "hr": 86, "note": "Proteinuria 1.8g"},
        {"date": "2025-12-03", "glucose": 112, "bp": "145/92", "hr": 88, "note": "Nephritis flare suspected"},
    ],
    "P011": [
        {"date": "2025-09-30", "glucose": 182, "bp": "110/68", "hr": 86, "note": "FEV1 65%"},
        {"date": "2025-11-30", "glucose": 195, "bp": "112/70", "hr": 88, "note": "FEV1 declined to 58%"},
    ],
    "P012": [
        {"date": "2025-09-01", "glucose": 88, "bp": "112/70", "hr": 72, "note": "Stable on natalizumab"},
        {"date": "2025-12-01", "glucose": 90, "bp": "115/72", "hr": 74, "note": "New MRI lesion found"},
    ],
    "P013": [
        {"date": "2025-09-25", "glucose": 92, "bp": "120/76", "hr": 70, "note": "FVC 68%"},
        {"date": "2025-11-25", "glucose": 95, "bp": "122/78", "hr": 72, "note": "FVC declined to 62%"},
    ],
}


def get_patient_bundle(patient_id: str) -> PatientBundle:
    patient = MOCK_PATIENTS.get(patient_id)
    if not patient:
        return MOCK_PATIENTS["P001"]
    return patient


def get_patient_history(patient_id: str) -> list:
    return MOCK_HISTORY.get(patient_id, [])
