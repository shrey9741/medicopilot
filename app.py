"""
MediCopilot — Dashboard
"""
import streamlit as st
from datetime import datetime
from utils import SHARED_CSS, PATIENTS, topnav

st.set_page_config(page_title="MediCopilot · Dashboard", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("dashboard"), unsafe_allow_html=True)

# ── Navigation row ──
c = st.columns([1,1,1,1,6])
with c[0]: st.page_link("app.py",                          label="🏠 Dashboard",        )
with c[1]: st.page_link("pages/1_Patient_Briefing.py",     label="🔬 Patient Briefing", )
with c[2]: st.page_link("pages/2_SOAP_Generator.py",       label="📝 SOAP Generator",   )
with c[3]: st.page_link("pages/3_Agent_Status.py",         label="🤖 Agent Status",     )

st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

# ── Header ──
st.markdown(f"""
<div class="page-header">
  <div style="font-size:0.82rem;color:#4a7fa5;margin-bottom:4px">{datetime.now().strftime("%A, %B %d, %Y")}</div>
  <div class="page-title">Clinical Dashboard</div>
  <div class="page-sub">13 patients scheduled today · AI briefings ready for critical cases</div>
</div>
""", unsafe_allow_html=True)

# ── Stat cards ──
critical = sum(1 for p in PATIENTS.values() if p["status"] == "critical")
urgent   = sum(1 for p in PATIENTS.values() if p["status"] == "urgent")
normal   = sum(1 for p in PATIENTS.values() if p["status"] == "normal")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""<div class="card" style="border-left:3px solid #1a6b9a">
        <div class="card-label">Total Patients</div>
        <div style="font-size:2rem;font-weight:800;color:#38bdf8;font-family:Manrope,sans-serif">13</div>
        <div style="font-size:0.75rem;color:#4a7fa5">Scheduled today</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="card" style="border-left:3px solid #ef4444">
        <div class="card-label">Critical</div>
        <div style="font-size:2rem;font-weight:800;color:#ef4444;font-family:Manrope,sans-serif">{critical}</div>
        <div style="font-size:0.75rem;color:#4a7fa5">Immediate attention</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="card" style="border-left:3px solid #f59e0b">
        <div class="card-label">Urgent</div>
        <div style="font-size:2rem;font-weight:800;color:#f59e0b;font-family:Manrope,sans-serif">{urgent}</div>
        <div style="font-size:0.75rem;color:#4a7fa5">Needs review</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="card" style="border-left:3px solid #10b981">
        <div class="card-label">Stable</div>
        <div style="font-size:2rem;font-weight:800;color:#10b981;font-family:Manrope,sans-serif">{normal}</div>
        <div style="font-size:0.75rem;color:#4a7fa5">Routine follow-up</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Patient table ──
times = ["08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00"]
status_badges = {
    "critical": '<span class="badge badge-critical">🔴 Critical</span>',
    "urgent":   '<span class="badge badge-urgent">⚠️ Urgent</span>',
    "normal":   '<span class="badge badge-info">✦ Ready</span>',
}
time_classes = {"critical": "time-critical", "urgent": "time-urgent", "normal": "time-normal"}

rows = ""
for i, (pid, p) in enumerate(PATIENTS.items()):
    tc  = time_classes[p["status"]]
    bdg = status_badges[p["status"]]
    rows += f"""<tr>
      <td><span class="time-badge {tc}">{times[i]}</span></td>
      <td><div class="patient-name">{p['name']}</div><div class="patient-id">ID: {pid} · {p['age']}</div></td>
      <td><span style="font-size:0.82rem;color:#64748b">{p['conditions']}</span></td>
      <td>{bdg}</td>
    </tr>"""

st.markdown(f"""
<div class="card" style="padding:0;overflow:hidden">
  <table class="patient-table">
    <thead><tr>
      <th>Time</th><th>Patient</th><th>Conditions</th><th>Status</th>
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>
<p style="font-size:0.75rem;color:#334155;margin-top:8px;padding:0 4px">
  Showing 13 of 13 patients · Navigate to Patient Briefing to generate AI clinical reports
</p>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card" style="margin-top:16px;border-color:#1a6b9a;background:linear-gradient(135deg,#0d1425,#0a1628)">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="font-size:1.5rem">🤖</div>
    <div>
      <div style="font-size:0.9rem;font-weight:700;color:#e2e8f0;margin-bottom:3px">MediCopilot AI · 9 Agents Active</div>
      <div style="font-size:0.8rem;color:#4a7fa5">FHIR · Memory · Anomaly · RAG · Diagnosis · Drug Safety · Risk · Second Opinion · SOAP</div>
    </div>
    <div style="margin-left:auto;font-size:0.75rem;color:#10b981;font-weight:600;background:#002d1a;padding:4px 10px;border-radius:6px;border:1px solid #10b981">● ONLINE</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
