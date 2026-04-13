"""
MediCopilot — Patient Briefing
"""
import streamlit as st
import httpx
import time
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="Patient Briefing · MediCopilot", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("briefing"), unsafe_allow_html=True)

c = st.columns([1,1,1,1,6])
with c[0]: st.page_link("app.py",                      label="🏠 Dashboard")
with c[1]: st.page_link("pages/1_Patient_Briefing.py", label="🔬 Patient Briefing")
with c[2]: st.page_link("pages/2_SOAP_Generator.py",   label="📝 SOAP Generator")
with c[3]: st.page_link("pages/3_Agent_Status.py",     label="🤖 Agent Status")

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-title">Patient Briefing</div>
  <div class="page-sub">Select a patient and run all 9 AI agents for a complete clinical briefing</div>
</div>
""", unsafe_allow_html=True)

# ── Patient selector ──
options = {f"{pid} — {p['name']} ({p['age']}) · {p['conditions']}": pid for pid, p in PATIENTS.items()}
col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected_label = st.selectbox("Select Patient", list(options.keys()), label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("⚡ Generate Briefing", use_container_width=True)

# ── Patient info strip ──
p = PATIENTS[patient_id]
sc = {"critical":"#ef4444","urgent":"#f59e0b","normal":"#10b981"}[p["status"]]
st.markdown(f"""
<div class="card" style="border-left:3px solid {sc};margin-top:8px;margin-bottom:16px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div style="font-family:Manrope,sans-serif;font-size:1rem;font-weight:700;color:#e2e8f0">{p['name']}</div>
      <div style="font-size:0.78rem;color:#4a7fa5;margin-top:2px">ID: {patient_id} · {p['age']} · {p['conditions']}</div>
    </div>
    <span class="badge badge-{'critical' if p['status']=='critical' else 'urgent' if p['status']=='urgent' else 'normal'}">{p['status'].upper()}</span>
  </div>
</div>
""", unsafe_allow_html=True)

if not run:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0">
      <div style="font-size:3rem;margin-bottom:12px">🏥</div>
      <div style="font-size:1rem;font-weight:600;color:#64748b">Click Generate Briefing to run all 9 AI agents</div>
      <div style="font-size:0.82rem;color:#334155;margin-top:6px">FHIR → Memory → Anomaly → RAG → Diagnosis → Drug Safety → Risk → Second Opinion → SOAP</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Loading with agent steps ──
agent_steps = [
    ("🏥", "FHIRAgent",          "Fetching FHIR patient bundle..."),
    ("📈", "MemoryAgent",        "Analyzing visit trends..."),
    ("🔍", "AnomalyDetector",    "Scanning vital signs..."),
    ("📚", "RAGAgent",           "Retrieving medical guidelines..."),
    ("🧠", "DiagnosisAgent",     "Generating differential diagnosis..."),
    ("💊", "DrugSafetyAgent",    "Checking drug interactions..."),
    ("📊", "RiskScoringAgent",   "Computing risk scores..."),
    ("🧐", "SecondOpinionAgent", "Reviewing primary diagnosis..."),
    ("📋", "SOAPNoteGenerator",  "Writing clinical SOAP note..."),
]

progress_placeholder = st.empty()
with progress_placeholder.container():
    st.markdown("""
    <div class="card" style="text-align:center;padding:2rem">
      <div style="font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">⚡ Running 9 Clinical Agents</div>
      <div style="font-size:0.82rem;color:#4a7fa5" id="current-step">Initializing pipeline...</div>
    </div>
    """, unsafe_allow_html=True)
    
    step_cols = st.columns(3)
    step_placeholders = []
    for i in range(9):
        with step_cols[i % 3]:
            sp = st.empty()
            sp.markdown(f"""
            <div class="agent-card" style="margin-bottom:8px;opacity:0.4">
              <div class="agent-emoji">{agent_steps[i][0]}</div>
              <div class="agent-name">{agent_steps[i][1]}</div>
              <div class="agent-desc">{agent_steps[i][2]}</div>
              <div style="margin-top:6px"><span class="agent-status-dot dot-idle"></span><span style="font-size:0.68rem;color:#334155">IDLE</span></div>
            </div>""", unsafe_allow_html=True)
            step_placeholders.append(sp)

# ── API call with animated steps ──
def animate_and_fetch():
    import threading
    result = {"data": None, "error": None}
    done = threading.Event()

    def fetch():
        try:
            r = httpx.post(
                f"{API_BASE}/invoke",
                json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
                timeout=120.0
            )
            r.raise_for_status()
            result["data"] = r.json()
        except Exception as e:
            result["error"] = str(e)
        finally:
            done.set()

    t = threading.Thread(target=fetch, daemon=True)
    t.start()

    step_idx = 0
    while not done.is_set():
        if step_idx < len(agent_steps):
            # Mark previous as done
            if step_idx > 0:
                ei, en, ed = agent_steps[step_idx - 1]
                step_placeholders[step_idx - 1].markdown(f"""
                <div class="agent-card done" style="margin-bottom:8px">
                  <div class="agent-emoji">{ei}</div>
                  <div class="agent-name">{en}</div>
                  <div class="agent-desc">{ed}</div>
                  <div style="margin-top:6px"><span class="agent-status-dot dot-done"></span><span style="font-size:0.68rem;color:#10b981">DONE</span></div>
                </div>""", unsafe_allow_html=True)
            # Mark current as active
            ei, en, ed = agent_steps[step_idx]
            step_placeholders[step_idx].markdown(f"""
            <div class="agent-card active" style="margin-bottom:8px">
              <div class="agent-emoji">{ei}</div>
              <div class="agent-name">{en}</div>
              <div class="agent-desc">{ed}</div>
              <div style="margin-top:6px"><span class="agent-status-dot dot-active"></span><span style="font-size:0.68rem;color:#38bdf8">RUNNING</span></div>
            </div>""", unsafe_allow_html=True)
            step_idx += 1
        time.sleep(1.4)

    # Mark remaining as done
    for i in range(max(0, step_idx - 1), len(agent_steps)):
        ei, en, ed = agent_steps[i]
        step_placeholders[i].markdown(f"""
        <div class="agent-card done" style="margin-bottom:8px">
          <div class="agent-emoji">{ei}</div>
          <div class="agent-name">{en}</div>
          <div class="agent-desc">{ed}</div>
          <div style="margin-top:6px"><span class="agent-status-dot dot-done"></span><span style="font-size:0.68rem;color:#10b981">DONE</span></div>
        </div>""", unsafe_allow_html=True)

    return result

result = animate_and_fetch()
progress_placeholder.empty()

if result["error"]:
    st.error(f"API Error: {result['error']}. Backend may be waking up — please retry in 30 seconds.")
    st.stop()

data = result["data"]
st.session_state["last_data"]    = data
st.session_state["last_patient"] = patient_id

# ── Results ──
anomaly = data["anomaly_flag"]
level   = anomaly["level"]
aclass  = f"anomaly-{level.lower()}"
emoji   = {"CRITICAL":"🚨","URGENT":"⚠️","WARNING":"🔶","NORMAL":"✅"}.get(level,"ℹ️")

if anomaly["triggered"]:
    items = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
    st.markdown(f'<div class="{aclass}"><div class="anomaly-title">{emoji} {level} — Vital Anomaly Detected</div>{items}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ All vitals within acceptable ranges</div></div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="card">
  <div style="font-family:Manrope,sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0;margin-bottom:4px">{data['patient_name']}</div>
  <div style="font-size:0.85rem;color:#94a3b8;line-height:1.6">{data['summary']}</div>
</div>
""", unsafe_allow_html=True)

if data.get("memory_trend"):
    with st.expander("📈 Patient Memory Trends"):
        st.code(data["memory_trend"], language="text")

tab1, tab2, tab3 = st.tabs(["🔬 Diagnosis", "💊 Drug Safety", "📊 Risk Scores"])

with tab1:
    st.markdown('<div class="section-hdr">Differential Diagnosis</div>', unsafe_allow_html=True)
    for i, dx in enumerate(data["diagnoses"]):
        tier = dx["tier"]
        conf = dx["confidence"]
        st.markdown(f"""
        <div class="card">
          <div class="card-label">Diagnosis {str(i+1).zfill(2)}</div>
          <div class="card-title">{dx['condition']}</div>
          <div class="card-body">{dx['reasoning']}</div>
          <div class="conf-wrap">
            <span class="tier-{tier}">{tier.upper()}</span>
            <div class="conf-bg"><div class="conf-fill" style="width:{conf}%"></div></div>
            <span class="conf-pct">{conf}%</span>
          </div>
        </div>""", unsafe_allow_html=True)

    if data.get("second_opinion"):
        op = data["second_opinion"]
        st.markdown(f"""
        <div class="card" style="border-color:#10b981;border-left:3px solid #10b981;margin-top:16px">
          <div class="card-label" style="color:#10b981">🧐 Second Opinion Review</div>
          <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:6px"><strong style="color:#e2e8f0">Challenge:</strong> {op['challenge']}</div>
          <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:8px"><strong style="color:#e2e8f0">Counter-evidence:</strong> {op['counter_evidence']}</div>
          <div style="font-size:0.82rem;color:#10b981;font-weight:600;background:#002d1a;padding:10px 14px;border-radius:8px">✓ {op['final_recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-hdr">Drug Interaction Matrix</div>', unsafe_allow_html=True)
    warnings = data["drug_warnings"]
    if not warnings:
        st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ No significant drug interactions detected</div></div>', unsafe_allow_html=True)
    else:
        icons = {"critical":"🔴","major":"🟠","moderate":"🟡","minor":"🟢"}
        for w in warnings:
            tier_key = w["severity"] if w["severity"] in ["critical","high","moderate","low"] else "moderate"
            st.markdown(f"""
            <div class="drug-card">
              <div class="drug-pair">{icons.get(w['severity'],'⚪')} {w['drug_a']} + {w['drug_b']} &nbsp;<span class="tier-{tier_key}">{w['severity'].upper()}</span></div>
              <div class="drug-rec">{w['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-hdr">Risk Score Assessment</div>', unsafe_allow_html=True)
    for r in data["risk_scores"]:
        score = r["score"]
        rc = "#ef4444" if score>=70 else "#f59e0b" if score>=40 else "#10b981"
        factors = "".join(f'<div style="font-size:0.78rem;color:#64748b;margin:3px 0;padding-left:12px">— {f}</div>' for f in r["factors"])
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <div style="font-family:Manrope,sans-serif;font-weight:700;color:#e2e8f0">{r['condition']}</div>
            <div style="font-size:1.4rem;font-weight:800;color:{rc}">{score}%</div>
          </div>
          <div class="risk-bar-bg"><div style="width:{score}%;height:100%;border-radius:20px;background:{rc}"></div></div>
          {factors}
          <div style="font-size:0.78rem;color:#38bdf8;margin-top:10px;padding:8px 12px;background:#001945;border-radius:8px;border-left:2px solid #1a6b9a">{r['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

st.markdown(f"""
<div class="footer">
  <span>MediCopilot v1.0 · {data['generated_at'][:10]}</span>
  <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents · A2A</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
