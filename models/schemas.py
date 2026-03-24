from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class VitalSigns(BaseModel):
    blood_pressure: str
    heart_rate: int
    glucose: int
    bmi: float
    temperature: Optional[float] = None
    oxygen_saturation: Optional[int] = None


class PatientBundle(BaseModel):
    patient_id: str
    name: str
    age: int
    gender: str
    conditions: list[str]
    medications: list[str]
    allergies: list[str]
    recent_vitals: VitalSigns
    last_visit: str
    observations: list[str]


class MemoryEntry(BaseModel):
    timestamp: str
    glucose: int
    blood_pressure: str
    heart_rate: int
    conditions: list[str]
    medications: list[str]
    visit_summary: str


class DiagnosisResult(BaseModel):
    condition: str
    reasoning: str
    confidence: int
    tier: str


class DrugWarning(BaseModel):
    drug_a: str
    drug_b: str
    severity: str
    recommendation: str


class RiskScore(BaseModel):
    condition: str
    score: int
    factors: list[str]
    recommendation: str


class ReasoningStep(BaseModel):
    agent: str
    action: str
    finding: str


class SOAPNote(BaseModel):
    subjective: str
    objective: str
    assessment: str
    plan: str


class SecondOpinion(BaseModel):
    challenge: str
    counter_evidence: str
    final_recommendation: str


class AnomalyFlag(BaseModel):
    triggered: bool
    level: str
    reasons: list[str]


class MediCopilotResponse(BaseModel):
    patient_id: str
    patient_name: str
    anomaly_flag: AnomalyFlag
    summary: str
    diagnoses: list[DiagnosisResult]
    drug_warnings: list[DrugWarning]
    risk_scores: list[RiskScore]
    second_opinion: SecondOpinion
    soap_note: SOAPNote
    reasoning_trace: list[ReasoningStep]
    rag_citations: list[str]
    memory_trend: Optional[str] = None
    generated_at: str


class InvokeRequest(BaseModel):
    patient_id: str
    sharp_token: Optional[str] = None
    fhir_token: Optional[str] = None
