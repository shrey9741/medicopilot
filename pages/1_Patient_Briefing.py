"""
MediCopilot — Patient Briefing Page
"""
import streamlit as st
import httpx
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="Patient Briefing · MediCopilot", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("briefing"), unsafe_allow_html=True)

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
  <div class="page-title">Patient Briefing</div>
  <div class="page-sub">Select a patient to run all 9 AI agents and generate a complete clinical briefing</div>
</div>
""", unsafe_allow_html=True)

# ── Patient selector ──
col_sel, col_btn = st.columns([3, 1])
with col_sel:
    options = {f"{pid} — {p['name']} ({p['age']})": pid for pid, p in PATIENTS.items()}
    selected_label = st.selectbox("Select Patient", list(options.keys()), label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("⚡ Generate Briefing", use_container_width=True)

# ── Show patient info strip ──
p = PATIENTS[patient_id]
status_color = {"critical": "#dc2626", "urgent": "#f59e0b", "normal": "#16a34a"}[p["status"]]
st.markdown(f"""
<div class="card" style="border-left:3px solid {status_color};margin-top:8px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div style="font-family:Manrope,sans-serif;font-size:1.1rem;font-weight:700;color:#0f172a">{p['name']}</div>
      <div style="font-size:0.8rem;color:#64748b;margin-top:2px">ID: {patient_id} · {p['age']} · {p['conditions']}</div>
    </div>
    <div style="font-size:0.75rem;color:{status_color};font-weight:700;text-transform:uppercase">{p['status']}</div>
  </div>
</div>
""", unsafe_allow_html=True)

if not run:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0;color:#94a3b8">
      <div style="font-size:3rem;margin-bottom:12px">🏥</div>
      <div style="font-size:1rem;font-weight:600;color:#64748b">Select a patient and click Generate Briefing</div>
      <div style="font-size:0.82rem;margin-top:4px">9 specialized AI agents will analyze the patient data</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── API Call ──
with st.spinner("Running 9 clinical agents..."):
    try:
        response = httpx.post(
            f"{API_BASE}/invoke",
            json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
            timeout=120.0
        )
        response.raise_for_status()
        data = response.json()
    except httpx.ConnectError:
        st.error("Cannot connect to API backend. Please try again in 30 seconds.")
        st.stop()
    except Exception as e:
        st.error(f"API error: {e}")
        st.stop()

# ── Store in session for other pages ──
st.session_state["last_data"] = data
st.session_state["last_patient"] = patient_id

# ── Anomaly banner ──
anomaly = data["anomaly_flag"]
level = anomaly["level"]
anomaly_class = f"anomaly-{level.lower()}"
level_emoji = {"CRITICAL": "🚨", "URGENT": "⚠️", "WARNING": "🔶", "NORMAL": "✅"}.get(level, "ℹ️")

if anomaly["triggered"]:
    items = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
    st.markdown(f'<div class="{anomaly_class}"><div class="anomaly-title">{level_emoji} {level} — Vital Anomaly Detected</div>{items}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ All vitals within acceptable ranges</div></div>', unsafe_allow_html=True)

# ── Summary ──
st.markdown(f"""
<div class="card">
  <div style="font-family:Manrope,sans-serif;font-size:1.1rem;font-weight:700;color:#0f172a;margin-bottom:4px">{data['patient_name']}</div>
  <div style="font-size:0.85rem;color:#64748b;line-height:1.6">{data['summary']}</div>
</div>
""", unsafe_allow_html=True)

# ── Memory trend ──
if data.get("memory_trend"):
    with st.expander("📈 Patient Memory Trends"):
        st.code(data["memory_trend"], language="text")

# ── Tabs ──
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
        <div class="card" style="border-color:#86efac;border-left:3px solid #16a34a;margin-top:16px">
          <div class="card-label" style="color:#16a34a">🧐 Second Opinion Review</div>
          <div style="font-size:0.82rem;color:#334155;margin-bottom:6px"><strong>Challenge:</strong> {op['challenge']}</div>
          <div style="font-size:0.82rem;color:#334155;margin-bottom:8px"><strong>Counter-evidence:</strong> {op['counter_evidence']}</div>
          <div style="font-size:0.82rem;color:#16a34a;font-weight:600;background:#f0fdf4;padding:10px 14px;border-radius:8px">✓ {op['final_recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-hdr">Drug Interaction Matrix</div>', unsafe_allow_html=True)
    warnings = data["drug_warnings"]
    if not warnings:
        st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ No significant drug interactions detected</div></div>', unsafe_allow_html=True)
    else:
        sev_icons = {"critical": "🔴", "major": "🟠", "moderate": "🟡", "minor": "🟢"}
        for w in warnings:
            icon = sev_icons.get(w["severity"], "⚪")
            st.markdown(f"""
            <div class="drug-card">
              <div class="drug-pair">{icon} {w['drug_a']} + {w['drug_b']} &nbsp;<span class="tier-{w['severity'] if w['severity'] in ['critical','high','moderate','low'] else 'moderate'}">{w['severity'].upper()}</span></div>
              <div class="drug-rec">{w['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-hdr">Risk Score Assessment</div>', unsafe_allow_html=True)
    for r in data["risk_scores"]:
        score = r["score"]
        risk_color = "#dc2626" if score >= 70 else ("#d97706" if score >= 40 else "#16a34a")
        factors_html = "".join(f'<div style="font-size:0.78rem;color:#64748b;margin:3px 0;padding-left:12px">— {f}</div>' for f in r["factors"])
        st.markdown(f"""
        <div class="card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
            <div style="font-family:Manrope,sans-serif;font-weight:700;color:#0f172a">{r['condition']}</div>
            <div style="font-size:1.4rem;font-weight:800;color:{risk_color}">{score}%</div>
          </div>
          <div class="risk-bar-bg"><div style="width:{score}%;height:100%;border-radius:20px;background:{risk_color}"></div></div>
          {factors_html}
          <div style="font-size:0.78rem;color:#003178;margin-top:10px;padding:8px 12px;background:#eff6ff;border-radius:8px;border-left:2px solid #003178">{r['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

# ── Footer ──
st.markdown(f"""
<div class="footer">
  <span>MediCopilot v1.0 · Generated {data['generated_at'][:10]}</span>
  <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
