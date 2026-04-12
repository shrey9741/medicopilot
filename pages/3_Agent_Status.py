"""
MediCopilot — Agent Status / Orchestration Page
"""
import streamlit as st
import httpx
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="Agent Status · MediCopilot", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("agents"), unsafe_allow_html=True)

with st.container():
    cols = st.columns([1,1,1,1,8])
    with cols[0]:
        st.page_link("app.py", label="Dashboard", icon="🏠")
    with cols[1]:
        st.page_link("pages/1_Patient_Briefing.py", label="Patient Briefing", icon="🔬")
    with cols[2]:
        st.page_link("pages/2_SOAP_Generator.py", label="SOAP Generator", icon="📝")
    with cols[3]:
        st.page_link("pages/3_Agent_Status.py", label="Agent Status", icon="🤖")

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-title">Agent Orchestration</div>
  <div class="page-sub">Real-time visualization of all 9 clinical AI agents · Full reasoning trace</div>
</div>
""", unsafe_allow_html=True)

# ── Agent overview cards ──
agents_info = [
    ("FHIRAgent",          "Fetches patient bundle from FHIR R4",          "🏥"),
    ("MemoryAgent",        "Analyzes visit history and trends",             "📈"),
    ("AnomalyDetector",    "Rule-based vital sign anomaly detection",       "🔍"),
    ("RAGAgent",           "Retrieves medical guidelines from FAISS",       "📚"),
    ("DiagnosisAgent",     "Generates differential diagnosis",              "🧠"),
    ("DrugSafetyAgent",    "Checks medication interactions",                "💊"),
    ("RiskScoringAgent",   "Calculates condition risk percentages",         "📊"),
    ("SecondOpinionAgent", "Challenges primary diagnosis",                  "🧐"),
    ("SOAPNoteGenerator",  "Synthesizes clinical documentation",            "📋"),
]

cols = st.columns(3)
for i, (name, desc, emoji) in enumerate(agents_info):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="card" style="margin-bottom:10px">
          <div style="font-size:1.2rem;margin-bottom:6px">{emoji}</div>
          <div style="font-size:0.82rem;font-weight:700;color:#0f172a;margin-bottom:3px">{name}</div>
          <div style="font-size:0.75rem;color:#64748b">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Check session data ──
data = st.session_state.get("last_data")
last_patient = st.session_state.get("last_patient")

col_sel, col_btn = st.columns([3, 1])
with col_sel:
    options = {f"{pid} — {p['name']} ({p['age']})": pid for pid, p in PATIENTS.items()}
    default_idx = list(options.values()).index(last_patient) if last_patient in list(options.values()) else 0
    selected_label = st.selectbox("Select Patient", list(options.keys()), index=default_idx, label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("🤖 Run Agents", use_container_width=True)

if not run and data is None:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0;color:#94a3b8">
      <div style="font-size:0.9rem;font-weight:600;color:#64748b">Select a patient and click Run Agents to see the full reasoning trace</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if run or last_patient != patient_id:
    with st.spinner("Running all 9 agents..."):
        try:
            response = httpx.post(
                f"{API_BASE}/invoke",
                json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
                timeout=120.0
            )
            response.raise_for_status()
            data = response.json()
            st.session_state["last_data"] = data
            st.session_state["last_patient"] = patient_id
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

if not data:
    st.stop()

# ── Status bar ──
st.markdown(f"""
<div class="card" style="border-left:3px solid #16a34a;margin-bottom:20px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="width:10px;height:10px;border-radius:50%;background:#16a34a;display:inline-block"></span>
      <span style="font-weight:700;color:#0f172a">9/9 Agents Completed · {data['patient_name']}</span>
      <span class="badge badge-info">LIVE PIPELINE</span>
    </div>
    <span style="font-size:0.75rem;color:#94a3b8">{data['generated_at'][11:19]} UTC</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Reasoning trace ──
st.markdown('<div class="section-hdr">Agent Reasoning Trace</div>', unsafe_allow_html=True)
for i, step in enumerate(data["reasoning_trace"]):
    st.markdown(f"""
    <div class="trace-card">
      <div class="trace-num">{str(i+1).zfill(2)}</div>
      <div>
        <div class="trace-agent">{step['agent']}</div>
        <div class="trace-action">{step['action']}</div>
        <div class="trace-find">{step['finding']}</div>
      </div>
    </div>""", unsafe_allow_html=True)

# ── RAG citations ──
if data.get("rag_citations"):
    st.markdown('<div class="section-hdr">📚 RAG Citations</div>', unsafe_allow_html=True)
    for i, citation in enumerate(data["rag_citations"]):
        st.markdown(f'<div class="citation"><strong style="color:#003178">Guideline {i+1}</strong><br><br>{citation}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
  <span>MediCopilot v1.0 · {data['generated_at'][:10]}</span>
  <span>Groq · Llama 3.1-8b · FAISS RAG · A2A Protocol</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
