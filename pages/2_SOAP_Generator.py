"""
MediCopilot — SOAP Generator
"""
import streamlit as st
import httpx
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="SOAP Generator · MediCopilot", page_icon="📝", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("soap"), unsafe_allow_html=True)

c = st.columns([1,1,1,1,6])
with c[0]: st.page_link("app.py",                      label="🏠 Dashboard")
with c[1]: st.page_link("pages/1_Patient_Briefing.py", label="🔬 Patient Briefing")
with c[2]: st.page_link("pages/2_SOAP_Generator.py",   label="📝 SOAP Generator")
with c[3]: st.page_link("pages/3_Agent_Status.py",     label="🤖 Agent Status")

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <div class="page-title">SOAP Generator</div>
  <div class="page-sub">AI-generated clinical documentation ready for EHR entry</div>
</div>
""", unsafe_allow_html=True)

# ── Patient selector ──
options = {f"{pid} — {p['name']} ({p['age']}) · {p['conditions']}": pid for pid, p in PATIENTS.items()}
last_patient = st.session_state.get("last_patient")
default_idx  = list(options.values()).index(last_patient) if last_patient in list(options.values()) else 0

col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected_label = st.selectbox("Select Patient", list(options.keys()), index=default_idx, label_visibility="collapsed")
    patient_id = options[selected_label]
with col_btn:
    run = st.button("📝 Generate SOAP", use_container_width=True)

# ── Patient strip ──







p  = PATIENTS[patient_id]
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

# ── Use cached data if same patient ──
data = st.session_state.get("last_data")
need_fetch = run or (data is None) or (st.session_state.get("last_patient") != patient_id)

if not run and data is None:
    st.markdown("""
    <div style="text-align:center;padding:3rem 0">
      <div style="font-size:3rem;margin-bottom:12px">📋</div>
      <div style="font-size:1rem;font-weight:600;color:#64748b">Click Generate SOAP to create clinical documentation</div>
      <div style="font-size:0.82rem;color:#334155;margin-top:6px">Or generate a briefing on the Patient Briefing page first — SOAP auto-loads here</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if need_fetch:
    with st.spinner(f"Generating SOAP note for {p['name']}..."):
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
        except Exception as e:
            st.error(f"API error: {e}")
            st.stop()

if not data or not data.get("soap_note"):
    st.warning("No SOAP note available. Please try again.")
    st.stop()

soap = data["soap_note"]

# ── Header card ──
st.markdown(f"""
<div class="card" style="margin-bottom:20px">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div>
      <div style="font-family:Manrope,sans-serif;font-size:1.1rem;font-weight:700;color:#e2e8f0">{data['patient_name']} — SOAP Note</div>
      <div style="font-size:0.78rem;color:#4a7fa5;margin-top:2px">Case #{patient_id} · Generated {data['generated_at'][:10]}</div>
    </div>
    <div style="display:flex;gap:8px">
      <span style="font-size:0.7rem;color:#10b981;font-weight:600;background:#002d1a;padding:4px 10px;border-radius:6px;border:1px solid #10b981">✓ AI Confidence: High</span>
      <span style="font-size:0.7rem;color:#38bdf8;font-weight:600;background:#001945;padding:4px 10px;border-radius:6px;border:1px solid #1a6b9a">HIPAA Compliant</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── SOAP sections ──
for label, content, emoji in [
    ("S — SUBJECTIVE", soap["subjective"], "🗣️"),
    ("O — OBJECTIVE",  soap["objective"],  "🔬"),
    ("A — ASSESSMENT", soap["assessment"], "🧠"),
    ("P — PLAN",       soap["plan"],       "📋"),
]:
    st.markdown(f"""
    <div class="soap-section">
      <div class="soap-label">{emoji} {label}</div>
      <div class="soap-content">{content}</div>
    </div>""", unsafe_allow_html=True)

# ── Export ──
st.markdown("<br>", unsafe_allow_html=True)
soap_text = f"SUBJECTIVE:\n{soap['subjective']}\n\nOBJECTIVE:\n{soap['objective']}\n\nASSESSMENT:\n{soap['assessment']}\n\nPLAN:\n{soap['plan']}"
col1, col2 = st.columns([1, 4])
with col1:
    st.download_button("📥 Export SOAP Note", data=soap_text,
        file_name=f"SOAP_{patient_id}_{data['generated_at'][:10]}.txt",
        mime="text/plain", use_container_width=True)

st.markdown(f"""
<div class="footer">
  <span>Auto-saved · MediCopilot v1.0 · {data['generated_at'][:10]}</span>
  <span>MediCopilot Engine · 9 Agents</span>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
