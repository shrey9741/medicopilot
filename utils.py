"""
Shared styles, utilities and constants for MediCopilot Streamlit UI.
"""

API_BASE = "https://medicopilot.onrender.com"

PATIENTS = {
    "P001": {"name": "John Doe",          "age": "62M", "conditions": "T2 Diabetes · Hypertension · CKD",                  "status": "urgent"},
    "P002": {"name": "Sarah Chen",         "age": "45F", "conditions": "Atrial Fibrillation · Hypothyroidism",               "status": "normal"},
    "P003": {"name": "Marcus Johnson",     "age": "71M", "conditions": "COPD · Heart Failure · T2 Diabetes",                 "status": "critical"},
    "P004": {"name": "Patricia Williams",  "age": "54F", "conditions": "Breast Cancer HER2+ · Neuropathy",                   "status": "normal"},
    "P005": {"name": "Robert Nguyen",      "age": "67M", "conditions": "Lung Cancer Stage IV · COPD",                        "status": "urgent"},
    "P006": {"name": "Aiden Patel",        "age": "8M",  "conditions": "T1 Diabetes · Asthma · Celiac Disease",              "status": "critical"},
    "P007": {"name": "Lily Thompson",      "age": "5F",  "conditions": "ALL Leukemia · Febrile Neutropenia",                 "status": "critical"},
    "P008": {"name": "Diana Foster",       "age": "34F", "conditions": "Bipolar I · Anxiety · Hypothyroidism",               "status": "normal"},
    "P009": {"name": "Carlos Rivera",      "age": "28M", "conditions": "Schizophrenia · Substance Use Disorder",             "status": "urgent"},
    "P010": {"name": "Eleanor Voss",       "age": "41F", "conditions": "Lupus · Antiphospholipid Syndrome",                  "status": "urgent"},
    "P011": {"name": "Samuel Okafor",      "age": "19M", "conditions": "Cystic Fibrosis · CF-related Diabetes",              "status": "urgent"},
    "P012": {"name": "Ingrid Larsson",     "age": "37F", "conditions": "Multiple Sclerosis · Depression",                    "status": "normal"},
    "P013": {"name": "Theo Blackwood",     "age": "52M", "conditions": "ALS · Dysphagia · Respiratory Failure",              "status": "critical"},
}

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #f8fafc !important;
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Top Navigation ── */
.topnav {
    background: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 0 2rem;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.topnav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.topnav-logo {
    width: 32px; height: 32px;
    background: #003178;
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 16px; font-weight: 800;
}
.topnav-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: #0f172a; letter-spacing: -0.3px;
}
.topnav-subtitle {
    font-size: 0.65rem; text-transform: uppercase;
    letter-spacing: 2px; color: #94a3b8; font-weight: 600;
}
.topnav-links {
    display: flex; align-items: center; gap: 2px;
}
.topnav-link {
    padding: 6px 14px; border-radius: 8px;
    font-size: 0.82rem; font-weight: 500;
    color: #64748b; cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
    border: none; background: transparent;
}
.topnav-link:hover { background: #f1f5f9; color: #0f172a; }
.topnav-link.active {
    background: #eff6ff; color: #003178;
    font-weight: 700;
}
.topnav-right {
    display: flex; align-items: center; gap: 12px;
}
.emergency-btn {
    background: #dc2626; color: white;
    border: none; border-radius: 6px;
    padding: 5px 12px; font-size: 0.72rem;
    font-weight: 700; text-transform: uppercase;
    letter-spacing: 0.5px; cursor: pointer;
}
.doctor-info {
    display: flex; align-items: center; gap: 8px;
}
.doctor-avatar {
    width: 30px; height: 30px; border-radius: 50%;
    background: #003178; color: white;
    display: flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700;
}

/* ── Page Content ── */
.page-wrap { padding: 2rem 2.5rem; }
.page-header { margin-bottom: 1.5rem; }
.page-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.6rem; font-weight: 800;
    color: #0f172a; letter-spacing: -0.5px;
}
.page-sub { font-size: 0.875rem; color: #64748b; margin-top: 4px; }

/* ── Cards ── */
.card {
    background: #ffffff; border: 1px solid #e2e8f0;
    border-radius: 12px; padding: 1.25rem 1.5rem;
    margin-bottom: 12px;
    transition: border-color 0.15s ease;
}
.card:hover { border-color: #003178; }
.card-label {
    font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 2px;
    color: #94a3b8; margin-bottom: 6px;
}
.card-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1rem; font-weight: 700; color: #0f172a;
    margin-bottom: 6px;
}
.card-body { font-size: 0.82rem; color: #64748b; line-height: 1.6; }

/* ── Badges ── */
.badge {
    display: inline-flex; align-items: center; gap: 4px;
    padding: 3px 10px; border-radius: 20px;
    font-size: 0.7rem; font-weight: 700;
}
.badge-critical { background: #fef2f2; color: #dc2626; border: 1px solid #fca5a5; }
.badge-urgent   { background: #fffbeb; color: #d97706; border: 1px solid #fcd34d; }
.badge-normal   { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; }
.badge-info     { background: #eff6ff; color: #003178; border: 1px solid #bfdbfe; }

/* ── Anomaly banners ── */
.anomaly-critical { background:#fef2f2; border:1px solid #fca5a5; border-left:4px solid #dc2626; border-radius:10px; padding:14px 18px; margin-bottom:16px; }
.anomaly-urgent   { background:#fffbeb; border:1px solid #fcd34d; border-left:4px solid #f59e0b; border-radius:10px; padding:14px 18px; margin-bottom:16px; }
.anomaly-warning  { background:#fffbeb; border:1px solid #fde68a; border-left:4px solid #fbbf24; border-radius:10px; padding:14px 18px; margin-bottom:16px; }
.anomaly-normal   { background:#f0fdf4; border:1px solid #86efac; border-left:4px solid #22c55e; border-radius:10px; padding:14px 18px; margin-bottom:16px; }
.anomaly-title    { font-weight:700; font-size:0.875rem; color:#0f172a; margin-bottom:6px; }
.anomaly-item     { font-size:0.8rem; color:#475569; margin:3px 0 3px 12px; }

/* ── Patient table ── */
.patient-table { width:100%; border-collapse:collapse; }
.patient-table th {
    background:#f8fafc; padding:10px 16px;
    font-size:0.68rem; font-weight:700; text-transform:uppercase;
    letter-spacing:1.5px; color:#94a3b8;
    border-bottom:1px solid #e2e8f0; text-align:left;
}
.patient-table td {
    padding:14px 16px; border-bottom:1px solid #f1f5f9;
    font-size:0.82rem; vertical-align:middle;
}
.patient-table tr:hover td { background:#f8fafc; }
.patient-name { font-weight:700; color:#0f172a; }
.patient-id   { font-size:0.72rem; color:#94a3b8; margin-top:2px; }
.time-badge {
    display:inline-block; padding:3px 8px; border-radius:6px;
    font-size:0.72rem; font-weight:700;
}
.time-critical { background:#fef2f2; color:#dc2626; }
.time-urgent   { background:#fffbeb; color:#d97706; }
.time-normal   { background:#f0f9ff; color:#003178; }

/* ── Conf bar ── */
.conf-wrap { display:flex; align-items:center; gap:8px; margin-top:8px; }
.conf-bg   { flex:1; background:#f1f5f9; border-radius:20px; height:5px; overflow:hidden; }
.conf-fill { height:100%; border-radius:20px; background:linear-gradient(90deg,#003178,#3b82f6); }
.conf-pct  { font-size:0.75rem; font-weight:700; color:#003178; min-width:32px; }

/* ── Risk bar ── */
.risk-bar-bg  { background:#f1f5f9; border-radius:20px; height:7px; margin:8px 0; overflow:hidden; }

/* ── SOAP sections ── */
.soap-section  { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:1.25rem 1.5rem; margin-bottom:12px; }
.soap-label    { font-size:0.65rem; font-weight:700; text-transform:uppercase; letter-spacing:2.5px; color:#003178; margin-bottom:10px; }
.soap-content  { font-size:0.85rem; color:#334155; line-height:1.8; }

/* ── Trace card ── */
.trace-card { background:#fff; border:1px solid #e2e8f0; border-radius:10px; padding:1rem 1.25rem; margin-bottom:8px; display:grid; grid-template-columns:40px 1fr; gap:12px; }
.trace-num  { background:#eff6ff; border-radius:6px; display:flex; align-items:center; justify-content:center; font-size:0.7rem; font-weight:700; color:#003178; height:32px; }
.trace-agent  { font-size:0.85rem; font-weight:700; color:#0f172a; margin-bottom:3px; }
.trace-action { font-size:0.75rem; color:#64748b; }
.trace-find   { font-size:0.75rem; color:#003178; font-style:italic; margin-top:3px; }

/* ── Section header ── */
.section-hdr { font-family:'Manrope',sans-serif; font-size:0.95rem; font-weight:700; color:#0f172a; padding-bottom:8px; border-bottom:2px solid #e2e8f0; margin:20px 0 12px; }

/* ── Drug card ── */
.drug-card { background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:1.1rem 1.4rem; margin-bottom:10px; }
.drug-pair { font-size:0.88rem; font-weight:600; color:#0f172a; margin-bottom:6px; }
.drug-rec  { font-size:0.8rem; color:#64748b; line-height:1.6; background:#f8fafc; padding:8px 12px; border-radius:6px; border-left:2px solid #003178; margin-top:6px; }

/* ── Tier badges ── */
.tier-critical { background:#fef2f2; color:#dc2626; border:1px solid #fca5a5; border-radius:4px; padding:2px 8px; font-size:0.68rem; font-weight:700; text-transform:uppercase; }
.tier-high     { background:#fff7ed; color:#ea580c; border:1px solid #fdba74; border-radius:4px; padding:2px 8px; font-size:0.68rem; font-weight:700; text-transform:uppercase; }
.tier-moderate { background:#fffbeb; color:#d97706; border:1px solid #fcd34d; border-radius:4px; padding:2px 8px; font-size:0.68rem; font-weight:700; text-transform:uppercase; }
.tier-low      { background:#f0fdf4; color:#16a34a; border:1px solid #86efac; border-radius:4px; padding:2px 8px; font-size:0.68rem; font-weight:700; text-transform:uppercase; }

/* ── Citation ── */
.citation { background:#f8fafc; border:1px solid #e2e8f0; border-left:3px solid #003178; border-radius:8px; padding:12px 16px; margin-bottom:8px; font-size:0.78rem; color:#64748b; font-family:monospace; line-height:1.7; }

/* ── Footer ── */
.footer { margin-top:2.5rem; padding-top:1rem; border-top:1px solid #e2e8f0; font-size:0.7rem; color:#94a3b8; display:flex; justify-content:space-between; font-family:monospace; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: #003178 !important; color: #fff !important;
    border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover { background: #1e40af !important; transform: translateY(-1px) !important; }
.stSelectbox > div > div { background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:8px !important; }
.stTabs [data-baseweb="tab-list"] { background:#fff !important; border:1px solid #e2e8f0 !important; border-radius:10px !important; padding:4px !important; gap:4px !important; }
.stTabs [data-baseweb="tab"] { background:transparent !important; color:#64748b !important; border-radius:8px !important; font-size:0.82rem !important; font-weight:500 !important; border:none !important; }
.stTabs [aria-selected="true"] { background:#eff6ff !important; color:#003178 !important; border:1px solid #bfdbfe !important; font-weight:700 !important; }
.stTabs [data-baseweb="tab-panel"] { padding:1rem 0 !important; background:transparent !important; }
div[data-testid="stExpander"] { border:1px solid #e2e8f0 !important; border-radius:10px !important; background:#fff !important; }
</style>
"""


def topnav(active_page: str):
    pages = {
        "dashboard":  ("Dashboard",       "app"),
        "briefing":   ("Patient Briefing","pages/1_Patient_Briefing"),
        "soap":       ("SOAP Generator",  "pages/2_SOAP_Generator"),
        "agents":     ("Agent Status",    "pages/3_Agent_Status"),
    }
    links_html = ""
    for key, (label, _) in pages.items():
        active_cls = "active" if key == active_page else ""
        href = "/" if key == "dashboard" else f"/{key.replace('_', '-')}"
        # Use streamlit page links rendered separately
        links_html += f'<span class="topnav-link {active_cls}">{label}</span>'

    return f"""
    <div class="topnav">
      <div class="topnav-brand">
        <div class="topnav-logo">M+</div>
        <div>
          <div class="topnav-title">MediCopilot</div>
          <div class="topnav-subtitle">AI Clinical Copilot</div>
        </div>
      </div>
      <div class="topnav-links">{links_html}</div>
      <div class="topnav-right">
        <button class="emergency-btn">Emergency Mode</button>
        <div class="doctor-info">
          <div class="doctor-avatar">JT</div>
          <div>
            <div style="font-size:0.75rem;font-weight:700;color:#0f172a">Dr. Julian Thorne</div>
            <div style="font-size:0.65rem;color:#94a3b8">Chief Medical Officer</div>
          </div>
        </div>
      </div>
    </div>
    """
