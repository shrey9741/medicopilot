"""
MediCopilot — Agent Status / Orchestration
"""
import streamlit as st
import httpx
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="Agent Status · MediCopilot", page_icon="🤖", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("agents"), unsafe_allow_html=True)

c = st.columns([1,1,1,1,6])
with c[0]: st.page_link("app.py",                      label="🏠 Dashboard")
with c[1]: st.page_link("pages/1_Patient_Briefing.py", label="🔬 Patient Briefing")
with c[2]: st.page_link("pages/2_SOAP_Generator.py",   label="📝 SOAP Generator")
with c[3]: st.page_link("pages/3_Agent_Status.py",     label="🤖 Agent Status")

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-title">Agent Orchestration</div>
  <div class="page-sub">Run a patient briefing to see live agent activity and full reasoning trace</div>
</div>
""", unsafe_allow_html=True)

# ── Agent cards (always visible) ──
agents_info = [
    ("🏥","FHIRAgent",          "Fetches patient bundle from FHIR R4"),
    ("📈","MemoryAgent",        "Analyzes visit history for trends"),
    ("🔍","AnomalyDetector",    "Rule-based vital sign anomaly detection"),
    ("📚","RAGAgent",           "Retrieves medical guidelines from FAISS"),
    ("🧠","DiagnosisAgent",     "Generates differential diagnosis with DDx"),
    ("💊","DrugSafetyAgent",    "Checks all medication interactions"),
    ("📊","RiskScoringAgent",   "Calculates condition risk percentages"),
    ("🧐","SecondOpinionAgent", "Challenges primary diagnosis"),
    ("📋","SOAPNoteGenerator",  "Synthesizes clinical SOAP documentation"),
]

data        = st.session_state.get("last_data")
last_patient = st.session_state.get("last_patient")
trace       = data.get("reasoning_trace", []) if data else []

# Show agent cards with live status if trace available
cols = st.columns(3)
for i, (emoji, name, desc) in enumerate(agents_info):
    # Find this agent in trace
    agent_trace = next((s for s in trace if s["agent"] == name), None)
    if agent_trace:
        card_cls = "done"
        status_html = f'<span class="agent-status-dot dot-done"></span><span style="font-size:0.68rem;color:#10b981">COMPLETED</span>'
        finding_html = f'<div style="font-size:0.72rem;color:#38bdf8;font-style:italic;margin-top:4px;border-top:1px solid #1e2d4a;padding-top:4px">{agent_trace["finding"]}</div>'
    else:
        card_cls = ""
        status_html = f'<span class="agent-status-dot dot-idle"></span><span style="font-size:0.68rem;color:#334155">{"IDLE — select a patient to run" if not data else "IDLE"}</span>'
        finding_html = ""
    
    with cols[i % 3]:
        st.markdown(f"""
        <div class="agent-card {card_cls}" style="margin-bottom:10px">
          <div class="agent-emoji">{emoji}</div>
          <div class="agent-name">{name}</div>
          <div class="agent-desc">{desc}</div>
          <div style="margin-top:6px">{status_html}</div>
          {finding_html}
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Patient selector ──
options = {f"{pid} — {p['name']} ({p['age']}) · {p['conditions']}": pid for pid, p in PATIENTS.items()}
default_idx = list(options.values()).index(last_patient) if last_patient in list(options.values()) else 0

col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected_label = st.selectbox("Select Patient", list(options.keys()), index=default_idx, label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("🤖 Run All Agents", use_container_width=True)

if run or (data is None and not run):
    if run:
        with st.spinner(f"Running 9 agents for {PATIENTS[patient_id]['name']}..."):
            try:
                r = httpx.post(
                    f"{API_BASE}/invoke",
                    json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
                    timeout=120.0
                )
                r.raise_for_status()
                data = r.json()
                st.session_state["last_data"]    = data
                st.session_state["last_patient"] = patient_id
                st.rerun()
            except Exception as e:
                st.error(f"API error: {e}")
                st.stop()

if not data:
    st.markdown("""
    <div style="text-align:center;padding:2rem 0">
      <div style="font-size:0.9rem;color:#334155">Select a patient and click Run All Agents to see the reasoning trace</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Status bar ──
st.markdown(f"""
<div class="card" style="border-left:3px solid #10b981;margin-bottom:20px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div style="display:flex;align-items:center;gap:8px">
      <span style="width:10px;height:10px;border-radius:50%;background:#10b981;display:inline-block"></span>
      <span style="font-weight:700;color:#e2e8f0">9/9 Agents Completed · {data['patient_name']}</span>
      <span class="badge badge-info">● LIVE PIPELINE</span>
    </div>
    <span style="font-size:0.75rem;color:#4a7fa5">{data['generated_at'][11:19]} UTC · {data['generated_at'][:10]}</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Full reasoning trace ──
st.markdown('<div class="section-hdr">Full Reasoning Trace</div>', unsafe_allow_html=True)
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
        st.markdown(f'<div class="citation"><strong style="color:#38bdf8">Guideline {i+1}</strong><br><br>{citation}</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
  <span>MediCopilot v1.0 · {data['generated_at'][:10]}</span>
  <span>Groq · Llama 3.1-8b · FAISS RAG · A2A Protocol</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
