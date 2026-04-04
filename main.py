"""
MediCopilot FastAPI Backend.
Exposes the A2A agent via HTTP endpoints.
The /.well-known/agent.json endpoint registers it with Prompt Opinion.
"""
import os
import asyncio
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
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
    print("Loading RAG vectorstore in background...")
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
    return {
        "name": "MediCopilot",
        "description": "AI Clinical Copilot — pre-visit patient briefing with multi-agent reasoning, drug safety, risk scoring and SOAP notes.",
        "url": "https://medicopilot.onrender.com",
        "version": "1.0.0",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False
        },
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": "clinical_briefing",
                "name": "Clinical Briefing",
                "description": "Generates pre-visit patient briefing from FHIR data including DDx, drug safety, risk scores and SOAP note",
                "inputModes": ["text"],
                "outputModes": ["text"],
                "examples": ["Generate briefing for patient P001"]
            }
        ]
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


@app.head("/health")
async def health_head():
    """HEAD endpoint for UptimeRobot monitoring."""
    return Response(status_code=200)


@app.get("/patients")
async def list_patients():
    """Demo endpoint — lists all available mock patients."""
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