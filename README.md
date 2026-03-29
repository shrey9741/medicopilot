# 🏥 MediCopilot — AI Clinical Copilot

> A2A-powered pre-visit patient briefing system built for the Prompt Opinion Healthcare AI Hackathon

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.36-ff4b4b?style=flat&logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-orange?style=flat)](https://groq.com)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-ff4b4b?style=flat&logo=streamlit)](https://medicopilot-swrq8wx29e4obrraeuamku.streamlit.app)
[![Backend](https://img.shields.io/badge/Backend-Render-46E3B7?style=flat&logo=render)](https://medicopilot.onrender.com/health)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat)](LICENSE)

---

## 📌 The Problem

Doctors waste 8–15 minutes per patient reviewing scattered chart data before each visit — conditions, medications, recent labs, vitals, interaction risks. This time pressure leads to missed findings and rushed decisions.

## 💡 The Solution

MediCopilot is an intelligent A2A agent that generates a structured 60-second clinical briefing before the doctor walks in. It reads FHIR patient data, runs it through 9 specialized AI sub-agents, and delivers a complete pre-visit report with differential diagnosis, drug safety alerts, risk scores, and a ready-to-file SOAP note.

---

## 🌐 Live Links

| Service | URL |
|---|---|
| 🖥️ Frontend (Streamlit) | https://medicopilot-swrq8wx29e4obrraeuamku.streamlit.app |
| ⚙️ Backend API (Render) | https://medicopilot.onrender.com |
| 📋 API Docs (Swagger) | https://medicopilot.onrender.com/docs |
| ❤️ Health Check | https://medicopilot.onrender.com/health |

---

## ✨ Features

| Feature | Description |
|---|---|
| **Vital Anomaly Detection** | Rule-based pre-LLM check — flags URGENT/CRITICAL vitals instantly |
| **Temporal Patient Memory** | Tracks glucose, BP, HR trends across visits — detects worsening patterns |
| **RAG Medical Knowledge** | FAISS vectorstore with WHO/ADA/ACC/JNC guidelines — cited in every output |
| **Differential Diagnosis** | Ranked DDx with confidence scores, clinical reasoning, and explainability |
| **Drug Interaction Matrix** | Checks all medications for interactions, contraindications, and allergy conflicts |
| **Risk Scoring** | Cardiovascular and condition-specific risk percentages with contributing factors |
| **Second Opinion Mode** | A separate agent challenges the primary diagnosis — devil's advocate reasoning |
| **SOAP Note Generator** | Synthesizes all agent outputs into structured S/O/A/P clinical documentation |
| **Agent Reasoning Trace** | Full audit trail showing which agent did what and why |

---

## 🏗️ Architecture

```
Clinician / EHR Session (SHARP Context + Patient ID)
                    ↓
        Prompt Opinion A2A Platform
                    ↓
        MediCopilot Orchestrator Agent
          ↙         ↓          ↘
 DiagnosisAgent  DrugSafetyAgent  RiskScoringAgent
          ↘         ↓          ↙
      FHIR Layer    +    RAG Knowledge Layer
          ↘         ↓          ↙
            LLM Reasoning Layer
            (Groq · Llama 3.1-8b)
                    ↓
         Structured Clinical Briefing
   (DDx · Drug Safety · Risk · SOAP · Trace)
```

### The 9 Agents

| Agent | Role |
|---|---|
| FHIRAgent | Fetches patient bundle from FHIR R4 server |
| MemoryAgent | Analyzes visit history for clinical trends |
| AnomalyDetector | Rule-based vital sign anomaly detection (runs before LLM) |
| RAGAgent | Retrieves relevant medical guidelines from FAISS |
| DiagnosisAgent | Generates differential diagnosis with confidence scores |
| DrugSafetyAgent | Checks medication interactions and contraindications |
| RiskScoringAgent | Calculates risk percentages using Framingham/ACC guidelines |
| SecondOpinionAgent | Challenges primary diagnosis for balanced assessment |
| SOAPNoteGenerator | Synthesizes all outputs into clinical documentation |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Groq API — `llama-3.1-8b-instant` |
| **RAG** | LangChain + FAISS + TF-IDF embeddings (sklearn) |
| **Backend** | FastAPI + Uvicorn |
| **Frontend** | Streamlit — "Clinical Luminary" dark UI |
| **FHIR** | Simulated FHIR R4 patient bundles (13 patients) |
| **Platform** | Prompt Opinion A2A (COIN protocol) |
| **Backend Deploy** | Render (free tier) |
| **Frontend Deploy** | Streamlit Community Cloud (free tier) |

---

## 📁 Project Structure

```
medicopilot/
├── main.py                      # FastAPI app — /invoke, /.well-known/agent.json
├── app.py                       # Streamlit UI — Clinical Luminary dark theme
├── agent_card.json              # Prompt Opinion Marketplace registration
├── requirements.txt
├── render.yaml                  # Render deployment config
├── Procfile                     # Process file for deployment
├── test_local.py                # 27-check pre-flight test suite
├── models/
│   └── schemas.py               # All Pydantic data models
├── fhir/
│   └── mock_client.py           # Simulated FHIR R4 — 13 patients across 4 categories
├── rag/
│   └── retriever.py             # FAISS vectorstore + TF-IDF medical guidelines
└── agents/
    ├── orchestrator.py          # Main pipeline — coordinates all 9 agents
    ├── anomaly_detector.py      # Rule-based vital sign checks
    ├── memory.py                # Temporal patient trend analysis
    ├── diagnosis_agent.py       # Differential diagnosis with DDx format
    ├── drug_agent.py            # Drug interaction severity matrix
    ├── risk_agent.py            # Risk percentage scoring
    ├── second_opinion_agent.py  # Devil's advocate analysis
    └── soap_generator.py        # SOAP note generation
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.11+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/shrey9741/medicopilot.git
cd medicopilot/medicopilot

# 2. Create virtual environment
python -m venv venv

# Windows PowerShell
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run pre-flight tests (should show 27/27 checks passed)
python test_local.py

# 6. Start the backend (Terminal 1)
uvicorn main:app --reload --port 8000

# 7. Start the Streamlit UI (Terminal 2)
streamlit run app.py
```

### Verify Installation

| URL | Expected Response |
|---|---|
| http://localhost:8000/health | `{"status": "ok"}` |
| http://localhost:8000/.well-known/agent.json | Agent card JSON |
| http://localhost:8000/patients | List of 13 demo patients |
| http://localhost:8501 | Streamlit Clinical Luminary UI |

---

## 🔌 API Reference

### POST /invoke

Main A2A endpoint. Accepts patient ID and optional SHARP context.

**Request:**
```json
{
  "patient_id": "P001",
  "sharp_token": "optional-sharp-token",
  "fhir_token": "optional-fhir-bearer-token"
}
```

**Response:**
```json
{
  "patient_id": "P001",
  "patient_name": "John Doe",
  "anomaly_flag": {
    "triggered": true,
    "level": "URGENT",
    "reasons": ["Stage 2 hypertension: 148/92", "Elevated glucose: 210 mg/dL"]
  },
  "summary": "John Doe (62y Male) presents with 3 active conditions...",
  "diagnoses": [
    {
      "condition": "Uncontrolled Type 2 Diabetes",
      "reasoning": "HbA1c 8.2% and glucose 210 mg/dL indicate poor glycemic control",
      "confidence": 92,
      "tier": "critical"
    }
  ],
  "drug_warnings": [...],
  "risk_scores": [...],
  "second_opinion": {...},
  "soap_note": {
    "subjective": "...",
    "objective": "...",
    "assessment": "...",
    "plan": "..."
  },
  "reasoning_trace": [...],
  "rag_citations": [...],
  "memory_trend": "Glucose trend: 195 → 202 → 210 mg/dL (worsening, Δ+15)",
  "generated_at": "2026-03-29T00:00:00"
}
```

---

## 👥 Demo Patients

13 mock patients across 4 clinical categories:

### General Medicine
| ID | Name | Conditions |
|---|---|---|
| P001 | John Doe, 62M | Type 2 Diabetes, Hypertension, CKD Stage 2 |
| P002 | Sarah Chen, 45F | Atrial Fibrillation, Hypothyroidism, Obesity |
| P003 | Marcus Johnson, 71M | COPD, Heart Failure (EF 35%), T2 Diabetes |

### Oncology
| ID | Name | Conditions |
|---|---|---|
| P004 | Patricia Williams, 54F | Stage III Breast Cancer (HER2+), Anemia |
| P005 | Robert Nguyen, 67M | Stage IV Lung Cancer, COPD, Cachexia |

### Pediatric
| ID | Name | Conditions |
|---|---|---|
| P006 | Aiden Patel, 8M | Type 1 Diabetes, Asthma (Moderate Persistent), ADHD |
| P007 | Lily Thompson, 5F | ALL Leukemia (Maintenance Phase), Immunosuppression |

### Mental Health
| ID | Name | Conditions |
|---|---|---|
| P008 | Diana Foster, 34F | Bipolar I Disorder, Generalized Anxiety, Hypothyroidism |
| P009 | Carlos Rivera, 28M | Schizophrenia, Substance Use Disorder, Metabolic Syndrome |

### Rare & Complex Diseases
| ID | Name | Conditions |
|---|---|---|
| P010 | Eleanor Voss, 41F | Systemic Lupus Erythematosus, Lupus Nephritis, Antiphospholipid Syndrome |
| P011 | Samuel Okafor, 19M | Cystic Fibrosis (F508del), CF-related Diabetes, Chronic Pseudomonas |
| P012 | Ingrid Larsson, 37F | Multiple Sclerosis (RRMS), Neurogenic Bladder, Major Depression |
| P013 | Theo Blackwood, 52M | ALS, Respiratory Insufficiency, Dysphagia |

---

## 🔐 SHARP Context Integration

MediCopilot supports SHARP context propagation from the Prompt Opinion platform:

```json
{
  "sharp_context": {
    "patient_id": { "required": true },
    "fhir_token":  { "required": false },
    "sharp_token": { "required": false }
  }
}
```

The `fhir_token` is used as a Bearer token for FHIR R4 API calls. In the current version, patient data is simulated — replace `fhir/mock_client.py` with real FHIR API calls for production.

---

## 🌐 Deployment

### Backend → Render

```bash
# Render auto-deploys from GitHub on every push
# Required environment variable on Render dashboard:
# GROQ_API_KEY = your_groq_key
```

Live backend: https://medicopilot.onrender.com

### Frontend → Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Connect `shrey9741/medicopilot` repo
3. Set main file: `medicopilot/app.py`
4. Add secrets:

```toml
GROQ_API_KEY = "your_key"
API_BASE = "https://medicopilot.onrender.com"
```

### Prompt Opinion Marketplace

Register the agent using the agent card URL:
```
https://medicopilot.onrender.com/.well-known/agent.json
```

---

## 🧪 Testing

```bash
# Run full pre-flight test suite (27 checks)
python test_local.py
```

The test suite covers: environment setup, all module imports, FHIR mock data, anomaly detector, temporal memory, RAG vectorstore, Groq API connectivity, and the full end-to-end orchestrator pipeline.

---

## 📊 Sample Output

```
Patient: John Doe (62M)
Anomaly: ⚠️ URGENT — Stage 2 hypertension + elevated glucose

Differential Diagnosis:
  01. Uncontrolled T2 Diabetes          [CRITICAL] 92%
  02. Hypertensive Nephropathy          [HIGH]     78%
  03. CKD Progression                   [MODERATE] 65%

Drug Warnings:
  🟠 Metformin + CKD Stage 2            [MAJOR]
     Monitor renal function; consider dose reduction if eGFR < 45

Risk Scores:
  Cardiovascular Disease (10-year)      82%
  CKD Progression                       71%
  Diabetes Complications                68%

Memory Trend:
  Glucose: 195 → 202 → 210 mg/dL (worsening, Δ+15)
  BP: 145/90 → 150/94 → 148/92

SOAP Note:
  S: Patient reports fatigue and polyuria...
  O: BP 148/92, HR 88, Glucose 210, BMI 29.4...
  A: Uncontrolled T2DM with early CKD progression...
  P: 1. Increase Metformin to 1000mg BID
     2. Add SGLT2 inhibitor (Empagliflozin)
     3. Refer to nephrology
     4. Repeat HbA1c in 3 months
```

---

## 🔮 Future Scope

- **Real FHIR Integration** — Connect to Epic, Cerner, or any FHIR R4 compliant EHR
- **Multi-hospital Support** — Multi-tenant architecture with SHARP token isolation
- **Streaming Responses** — Real-time agent output streaming via WebSockets
- **Voice Briefings** — Text-to-speech SOAP note delivery for hands-free use
- **Specialist Mode** — Cardiology, Oncology, Pediatrics specialist agent prompts
- **Outcome Tracking** — Compare AI predictions against actual diagnoses over time

---

## 👨‍💻 Author

**Shrey Kumar**
- GitHub: [@shrey9741](https://github.com/shrey9741)
- Repository: [github.com/shrey9741/medicopilot](https://github.com/shrey9741/medicopilot)

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

> Built for the Prompt Opinion Healthcare AI Hackathon · Powered by Groq · FHIR R4 Ready · A2A Compatible
