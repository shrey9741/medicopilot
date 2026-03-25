"""
MediCopilot FastAPI Backend.
Exposes the A2A agent via HTTP endpoints.
The /.well-known/agent.json endpoint registers it with Prompt Opinion.
"""
import json
import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from rag.retriever import load_vectorstore
from agents.orchestrator import run_medicopilot
from models.schemas import InvokeRequest, MediCopilotResponse

# Global vectorstore (loaded once at startup)
vectorstore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore
    loop = asyncio.get_event_loop()
    print("Loading RAG vectorstore...")
    vectorstore = await loop.run_in_executor(None, load_vectorstore)
    print("MediCopilot ready.")
    yield


app = FastAPI(
    title="MediCopilot A2A Agent",
    description="AI Clinical Copilot — Pre-visit patient briefing with multi-agent collaboration",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/.well-known/agent.json")
async def agent_card():
    """
    A2A Agent Card — required by Prompt Opinion for Marketplace registration.
    SHARP context fields signal FHIR integration capability.
    """
    return {
        "name": "MediCopilot",
        "version": "1.0.0",
        "description": "AI Clinical Copilot that generates structured pre-visit patient briefings using FHIR data, multi-agent reasoning, RAG medical knowledge, and SOAP note generation.",
        "author": "MediCopilot Team",
        "capabilities": [
            "clinical_summary",
            "differential_diagnosis",
            "drug_interaction_check",
            "risk_scoring",
            "soap_note_generation",
            "second_opinion",
            "temporal_memory",
            "vital_anomaly_detection",
            "rag_medical_knowledge"
        ],
        "sharp_context": {
            "patient_id": {
                "required": True,
                "description": "FHIR Patient resource ID"
            },
            "fhir_token": {
                "required": False,
                "description": "Bearer token for FHIR R4 server access"
            },
            "sharp_token": {
                "required": False,
                "description": "SHARP session token from EHR"
            }
        },
        "invoke_endpoint": "/invoke",
        "input_schema": {
            "patient_id": "string",
            "sharp_token": "string (optional)",
            "fhir_token": "string (optional)"
        },
        "output_schema": "MediCopilotResponse — structured clinical briefing with DDx, drug safety, risk scores, SOAP note, and reasoning trace"
    }


@app.post("/invoke", response_model=MediCopilotResponse)
async def invoke(request: InvokeRequest):
    """
    Main A2A invocation endpoint.
    Accepts patient_id + optional SHARP context.
    Returns full clinical briefing.
    """
    if not vectorstore:
        raise HTTPException(status_code=503, detail="RAG vectorstore not initialized")

    try:
        result = run_medicopilot(
            patient_id=request.patient_id,
            vectorstore=vectorstore,
            sharp_token=request.sharp_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "rag_loaded": vectorstore is not None,
        "model": "llama-3.1-8b-instant",
        "agents": ["FHIRAgent", "MemoryAgent", "AnomalyDetector", "RAGAgent",
                   "DiagnosisAgent", "DrugSafetyAgent", "RiskScoringAgent",
                   "SecondOpinionAgent", "SOAPNoteGenerator"]
    }


@app.get("/patients")
async def list_patients():
    """Demo endpoint — lists available mock patients."""
    return {
        "patients": [
            {"id": "P001", "name": "John Doe", "age": 62, "conditions": ["T2 Diabetes", "Hypertension", "CKD"]},
            {"id": "P002", "name": "Sarah Chen", "age": 45, "conditions": ["Atrial Fibrillation", "Hypothyroidism"]},
            {"id": "P003", "name": "Marcus Johnson", "age": 71, "conditions": ["COPD", "Heart Failure", "T2 Diabetes"]},
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)