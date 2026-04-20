"""
MediCopilot FastAPI Backend — v2.0.0
Upgraded from v1.0.0 with:
  - JWT authentication on /invoke and /patients
  - HAPI FHIR sandbox with mock fallback
  - Structured request logging with trace IDs
  - React frontend CORS support

Everything from the original is preserved:
  - RAG vectorstore loaded at startup
  - run_medicopilot orchestrator (unchanged)
  - All original endpoints still work
"""
import os
import asyncio
from contextlib import asynccontextmanager

import structlog
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware

# ── New modules (Week 1) ─────────────────────────────────────────────

from logging_config import configure_logging
from middleware import RequestTracingMiddleware
from auth import get_current_doctor
from routes.auth_router import router as auth_router
from fhir.hapi_client import get_patient_data, HAPIFHIRClient

# ── Original modules (unchanged) ─────────────────────────────────────

from rag.retriever import load_vectorstore
from agents.orchestrator import run_medicopilot
from models.schemas import InvokeRequest, MediCopilotResponse

load_dotenv()
configure_logging()
logger = structlog.get_logger("main")

# Global vectorstore — loaded once at startup, just like before

vectorstore = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global vectorstore
    loop = asyncio.get_event_loop()
    logger.info("medicopilot.startup", env=os.getenv("ENV", "production"))
    logger.info("rag.loading")
    vectorstore = await loop.run_in_executor(None, load_vectorstore)
    logger.info("rag.ready")
    yield
    logger.info("medicopilot.shutdown")


app = FastAPI(
    title="MediCopilot API",
    description="AI Clinical Copilot — Pre-visit patient briefing with multi-agent collaboration",
    version="2.0.0",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────────────
app.add_middleware(RequestTracingMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        os.getenv("FRONTEND_URL", ""),
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────
app.include_router(auth_router)


# ── Endpoints ─────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "rag_loaded": vectorstore is not None,
        "model": "llama-3.1-8b-instant",
        "agents": [
            "FHIRAgent", "MemoryAgent", "AnomalyDetector", "RAGAgent",
            "DiagnosisAgent", "DrugSafetyAgent", "RiskScoringAgent",
            "SecondOpinionAgent", "SOAPNoteGenerator"
        ],
    }


@app.head("/health")
async def health_head():
    return Response(status_code=200)


@app.get("/.well-known/agent.json")
async def agent_card():
    return {
        "name": "MediCopilot",
        "description": "AI Clinical Copilot — pre-visit patient briefing with multi-agent reasoning.",
        "url": os.getenv("BACKEND_URL", "https://medicopilot.onrender.com"),
        "version": "2.0.0",
        "capabilities": {"streaming": False, "pushNotifications": False},
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [{
            "id": "clinical_briefing",
            "name": "Clinical Briefing",
            "description": "Generates pre-visit patient briefing from FHIR data",
            "inputModes": ["text"],
            "outputModes": ["text"],
            "examples": ["Generate briefing for patient P001"],
        }],
    }


@app.get("/patients")
async def list_patients(
    name: str | None = None,
    current_doctor: dict = Depends(get_current_doctor),
):
    logger.info("patients.list", doctor=current_doctor.get("sub"), query=name)
    try:
        if os.getenv("FHIR_USE_MOCK", "false").lower() == "true":
            raise ValueError("mock mode enabled")
        client = HAPIFHIRClient()
        patients = await client.search_patients(name=name, count=20)
        await client.close()
        logger.info("patients.fhir_ok", count=len(patients))
        return {"patients": patients, "source": "hapi_fhir"}
    except Exception as exc:
        logger.warning("patients.fallback_mock", error=str(exc))
        from fhir.mock_client import MOCK_PATIENTS
        return {
            "patients": [
                {"id": p.patient_id, "name": p.name, "age": p.age, "conditions": p.conditions}
                for p in MOCK_PATIENTS.values()
            ],
            "source": "mock",
        }


@app.post("/invoke", response_model=MediCopilotResponse)
async def invoke(
    request: InvokeRequest,
    current_doctor: dict = Depends(get_current_doctor),
):
    if not vectorstore:
        raise HTTPException(status_code=503, detail="RAG vectorstore not initialized")

    logger.info(
        "invoke.start",
        patient_id=request.patient_id,
        doctor=current_doctor.get("sub"),
    )

    try:
        result = run_medicopilot(
            patient_id=request.patient_id,
            vectorstore=vectorstore,
            sharp_token=request.sharp_token,
        )
        logger.info("invoke.complete", patient_id=request.patient_id)
        return result
    except Exception as e:
        logger.error("invoke.failed", patient_id=request.patient_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
