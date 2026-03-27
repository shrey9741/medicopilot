"""
MediCopilot — Streamlit UI
Design: "The Clinical Luminary" — cinematic, editorial, glassmorphic dark UI.
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
@import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200;300;400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

.material-symbols-outlined {
    font-family: 'Material Symbols Outlined';
    font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
    vertical-align: middle;
    font-size: 20px;
}

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0b0e14 !important;
    color: #ecedf6 !important;
    font-family: 'Inter', sans-serif !important;
    overflow: hidden;
}

#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
[data-testid="stSidebar"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── LAYOUT SHELL ── */
.app-shell {
    display: flex;
    height: 100vh;
    width: 100%;
    overflow: hidden;
    background: #0b0e14;
}

/* ── LEFT ICON NAV ── */
.icon-nav {
    width: 64px;
    background: #161a21;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px 0;
    gap: 8px;
    border-right: 1px solid rgba(255,255,255,0.04);
    flex-shrink: 0;
    z-index: 50;
}
.nav-logo {
    width: 38px; height: 38px;
    background: #69daff;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 16px;
    color: #004a5d;
    font-size: 20px;
}
.nav-item {
    width: 40px; height: 40px;
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    color: #a9abb3;
    cursor: pointer;
    transition: all 0.2s;
    font-size: 20px;
}
.nav-item:hover { background: #282c36; color: #ecedf6; }
.nav-item.active {
    background: rgba(40, 44, 54, 0.5);
    color: #69daff;
    border-left: 3px solid #69daff;
    border-radius: 0 12px 12px 0;
    width: 43px;
    margin-left: -3px;
    padding-left: 3px;
}
.nav-bottom { margin-top: auto; display: flex; flex-direction: column; gap: 8px; align-items: center; }

/* ── MAIN CONTENT ── */
.main-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    min-width: 0;
}

/* ── TOP NAV BAR ── */
.top-nav {
    background: #161a21;
    border-bottom: 1px solid rgba(255,255,255,0.04);
    padding: 0 24px;
    height: 56px;
    display: flex;
    align-items: center;
    gap: 28px;
    flex-shrink: 0;
}
.top-nav-tab {
    font-size: 0.85rem;
    font-weight: 500;
    color: #a9abb3;
    cursor: pointer;
    padding: 4px 0;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
}
.top-nav-tab.active { color: #69daff; border-bottom-color: #69daff; }
.top-nav-tab:hover { color: #ecedf6; }
.top-nav-right { margin-left: auto; display: flex; align-items: center; gap: 12px; }
.ai-badge {
    display: flex; align-items: center; gap: 6px;
    background: rgba(105, 218, 255, 0.08);
    border: 1px solid rgba(105, 218, 255, 0.2);
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.7rem;
    font-weight: 700;
    color: #69daff;
    letter-spacing: 0.05em;
    font-family: 'Inter', sans-serif;
}
.ai-dot { width: 6px; height: 6px; background: #69daff; border-radius: 50%; animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.4;} }

/* ── THREE PANEL LAYOUT ── */
.panels {
    flex: 1;
    display: flex;
    overflow: hidden;
    min-height: 0;
}

/* ── LEFT PANEL ── */
.left-panel {
    width: 280px;
    flex-shrink: 0;
    background: #0b0e14;
    display: flex;
    flex-direction: column;
    padding: 24px 20px;
    border-right: 1px solid rgba(255,255,255,0.04);
    overflow-y: auto;
}
.panel-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.1rem;
    font-weight: 800;
    color: #ecedf6;
    margin-bottom: 16px;
    display: flex; align-items: center; gap: 10px;
}
.model-badge {
    display: flex; align-items: center; gap: 5px;
    background: rgba(105, 218, 255, 0.08);
    border: 1px solid rgba(105, 218, 255, 0.2);
    border-radius: 20px;
    padding: 3px 8px;
    font-size: 0.65rem;
    font-weight: 700;
    color: #69daff;
    letter-spacing: 0.05em;
}

/* Patient select */
.patient-select-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #a9abb3;
    margin-bottom: 8px;
}
.stSelectbox > div > div {
    background: #10131a !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #ecedf6 !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.82rem !important;
}
.stSelectbox > div > div:focus-within {
    border-color: rgba(105,218,255,0.4) !important;
    box-shadow: 0 0 0 3px rgba(105,218,255,0.08) !important;
}

/* Run button */
.stButton > button {
    background: linear-gradient(135deg, #69daff 0%, #17c0fd 100%) !important;
    color: #004a5d !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 1.5rem !important;
    font-family: 'Manrope', sans-serif !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 20px rgba(105,218,255,0.25), inset 0 1px 1px rgba(255,255,255,0.2) !important;
    width: 100%;
}
.stButton > button:hover {
    box-shadow: 0 6px 28px rgba(105,218,255,0.4), inset 0 1px 1px rgba(255,255,255,0.2) !important;
    transform: translateY(-1px) !important;
}

/* Agent pills */
.agents-grid { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.agent-pill {
    background: #1c2028;
    border-radius: 8px;
    padding: 4px 10px;
    font-size: 0.68rem;
    font-weight: 600;
    color: #17c0fd;
    font-family: 'Inter', sans-serif;
    letter-spacing: 0.03em;
}

/* ── CENTER PANEL ── */
.center-panel {
    flex: 1;
    min-width: 0;
    overflow-y: auto;
    padding: 24px;
    background: #0b0e14;
}

/* Tab bar */
.tab-bar {
    display: flex; align-items: center; gap: 4px;
    margin-bottom: 20px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    padding-bottom: 0;
}
.ctab {
    font-size: 0.82rem; font-weight: 500;
    color: #a9abb3; cursor: pointer;
    padding: 8px 16px;
    border-bottom: 2px solid transparent;
    transition: all 0.2s;
    font-family: 'Inter', sans-serif;
    border-radius: 0;
    white-space: nowrap;
}
.ctab.active { color: #69daff; border-bottom-color: #69daff; }
.ctab:hover { color: #ecedf6; }
.thinking-btn {
    margin-left: auto;
    display: flex; align-items: center; gap: 6px;
    background: #1c2028;
    border-radius: 20px;
    padding: 5px 12px;
    font-size: 0.68rem; font-weight: 700;
    color: #a9abb3;
    font-family: 'Inter', sans-serif;
}

/* Glass card */
.glass-card {
    background: rgba(34, 38, 47, 0.4);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(105,218,255,0.15);
    border-radius: 16px;
    padding: 28px;
    margin-bottom: 16px;
    box-shadow: 0 20px 40px rgba(0, 209, 255, 0.06);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: -40px; right: -40px;
    width: 120px; height: 120px;
    background: rgba(105,218,255,0.04);
    filter: blur(30px);
    border-radius: 50%;
    pointer-events: none;
}

.card-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: 20px; }
.card-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1.1rem; font-weight: 800;
    color: #ecedf6;
    display: flex; align-items: center; gap: 10px;
}
.conf-badge {
    background: rgba(105,218,255,0.1);
    border: 1px solid rgba(105,218,255,0.2);
    border-radius: 20px;
    padding: 2px 8px;
    font-size: 0.65rem; font-weight: 900;
    color: #69daff; letter-spacing: 0.08em;
}
.card-sub { font-size: 0.78rem; color: #a9abb3; margin-top: 4px; }

/* Diagnosis inner card */
.dx-inner {
    background: rgba(0,0,0,0.3);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 14px;
}
.dx-label {
    font-size: 0.65rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #17c0fd; margin-bottom: 8px;
}
.dx-name {
    font-family: 'Manrope', sans-serif;
    font-size: 1.5rem; font-weight: 700;
    color: #ecedf6; line-height: 1.2;
    margin-bottom: 8px;
}
.dx-reasoning { font-size: 0.8rem; color: #a9abb3; line-height: 1.6; }

/* Two col grid */
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 14px; }
.inner-box {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 16px;
}
.inner-box-label {
    font-size: 0.6rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #a9abb3; margin-bottom: 10px;
}
.inner-box-item {
    display: flex; align-items: center; gap: 8px;
    font-size: 0.82rem; color: #ecedf6; margin-bottom: 6px;
}
.dot { width: 6px; height: 6px; border-radius: 50%; background: #17c0fd; flex-shrink: 0; }
.critical-item { color: #ff716c; }
.info-item { color: #69daff; }

/* Drug conflict bar */
.drug-conflict-bar {
    background: rgba(28, 32, 40, 0.5);
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 14px;
}
.conflict-icon {
    width: 40px; height: 40px;
    background: #006688;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    color: #17c0fd; flex-shrink: 0;
}
.conflict-info { flex: 1; margin-left: 12px; }
.conflict-title { font-size: 0.82rem; font-weight: 700; color: #ecedf6; }
.conflict-sub { font-size: 0.7rem; color: #a9abb3; margin-top: 2px; }
.severity-ring {
    width: 48px; height: 48px;
    position: relative;
    flex-shrink: 0;
}
.severity-ring svg { width: 100%; height: 100%; transform: rotate(-90deg); }
.severity-label {
    position: absolute; top: 50%; left: 50%;
    transform: translate(-50%, -50%);
    font-size: 0.6rem; font-weight: 900;
    color: #ff716c;
}

/* Anomaly banner */
.anomaly-banner {
    border-radius: 12px;
    padding: 14px 18px;
    margin-bottom: 16px;
    display: flex; align-items: flex-start; gap: 12px;
}
.anomaly-urgent { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.3); border-left: 3px solid #f59e0b; }
.anomaly-critical { background: rgba(255,113,108,0.08); border: 1px solid rgba(255,113,108,0.3); border-left: 3px solid #ff716c; }
.anomaly-normal { background: rgba(105,218,255,0.04); border: 1px solid rgba(105,218,255,0.15); border-left: 3px solid #69daff; }
.anomaly-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
.anomaly-title { font-size: 0.82rem; font-weight: 700; color: #ecedf6; margin-bottom: 4px; }
.anomaly-item { font-size: 0.75rem; color: #a9abb3; margin: 2px 0; }

/* Patient card */
.patient-card {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
}
.patient-name-lg {
    font-family: 'Manrope', sans-serif;
    font-size: 1.3rem; font-weight: 800;
    color: #ecedf6; margin-bottom: 6px;
}
.patient-summary-text { font-size: 0.78rem; color: #a9abb3; line-height: 1.6; }

/* Risk cards */
.risk-card {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.risk-name { font-size: 0.88rem; font-weight: 600; color: #ecedf6; }
.risk-pct { font-family: 'Manrope', sans-serif; font-size: 1.1rem; font-weight: 800; }
.risk-bar-bg { background: #0b0e14; border-radius: 20px; height: 6px; margin-bottom: 10px; overflow: hidden; }
.risk-factor { font-size: 0.74rem; color: #a9abb3; margin: 3px 0; padding-left: 14px; position: relative; }
.risk-factor::before { content: '→'; position: absolute; left: 0; color: #45484f; }
.risk-rec { font-size: 0.74rem; color: #69daff; margin-top: 10px; padding: 8px 12px; background: rgba(105,218,255,0.05); border-radius: 8px; border-left: 2px solid #69daff; }

/* SOAP */
.soap-card {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 12px;
}
.soap-label {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: #69daff; margin-bottom: 10px;
}
.soap-content { font-size: 0.82rem; color: #a9abb3; line-height: 1.7; }

/* Trace */
.trace-card {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 8px;
    display: flex; gap: 14px; align-items: flex-start;
}
.trace-num {
    font-family: 'Inter', sans-serif;
    font-size: 0.65rem; font-weight: 700;
    color: #69daff;
    background: rgba(105,218,255,0.08);
    border-radius: 6px;
    padding: 3px 7px;
    flex-shrink: 0;
    letter-spacing: 0.05em;
}
.trace-agent { font-size: 0.8rem; font-weight: 600; color: #ecedf6; margin-bottom: 3px; }
.trace-action { font-size: 0.72rem; color: #a9abb3; }
.trace-finding { font-size: 0.72rem; color: #69daff; margin-top: 3px; font-style: italic; }

/* Second opinion */
.opinion-card {
    background: rgba(105,218,255,0.03);
    border: 1px solid rgba(105,218,255,0.15);
    border-radius: 14px;
    padding: 20px;
    margin-top: 12px;
}
.opinion-label {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 0.18em; text-transform: uppercase;
    color: #69daff; margin-bottom: 12px;
}

/* ── RIGHT PANEL ── */
.right-panel {
    width: 264px;
    flex-shrink: 0;
    background: #0b0e14;
    border-left: 1px solid rgba(255,255,255,0.04);
    padding: 24px 16px;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 12px;
}
.panel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.panel-header-title {
    font-family: 'Manrope', sans-serif;
    font-size: 1rem; font-weight: 800; color: #ecedf6;
}

/* History cards */
.history-card {
    background: #10131a;
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 14px;
    cursor: pointer;
    transition: all 0.2s;
}
.history-card:hover { background: #161a21; border-color: rgba(105,218,255,0.15); }
.history-meta { display: flex; justify-content: space-between; margin-bottom: 6px; }
.history-case { font-size: 0.62rem; font-weight: 700; color: #a9abb3; text-transform: uppercase; letter-spacing: 0.08em; }
.history-time { font-size: 0.62rem; color: #a9abb3; }
.history-name { font-size: 0.82rem; font-weight: 600; color: #ecedf6; margin-bottom: 8px; line-height: 1.3; }
.history-tags { display: flex; flex-wrap: wrap; gap: 4px; }
.tag-critical { background: rgba(255,113,108,0.1); color: #ff716c; border-radius: 20px; padding: 2px 8px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; }
.tag-stable { background: rgba(137,165,255,0.1); color: #89a5ff; border-radius: 20px; padding: 2px 8px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; }
.tag-routine { background: rgba(137,165,255,0.1); color: #89a5ff; border-radius: 20px; padding: 2px 8px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; }
.tag-category { background: #1c2028; color: #a9abb3; border-radius: 20px; padding: 2px 8px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; }
.tag-urgent { background: rgba(245,158,11,0.1); color: #f59e0b; border-radius: 20px; padding: 2px 8px; font-size: 0.62rem; font-weight: 700; text-transform: uppercase; }

/* Copilot pro box */
.copilot-pro {
    background: rgba(105,218,255,0.04);
    border: 1px solid rgba(105,218,255,0.18);
    border-radius: 14px;
    padding: 16px;
    margin-top: auto;
}
.copilot-pro-label {
    font-size: 0.62rem; font-weight: 700;
    letter-spacing: 0.15em; text-transform: uppercase;
    color: #69daff; margin-bottom: 8px;
}
.copilot-pro-text { font-size: 0.72rem; color: #a9abb3; line-height: 1.6; }

/* Tier badges */
.tier-critical { background: rgba(255,113,108,0.1); color: #ff716c; border: 1px solid rgba(255,113,108,0.3); border-radius: 6px; padding: 2px 8px; font-size: 0.65rem; font-weight: 700; font-family: 'Inter'; }
.tier-high { background: rgba(249,115,22,0.1); color: #f97316; border: 1px solid rgba(249,115,22,0.3); border-radius: 6px; padding: 2px 8px; font-size: 0.65rem; font-weight: 700; }
.tier-moderate { background: rgba(245,158,11,0.1); color: #f59e0b; border: 1px solid rgba(245,158,11,0.3); border-radius: 6px; padding: 2px 8px; font-size: 0.65rem; font-weight: 700; }
.tier-low { background: rgba(105,218,255,0.08); color: #69daff; border: 1px solid rgba(105,218,255,0.2); border-radius: 6px; padding: 2px 8px; font-size: 0.65rem; font-weight: 700; }
.conf-bar-bg { background: #0b0e14; border-radius: 20px; height: 5px; flex: 1; overflow: hidden; }
.conf-bar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #17c0fd, #69daff); }

/* Drug card */
.drug-card {
    background: #161a21;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 10px;
}
.drug-pair { font-size: 0.85rem; font-weight: 600; color: #ecedf6; margin-bottom: 6px; }
.drug-rec { font-size: 0.75rem; color: #a9abb3; line-height: 1.5; }
.sev-critical { color: #ff716c; } .sev-major { color: #f97316; }
.sev-moderate { color: #f59e0b; } .sev-minor { color: #69daff; }

/* citation */
.citation-card {
    background: #10131a;
    border: 1px solid rgba(255,255,255,0.04);
    border-radius: 10px;
    padding: 12px 14px;
    font-size: 0.74rem;
    color: #a9abb3;
    line-height: 1.6;
    margin-bottom: 8px;
}

/* scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #45484f; border-radius: 10px; }

/* Streamlit overrides */
.stSpinner > div { border-top-color: #69daff !important; }
div[data-testid="stExpander"] > div:first-child {
    background: #161a21 !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-radius: 12px !important;
    color: #a9abb3 !important;
}
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────────────
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "Diagnosis"
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

# ── LAYOUT ────────────────────────────────────────────────────────────────────
st.markdown('<div class="app-shell">', unsafe_allow_html=True)

# Icon Nav
st.markdown("""
<div class="icon-nav">
    <div class="nav-logo"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1;color:#004a5d;font-size:22px">medical_services</span></div>
    <div class="nav-item active"><span class="material-symbols-outlined">dashboard</span></div>
    <div class="nav-item"><span class="material-symbols-outlined">group</span></div>
    <div class="nav-item"><span class="material-symbols-outlined">description</span></div>
    <div class="nav-item"><span class="material-symbols-outlined">medication</span></div>
    <div class="nav-item"><span class="material-symbols-outlined">settings</span></div>
    <div class="nav-bottom">
        <div class="nav-item"><span class="material-symbols-outlined">help_outline</span></div>
        <div class="nav-item"><span class="material-symbols-outlined">logout</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content wrapper
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Top nav
st.markdown("""
<div class="top-nav">
    <span class="top-nav-tab active">RAG</span>
    <span class="top-nav-tab">Multi-Agent</span>
    <span class="top-nav-tab">Drug Safety</span>
    <span class="top-nav-tab">SOAP Notes</span>
    <div class="top-nav-right">
        <div class="ai-badge"><div class="ai-dot"></div>AI CLINICAL COPILOT</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Three-panel area
st.markdown('<div class="panels">', unsafe_allow_html=True)

# ── LEFT PANEL (Streamlit widgets live here) ──────────────────────────────────
left, center, right = st.columns([2.2, 5, 2.1])

with left:
    st.markdown("""
    <div class="left-panel" style="height:calc(100vh - 56px);overflow-y:auto;">
        <div class="panel-title">
            Patient Summary
            <span class="model-badge">⚡ LLAMA 3.1</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="patient-select-label">Select Patient</div>', unsafe_allow_html=True)
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡  Run AI Analysis", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="patient-select-label">Active Agents</div>', unsafe_allow_html=True)
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    pills = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
    st.markdown(f'<div class="agents-grid">{pills}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── CENTER PANEL ──────────────────────────────────────────────────────────────
with center:
    tabs = ["Diagnosis", "Drug Interactions", "Risk Score", "SOAP Notes", "Reasoning"]
    tab_html = '<div class="tab-bar">'
    for t in tabs:
        active = "active" if t == st.session_state.active_tab else ""
        tab_html += f'<span class="ctab {active}">{t}</span>'
    tab_html += '<span class="thinking-btn">● ● ● AI THINKING...</span></div>'
    st.markdown(tab_html, unsafe_allow_html=True)

    # Handle API call
    if run_btn:
        with st.spinner("Running MediCopilot agents..."):
            try:
                response = httpx.post(
                    f"{API_BASE}/invoke",
                    json={"patient_id": patient_id, "sharp_token": "demo", "fhir_token": "demo"},
                    timeout=120.0
                )
                response.raise_for_status()
                st.session_state.data = response.json()
            except httpx.ConnectError:
                st.error("Cannot connect to API backend.")
            except Exception as e:
                st.error(f"API error: {e}")

    data = st.session_state.data

    if not data:
        st.markdown("""
        <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:60vh;gap:16px;opacity:0.4;">
            <span class="material-symbols-outlined" style="font-size:48px;color:#69daff">biotech</span>
            <div style="font-family:'Manrope',sans-serif;font-size:1rem;font-weight:700;color:#ecedf6;">Select a patient and run AI Analysis</div>
            <div style="font-size:0.78rem;color:#a9abb3;">Multi-agent clinical reasoning will appear here</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Anomaly banner
        anomaly = data["anomaly_flag"]
        level = anomaly["level"]
        level_emoji = {"CRITICAL": "🚨", "URGENT": "⚠️", "WARNING": "🔶", "NORMAL": "✅"}.get(level, "ℹ️")
        a_class = f"anomaly-{level.lower()}" if level.lower() in ["critical","urgent","normal","warning"] else "anomaly-normal"
        if anomaly["triggered"]:
            items_html = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
            st.markdown(f"""
            <div class="anomaly-banner {a_class}">
                <div class="anomaly-icon">{level_emoji}</div>
                <div><div class="anomaly-title">{level} — Vital Anomaly Detected</div>{items_html}</div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div class="anomaly-banner anomaly-normal"><div class="anomaly-icon">✅</div><div><div class="anomaly-title">All vitals within acceptable ranges</div></div></div>', unsafe_allow_html=True)

        # Patient summary card
        st.markdown(f"""
        <div class="patient-card">
            <div class="patient-name-lg">{data['patient_name']}</div>
            <div class="patient-summary-text">{data['summary']}</div>
        </div>""", unsafe_allow_html=True)

        # Streamlit tabs
        t1, t2, t3, t4, t5 = st.tabs(["🔬 Diagnosis", "💊 Drug Safety", "📊 Risk Scores", "📝 SOAP Note", "🔍 Reasoning"])

        with t1:
            diagnoses = data.get("diagnoses", [])
            if diagnoses:
                top = diagnoses[0]
                conf = top["confidence"]
                st.markdown(f"""
                <div class="glass-card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Primary Differential <span class="conf-badge">{conf}% CONFIDENCE</span></div>
                            <div class="card-sub">Based on RAG analysis of medical guidelines</div>
                        </div>
                    </div>
                    <div class="dx-inner">
                        <div class="dx-label">Diagnosis</div>
                        <div class="dx-name">{top['condition']}</div>
                        <div class="dx-reasoning">{top['reasoning']}</div>
                    </div>
                """, unsafe_allow_html=True)

                if len(diagnoses) > 1:
                    secondary_items = "".join(f'<div class="inner-box-item"><div class="dot"></div>{d["condition"]}</div>' for d in diagnoses[1:3])
                    warnings = data.get("drug_warnings", [])
                    critical_items = ""
                    if warnings:
                        critical_items = f'<div class="inner-box-item critical-item"><span class="material-symbols-outlined" style="font-size:14px">warning</span>{warnings[0]["drug_a"]} + {warnings[0]["drug_b"]}</div>'
                    if len(warnings) > 1:
                        critical_items += f'<div class="inner-box-item info-item"><span class="material-symbols-outlined" style="font-size:14px">info</span>Monitor: {warnings[1]["drug_b"]}</div>'

                    st.markdown(f"""
                    <div class="two-col">
                        <div class="inner-box">
                            <div class="inner-box-label">Secondary Findings</div>
                            {secondary_items}
                        </div>
                        <div class="inner-box">
                            <div class="inner-box-label">Critical Actions</div>
                            {critical_items or '<div class="inner-box-item info-item">No critical flags</div>'}
                        </div>
                    </div>""", unsafe_allow_html=True)

                if warnings:
                    w = warnings[0]
                    sev = w['severity'].lower()
                    ring_color = "#ff716c" if sev in ["critical","major"] else "#f59e0b"
                    st.markdown(f"""
                    <div class="drug-conflict-bar">
                        <div class="conflict-icon"><span class="material-symbols-outlined" style="font-variation-settings:'FILL' 1">shield_with_heart</span></div>
                        <div class="conflict-info">
                            <div class="conflict-title">Drug-Drug Conflict Detected</div>
                            <div class="conflict-sub">{w['drug_a']} + {w['drug_b']} ({w['severity'].upper()} Risk)</div>
                        </div>
                        <div class="severity-ring">
                            <svg viewBox="0 0 48 48"><circle cx="24" cy="24" r="20" fill="transparent" stroke="#22262f" stroke-width="4"/><circle cx="24" cy="24" r="20" fill="transparent" stroke="{ring_color}" stroke-width="4" stroke-dasharray="125.6" stroke-dashoffset="30"/></svg>
                            <div class="severity-label">{sev[:4].title()}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)

                st.markdown("</div>", unsafe_allow_html=True)

                # Remaining diagnoses
                if len(diagnoses) > 1:
                    st.markdown("<br>", unsafe_allow_html=True)
                    for i, dx in enumerate(diagnoses[1:], 2):
                        tier = dx["tier"]
                        c = dx["confidence"]
                        st.markdown(f"""
                        <div class="drug-card">
                            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px">
                                <div class="drug-pair">{i}. {dx['condition']}</div>
                                <div style="display:flex;align-items:center;gap:8px">
                                    <span class="tier-{tier}">{tier.upper()}</span>
                                    <div class="conf-bar-bg" style="width:80px"><div class="conf-bar-fill" style="width:{c}%"></div></div>
                                    <span style="font-size:0.7rem;color:#69daff;min-width:30px">{c}%</span>
                                </div>
                            </div>
                            <div class="drug-rec">{dx['reasoning']}</div>
                        </div>""", unsafe_allow_html=True)

            if data.get("second_opinion"):
                op = data["second_opinion"]
                st.markdown(f"""
                <div class="opinion-card">
                    <div class="opinion-label">🧐 Second Opinion Analysis</div>
                    <div style="font-size:0.78rem;color:#a9abb3;margin-bottom:8px"><strong style="color:#ecedf6">Challenge:</strong> {op['challenge']}</div>
                    <div style="font-size:0.78rem;color:#a9abb3;margin-bottom:8px"><strong style="color:#ecedf6">Counter-evidence:</strong> {op['counter_evidence']}</div>
                    <div style="font-size:0.78rem;color:#69daff"><strong>Final Recommendation:</strong> {op['final_recommendation']}</div>
                </div>""", unsafe_allow_html=True)

        with t2:
            warnings = data.get("drug_warnings", [])
            if not warnings:
                st.markdown('<div class="anomaly-banner anomaly-normal"><div>✅ No significant drug interactions detected</div></div>', unsafe_allow_html=True)
            else:
                sev_icons = {"critical": "🔴", "major": "🟠", "moderate": "🟡", "minor": "🟢"}
                for w in warnings:
                    icon = sev_icons.get(w["severity"], "⚪")
                    sc = f"sev-{w['severity']}"
                    st.markdown(f"""
                    <div class="drug-card">
                        <div class="drug-pair">{icon} {w['drug_a']} <span style="color:#45484f">+</span> {w['drug_b']} <span class="{sc}" style="font-size:0.68rem;margin-left:6px;font-weight:700">{w['severity'].upper()}</span></div>
                        <div class="drug-rec">{w['recommendation']}</div>
                    </div>""", unsafe_allow_html=True)

        with t3:
            for r in data.get("risk_scores", []):
                score = r["score"]
                rc = "#ff716c" if score >= 70 else ("#f59e0b" if score >= 40 else "#69daff")
                factors = "".join(f'<div class="risk-factor">{f}</div>' for f in r["factors"])
                st.markdown(f"""
                <div class="risk-card">
                    <div class="risk-header">
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
                    <div class="soap-content">{content}</div>
                </div>""", unsafe_allow_html=True)

            if st.button("📋 Export SOAP Note"):
                soap_text = f"S: {soap.get('subjective','')}\nO: {soap.get('objective','')}\nA: {soap.get('assessment','')}\nP: {soap.get('plan','')}"
                st.code(soap_text, language="text")

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
                st.markdown('<div style="font-size:0.68rem;font-weight:700;letter-spacing:0.15em;text-transform:uppercase;color:#69daff;margin:16px 0 8px">📚 RAG Citations</div>', unsafe_allow_html=True)
                for i, c in enumerate(data["rag_citations"]):
                    st.markdown(f'<div class="citation-card"><strong style="color:#69daff">Guideline {i+1}</strong><br><br>{c}</div>', unsafe_allow_html=True)

# ── RIGHT PANEL ───────────────────────────────────────────────────────────────
with right:
    st.markdown("""
    <div class="right-panel" style="height:calc(100vh - 56px);overflow-y:auto;">
        <div class="panel-header">
            <div class="panel-header-title">Recent Analyses</div>
            <span class="material-symbols-outlined" style="color:#a9abb3;cursor:pointer">history</span>
        </div>
    """, unsafe_allow_html=True)

    history_items = [
        ("8821", "2h ago", "Jane Doe — Acute Respiratory Distress", "Critical", "Pulmonary", "tag-critical"),
        ("8819", "Yesterday", "John Smith — Post-Op Hypertension", "Stable", "Cardio", "tag-stable"),
        ("8814", "2d ago", "Maria Garcia — T2 Diabetes Follow-up", "Routine", "Endo", "tag-routine"),
        ("8801", "3d ago", "Aiden Patel — Asthma Exacerbation", "Urgent", "Pediatric", "tag-urgent"),
        ("8795", "4d ago", "Eleanor Voss — Lupus Flare", "Critical", "Rheumatology", "tag-critical"),
    ]
    for case, time, name, status, category, tag_class in history_items:
        st.markdown(f"""
        <div class="history-card">
            <div class="history-meta">
                <span class="history-case">Case #{case}</span>
                <span class="history-time">{time}</span>
            </div>
            <div class="history-name">{name}</div>
            <div class="history-tags">
                <span class="{tag_class}">{status}</span>
                <span class="tag-category">{category}</span>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown("""
        <div class="copilot-pro">
            <div class="copilot-pro-label">Copilot Pro</div>
            <div class="copilot-pro-text">Multi-agent clinical reasoning is active. Analyzing records from 4 medical registries.</div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("</div></div></div>", unsafe_allow_html=True)