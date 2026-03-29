"""
MediCopilot — Streamlit UI
Design: "The Clinical Luminary"
"""
import streamlit as st
import httpx
import os

st.set_page_config(
    page_title="MediCopilot | Clinical AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_BASE = os.getenv("API_BASE", "https://medicopilot.onrender.com")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

html, body, .stApp { background: #0b0e14 !important; color: #ecedf6 !important; font-family: 'Inter', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 1.5rem 1rem !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: #10131a !important; border: 1px solid rgba(255,255,255,0.07) !important;
    color: #ecedf6 !important; border-radius: 12px !important; font-size: 0.82rem !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #69daff 0%, #17c0fd 100%) !important;
    color: #003d4f !important; border: none !important; border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important; font-family: 'Manrope', sans-serif !important;
    font-weight: 800 !important; font-size: 0.88rem !important;
    box-shadow: 0 4px 20px rgba(105,218,255,0.25), inset 0 1px 0 rgba(255,255,255,0.2) !important;
    transition: all 0.2s !important; width: 100%;
}
.stButton > button:hover { box-shadow: 0 6px 28px rgba(105,218,255,0.4) !important; transform: translateY(-1px) !important; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: #161a21 !important; border-radius: 12px !important;
    padding: 4px !important; border: 1px solid rgba(255,255,255,0.05) !important; gap: 2px !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #a9abb3 !important;
    border-radius: 8px !important; font-family: 'Inter', sans-serif !important;
    font-size: 0.8rem !important; font-weight: 500 !important;
    padding: 7px 14px !important; border: none !important;
}
.stTabs [aria-selected="true"] { background: #282c36 !important; color: #69daff !important; }
.stTabs [data-baseweb="tab-panel"] { padding: 1rem 0 0 !important; background: transparent !important; }

/* Expander */
details > summary { background: #161a21 !important; border-radius: 10px !important; color: #a9abb3 !important; border: 1px solid rgba(255,255,255,0.05) !important; }

/* Spinner */
.stSpinner > div { border-top-color: #69daff !important; }

/* Progress */
.stProgress > div > div { background: #161a21 !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #17c0fd, #69daff) !important; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #45484f; border-radius: 10px; }

/* ── COMPONENTS ── */
.top-bar {
    display: flex; align-items: center; gap: 24px;
    background: #161a21; border-radius: 14px;
    padding: 12px 20px; margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.05);
}
.top-bar-tab { font-size: 0.82rem; font-weight: 500; color: #a9abb3; cursor: pointer; padding: 4px 0; border-bottom: 2px solid transparent; }
.top-bar-tab.active { color: #69daff; border-bottom-color: #69daff; }
.ai-badge {
    margin-left: auto; display: flex; align-items: center; gap: 6px;
    background: rgba(105,218,255,0.08); border: 1px solid rgba(105,218,255,0.2);
    border-radius: 20px; padding: 5px 14px;
    font-size: 0.68rem; font-weight: 700; color: #69daff; letter-spacing: 0.08em;
}
.ai-dot { width: 6px; height: 6px; background: #69daff; border-radius: 50%; display: inline-block; animation: pulse 2s infinite; margin-right: 4px; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.3} }

.left-panel-box {
    background: #161a21; border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.05);
    padding: 20px; height: 100%;
}
.panel-title {
    font-family: 'Manrope', sans-serif; font-size: 1rem; font-weight: 800;
    color: #ecedf6; margin-bottom: 16px;
    display: flex; align-items: center; gap: 8px;
}
.model-badge {
    background: rgba(105,218,255,0.08); border: 1px solid rgba(105,218,255,0.2);
    border-radius: 20px; padding: 2px 8px;
    font-size: 0.6rem; font-weight: 700; color: #69daff; letter-spacing: 0.05em;
}
.section-label {
    font-size: 0.62rem; font-weight: 700; letter-spacing: 0.15em;
    text-transform: uppercase; color: #a9abb3; margin-bottom: 8px; margin-top: 16px;
}
.agents-wrap { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 6px; }
.agent-pill {
    background: #1c2028; border-radius: 8px; padding: 3px 9px;
    font-size: 0.66rem; font-weight: 600; color: #17c0fd; font-family: 'Inter', sans-serif;
}

.glass-card {
    background: rgba(34,38,47,0.5); backdrop-filter: blur(12px);
    border: 1px solid rgba(105,218,255,0.15); border-radius: 16px;
    padding: 24px; margin-bottom: 14px;
    box-shadow: 0 20px 40px rgba(0,209,255,0.06);
    position: relative; overflow: hidden;
}
.glass-card::after {
    content:''; position:absolute; top:-30px; right:-30px;
    width:100px; height:100px;
    background: rgba(105,218,255,0.05); filter: blur(25px);
    border-radius: 50%; pointer-events: none;
}
.card-title {
    font-family: 'Manrope', sans-serif; font-size: 1.05rem; font-weight: 800;
    color: #ecedf6; display: flex; align-items: center; gap: 10px; margin-bottom: 4px;
}
.conf-badge {
    background: rgba(105,218,255,0.1); border: 1px solid rgba(105,218,255,0.25);
    border-radius: 20px; padding: 2px 8px;
    font-size: 0.62rem; font-weight: 900; color: #69daff; letter-spacing: 0.08em;
}
.card-sub { font-size: 0.75rem; color: #a9abb3; margin-bottom: 16px; }

.dx-inner {
    background: rgba(0,0,0,0.35); border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px; padding: 18px; margin-bottom: 12px;
}
.dx-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #17c0fd; margin-bottom: 6px; }
.dx-name { font-family: 'Manrope', sans-serif; font-size: 1.4rem; font-weight: 700; color: #ecedf6; line-height: 1.2; margin-bottom: 8px; }
.dx-text { font-size: 0.78rem; color: #a9abb3; line-height: 1.6; }

.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 12px; }
.inner-box { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 10px; padding: 14px; }
.inner-label { font-size: 0.58rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #a9abb3; margin-bottom: 8px; }
.inner-item { display: flex; align-items: center; gap: 7px; font-size: 0.78rem; color: #ecedf6; margin-bottom: 5px; }
.dot-blue { width: 5px; height: 5px; border-radius: 50%; background: #17c0fd; flex-shrink: 0; }
.item-critical { color: #ff716c; }
.item-info { color: #69daff; }

.conflict-bar {
    background: rgba(28,32,40,0.6); border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px; padding: 12px 16px;
    display: flex; align-items: center; gap: 12px; margin-bottom: 12px;
}
.conflict-icon { width: 38px; height: 38px; background: #006688; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; font-size: 18px; }
.conflict-title { font-size: 0.8rem; font-weight: 700; color: #ecedf6; }
.conflict-sub { font-size: 0.68rem; color: #a9abb3; margin-top: 2px; }
.conflict-sev { margin-left: auto; font-size: 0.72rem; font-weight: 900; color: #ff716c; background: rgba(255,113,108,0.1); border: 1px solid rgba(255,113,108,0.3); border-radius: 8px; padding: 4px 10px; }

.anomaly-urgent { background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.25); border-left: 3px solid #f59e0b; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; }
.anomaly-critical { background: rgba(255,113,108,0.07); border: 1px solid rgba(255,113,108,0.25); border-left: 3px solid #ff716c; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; }
.anomaly-warning { background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.2); border-left: 3px solid #f59e0b; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; }
.anomaly-normal { background: rgba(105,218,255,0.04); border: 1px solid rgba(105,218,255,0.15); border-left: 3px solid #69daff; border-radius: 10px; padding: 12px 16px; margin-bottom: 14px; }
.anomaly-title { font-size: 0.82rem; font-weight: 700; color: #ecedf6; margin-bottom: 4px; }
.anomaly-item { font-size: 0.74rem; color: #a9abb3; margin: 2px 0; }

.patient-card { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 14px; }
.patient-name { font-family: 'Manrope', sans-serif; font-size: 1.25rem; font-weight: 800; color: #ecedf6; margin-bottom: 6px; }
.patient-text { font-size: 0.76rem; color: #a9abb3; line-height: 1.6; }

.std-card { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
.std-title { font-size: 0.85rem; font-weight: 600; color: #ecedf6; margin-bottom: 6px; }
.std-text { font-size: 0.76rem; color: #a9abb3; line-height: 1.5; }

.tier-critical { background: rgba(255,113,108,0.1); color: #ff716c; border: 1px solid rgba(255,113,108,0.3); border-radius: 6px; padding: 1px 7px; font-size: 0.62rem; font-weight: 700; }
.tier-high { background: rgba(249,115,22,0.1); color: #f97316; border: 1px solid rgba(249,115,22,0.3); border-radius: 6px; padding: 1px 7px; font-size: 0.62rem; font-weight: 700; }
.tier-moderate { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); border-radius: 6px; padding: 1px 7px; font-size: 0.62rem; font-weight: 700; }
.tier-low { background: rgba(105,218,255,0.08); color: #69daff; border: 1px solid rgba(105,218,255,0.2); border-radius: 6px; padding: 1px 7px; font-size: 0.62rem; font-weight: 700; }
.cbar-bg { background: #0b0e14; border-radius: 20px; height: 5px; flex: 1; overflow: hidden; }
.cbar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg,#17c0fd,#69daff); }

.risk-card { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
.risk-hdr { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.risk-name { font-size: 0.85rem; font-weight: 600; color: #ecedf6; }
.risk-pct { font-family: 'Manrope', sans-serif; font-size: 1.05rem; font-weight: 800; }
.risk-bar-bg { background: #0b0e14; border-radius: 20px; height: 6px; margin-bottom: 10px; overflow: hidden; }
.risk-factor { font-size: 0.72rem; color: #a9abb3; margin: 3px 0; padding-left: 12px; position: relative; }
.risk-factor::before { content: '→'; position: absolute; left: 0; color: #45484f; }
.risk-rec { font-size: 0.72rem; color: #69daff; margin-top: 8px; padding: 7px 12px; background: rgba(105,218,255,0.05); border-radius: 8px; border-left: 2px solid #69daff; }

.soap-card { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 14px; padding: 18px; margin-bottom: 10px; }
.soap-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #69daff; margin-bottom: 8px; }
.soap-text { font-size: 0.8rem; color: #a9abb3; line-height: 1.7; }

.trace-card { background: #161a21; border: 1px solid rgba(255,255,255,0.05); border-radius: 12px; padding: 12px 14px; margin-bottom: 8px; display: flex; gap: 12px; align-items: flex-start; }
.trace-num { font-size: 0.62rem; font-weight: 700; color: #69daff; background: rgba(105,218,255,0.08); border-radius: 6px; padding: 3px 7px; flex-shrink: 0; }
.trace-agent { font-size: 0.78rem; font-weight: 600; color: #ecedf6; margin-bottom: 3px; }
.trace-action { font-size: 0.7rem; color: #a9abb3; }
.trace-finding { font-size: 0.7rem; color: #69daff; margin-top: 3px; font-style: italic; }

.opinion-card { background: rgba(105,218,255,0.03); border: 1px solid rgba(105,218,255,0.15); border-radius: 14px; padding: 18px; margin-top: 12px; }
.opinion-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: #69daff; margin-bottom: 10px; }

.right-panel-box { background: #161a21; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); padding: 18px; }
.rp-title { font-family: 'Manrope', sans-serif; font-size: 0.95rem; font-weight: 800; color: #ecedf6; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center; }
.history-card { background: #10131a; border: 1px solid rgba(255,255,255,0.04); border-radius: 12px; padding: 12px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
.history-card:hover { background: #1c2028; border-color: rgba(105,218,255,0.15); }
.h-meta { display: flex; justify-content: space-between; margin-bottom: 5px; }
.h-case { font-size: 0.6rem; font-weight: 700; color: #a9abb3; text-transform: uppercase; letter-spacing: 0.08em; }
.h-time { font-size: 0.6rem; color: #a9abb3; }
.h-name { font-size: 0.78rem; font-weight: 600; color: #ecedf6; margin-bottom: 7px; line-height: 1.3; }
.h-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.t-crit { background: rgba(255,113,108,0.1); color: #ff716c; border-radius: 20px; padding: 2px 7px; font-size: 0.58rem; font-weight: 700; text-transform: uppercase; }
.t-stable { background: rgba(137,165,255,0.1); color: #89a5ff; border-radius: 20px; padding: 2px 7px; font-size: 0.58rem; font-weight: 700; text-transform: uppercase; }
.t-routine { background: rgba(137,165,255,0.1); color: #89a5ff; border-radius: 20px; padding: 2px 7px; font-size: 0.58rem; font-weight: 700; text-transform: uppercase; }
.t-urgent { background: rgba(245,158,11,0.1); color: #f59e0b; border-radius: 20px; padding: 2px 7px; font-size: 0.58rem; font-weight: 700; text-transform: uppercase; }
.t-cat { background: #1c2028; color: #a9abb3; border-radius: 20px; padding: 2px 7px; font-size: 0.58rem; font-weight: 700; text-transform: uppercase; }

.copilot-pro-box { background: rgba(105,218,255,0.04); border: 1px solid rgba(105,218,255,0.18); border-radius: 12px; padding: 14px; margin-top: 12px; }
.cp-label { font-size: 0.6rem; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: #69daff; margin-bottom: 6px; }
.cp-text { font-size: 0.7rem; color: #a9abb3; line-height: 1.6; }

.empty-state { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px 20px; opacity: 0.4; text-align: center; }
.empty-icon { font-size: 3rem; margin-bottom: 12px; }
.empty-title { font-family: 'Manrope', sans-serif; font-size: 0.95rem; font-weight: 700; color: #ecedf6; margin-bottom: 6px; }
.empty-sub { font-size: 0.75rem; color: #a9abb3; }

.sev-crit { color: #ff716c; font-weight: 700; }
.sev-major { color: #f97316; font-weight: 700; }
.sev-moderate { color: #f59e0b; font-weight: 700; }
.sev-minor { color: #69daff; font-weight: 700; }

.citation-card { background: #10131a; border: 1px solid rgba(255,255,255,0.04); border-radius: 10px; padding: 12px 14px; font-size: 0.72rem; color: #a9abb3; line-height: 1.6; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────────
if "data" not in st.session_state:
    st.session_state.data = None

patient_options = {
    "P001 — John Doe (62M, Diabetes + HTN + CKD)": "P001",
    "P002 — Sarah Chen (45F, AFib + Hypothyroidism)": "P002",
    "P003 — Marcus Johnson (71M, COPD + Heart Failure)": "P003",
    "P004 — Patricia Williams (54F, Breast Cancer HER2+)": "P004",
    "P005 — Robert Nguyen (67M, Lung Cancer Stage IV)": "P005",
    "P006 — Aiden Patel (8M, T1 Diabetes + Asthma)": "P006",
    "P007 — Lily Thompson (5F, ALL Leukemia)": "P007",
    "P008 — Diana Foster (34F, Bipolar I + Anxiety)": "P008",
    "P009 — Carlos Rivera (28M, Schizophrenia + SUD)": "P009",
    "P010 — Eleanor Voss (41F, Lupus + Antiphospholipid)": "P010",
    "P011 — Samuel Okafor (19M, Cystic Fibrosis)": "P011",
    "P012 — Ingrid Larsson (37F, Multiple Sclerosis)": "P012",
    "P013 — Theo Blackwood (52M, ALS)": "P013",
}

# ── Top bar ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="top-bar">
    <span class="top-bar-tab active">RAG</span>
    <span class="top-bar-tab">Multi-Agent</span>
    <span class="top-bar-tab">Drug Safety</span>
    <span class="top-bar-tab">SOAP Notes</span>
    <div class="ai-badge"><span class="ai-dot"></span>AI CLINICAL COPILOT</div>
</div>
""", unsafe_allow_html=True)

# ── Three columns ─────────────────────────────────────────────────────────────
left_col, center_col, right_col = st.columns([2.2, 5, 2.1])

# ── LEFT PANEL ────────────────────────────────────────────────────────────────
with left_col:
    st.markdown("""
    <div class="left-panel-box">
        <div class="panel-title">Patient Summary <span class="model-badge">⚡ LLAMA 3.1</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Select Patient</div>', unsafe_allow_html=True)
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡  Run AI Analysis", use_container_width=True)

    st.markdown('<div class="section-label">Active Agents</div>', unsafe_allow_html=True)
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    pills = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
    st.markdown(f'<div class="agents-wrap">{pills}</div>', unsafe_allow_html=True)

# ── API call ──────────────────────────────────────────────────────────────────
if run_btn:
    with center_col:
        st.markdown("""
        <style>
        @keyframes shimmer { 0%{transform:translateX(-100%)} 100%{transform:translateX(300%)} }
        </style>
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:80px 20px;text-align:center;">
            <div style="font-size:3rem;margin-bottom:16px">🧠</div>
            <div style="font-family:'Manrope',sans-serif;font-size:1.1rem;font-weight:800;color:#ecedf6;margin-bottom:8px">Generating Clinical Briefing...</div>
            <div style="font-size:0.76rem;color:#a9abb3;margin-bottom:28px">9 AI agents are collaborating on your patient analysis</div>
            <div style="width:260px;height:5px;background:#161a21;border-radius:20px;overflow:hidden;position:relative;">
                <div style="position:absolute;height:100%;width:40%;background:linear-gradient(90deg,transparent,#17c0fd,#69daff,transparent);border-radius:20px;animation:shimmer 1.6s ease-in-out infinite;"></div>
            </div>
            <div style="font-size:0.68rem;color:#45484f;margin-top:14px;">This may take 20–40 seconds on first request</div>
        </div>
        """, unsafe_allow_html=True)
    try:
        response = httpx.post(
            f"{API_BASE}/invoke",
            json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
            timeout=120.0
        )
        response.raise_for_status()
        st.session_state.data = response.json()
        st.rerun()
    except httpx.ConnectError:
        st.error("Cannot connect to API backend.")
    except Exception as e:
        st.error(f"API error: {e}")

data = st.session_state.data

# ── CENTER PANEL ──────────────────────────────────────────────────────────────
with center_col:
    if not data:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🔬</div>
            <div class="empty-title">Select a patient and run AI Analysis</div>
            <div class="empty-sub">Multi-agent clinical reasoning will appear here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Anomaly
        anomaly = data["anomaly_flag"]
        level = anomaly["level"]
        emoji = {"CRITICAL":"🚨","URGENT":"⚠️","WARNING":"🔶","NORMAL":"✅"}.get(level,"ℹ️")
        a_cls = f"anomaly-{level.lower()}" if level.lower() in ["critical","urgent","warning","normal"] else "anomaly-normal"
        if anomaly["triggered"]:
            items = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
            st.markdown(f'<div class="{a_cls}"><div class="anomaly-title">{emoji} {level} — Vital Anomaly Detected</div>{items}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ All vitals within acceptable ranges</div></div>', unsafe_allow_html=True)

        # Patient card
        st.markdown(f"""
        <div class="patient-card">
            <div class="patient-name">{data['patient_name']}</div>
            <div class="patient-text">{data['summary']}</div>
        </div>""", unsafe_allow_html=True)

        if data.get("memory_trend"):
            with st.expander("📈 Patient Memory Trends"):
                st.code(data["memory_trend"], language="text")

        # Tabs
        t1, t2, t3, t4, t5 = st.tabs(["🔬 Diagnosis", "💊 Drug Safety", "📊 Risk Scores", "📝 SOAP Note", "🔍 Reasoning"])

        with t1:
            diagnoses = data.get("diagnoses", [])
            if diagnoses:
                top = diagnoses[0]
                conf = top["confidence"]
                warnings = data.get("drug_warnings", [])

                st.markdown(f"""
                <div class="glass-card">
                    <div class="card-title">Primary Differential <span class="conf-badge">{conf}% CONFIDENCE</span></div>
                    <div class="card-sub">Based on RAG analysis of medical guidelines</div>
                    <div class="dx-inner">
                        <div class="dx-label">Diagnosis</div>
                        <div class="dx-name">{top['condition']}</div>
                        <div class="dx-text">{top['reasoning']}</div>
                    </div>
                """, unsafe_allow_html=True)

                if len(diagnoses) > 1:
                    sec = "".join(f'<div class="inner-item"><div class="dot-blue"></div>{d["condition"]}</div>' for d in diagnoses[1:3])
                    crits = ""
                    if warnings:
                        crits += f'<div class="inner-item item-critical">⚠ {warnings[0]["drug_a"]} + {warnings[0]["drug_b"]}</div>'
                    if len(warnings) > 1:
                        crits += f'<div class="inner-item item-info">ℹ Monitor: {warnings[1]["drug_b"]}</div>'
                    if not crits:
                        crits = '<div class="inner-item item-info">No critical flags</div>'
                    st.markdown(f"""
                    <div class="two-col">
                        <div class="inner-box"><div class="inner-label">Secondary Findings</div>{sec}</div>
                        <div class="inner-box"><div class="inner-label">Critical Actions</div>{crits}</div>
                    </div>""", unsafe_allow_html=True)

                if warnings:
                    w = warnings[0]
                    sev = w['severity'].lower()
                    sev_color = "HIGH" if sev in ["critical","major"] else sev.title()
                    st.markdown(f"""
                    <div class="conflict-bar">
                        <div class="conflict-icon">🛡️</div>
                        <div>
                            <div class="conflict-title">Drug-Drug Conflict Detected</div>
                            <div class="conflict-sub">{w['drug_a']} + {w['drug_b']} (K+ Risk)</div>
                        </div>
                        <div class="conflict-sev">{sev_color}</div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                if len(diagnoses) > 1:
                    for i, dx in enumerate(diagnoses[1:], 2):
                        tier = dx["tier"]
                        c = dx["confidence"]
                        st.markdown(f"""
                        <div class="std-card">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                                <div class="std-title">{i}. {dx['condition']}</div>
                                <div style="display:flex;align-items:center;gap:8px">
                                    <span class="tier-{tier}">{tier.upper()}</span>
                                    <div class="cbar-bg" style="width:70px"><div class="cbar-fill" style="width:{c}%"></div></div>
                                    <span style="font-size:0.68rem;color:#69daff">{c}%</span>
                                </div>
                            </div>
                            <div class="std-text">{dx['reasoning']}</div>
                        </div>""", unsafe_allow_html=True)

            if data.get("second_opinion"):
                op = data["second_opinion"]
                st.markdown(f"""
                <div class="opinion-card">
                    <div class="opinion-label">🧐 Second Opinion Analysis</div>
                    <div style="font-size:0.76rem;color:#a9abb3;margin-bottom:7px"><strong style="color:#ecedf6">Challenge:</strong> {op['challenge']}</div>
                    <div style="font-size:0.76rem;color:#a9abb3;margin-bottom:7px"><strong style="color:#ecedf6">Counter-evidence:</strong> {op['counter_evidence']}</div>
                    <div style="font-size:0.76rem;color:#69daff"><strong>Final Recommendation:</strong> {op['final_recommendation']}</div>
                </div>""", unsafe_allow_html=True)

        with t2:
            warnings = data.get("drug_warnings", [])
            if not warnings:
                st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ No significant drug interactions detected</div></div>', unsafe_allow_html=True)
            else:
                icons = {"critical":"🔴","major":"🟠","moderate":"🟡","minor":"🟢"}
                for w in warnings:
                    icon = icons.get(w["severity"],"⚪")
                    sc = f"sev-{w['severity']}"
                    st.markdown(f"""
                    <div class="std-card">
                        <div class="std-title">{icon} {w['drug_a']} + {w['drug_b']} <span class="{sc}" style="font-size:0.68rem;margin-left:6px">{w['severity'].upper()}</span></div>
                        <div class="std-text">{w['recommendation']}</div>
                    </div>""", unsafe_allow_html=True)

        with t3:
            for r in data.get("risk_scores", []):
                score = r["score"]
                rc = "#ff716c" if score >= 70 else ("#f59e0b" if score >= 40 else "#69daff")
                factors = "".join(f'<div class="risk-factor">{f}</div>' for f in r["factors"])
                st.markdown(f"""
                <div class="risk-card">
                    <div class="risk-hdr">
                        <div class="risk-name">{r['condition']}</div>
                        <div class="risk-pct" style="color:{rc}">{score}%</div>
                    </div>
                    <div class="risk-bar-bg"><div style="width:{score}%;height:100%;border-radius:20px;background:linear-gradient(90deg,{rc}88,{rc})"></div></div>
                    {factors}
                    <div class="risk-rec">{r['recommendation']}</div>
                </div>""", unsafe_allow_html=True)

        with t4:
            soap = data.get("soap_note", {})
            for label, content, emoji in [
                ("S — SUBJECTIVE", soap.get("subjective",""), "🗣️"),
                ("O — OBJECTIVE", soap.get("objective",""), "🔬"),
                ("A — ASSESSMENT", soap.get("assessment",""), "🧠"),
                ("P — PLAN", soap.get("plan",""), "📋"),
            ]:
                st.markdown(f"""
                <div class="soap-card">
                    <div class="soap-label">{emoji} {label}</div>
                    <div class="soap-text">{content}</div>
                </div>""", unsafe_allow_html=True)
            if st.button("📋 Export SOAP Note"):
                st.code(f"S: {soap.get('subjective','')}\nO: {soap.get('objective','')}\nA: {soap.get('assessment','')}\nP: {soap.get('plan','')}", language="text")

        with t5:
            for i, step in enumerate(data.get("reasoning_trace", [])):
                num = f"0{i+1}" if i < 9 else str(i+1)
                st.markdown(f"""
                <div class="trace-card">
                    <div class="trace-num">{num}</div>
                    <div>
                        <div class="trace-agent">{step['agent']}</div>
                        <div class="trace-action">{step['action']}</div>
                        <div class="trace-finding">{step['finding']}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            if data.get("rag_citations"):
                st.markdown('<div style="font-size:0.6rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#69daff;margin:14px 0 8px">📚 RAG Citations</div>', unsafe_allow_html=True)
                for i, c in enumerate(data["rag_citations"]):
                    st.markdown(f'<div class="citation-card"><strong style="color:#69daff">Guideline {i+1}</strong><br><br>{c}</div>', unsafe_allow_html=True)

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with right_col:
    st.markdown("""
    <div class="right-panel-box">
        <div class="rp-title">Recent Analyses <span style="font-size:16px;color:#a9abb3;cursor:pointer">🕐</span></div>
    """, unsafe_allow_html=True)

    history = [
        ("8821","2h ago","Jane Doe — Acute Respiratory Distress","t-crit","Critical","t-cat","Pulmonary"),
        ("8819","Yesterday","John Smith — Post-Op Hypertension","t-stable","Stable","t-cat","Cardio"),
        ("8814","2d ago","Maria Garcia — T2 Diabetes Follow-up","t-routine","Routine","t-cat","Endo"),
        ("8801","3d ago","Aiden Patel — Asthma Exacerbation","t-urgent","Urgent","t-cat","Pediatric"),
        ("8795","4d ago","Eleanor Voss — Lupus Flare","t-crit","Critical","t-cat","Rheumatology"),
    ]
    for case, time, name, stag, slabel, ctag, clabel in history:
        st.markdown(f"""
        <div class="history-card">
            <div class="h-meta"><span class="h-case">Case #{case}</span><span class="h-time">{time}</span></div>
            <div class="h-name">{name}</div>
            <div class="h-tags"><span class="{stag}">{slabel}</span><span class="{ctag}">{clabel}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
        <div class="copilot-pro-box">
            <div class="cp-label">Copilot Pro</div>
            <div class="cp-text">Multi-agent clinical reasoning is active. Analyzing records from 4 medical registries.</div>
        </div>
    </div>""", unsafe_allow_html=True)

# Footer
if data:
    st.markdown(f"""
    <div style="margin-top:1rem;padding-top:0.75rem;border-top:1px solid rgba(255,255,255,0.05);font-size:0.68rem;color:#45484f;font-family:'Inter',sans-serif;display:flex;justify-content:space-between;">
        <span>MediCopilot v1.0 · {data['generated_at'][:10]} UTC</span>
        <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents</span>
    </div>""", unsafe_allow_html=True)