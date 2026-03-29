"""
MediCopilot FastAPI Backend.
Exposes the A2A agent via HTTP endpoints.
The /.well-known/agent.json endpoint registers it with Prompt Opinion.
"""
import json
import os
import threading
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

from rag.retriever import load_vectorstore
from agents.orchestrator import run_medicopilot
from models.schemas import InvokeRequest, MediCopilotResponse

# Global vectorstore (loaded in background thread)
vectorstore = None
vectorstore_ready = False


def _load_vectorstore():
    """Load vectorstore in background so server starts instantly."""
    global vectorstore, vectorstore_ready
    print("Loading RAG vectorstore in background...")
    vectorstore = load_vectorstore()
    vectorstore_ready = True
    print("MediCopilot ready.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    t = threading.Thread(target=_load_vectorstore, daemon=True)
    t.start()
    print("Server starting — vectorstore loading in background...")
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
    return {
        "name": "MediCopilot",
        "version": "1.0.0",
        "description": "AI Clinical Copilot that generates structured pre-visit patient briefings using FHIR data, multi-agent reasoning, RAG medical knowledge, and SOAP note generation.",
        "author": "MediCopilot Team",
        "capabilities": [
            "clinical_summary", "differential_diagnosis", "drug_interaction_check",
            "risk_scoring", "soap_note_generation", "second_opinion",
            "temporal_memory", "vital_anomaly_detection", "rag_medical_knowledge"
        ],
        "sharp_context": {
            "patient_id": {"required": True, "description": "FHIR Patient resource ID"},
            "fhir_token": {"required": False, "description": "Bearer token for FHIR R4 server access"},
            "sharp_token": {"required": False, "description": "SHARP session token from EHR"}
        },
        "invoke_endpoint": "/invoke",
        "input_schema": {
            "patient_id": "string",
            "sharp_token": "string (optional)",
            "fhir_token": "string (optional)"
        }
    }


@app.post("/invoke", response_model=MediCopilotResponse)
async def invoke(request: InvokeRequest):
    if not vectorstore_ready:
        raise HTTPException(
            status_code=503,
            detail="RAG vectorstore is still loading. Please retry in 30 seconds."
        )
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
        "status": "ok" if vectorstore_ready else "loading",
        "rag_loaded": vectorstore_ready,
        "model": "llama-3.1-8b-instant",
        "agents": [
            "FHIRAgent", "MemoryAgent", "AnomalyDetector", "RAGAgent",
            "DiagnosisAgent", "DrugSafetyAgent", "RiskScoringAgent",
            "SecondOpinionAgent", "SOAPNoteGenerator"
        ]
    }


@app.get("/patients")
async def list_patients():
    from fhir.mock_client import MOCK_PATIENTS
    return {
        "patients": [
            {"id": p.patient_id, "name": p.name, "age": p.age, "conditions": p.conditions}
            for p in MOCK_PATIENTS.values()
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)