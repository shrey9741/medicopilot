"""
MediCopilot — Shared utilities, CSS and constants.
"""

API_BASE = "https://medicopilot.onrender.com"

PATIENTS = {
    "P001": {"name": "John Doe",         "age": "62M", "conditions": "T2 Diabetes · Hypertension · CKD",               "status": "urgent"},
    "P002": {"name": "Sarah Chen",        "age": "45F", "conditions": "Atrial Fibrillation · Hypothyroidism",            "status": "normal"},
    "P003": {"name": "Marcus Johnson",    "age": "71M", "conditions": "COPD · Heart Failure · T2 Diabetes",              "status": "critical"},
    "P004": {"name": "Patricia Williams", "age": "54F", "conditions": "Breast Cancer HER2+ · Neuropathy",                "status": "normal"},
    "P005": {"name": "Robert Nguyen",     "age": "67M", "conditions": "Lung Cancer Stage IV · COPD",                     "status": "urgent"},
    "P006": {"name": "Aiden Patel",       "age": "8M",  "conditions": "T1 Diabetes · Asthma · Celiac Disease",           "status": "critical"},
    "P007": {"name": "Lily Thompson",     "age": "5F",  "conditions": "ALL Leukemia · Febrile Neutropenia",              "status": "critical"},
    "P008": {"name": "Diana Foster",      "age": "34F", "conditions": "Bipolar I · Anxiety · Hypothyroidism",            "status": "normal"},
    "P009": {"name": "Carlos Rivera",     "age": "28M", "conditions": "Schizophrenia · Substance Use Disorder",          "status": "urgent"},
    "P010": {"name": "Eleanor Voss",      "age": "41F", "conditions": "Lupus · Antiphospholipid Syndrome",               "status": "urgent"},
    "P011": {"name": "Samuel Okafor",     "age": "19M", "conditions": "Cystic Fibrosis · CF-related Diabetes",           "status": "urgent"},
    "P012": {"name": "Ingrid Larsson",    "age": "37F", "conditions": "Multiple Sclerosis · Depression",                 "status": "normal"},
    "P013": {"name": "Theo Blackwood",    "age": "52M", "conditions": "ALS · Dysphagia · Respiratory Failure",           "status": "critical"},
}

SHARED_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Manrope:wght@600;700;800&display=swap');

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: #0a0f1e !important;
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }

/* ── Top Navigation ── */
.topnav {
    background: #0d1425;
    border-bottom: 1px solid #1e2d4a;
    padding: 0 2rem;
    height: 56px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 100;
}
.topnav-brand { display: flex; align-items: center; gap: 10px; }
.topnav-logo {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #1a6b9a, #003178);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    color: white; font-size: 13px; font-weight: 800;
}
.topnav-title { font-family: 'Manrope', sans-serif; font-size: 1rem; font-weight: 800; color: #ffffff; letter-spacing: -0.3px; }
.topnav-subtitle { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 2px; color: #4a7fa5; font-weight: 600; }
.topnav-right { display: flex; align-items: center; gap: 12px; }
.emergency-btn {
    background: #dc2626; color: white; border: none; border-radius: 6px;
    padding: 5px 12px; font-size: 0.68rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.5px; cursor: pointer;
}
.doctor-avatar {
    width: 30px; height: 30px; border-radius: 50%;
    background: linear-gradient(135deg,#1a6b9a,#003178);
    color: white; display: flex; align-items: center;
    justify-content: center; font-size: 11px; font-weight: 700;
}
.doctor-name { font-size: 0.75rem; font-weight: 700; color: #e2e8f0; }
.doctor-role { font-size: 0.62rem; color: #4a7fa5; }

/* ── Page nav row (streamlit page links) ── */
[data-testid="stPageLink"] a {
    background: #131d35 !important;
    border: 1px solid #1e2d4a !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    padding: 6px 14px !important;
    text-decoration: none !important;
    transition: all 0.15s ease !important;
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    white-space: nowrap !important;
}
[data-testid="stPageLink"] a:hover {
    background: #1e2d4a !important;
    color: #e2e8f0 !important;
    border-color: #2a3d5a !important;
}
[data-testid="stPageLink-active"] a {
    background: #1a3a5c !important;
    border-color: #1a6b9a !important;
    color: #38bdf8 !important;
    font-weight: 700 !important;
}
.nav-row {
    display: flex; gap: 6px; padding: 10px 2rem 0;
    background: #0a0f1e; border-bottom: 1px solid #1e2d4a;
    margin-bottom: 0;
}

/* ── Page content ── */
.page-wrap { padding: 1.5rem 2rem; }
.page-header { margin-bottom: 1.5rem; }
.page-title { font-family: 'Manrope', sans-serif; font-size: 1.6rem; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; }
.page-sub { font-size: 0.875rem; color: #64748b; margin-top: 4px; }

/* ── Cards ── */
.card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 12px; transition: border-color 0.15s ease; }
.card:hover { border-color: #1a6b9a; }
.card-label { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; color: #4a7fa5; margin-bottom: 6px; }
.card-title { font-family: 'Manrope', sans-serif; font-size: 1rem; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
.card-body { font-size: 0.82rem; color: #94a3b8; line-height: 1.6; }

/* ── Anomaly banners ── */
.anomaly-critical { background: linear-gradient(135deg,#1a0a0a,#2d0f0f); border: 1px solid #ef4444; border-left: 4px solid #ef4444; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px; }
.anomaly-urgent   { background: linear-gradient(135deg,#1a1200,#2d1f00); border: 1px solid #f59e0b; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px; }
.anomaly-warning  { background: linear-gradient(135deg,#1a1200,#2d1f00); border: 1px solid #fbbf24; border-left: 4px solid #fbbf24; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px; }
.anomaly-normal   { background: linear-gradient(135deg,#001a0f,#002d1a); border: 1px solid #10b981; border-left: 4px solid #10b981; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px; }
.anomaly-title { font-weight: 700; font-size: 0.875rem; color: #e2e8f0; margin-bottom: 6px; }
.anomaly-item  { font-size: 0.8rem; color: #94a3b8; margin: 3px 0 3px 12px; }

/* ── Patient table ── */
.patient-table { width: 100%; border-collapse: collapse; }
.patient-table th { background: #0a0f1e; padding: 10px 16px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #4a7fa5; border-bottom: 1px solid #1e2d4a; text-align: left; }
.patient-table td { padding: 14px 16px; border-bottom: 1px solid #131d35; font-size: 0.82rem; vertical-align: middle; }
.patient-table tr:hover td { background: #0d1425; }
.patient-name { font-weight: 700; color: #e2e8f0; }
.patient-id { font-size: 0.72rem; color: #4a7fa5; margin-top: 2px; }
.time-badge { display: inline-block; padding: 3px 8px; border-radius: 6px; font-size: 0.72rem; font-weight: 700; }
.time-critical { background: #2d0f0f; color: #ef4444; }
.time-urgent   { background: #2d1f00; color: #f59e0b; }
.time-normal   { background: #001945; color: #60a5fa; }

/* ── Badges ── */
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 3px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; }
.badge-critical { background: #2d0f0f; color: #ef4444; border: 1px solid #ef4444; }
.badge-urgent   { background: #2d1f00; color: #f59e0b; border: 1px solid #f59e0b; }
.badge-normal   { background: #002d1a; color: #10b981; border: 1px solid #10b981; }
.badge-info     { background: #001945; color: #60a5fa; border: 1px solid #1a6b9a; }

/* ── Confidence bar ── */
.conf-wrap { display: flex; align-items: center; gap: 8px; margin-top: 8px; }
.conf-bg   { flex: 1; background: #131d35; border-radius: 20px; height: 5px; overflow: hidden; }
.conf-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg,#1a6b9a,#38bdf8); }
.conf-pct  { font-size: 0.75rem; font-weight: 700; color: #38bdf8; min-width: 32px; }

/* ── Tier badges ── */
.tier-critical { background: #2d0f0f; color: #ef4444; border: 1px solid #ef4444; border-radius: 4px; padding: 2px 8px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }
.tier-high     { background: #2d1500; color: #f97316; border: 1px solid #f97316; border-radius: 4px; padding: 2px 8px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }
.tier-moderate { background: #2d2000; color: #f59e0b; border: 1px solid #f59e0b; border-radius: 4px; padding: 2px 8px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }
.tier-low      { background: #002d1a; color: #10b981; border: 1px solid #10b981; border-radius: 4px; padding: 2px 8px; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; }

/* ── Drug card ── */
.drug-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.1rem 1.4rem; margin-bottom: 10px; }
.drug-pair { font-size: 0.88rem; font-weight: 600; color: #e2e8f0; margin-bottom: 6px; }
.drug-rec  { font-size: 0.8rem; color: #94a3b8; line-height: 1.6; background: #131d35; padding: 8px 12px; border-radius: 6px; border-left: 2px solid #1a6b9a; margin-top: 6px; }

/* ── Risk bar ── */
.risk-bar-bg { background: #131d35; border-radius: 20px; height: 7px; margin: 8px 0; overflow: hidden; }

/* ── Section header ── */
.section-hdr { font-family: 'Manrope', sans-serif; font-size: 0.95rem; font-weight: 700; color: #e2e8f0; padding-bottom: 8px; border-bottom: 1px solid #1e2d4a; margin: 20px 0 12px; }

/* ── SOAP ── */
.soap-section { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 12px; }
.soap-label   { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 2.5px; color: #1a6b9a; margin-bottom: 10px; }
.soap-content { font-size: 0.85rem; color: #94a3b8; line-height: 1.8; }

/* ── Trace ── */
.trace-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1rem 1.25rem; margin-bottom: 8px; display: grid; grid-template-columns: 40px 1fr; gap: 12px; }
.trace-card:hover { border-color: #1a6b9a; }
.trace-num    { background: #131d35; border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 0.7rem; font-weight: 700; color: #38bdf8; height: 32px; }
.trace-agent  { font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 3px; }
.trace-action { font-size: 0.75rem; color: #64748b; }
.trace-find   { font-size: 0.75rem; color: #38bdf8; font-style: italic; margin-top: 3px; }

/* ── Agent card ── */
.agent-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.1rem; transition: border-color 0.2s; }
.agent-card:hover { border-color: #1a6b9a; }
.agent-card.active { border-color: #38bdf8; background: #0d1a2a; }
.agent-card.done   { border-color: #10b981; }
.agent-emoji { font-size: 1.4rem; margin-bottom: 8px; }
.agent-name  { font-size: 0.82rem; font-weight: 700; color: #e2e8f0; margin-bottom: 3px; }
.agent-desc  { font-size: 0.72rem; color: #64748b; }
.agent-status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }
.dot-idle    { background: #334155; }
.dot-active  { background: #38bdf8; animation: pulse 1s infinite; }
.dot-done    { background: #10b981; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }

/* ── Citation ── */
.citation { background: #0a0f1e; border: 1px solid #1e2d4a; border-left: 3px solid #1a6b9a; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; font-size: 0.78rem; color: #64748b; font-family: monospace; line-height: 1.7; }

/* ── Footer ── */
.footer { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #1e2d4a; font-size: 0.7rem; color: #334155; display: flex; justify-content: space-between; font-family: monospace; }

/* ── Streamlit overrides ── */
.stButton > button {
    background: linear-gradient(135deg,#1a6b9a,#003178) !important;
    color: #fff !important; border: none !important; border-radius: 8px !important;
    font-weight: 600 !important; font-size: 0.82rem !important;
    padding: 0.5rem 1.2rem !important; transition: all 0.15s ease !important;
}
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.stSelectbox label { color: #94a3b8 !important; font-size: 0.8rem !important; }
.stSelectbox > div > div {
    background: #131d35 !important; border: 1px solid #1e2d4a !important;
    border-radius: 8px !important; color: #e2e8f0 !important;
}
.stSelectbox > div > div > div { color: #e2e8f0 !important; }
.stTabs [data-baseweb="tab-list"] { background: #0d1425 !important; border: 1px solid #1e2d4a !important; border-radius: 10px !important; padding: 4px !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #64748b !important; border-radius: 8px !important; font-size: 0.82rem !important; font-weight: 500 !important; border: none !important; }
.stTabs [aria-selected="true"] { background: #131d35 !important; color: #38bdf8 !important; border: 1px solid #1e2d4a !important; font-weight: 700 !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 1rem 0 !important; background: transparent !important; }
div[data-testid="stExpander"] { border: 1px solid #1e2d4a !important; border-radius: 10px !important; background: #0d1425 !important; }
div[data-testid="stExpander"] summary { color: #e2e8f0 !important; }
.stDownloadButton > button {
    background: #131d35 !important; border: 1px solid #1a6b9a !important;
    color: #38bdf8 !important; border-radius: 8px !important;
    font-weight: 600 !important;
}
[data-testid="stSpinner"] { color: #38bdf8 !important; }
</style>
"""


def topnav(active_page: str):
    pages = [
        ("dashboard", "Dashboard"),
        ("briefing",  "Patient Briefing"),
        ("soap",      "SOAP Generator"),
        ("agents",    "Agent Status"),
    ]
    links_html = ""
    for key, label in pages:
        active_cls = "active" if key == active_page else ""
        links_html += f'<span class="topnav-link {active_cls}" style="padding:6px 14px;border-radius:8px;font-size:0.82rem;font-weight:{"700" if key==active_page else "500"};color:{"#38bdf8" if key==active_page else "#94a3b8"};background:{"#131d35" if key==active_page else "transparent"};cursor:pointer;margin:0 2px">{label}</span>'

    return f"""
    <div class="topnav">
      <div class="topnav-brand">
        <div class="topnav-logo">M+</div>
        <div>
          <div class="topnav-title">MediCopilot</div>
          <div class="topnav-subtitle">AI Clinical Copilot</div>
        </div>
      </div>
      <div style="display:flex;align-items:center;gap:2px">{links_html}</div>
      <div class="topnav-right">
        <button class="emergency-btn">⚡ Emergency Mode</button>
        <div style="display:flex;align-items:center;gap:8px">
          <div class="doctor-avatar">JT</div>
          <div>
            <div class="doctor-name">Dr. Julian Thorne</div>
            <div class="doctor-role">Chief Medical Officer</div>
          </div>
        </div>
      </div>
    </div>
    """
