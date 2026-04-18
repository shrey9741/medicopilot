# 🏥 MediCopilot — AI Clinical Copilot

> A2A-powered pre-visit patient briefing system — Production-Grade Edition v2.0.0

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)](https://react.dev)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange?style=flat)](https://groq.com)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat&logo=jsonwebtokens)](https://jwt.io)
[![FHIR](https://img.shields.io/badge/FHIR-R4-red?style=flat)](https://hapi.fhir.org)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat&logo=render)](https://medicopilot.onrender.com/health)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat)](LICENSE)

---

## 📌 The Problem

Doctors waste 8–15 minutes per patient reviewing scattered chart data before each visit — conditions, medications, recent labs, vitals, interaction risks. This time pressure leads to missed findings and rushed decisions.

## 💡 The Solution

MediCopilot is an intelligent A2A-powered clinical copilot that generates a structured 60-second pre-visit briefing. It reads real FHIR R4 patient data, runs it through 9 specialized AI agents, and delivers a complete report — differential diagnosis, drug safety alerts, risk scores, and a ready-to-file SOAP note — all behind JWT-protected endpoints with full request tracing.

---

## 🌐 Live Links

| Service | URL | Status |
|---------|-----|--------|
| 🖥️ Frontend (React) | — | Week 2 — Coming Soon |
| ⚙️ Backend API (Render) | https://medicopilot.onrender.com | ✅ Live |
| 📋 API Docs (Swagger) | https://medicopilot.onrender.com/docs | ✅ Live |
| ❤️ Health Check | https://medicopilot.onrender.com/health | ✅ Live |
| 🔐 Login Endpoint | https://medicopilot.onrender.com/auth/login | ✅ Live |

---

## 🆕 What's New in v2.0.0

| Feature | Details |
|---------|---------|
| **JWT Authentication** | Doctor login/logout with 8-hour tokens — `/auth/login`, `/auth/me`, `/auth/logout` |
| **HAPI FHIR Integration** | Real patient data from public R4 sandbox — automatic mock fallback |
| **Structured Logging** | Every request gets a unique trace ID — JSON logs in production |
| **Protected Endpoints** | `/invoke` and `/patients` now require a valid Bearer token |
| **React Frontend** | 4-page Clinical Sentinel UI — Dashboard, Briefing, SOAP, Agents (Week 2) |
| **Voice Briefings** | Hands-free pre-visit audio via gTTS — doctor listens while walking in (Phase 2) |
| **RAGAS Evaluation** | RAG faithfulness scores visible in UI — `/metrics` endpoint (Phase 3) |
| **CORS Ready** | Configured for React dev server and production frontend URL |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Vital Anomaly Detection** | Rule-based pre-LLM check — flags URGENT/CRITICAL vitals instantly |
| **Temporal Patient Memory** | Tracks glucose, BP, HR trends across visits — detects worsening patterns |
| **RAG Medical Knowledge** | FAISS vectorstore with WHO/ADA/ACC/JNC guidelines — cited in every output |
| **Differential Diagnosis** | Ranked DDx with confidence scores, clinical reasoning, and explainability |
| **Drug Interaction Matrix** | Checks all medications for interactions, contraindications, and allergy conflicts |
| **Risk Scoring** | Cardiovascular and condition-specific risk percentages with contributing factors |
| **Second Opinion Mode** | A separate agent challenges the primary diagnosis — devil's advocate reasoning |
| **SOAP Note Generator** | Synthesizes all agent outputs into structured S/O/A/P clinical documentation |
| **Agent Reasoning Trace** | Full audit trail showing which agent did what and why |
| **Voice Briefings** | Text-to-speech pre-visit audio — hands-free clinical workflow (Phase 2) |

---

## 🏗️ Architecture

```
Clinician / EHR Session
          ↓
  JWT Authentication Layer
          ↓
  MediCopilot Orchestrator Agent
    ↙         ↓          ↘
DiagnosisAgent  DrugSafetyAgent  RiskScoringAgent
    ↘         ↓          ↙
HAPI FHIR Layer  +  RAG Knowledge Layer
    ↘         ↓          ↙
      LLM Reasoning Layer
      (Groq · Llama 3.1-8b)
          ↓
   Structured Clinical Briefing
(DDx · Drug Safety · Risk · SOAP · Trace)
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | Groq API — `llama-3.1-8b-instant` | Fast inference for all 9 agents |
| **RAG** | LangChain + FAISS + TF-IDF | Medical guideline retrieval |
| **Backend** | FastAPI + Uvicorn | REST API + A2A endpoints |
| **Auth** | python-jose + passlib + bcrypt | JWT doctor authentication |
| **FHIR** | HAPI FHIR R4 public sandbox | Real patient data with mock fallback |
| **Logging** | structlog | Structured JSON logs with request tracing |
| **Frontend** | React + Vite + Tailwind | 4-page Clinical Sentinel UI (Week 2) |
| **Backend Deploy** | Render (free tier) | Auto-deploy from GitHub |
| **Frontend Deploy** | Netlify / Vercel | Static React build (Week 2) |

---

## 🤖 The 9 Agents

| Agent | Role |
|-------|------|
| **FHIRAgent** | Fetches patient bundle from HAPI FHIR R4 sandbox (real data) |
| **MemoryAgent** | Analyzes visit history for clinical trends |
| **AnomalyDetector** | Rule-based vital sign anomaly detection (runs before LLM) |
| **RAGAgent** | Retrieves relevant medical guidelines from FAISS vectorstore |
| **DiagnosisAgent** | Generates differential diagnosis with confidence scores |
| **DrugSafetyAgent** | Checks medication interactions and contraindications |
| **RiskScoringAgent** | Calculates risk percentages using Framingham/ACC guidelines |
| **SecondOpinionAgent** | Challenges primary diagnosis for balanced assessment |
| **SOAPNoteGenerator** | Synthesizes all outputs into clinical documentation |

---

## 📁 Project Structure

```
medicopilot/
├── main.py                      # FastAPI app v2.0 — JWT protected endpoints
├── logging_config.py            # Structlog configuration
├── middleware.py                # Request tracing middleware
├── requirements.txt
├── render.yaml                  # Render deployment config
├── Procfile
├── auth/
│   ├── __init__.py
│   ├── jwt_handler.py           # Token creation and verification
│   ├── middleware.py            # FastAPI JWT dependency
│   ├── models.py                # LoginRequest, TokenResponse schemas
│   └── registry.py             # Doctor credentials store
├── routes/
│   ├── __init__.py
│   └── auth_router.py          # /auth/login, /auth/me, /auth/logout
├── frontend/                    # React app — Week 2
│   └── src/pages/              # Dashboard, Briefing, SOAP, Agents
├── models/
│   └── schemas.py              # Pydantic data models
├── fhir/
│   ├── hapi_client.py          # HAPI FHIR R4 client + mock fallback
│   └── mock_client.py          # 13 demo patients — fallback data
├── rag/
│   └── retriever.py            # FAISS vectorstore + TF-IDF embeddings
└── agents/
    ├── orchestrator.py         # Main pipeline — coordinates all 9 agents
    ├── anomaly_detector.py
    ├── memory.py
    ├── diagnosis_agent.py
    ├── drug_agent.py
    ├── risk_agent.py
    ├── second_opinion_agent.py
    └── soap_generator.py
```

---

## 🚀 Local Setup

### Prerequisites

- Python 3.11+
- Node.js 18+ (for React frontend)
- Groq API key — free at [console.groq.com](https://console.groq.com)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/shrey9741/medicopilot.git
cd medicopilot

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in your keys
```

### Environment Variables

```env
GROQ_API_KEY=gsk_your_key_here
JWT_SECRET_KEY=your_32_char_secret_here
ENV=dev
FHIR_USE_MOCK=false
```

Generate your JWT secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Run the Backend

```bash
uvicorn main:app --reload --port 8000
```

| URL | Expected Response |
|-----|------------------|
| http://localhost:8000/health | `{"status": "ok", "version": "2.0.0"}` |
| http://localhost:8000/docs | Swagger UI with all endpoints |
| http://localhost:8000/auth/login | POST — returns JWT token |
| http://localhost:8000/patients | GET — requires Bearer token |

---

## 🔌 API Reference

### POST /auth/login

Doctor login. Returns a JWT valid for 8 hours (one shift).

```json
{
  "username": "dr.thorne",
  "password": "demo123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "doctor_name": "Dr. Julian Thorne",
  "role": "Chief Medical Officer"
}
```

### POST /invoke 🔒

Main briefing endpoint. Requires `Authorization: Bearer <token>`.

```json
{
  "patient_id": "P001",
  "sharp_token": "optional"
}
```

### GET /patients 🔒

Returns patient list from HAPI FHIR sandbox (or mock fallback).

### GET /auth/me 🔒

Returns the currently authenticated doctor's info from the JWT.

### GET /health

```json
{
  "status": "ok",
  "version": "2.0.0",
  "rag_loaded": true,
  "model": "llama-3.1-8b-instant"
}
```

---

## 👥 Demo Patients

13 mock patients across 5 clinical categories:

| ID | Name | Conditions |
|----|------|-----------|
| P001 | John Doe, 62M | Type 2 Diabetes, Hypertension, CKD Stage 2 |
| P002 | Sarah Chen, 45F | Atrial Fibrillation, Hypothyroidism, Obesity |
| P003 | Marcus Johnson, 71M | COPD, Heart Failure (EF 35%), T2 Diabetes |
| P004 | Patricia Williams, 54F | Stage III Breast Cancer (HER2+), Anemia |
| P005 | Robert Nguyen, 67M | Stage IV Lung Cancer, COPD, Cachexia |
| P006 | Aiden Patel, 8M | Type 1 Diabetes, Asthma, ADHD |
| P007 | Lily Thompson, 5F | ALL Leukemia (Maintenance), Immunosuppression |
| P008 | Diana Foster, 34F | Bipolar I, Generalized Anxiety, Hypothyroidism |
| P009 | Carlos Rivera, 28M | Schizophrenia, Substance Use, Metabolic Syndrome |
| P010 | Eleanor Voss, 41F | SLE, Lupus Nephritis, Antiphospholipid Syndrome |
| P011 | Samuel Okafor, 19M | Cystic Fibrosis, CF-related Diabetes |
| P012 | Ingrid Larsson, 37F | Multiple Sclerosis (RRMS), Major Depression |
| P013 | Theo Blackwood, 52M | ALS, Respiratory Insufficiency, Dysphagia |

---

## 🌐 Deployment

### Backend → Render

Render auto-deploys from GitHub on every push. Add these environment variables in the Render dashboard:

| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | your Groq API key |
| `JWT_SECRET_KEY` | 32-char random secret |
| `ENV` | `production` |
| `FHIR_USE_MOCK` | `false` |

### Frontend → Netlify (Week 2)

```bash
cd frontend
npm run build
# Deploy /dist to Netlify
# Set env: VITE_API_URL=https://medicopilot.onrender.com
```

---

## 🗺️ Roadmap

| Phase | Status | Features |
|-------|--------|---------|
| Phase 1 — Week 1 | ✅ Complete | JWT auth, HAPI FHIR, structured logging |
| Phase 1 — Week 2 | 🔄 In Progress | React frontend — 4 pages |
| Phase 2 | 📋 Planned | Voice briefings with gTTS / ElevenLabs |
| Phase 3 | 📋 Planned | RAGAS scores, `/metrics` endpoint, real performance numbers |

---

## 🔮 Future Scope

- **Real EHR Integration** — Connect to Epic, Cerner, or any FHIR R4 compliant EHR
- **Multi-hospital Support** — Multi-tenant architecture with SHARP token isolation
- **Streaming Responses** — Real-time agent output streaming via WebSockets
- **Voice Briefings** — Text-to-speech SOAP note delivery for hands-free use
- **Specialist Mode** — Cardiology, Oncology, Pediatrics specialist agent prompts
- **Outcome Tracking** — Compare AI predictions against actual diagnoses over time
- **RAGAS Evaluation** — Faithfulness, relevancy, and precision scores in the UI

---

## 👨‍💻 Author

**Shrey Kumar**

- GitHub: [@shrey9741](https://github.com/shrey9741)
- Repository: [github.com/shrey9741/medicopilot](https://github.com/shrey9741/medicopilot)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> Built for the Prompt Opinion Healthcare AI Hackathon · Powered by Groq · HAPI FHIR R4 · JWT Secured · A2A Compatible
