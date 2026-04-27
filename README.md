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

## ✨ Features

| Feature | Description |
|---------|-------------|
| **JWT Authentication** | Doctor login with 8-hour session tokens |
| **HAPI FHIR R4** | Real patient data from public sandbox + mock fallback |
| **9 AI Agents** | Specialized agents for diagnosis, drug safety, risk scoring |
| **Voice Briefings** | Browser TTS reads the AI briefing aloud — hands-free |
| **Structured Logging** | Every request has a unique trace ID — JSON logs in production |
| **SOAP Notes** | Auto-generated S/O/A/P clinical documentation |
| **RAG Pipeline** | FAISS vectorstore with WHO/ADA/ACC/JNC medical guidelines |
| **React Frontend** | 4-page Clinical Sentinel UI — dark sidebar, live FHIR data |
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
│   └── schemas.py           # Pydantic schemas
└── frontend/                # React app
    └── src/
        ├── components/      # Shared Sidebar component
        ├── pages/           # Dashboard, Briefing, SOAP, Agents
        ├── api/             # Axios client + JWT interceptors
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
```

Generate JWT secret:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 🔌 API Reference

### `POST /auth/login`
```json
{ "username": "dr.thorne", "password": "demo123" }
```
Returns a JWT valid for 8 hours (one shift).

### `POST /invoke` 🔒
```json
{ "patient_id": "P001", "sharp_token": null }
```
Runs 9 agents and returns a full clinical briefing.

### `GET /patients` 🔒
Returns patient list from HAPI FHIR sandbox (or mock fallback).

### `GET /health`
```json
{ "status": "ok", "version": "2.0.0", "rag_loaded": true }
```

---

## 👥 Demo Patients

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

| Phase | Status | Features |
|-------|--------|---------|
| Phase 1 — Week 1 | ✅ Complete | JWT auth, HAPI FHIR, structured logging |
| Phase 1 — Week 2 | ✅ Complete | React frontend, Netlify deployment |
| Phase 2 | 🔄 Next | Full FHIR patient briefings, ElevenLabs voice |
| Phase 3 | 📋 Planned | RAGAS scores, `/metrics` endpoint |

---

## 🔮 Future Scope

- **Full FHIR Briefings** — Wire real FHIR patient data into all 9 agents
- **Real EHR Integration** — Epic, Cerner, any FHIR R4 compliant system
- **ElevenLabs Voice** — Premium TTS for production voice briefings
- **Streaming Responses** — Real-time agent output via WebSockets
- **RAGAS Evaluation** — Faithfulness scores visible in the UI
- **Specialist Mode** — Cardiology, Oncology, Pediatrics agent tuning
- **Outcome Tracking** — Compare AI predictions against actual diagnoses

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
