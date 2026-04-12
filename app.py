"""
MediCopilot — Dashboard (Main Page)
"""
import streamlit as st
from utils import SHARED_CSS, PATIENTS, API_BASE, topnav

st.set_page_config(page_title="MediCopilot", page_icon="🏥", layout="wide", initial_sidebar_state="collapsed")
st.markdown(SHARED_CSS, unsafe_allow_html=True)
st.markdown(topnav("dashboard"), unsafe_allow_html=True)

# ── Page navigation using Streamlit page links (hidden but functional) ──
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

# ── Header ──
from datetime import datetime
st.markdown(f"""
<div class="page-header">
  <div style="font-size:0.85rem;color:#64748b;margin-bottom:4px">{datetime.now().strftime("%A, %B %d, %Y")}</div>
  <div class="page-title">Clinical Dashboard</div>
  <div class="page-sub">13 patients scheduled today · Next appointment: 08:00 AM</div>
</div>
""", unsafe_allow_html=True)

# ── Stats row ──
col1, col2, col3, col4 = st.columns(4)
critical = sum(1 for p in PATIENTS.values() if p["status"] == "critical")
urgent   = sum(1 for p in PATIENTS.values() if p["status"] == "urgent")
normal   = sum(1 for p in PATIENTS.values() if p["status"] == "normal")

with col1:
    st.markdown(f"""<div class="card" style="border-left:3px solid #003178">
        <div class="card-label">Total Patients</div>
        <div style="font-size:1.8rem;font-weight:800;color:#003178;font-family:Manrope,sans-serif">13</div>
        <div style="font-size:0.75rem;color:#64748b">Scheduled today</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""<div class="card" style="border-left:3px solid #dc2626">
        <div class="card-label">Critical</div>
        <div style="font-size:1.8rem;font-weight:800;color:#dc2626;font-family:Manrope,sans-serif">{critical}</div>
        <div style="font-size:0.75rem;color:#64748b">Immediate attention</div>
    </div>""", unsafe_allow_html=True)
with col3:
    st.markdown(f"""<div class="card" style="border-left:3px solid #f59e0b">
        <div class="card-label">Urgent</div>
        <div style="font-size:1.8rem;font-weight:800;color:#f59e0b;font-family:Manrope,sans-serif">{urgent}</div>
        <div style="font-size:0.75rem;color:#64748b">Needs review</div>
    </div>""", unsafe_allow_html=True)
with col4:
    st.markdown(f"""<div class="card" style="border-left:3px solid #16a34a">
        <div class="card-label">Stable</div>
        <div style="font-size:1.8rem;font-weight:800;color:#16a34a;font-family:Manrope,sans-serif">{normal}</div>
        <div style="font-size:0.75rem;color:#64748b">Routine follow-up</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Patient table ──
times = ["08:00","08:30","09:00","09:30","10:00","10:30","11:00","11:30","12:00","12:30","13:00","13:30","14:00"]
status_badges = {
    "critical": '<span class="badge badge-critical">🔴 Critical</span>',
    "urgent":   '<span class="badge badge-urgent">⚠️ Anomaly</span>',
    "normal":   '<span class="badge badge-info">✦ Ready</span>',
}
time_classes = {"critical": "time-critical", "urgent": "time-urgent", "normal": "time-normal"}

rows_html = ""
for i, (pid, p) in enumerate(PATIENTS.items()):
    tc = time_classes[p["status"]]
    badge = status_badges[p["status"]]
    rows_html += f"""
    <tr>
      <td><span class="time-badge {tc}">{times[i]}</span></td>
      <td>
        <div class="patient-name">{p['name']}</div>
        <div class="patient-id">ID: {pid} · {p['age']}</div>
      </td>
      <td><span style="font-size:0.82rem;color:#334155">{p['conditions']}</span></td>
      <td>{badge}</td>
    </tr>"""

st.markdown(f"""
<div class="card" style="padding:0;overflow:hidden">
  <table class="patient-table">
    <thead>
      <tr>
        <th>Time</th>
        <th>Patient</th>
        <th>Conditions</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>
<p style="font-size:0.75rem;color:#94a3b8;margin-top:8px;padding:0 4px">Showing 13 of 13 patients · Click Patient Briefing above to generate AI briefing</p>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
