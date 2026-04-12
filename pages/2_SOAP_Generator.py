"""
MediCopilot — SOAP Generator Page
"""
import streamlit as st
import httpx
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="SOAP Generator · MediCopilot", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("soap"), unsafe_allow_html=True)

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
  <div class="page-title">SOAP Generator</div>
  <div class="page-sub">AI-generated clinical documentation ready for EHR entry</div>
</div>
""", unsafe_allow_html=True)

# ── Check if data from Patient Briefing page ──
data = st.session_state.get("last_data")
last_patient = st.session_state.get("last_patient")

# ── Patient selector ──
col_sel, col_btn = st.columns([3, 1])
with col_sel:
    options = {f"{pid} — {p['name']} ({p['age']})": pid for pid, p in PATIENTS.items()}
    default_idx = list(options.values()).index(last_patient) if last_patient in list(options.values()) else 0
    selected_label = st.selectbox("Select Patient", list(options.keys()), index=default_idx, label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("📝 Generate SOAP", use_container_width=True)

# ── If patient changed or no data, need to fetch ──
needs_fetch = run or (data is None) or (last_patient != patient_id)

if not run and data is None:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0;color:#94a3b8">
      <div style="font-size:3rem;margin-bottom:12px">📋</div>
      <div style="font-size:1rem;font-weight:600;color:#64748b">Select a patient and click Generate SOAP</div>
      <div style="font-size:0.82rem;margin-top:4px">Or generate a briefing on the Patient Briefing page first</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if run or last_patient != patient_id:
    with st.spinner("Generating SOAP note..."):
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

if not data or not data.get("soap_note"):
    st.warning("No SOAP note available. Please try again.")
    st.stop()

soap = data["soap_note"]

# ── Patient info bar ──
p = PATIENTS[patient_id]
st.markdown(f"""
<div class="card" style="margin-bottom:20px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div style="font-family:Manrope,sans-serif;font-size:1.1rem;font-weight:700;color:#0f172a">{data['patient_name']}</div>
      <div style="font-size:0.8rem;color:#64748b;margin-top:2px">Patient Case #{patient_id} · Generated {data['generated_at'][:10]}</div>
    </div>
    <div style="display:flex;gap:8px">
      <span style="font-size:0.72rem;color:#16a34a;font-weight:600;background:#f0fdf4;padding:4px 10px;border-radius:6px;border:1px solid #86efac">✓ AI Confidence: High</span>
      <span style="font-size:0.72rem;color:#003178;font-weight:600;background:#eff6ff;padding:4px 10px;border-radius:6px;border:1px solid #bfdbfe">HIPAA Compliant</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SOAP sections ──
sections = [
    ("S — SUBJECTIVE", soap["subjective"], "🗣️"),
    ("O — OBJECTIVE",  soap["objective"],  "🔬"),
    ("A — ASSESSMENT", soap["assessment"], "🧠"),
    ("P — PLAN",       soap["plan"],       "📋"),
]

for label, content, emoji in sections:
    st.markdown(f"""
    <div class="soap-section">
      <div class="soap-label">{emoji} {label}</div>
      <div class="soap-content">{content}</div>
    </div>""", unsafe_allow_html=True)

# ── Export ──
st.markdown("<br>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])
with col1:
    soap_text = f"SUBJECTIVE:\n{soap['subjective']}\n\nOBJECTIVE:\n{soap['objective']}\n\nASSESSMENT:\n{soap['assessment']}\n\nPLAN:\n{soap['plan']}"
    st.download_button(
        label="📥 Export SOAP Note",
        data=soap_text,
        file_name=f"SOAP_{patient_id}_{data['generated_at'][:10]}.txt",
        mime="text/plain",
        use_container_width=True
    )

st.markdown(f"""
<div class="footer">
  <span>Auto-saved · MediCopilot v1.0 · {data['generated_at'][:10]}</span>
  <span>Generated by MediCopilot Engine · 9 Agents</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
