# MediCopilot — AI Clinical Copilot

A2A-powered multi-agent clinical briefing system for the Prompt Opinion Marketplace.

## Features
- **Vital Anomaly Detection** — rule-based pre-LLM check (URGENT/CRITICAL flags)
- **Temporal Patient Memory** — tracks glucose, BP, HR trends across visits
- **RAG Medical Knowledge** — FAISS vectorstore with WHO/ADA/ACC guidelines
- **Differential Diagnosis** — ranked DDx with confidence scores and explainability
- **Drug Safety Check** — interaction matrix with severity levels
- **Risk Scoring** — cardiovascular and condition-specific risk percentages
- **Second Opinion Mode** — agent challenges its own primary diagnosis
- **SOAP Note Generator** — full S/O/A/P clinical documentation
- **Reasoning Trace** — full audit trail of all 9 agents

## Stack
- **LLM**: Groq (llama-3.1-8b-instant)
- **RAG**: LangChain + FAISS + sentence-transformers
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **FHIR**: Simulated FHIR R4 patient bundles
- **Platform**: Prompt Opinion A2A

## Setup

```bash
# 1. Clone and enter project
cd medicopilot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Run the FastAPI backend
uvicorn main:app --reload --port 8000

# 6. In a new terminal, run Streamlit UI
streamlit run app.py
```

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/.well-known/agent.json` | GET | A2A agent card for Prompt Opinion |
| `/invoke` | POST | Run full clinical briefing |
| `/health` | GET | Health check |
| `/patients` | GET | List demo patients |

## Invoke Example

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "P001", "sharp_token": "your-token"}'
```

## Demo Patients

| ID | Name | Conditions |
|---|---|---|
| P001 | John Doe, 62M | Type 2 Diabetes, Hypertension, CKD |
| P002 | Sarah Chen, 45F | Atrial Fibrillation, Hypothyroidism |
| P003 | Marcus Johnson, 71M | COPD, Heart Failure, T2 Diabetes |

## Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

## Prompt Opinion Registration

After deployment, register your agent at:
`https://promptopinion.com/marketplace/publish`

Use your deployed URL for the invoke endpoint in `agent_card.json`.
