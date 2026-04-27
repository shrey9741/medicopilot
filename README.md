# 🏥 MediCopilot — AI Clinical Copilot

> Production-Grade A2A Medical AI — Pre-visit patient briefing in under 5 seconds.

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat&logo=react)](https://react.dev)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange?style=flat)](https://groq.com)
[![JWT](https://img.shields.io/badge/Auth-JWT-black?style=flat&logo=jsonwebtokens)](https://jwt.io)
[![FHIR](https://img.shields.io/badge/FHIR-R4-red?style=flat)](https://hapi.fhir.org)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat&logo=render)](https://medicopilot.onrender.com/health)
[![Frontend](https://img.shields.io/badge/Frontend-Netlify-00C7B7?style=flat&logo=netlify)](https://medicopilotproj.netlify.app)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat)](LICENSE)

---

## 📌 The Problem

Doctors waste **8–15 minutes per patient** reviewing scattered chart data before each visit. This time pressure leads to missed findings and rushed decisions.

## 💡 The Solution

MediCopilot orchestrates **9 specialized AI agents** that process real FHIR R4 patient data and deliver a complete clinical briefing in under 5 seconds — differential diagnosis, drug safety alerts, risk scores, voice briefing, and a ready-to-file SOAP note — all behind JWT-protected endpoints.

---

## 🌐 Live Links

| Service | URL | Status |
|---------|-----|--------|
| 🖥️ Frontend (React) | [medicopilotproj.netlify.app](https://medicopilotproj.netlify.app) | ✅ Live |
| ⚙️ Backend API | [medicopilot.onrender.com](https://medicopilot.onrender.com) | ✅ Live |
| 📋 Swagger Docs | [medicopilot.onrender.com/docs](https://medicopilot.onrender.com/docs) | ✅ Live |
| ❤️ Health Check | [medicopilot.onrender.com/health](https://medicopilot.onrender.com/health) | ✅ Live |

**Demo login:** `dr.thorne` / `demo123`

---

## 📋 Version History

### v1.0.0 — Hackathon MVP
> The original submission — a working AI clinical copilot built in days.

**What was built:**
- Streamlit frontend — "Clinical Luminary" dark UI
- FastAPI backend with A2A `/invoke` endpoint
- 9 specialized AI agents orchestrated in sequence
- Mock FHIR R4 patient data (13 patients across 4 categories)
- FAISS vectorstore with WHO/ADA/ACC/JNC medical guidelines
- Differential diagnosis with confidence scores
- Drug interaction matrix
- Risk scoring (Framingham/ACC)
- Second opinion agent
- SOAP note generator
- Agent reasoning trace
- Deployed on Render (backend) + Streamlit Cloud (frontend)

**Tech Stack:** Python · FastAPI · Streamlit · Groq · LangChain · FAISS

---

### v2.0.0 — Production-Grade Edition ✅ Current
> A complete architectural upgrade — from hackathon demo to production-ready system.

**What changed:**

| Area | v1.0 | v2.0 |
|------|------|------|
| **Auth** | None — open endpoints | JWT authentication (8-hour tokens) |
| **Frontend** | Streamlit | React + Vite + Tailwind — 4-page Clinical Sentinel UI |
| **FHIR** | 13 hardcoded mock patients | HAPI FHIR R4 public sandbox (real data) + mock fallback |
| **Logging** | print() statements | structlog — JSON logs with unique trace IDs per request |
| **Security** | CORS open (`*`) | CORS locked to specific origins |
| **Deployment** | Streamlit Cloud | Netlify (frontend) + Render (backend) |
| **Voice** | None | Browser TTS — reads AI briefing aloud |
| **Endpoints** | Public | JWT-protected `/invoke` and `/patients` |

**New pages in React:**
- `/dashboard` — Live patient list from HAPI FHIR sandbox
- `/patient/:id` — Full clinical briefing with AI agent log
- `/soap` — Interactive SOAP note editor
- `/agents` — Agent orchestration trace visualizer

**New backend modules:**
- `auth/` — JWT handler, middleware, doctor registry
- `routes/auth_router.py` — `/auth/login`, `/auth/me`, `/auth/logout`
- `fhir/hapi_client.py` — Real FHIR R4 client with mock fallback
- `logging_config.py` — Structlog configuration
- `middleware.py` — Request tracing middleware

---

### v3.0.0 — The Intelligence Layer 🔭 Planned
> Making MediCopilot genuinely smarter and more production-hardened.

**3 features planned:**

#### 1. 🎙️ ElevenLabs Voice Briefings
Replace browser TTS with ElevenLabs premium voice synthesis.
- Doctor clicks a patient → AI generates briefing → plays as natural speech
- "Hands-free pre-visit briefing" — doctor listens while walking to the room
- Multiple voice options (male/female, accent, speed)
- Falls back to browser TTS if API key not set

```python
# Planned endpoint
POST /voice/briefing/{patient_id}
→ Returns MP3 stream of the clinical briefing
```

#### 2. 📊 RAGAS Evaluation + /metrics Endpoint
Make the AI measurable and trustworthy.
- Every briefing scored for faithfulness, relevancy, and context precision
- Live `/metrics` endpoint showing real performance numbers
- Scores visible in the Agent Orchestration page UI

```json
GET /metrics
{
  "total_briefings": 142,
  "avg_latency_ms": 4200,
  "avg_ragas_faithfulness": 0.87,
  "avg_context_precision": 0.91,
  "fhir_source": "hapi_sandbox"
}
```

#### 3. 🏥 Full FHIR Patient Briefings
Wire real HAPI FHIR patient data into all 9 agents (not just the patient list).
- Currently: patient list = real FHIR, briefing = mock patient profiles
- v3.0: both patient list AND briefing use real FHIR data end-to-end
- Requires rewriting agent input schemas to accept FHIR Bundle format
- Patients from the HAPI sandbox get real AI analysis, not mock data

```
Current flow:    FHIR list → mock briefing
v3.0 flow:       FHIR list → FHIR briefing → real clinical output
```

---

## ✨ Current Features (v2.0)

| Feature | Description |
|---------|-------------|
| **JWT Authentication** | Doctor login with 8-hour session tokens |
| **HAPI FHIR R4** | Real patient data from public sandbox + mock fallback |
| **9 AI Agents** | Specialized agents for diagnosis, drug safety, risk scoring |
| **Voice Briefings** | Browser TTS reads the AI briefing aloud — hands-free |
| **Structured Logging** | Every request has a unique trace ID — JSON logs |
| **SOAP Notes** | Auto-generated S/O/A/P clinical documentation |
| **RAG Pipeline** | FAISS vectorstore with WHO/ADA/ACC/JNC guidelines |
| **React Frontend** | 4-page Clinical Sentinel UI — dark sidebar, live data |
| **Second Opinion** | A separate agent challenges the primary diagnosis |
| **Anomaly Detection** | Rule-based pre-LLM vital sign checks |

---

## 🤖 The 9 Agents

| Agent | Role |
|-------|------|
| **FHIRAgent** | Fetches patient bundle from HAPI FHIR R4 sandbox |
| **MemoryAgent** | Analyzes visit history for clinical trends |
| **AnomalyDetector** | Rule-based vital sign anomaly detection (pre-LLM) |
| **RAGAgent** | Retrieves relevant medical guidelines from FAISS |
| **DiagnosisAgent** | Generates differential diagnosis with confidence scores |
| **DrugSafetyAgent** | Checks medication interactions and contraindications |
| **RiskScoringAgent** | Calculates risk % using Framingham/ACC guidelines |
| **SecondOpinionAgent** | Challenges primary diagnosis for balanced assessment |
| **SOAPNoteGenerator** | Synthesizes all outputs into clinical documentation |

---

## 🏗️ Architecture

```
Clinician Login (JWT)
        ↓
MediCopilot Orchestrator
   ↙      ↓       ↘
FHIR   RAG KB   Memory
   ↘      ↓       ↙
  9 Specialized AI Agents
  (Groq · Llama 3.1-8b-instant)
        ↓
  Structured Clinical Briefing
  DDx · Drug Safety · Risk · SOAP · Voice
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **LLM** | Groq — `llama-3.1-8b-instant` | Fast inference for all 9 agents |
| **RAG** | LangChain + FAISS + TF-IDF | Medical guideline retrieval |
| **Backend** | FastAPI + Uvicorn | REST API + A2A endpoints |
| **Auth** | python-jose + passlib + bcrypt | JWT doctor authentication |
| **FHIR** | HAPI FHIR R4 public sandbox | Real patient data |
| **Logging** | structlog | JSON logs with trace IDs |
| **Frontend** | React + Vite + Tailwind | 4-page Clinical Sentinel UI |
| **Backend Deploy** | Render | Auto-deploy from GitHub |
| **Frontend Deploy** | Netlify | Auto-deploy from GitHub |

---

## 📁 Project Structure

```
medicopilot/
├── main.py                  # FastAPI v2.0 — JWT protected endpoints
├── logging_config.py        # Structlog configuration
├── middleware.py            # Request tracing middleware
├── requirements.txt
├── render.yaml              # Render deployment config
├── Procfile
├── auth/                    # JWT auth — login, tokens, registry
│   ├── jwt_handler.py
│   ├── middleware.py
│   ├── models.py
│   └── registry.py
├── routes/
│   └── auth_router.py       # /auth/login, /auth/me, /auth/logout
├── fhir/
│   ├── hapi_client.py       # HAPI FHIR R4 client + mock fallback
│   └── mock_client.py       # 13 demo patients
├── rag/
│   └── retriever.py         # FAISS vectorstore
├── agents/
│   ├── orchestrator.py      # Main pipeline — 9 agents
│   ├── anomaly_detector.py
│   ├── diagnosis_agent.py
│   ├── drug_agent.py
│   ├── risk_agent.py
│   ├── second_opinion_agent.py
│   └── soap_generator.py
├── models/
│   └── schemas.py
└── frontend/                # React app
    └── src/
        ├── components/      # Shared Sidebar
        ├── pages/           # Dashboard, Briefing, SOAP, Agents
        ├── api/             # Axios + JWT interceptors
        └── store/           # Zustand auth store
```

---

## 🚀 Local Setup

```bash
# Clone
git clone https://github.com/shrey9741/medicopilot.git
cd medicopilot

# Backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Environment
cp .env.example .env
# Fill in GROQ_API_KEY and JWT_SECRET_KEY

# Run backend
uvicorn main:app --reload --port 8000

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Environment Variables

```env
GROQ_API_KEY=gsk_your_key_here
JWT_SECRET_KEY=your_32_char_secret
ENV=dev
FHIR_USE_MOCK=false
FRONTEND_URL=https://medicopilotproj.netlify.app
```

---

## 🔌 API Reference

### `POST /auth/login`
```json
{ "username": "dr.thorne", "password": "demo123" }
```

### `POST /invoke` 🔒
```json
{ "patient_id": "P001", "sharp_token": null }
```

### `GET /patients` 🔒
Returns patient list from HAPI FHIR sandbox or mock fallback.

### `GET /health`
```json
{
  "status": "ok",
  "version": "2.0.0",
  "rag_loaded": true,
  "model": "llama-3.1-8b-instant"
}
```

---

## 👥 Demo Patients (13 Mock Patients)

| ID | Name | Conditions |
|----|------|-----------|
| P001 | John Doe, 62M | Type 2 Diabetes, Hypertension, CKD Stage 2 |
| P002 | Sarah Chen, 45F | Atrial Fibrillation, Hypothyroidism |
| P003 | Marcus Johnson, 71M | COPD, Heart Failure (EF 35%) |
| P004 | Patricia Williams, 54F | Stage III Breast Cancer (HER2+) |
| P005 | Robert Nguyen, 67M | Stage IV Lung Cancer, COPD |
| P006 | Aiden Patel, 8M | Type 1 Diabetes, Asthma, ADHD |
| P007 | Lily Thompson, 5F | ALL Leukemia, Immunosuppression |
| P008 | Diana Foster, 34F | Bipolar I, Generalized Anxiety |
| P009 | Carlos Rivera, 28M | Schizophrenia, Substance Use |
| P010 | Eleanor Voss, 41F | SLE, Lupus Nephritis |
| P011 | Samuel Okafor, 19M | Cystic Fibrosis, CF-related Diabetes |
| P012 | Ingrid Larsson, 37F | Multiple Sclerosis (RRMS) |
| P013 | Theo Blackwood, 52M | ALS, Respiratory Insufficiency |

---

## 🌐 Deployment

### Backend → Render

| Variable | Value |
|----------|-------|
| `GROQ_API_KEY` | your Groq key |
| `JWT_SECRET_KEY` | 32-char random secret |
| `ENV` | `production` |
| `FHIR_USE_MOCK` | `false` |
| `FRONTEND_URL` | `https://medicopilotproj.netlify.app` |

### Frontend → Netlify

| Setting | Value |
|---------|-------|
| Base directory | `frontend` |
| Build command | `npm run build` |
| Publish directory | `frontend/dist` |
| `VITE_API_URL` | `https://medicopilot.onrender.com` |

---

## 🗺️ Roadmap

| Version | Status | Highlights |
|---------|--------|-----------|
| **v1.0.0** | ✅ Complete | Streamlit UI, 9 agents, mock FHIR, Groq LLM |
| **v2.0.0** | ✅ Complete | React frontend, JWT auth, real FHIR, structured logging |
| **v3.0.0** | 🔭 Planned | ElevenLabs voice, RAGAS metrics, full FHIR briefings |

---

## 👨‍💻 Author

**Shrey Kumar**
- GitHub: [@shrey9741](https://github.com/shrey9741)
- Repo: [github.com/shrey9741/medicopilot](https://github.com/shrey9741/medicopilot)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> Built for the Prompt Opinion Healthcare AI Hackathon · Powered by Groq · HAPI FHIR R4 · JWT Secured · React + Netlify · A2A Compatible
