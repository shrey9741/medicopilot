"""
MediCopilot — Streamlit Demo UI
Premium clinical interface with light/dark toggle.
"""
import streamlit as st
import httpx
import os

st.set_page_config(
    page_title="MediCopilot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = os.getenv("API_BASE", "https://medicopilot.onrender.com")

# ── Theme toggle (must be before CSS) ────────────────────────────────────────
with st.sidebar:
    light_mode = st.toggle("☀️ Light mode", value=False)

if light_mode:
    # ── Light theme variables ──
    BG          = "#f4f6f9"
    BG2         = "#ffffff"
    BG3         = "#eef1f6"
    BORDER      = "#dde3ed"
    BORDER2     = "#c8d0df"
    TEXT        = "#1a2035"
    TEXT2       = "#4a5568"
    TEXT3       = "#7a8ba0"
    ACCENT      = "#1a5fa8"
    ACCENT2     = "#2980d4"
    ACCENT_GLOW = "rgba(26,95,168,0.12)"
    TAB_BG      = "#ffffff"
    TAB_SEL     = "#eef4ff"
    FOOTER_TEXT = "#9aabbf"
    HERO_GLOW   = "rgba(26,95,168,0.06)"
    CARD_HOVER  = "#1a5fa8"
    TRACE_NUM_BG= "#eef4ff"
    CITE_BG     = "#f8fafd"
    RISK_BG     = "#eef4ff"
    SOAP_BG     = "#f8fafd"
    PATIENT_NAME= "#1a2035"
    SECTION_CLR = "#1a2035"
    PROG_BG     = "#dde8f5"
else:
    # ── Dark theme variables ──
    BG          = "#0a0f1e"
    BG2         = "#0d1425"
    BG3         = "#131d35"
    BORDER      = "#1e2d4a"
    BORDER2     = "#2a3d5a"
    TEXT        = "#e2e8f0"
    TEXT2       = "#94a3b8"
    TEXT3       = "#64748b"
    ACCENT      = "#1a6b9a"
    ACCENT2     = "#38bdf8"
    ACCENT_GLOW = "rgba(26,107,154,0.15)"
    TAB_BG      = "#0d1425"
    TAB_SEL     = "#131d35"
    FOOTER_TEXT = "#334155"
    HERO_GLOW   = "rgba(26,107,154,0.08)"
    CARD_HOVER  = "#2a4a6a"
    TRACE_NUM_BG= "#131d35"
    CITE_BG     = "#0a0f1e"
    RISK_BG     = "#131d35"
    SOAP_BG     = "#0d1425"
    PATIENT_NAME= "#ffffff"
    SECTION_CLR = "#ffffff"
    PROG_BG     = "#1e2d4a"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, .stApp {{
    background: {BG} !important;
    color: {TEXT} !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: background 0.3s ease, color 0.3s ease;
}}

#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 2rem 2.5rem !important; max-width: 1400px !important; }}

[data-testid="stSidebar"] {{
    background: {BG2} !important;
    border-right: 1px solid {BORDER} !important;
    transition: background 0.3s ease;
}}
[data-testid="stSidebar"] * {{ color: {TEXT} !important; }}
[data-testid="stSidebar"] .stSelectbox > div > div {{
    background: {BG3} !important;
    border: 1px solid {BORDER} !important;
    color: {TEXT} !important;
    border-radius: 8px !important;
}}

.logo-area {{ padding: 1.5rem 0 1rem; border-bottom: 1px solid {BORDER}; margin-bottom: 1.5rem; }}
.logo-title {{ font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: {TEXT} !important; letter-spacing: -0.5px; }}
.logo-sub {{ font-size: 0.75rem; color: {ACCENT} !important; letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; font-weight: 600; }}
.patient-label {{ font-size: 0.68rem; letter-spacing: 2px; text-transform: uppercase; color: {ACCENT} !important; margin-bottom: 8px; font-weight: 600; }}

.stButton > button {{
    background: linear-gradient(135deg, {ACCENT} 0%, #0a3d5c 100%) !important;
    color: #ffffff !important; border: none !important; border-radius: 8px !important;
    padding: 0.7rem 1.5rem !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.875rem !important; letter-spacing: 0.3px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 8px {ACCENT_GLOW} !important;
}}
.stButton > button:hover {{ transform: translateY(-1px) !important; box-shadow: 0 4px 16px {ACCENT_GLOW} !important; }}

.agent-pill {{ display: inline-block; background: {BG3}; border: 1px solid {BORDER}; border-radius: 20px; padding: 3px 10px; font-size: 0.68rem; color: {ACCENT} !important; margin: 2px; font-family: 'DM Mono', monospace; font-weight: 500; }}

.main-hero {{
    background: {BG2};
    border: 1px solid {BORDER};
    border-top: 3px solid {ACCENT};
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}}
.main-hero::before {{
    content: '';
    position: absolute;
    top: -40%;
    right: -5%;
    width: 350px;
    height: 350px;
    background: radial-gradient(circle, {HERO_GLOW} 0%, transparent 70%);
    pointer-events: none;
}}
.hero-eyebrow {{ font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: {ACCENT}; font-weight: 600; margin-bottom: 8px; }}
.hero-title {{ font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700; color: {TEXT}; letter-spacing: -1px; line-height: 1.2; }}
.hero-title span {{ color: {ACCENT}; font-style: italic; }}
.hero-sub {{ font-size: 0.85rem; color: {TEXT2}; margin-top: 6px; max-width: 500px; line-height: 1.6; }}
.hero-badges {{ margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }}
.badge {{ background: {BG3}; border: 1px solid {BORDER}; border-radius: 6px; padding: 4px 12px; font-size: 0.68rem; color: {ACCENT}; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; font-weight: 500; }}

.step-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem; }}
.step-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 10px; padding: 1.2rem 1.5rem; transition: border-color 0.2s; }}
.step-card:hover {{ border-color: {ACCENT}; }}
.step-num {{ font-family: 'DM Mono', monospace; font-size: 0.65rem; color: {ACCENT}; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; font-weight: 500; }}
.step-text {{ font-size: 0.85rem; color: {TEXT2}; }}

.anomaly-critical {{ background: {"#fff5f5" if light_mode else "linear-gradient(135deg,#1a0a0a,#2d0f0f)"}; border: 1px solid #ef4444; border-left: 4px solid #ef4444; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }}
.anomaly-urgent {{ background: {"#fffbeb" if light_mode else "linear-gradient(135deg,#1a1200,#2d1f00)"}; border: 1px solid #f59e0b; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }}
.anomaly-warning {{ background: {"#fffbeb" if light_mode else "linear-gradient(135deg,#1a1200,#2d1f00)"}; border: 1px solid #fbbf24; border-left: 4px solid #fbbf24; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }}
.anomaly-normal {{ background: {"#f0fdf4" if light_mode else "linear-gradient(135deg,#001a0f,#002d1a)"}; border: 1px solid #10b981; border-left: 4px solid #10b981; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }}
.anomaly-title {{ font-weight: 700; font-size: 0.875rem; margin-bottom: 6px; color: {TEXT}; }}
.anomaly-item {{ font-size: 0.8rem; color: {TEXT2}; margin: 3px 0 3px 12px; }}

.patient-summary {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }}
.patient-name {{ font-family: 'Playfair Display', serif; font-size: 1.4rem; color: {PATIENT_NAME}; margin-bottom: 6px; }}
.patient-desc {{ font-size: 0.85rem; color: {TEXT3}; line-height: 1.6; }}

.stTabs [data-baseweb="tab-list"] {{ background: {TAB_BG} !important; border-radius: 10px !important; padding: 4px !important; border: 1px solid {BORDER} !important; gap: 4px !important; }}
.stTabs [data-baseweb="tab"] {{ background: transparent !important; color: {TEXT3} !important; border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; padding: 8px 16px !important; border: none !important; }}
.stTabs [aria-selected="true"] {{ background: {TAB_SEL} !important; color: {TEXT} !important; border: 1px solid {BORDER} !important; }}
.stTabs [data-baseweb="tab-panel"] {{ background: transparent !important; padding: 1rem 0 !important; }}

.dx-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; transition: border-color 0.2s; }}
.dx-card:hover {{ border-color: {CARD_HOVER}; }}
.dx-rank {{ font-family: 'DM Mono', monospace; font-size: 0.62rem; color: {TEXT3}; margin-bottom: 4px; letter-spacing: 1.5px; text-transform: uppercase; }}
.dx-condition {{ font-family: 'Playfair Display', serif; font-size: 1rem; font-weight: 700; color: {TEXT}; margin-bottom: 6px; }}
.dx-reasoning {{ font-size: 0.8rem; color: {TEXT2}; line-height: 1.6; }}
.dx-meta {{ display: flex; gap: 10px; align-items: center; margin-top: 12px; }}
.tier-critical {{ background: {"#fff5f5" if light_mode else "#2d0f0f"}; color: #ef4444; border: 1px solid #ef4444; border-radius: 4px; padding: 2px 10px; font-size: 0.68rem; font-weight: 700; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }}
.tier-high {{ background: {"#fff7ed" if light_mode else "#2d1500"}; color: #f97316; border: 1px solid #f97316; border-radius: 4px; padding: 2px 10px; font-size: 0.68rem; font-weight: 700; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }}
.tier-moderate {{ background: {"#fffbeb" if light_mode else "#2d2000"}; color: #f59e0b; border: 1px solid #f59e0b; border-radius: 4px; padding: 2px 10px; font-size: 0.68rem; font-weight: 700; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }}
.tier-low {{ background: {"#f0fdf4" if light_mode else "#002d1a"}; color: #10b981; border: 1px solid #10b981; border-radius: 4px; padding: 2px 10px; font-size: 0.68rem; font-weight: 700; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }}
.conf-bar-bg {{ background: {PROG_BG}; border-radius: 20px; height: 5px; flex: 1; overflow: hidden; }}
.conf-bar-fill {{ height: 100%; border-radius: 20px; background: linear-gradient(90deg, {ACCENT}, {ACCENT2}); }}
.conf-label {{ font-family: 'DM Mono', monospace; font-size: 0.75rem; color: {ACCENT}; min-width: 36px; font-weight: 500; }}

.drug-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; }}
.drug-pair {{ font-size: 0.88rem; font-weight: 600; color: {TEXT}; margin-bottom: 8px; }}
.drug-rec {{ font-size: 0.8rem; color: {TEXT2}; line-height: 1.6; padding: 8px 12px; background: {BG3}; border-radius: 6px; border-left: 2px solid {ACCENT}; }}
.sev-critical {{ color: #ef4444; font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px; }}
.sev-major {{ color: #f97316; font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px; }}
.sev-moderate {{ color: #f59e0b; font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px; }}
.sev-minor {{ color: #10b981; font-family: 'DM Mono', monospace; font-size: 0.68rem; font-weight: 700; letter-spacing: 0.5px; }}

.risk-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.5rem; margin-bottom: 10px; }}
.risk-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }}
.risk-name {{ font-family: 'Playfair Display', serif; font-size: 0.95rem; font-weight: 700; color: {TEXT}; }}
.risk-pct {{ font-family: 'DM Mono', monospace; font-size: 1.3rem; font-weight: 700; }}
.risk-bar-bg {{ background: {PROG_BG}; border-radius: 20px; height: 6px; margin-bottom: 12px; overflow: hidden; }}
.risk-factor {{ font-size: 0.78rem; color: {TEXT2}; margin: 4px 0; padding-left: 14px; position: relative; }}
.risk-factor::before {{ content: "–"; position: absolute; left: 2px; color: {ACCENT}; }}
.risk-rec {{ font-size: 0.78rem; color: {ACCENT}; margin-top: 10px; padding: 8px 12px; background: {RISK_BG}; border-radius: 6px; border-left: 2px solid {ACCENT}; line-height: 1.5; }}

.soap-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.5rem; margin-bottom: 12px; }}
.soap-label {{ font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 3px; text-transform: uppercase; color: {ACCENT}; margin-bottom: 10px; font-weight: 600; }}
.soap-content {{ font-size: 0.85rem; color: {TEXT2}; line-height: 1.8; }}

.trace-card {{ background: {BG2}; border: 1px solid {BORDER}; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 8px; display: grid; grid-template-columns: auto 1fr; gap: 14px; align-items: start; transition: border-color 0.2s; }}
.trace-card:hover {{ border-color: {ACCENT}; }}
.trace-num {{ font-family: 'DM Mono', monospace; font-size: 0.7rem; color: {ACCENT}; background: {TRACE_NUM_BG}; border: 1px solid {BORDER}; border-radius: 6px; padding: 4px 8px; font-weight: 600; min-width: 32px; text-align: center; }}
.trace-agent {{ font-size: 0.85rem; font-weight: 600; color: {TEXT}; margin-bottom: 4px; }}
.trace-action {{ font-size: 0.76rem; color: {TEXT3}; }}
.trace-finding {{ font-size: 0.76rem; color: {ACCENT}; margin-top: 4px; font-style: italic; }}

.opinion-card {{ background: {BG2}; border: 1px solid {"#86efac" if light_mode else "#2a4a2a"}; border-left: 3px solid #10b981; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }}
.opinion-label {{ font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 3px; color: #10b981; text-transform: uppercase; margin-bottom: 12px; font-weight: 600; }}
.opinion-body {{ font-size: 0.82rem; color: {TEXT2}; margin-bottom: 8px; line-height: 1.6; }}
.opinion-final {{ font-size: 0.82rem; color: #10b981; margin-top: 10px; padding: 8px 12px; background: {"#f0fdf4" if light_mode else "#001a0f"}; border-radius: 6px; line-height: 1.5; }}

.section-header {{ font-family: 'Playfair Display', serif; font-size: 1.05rem; color: {SECTION_CLR}; margin-bottom: 1rem; padding-bottom: 10px; border-bottom: 1px solid {BORDER}; display: flex; align-items: center; gap: 8px; }}

.citation-card {{ background: {CITE_BG}; border: 1px solid {BORDER}; border-left: 2px solid {ACCENT}; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; font-size: 0.78rem; color: {TEXT2}; font-family: 'DM Mono', monospace; line-height: 1.7; }}

.footer-bar {{ margin-top: 2rem; padding-top: 1rem; border-top: 1px solid {BORDER}; font-size: 0.7rem; color: {FOOTER_TEXT}; font-family: 'DM Mono', monospace; display: flex; justify-content: space-between; align-items: center; }}

hr {{ border-color: {BORDER} !important; }}
</style>
""", unsafe_allow_html=True)


# ── Sidebar (rest) ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class="logo-area">
        <div class="logo-title">🏥 MediCopilot</div>
        <div class="logo-sub">AI Clinical Copilot</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="patient-label">Select Patient</div>', unsafe_allow_html=True)
    patient_options = {
        "P001 — John Doe (62M, Diabetes + HTN + CKD)": "P001",
        "P002 — Sarah Chen (45F, AFib + Hypothyroidism)": "P002",
        "P003 — Marcus Johnson (71M, COPD + Heart Failure)": "P003",
    }
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Generate Briefing", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="patient-label">Active Agents</div>', unsafe_allow_html=True)
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    pills_html = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
    st.markdown(pills_html, unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-hero">
    <div class="hero-eyebrow">Pre-Visit Clinical Intelligence System</div>
    <div class="hero-title">Medi<span>Copilot</span></div>
    <div class="hero-sub">AI-powered briefing system that reads patient history, flags risks, checks drug interactions, and generates SOAP notes — before the doctor walks in.</div>
    <div class="hero-badges">
        <span class="badge">MULTI-AGENT · 9 SPECIALISTS</span>
        <span class="badge">RAG · FAISS</span>
        <span class="badge">FHIR R4 READY</span>
        <span class="badge">GROQ · LLAMA 3.1</span>
        <span class="badge">SOAP NOTES</span>
        <span class="badge">A2A · PROMPT OPINION</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not run_btn:
    st.markdown("""
    <div class="step-grid">
        <div class="step-card"><div class="step-num">Step 01</div><div class="step-text">Select a patient from the sidebar</div></div>
        <div class="step-card"><div class="step-num">Step 02</div><div class="step-text">Click Generate Briefing to run all 9 agents</div></div>
        <div class="step-card"><div class="step-num">Step 03</div><div class="step-text">Review diagnosis, drug safety, SOAP note and trace</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── API Call ──────────────────────────────────────────────────────────────────
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
        st.error("Cannot connect to API backend.")
        st.stop()
    except Exception as e:
        st.error(f"API error: {e}")
        st.stop()


# ── Anomaly Banner ────────────────────────────────────────────────────────────
anomaly = data["anomaly_flag"]
level = anomaly["level"]
level_emoji = {"CRITICAL": "🚨", "URGENT": "⚠️", "WARNING": "🔶", "NORMAL": "✅"}.get(level, "ℹ️")

if anomaly["triggered"]:
    items = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
    st.markdown(f'<div class="anomaly-{level.lower()}"><div class="anomaly-title">{level_emoji} {level} — Vital Anomaly Detected</div>{items}</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ All vitals within acceptable ranges</div></div>', unsafe_allow_html=True)


# ── Patient Summary ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="patient-summary">
    <div class="patient-name">{data['patient_name']}</div>
    <div class="patient-desc">{data['summary']}</div>
</div>
""", unsafe_allow_html=True)

if data.get("memory_trend"):
    with st.expander("📈 Patient Memory Trends"):
        st.code(data["memory_trend"], language="text")


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔬 Diagnosis", "💊 Drug Safety", "📊 Risk Scores", "📝 SOAP Note", "🔍 Reasoning Trace"
])

with tab1:
    st.markdown('<div class="section-header">Differential Diagnosis</div>', unsafe_allow_html=True)
    for i, dx in enumerate(data["diagnoses"]):
        tier = dx["tier"]
        conf = dx["confidence"]
        st.markdown(f"""
        <div class="dx-card">
            <div class="dx-rank">Diagnosis {i+1:02d}</div>
            <div class="dx-condition">{dx['condition']}</div>
            <div class="dx-reasoning">{dx['reasoning']}</div>
            <div class="dx-meta">
                <span class="tier-{tier}">{tier.upper()}</span>
                <div class="conf-bar-bg"><div class="conf-bar-fill" style="width:{conf}%"></div></div>
                <span class="conf-label">{conf}%</span>
            </div>
        </div>""", unsafe_allow_html=True)

    if data.get("second_opinion"):
        op = data["second_opinion"]
        st.markdown(f"""
        <div class="opinion-card">
            <div class="opinion-label">Second Opinion Review</div>
            <div class="opinion-body"><strong>Challenge:</strong> {op['challenge']}</div>
            <div class="opinion-body"><strong>Counter-evidence:</strong> {op['counter_evidence']}</div>
            <div class="opinion-final">✓ Final Recommendation: {op['final_recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Drug Interaction Matrix</div>', unsafe_allow_html=True)
    warnings = data["drug_warnings"]
    if not warnings:
        st.markdown('<div class="anomaly-normal"><div class="anomaly-title">✅ No significant drug interactions detected</div></div>', unsafe_allow_html=True)
    else:
        sev_icons = {"critical": "🔴", "major": "🟠", "moderate": "🟡", "minor": "🟢"}
        for w in warnings:
            icon = sev_icons.get(w["severity"], "⚪")
            st.markdown(f"""
            <div class="drug-card">
                <div class="drug-pair">{icon} {w['drug_a']} <span style="opacity:0.4">+</span> {w['drug_b']} &nbsp;<span class="sev-{w['severity']}">{w['severity'].upper()}</span></div>
                <div class="drug-rec">{w['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Risk Score Assessment</div>', unsafe_allow_html=True)
    for r in data["risk_scores"]:
        score = r["score"]
        risk_color = "#ef4444" if score >= 70 else ("#f59e0b" if score >= 40 else "#10b981")
        factors_html = "".join(f'<div class="risk-factor">{f}</div>' for f in r["factors"])
        st.markdown(f"""
        <div class="risk-card">
            <div class="risk-header">
                <div class="risk-name">{r['condition']}</div>
                <div class="risk-pct" style="color:{risk_color}">{score}%</div>
            </div>
            <div class="risk-bar-bg"><div style="width:{score}%;height:100%;border-radius:20px;background:{risk_color}"></div></div>
            {factors_html}
            <div class="risk-rec">{r['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">SOAP Clinical Note</div>', unsafe_allow_html=True)
    soap = data["soap_note"]
    for label, content, emoji in [
        ("S — SUBJECTIVE", soap["subjective"], "🗣️"),
        ("O — OBJECTIVE",  soap["objective"],  "🔬"),
        ("A — ASSESSMENT", soap["assessment"], "🧠"),
        ("P — PLAN",       soap["plan"],       "📋"),
    ]:
        st.markdown(f"""
        <div class="soap-card">
            <div class="soap-label">{emoji} {label}</div>
            <div class="soap-content">{content}</div>
        </div>""", unsafe_allow_html=True)

    if st.button("📋 Export SOAP Note"):
        soap_text = f"SUBJECTIVE:\n{soap['subjective']}\n\nOBJECTIVE:\n{soap['objective']}\n\nASSESSMENT:\n{soap['assessment']}\n\nPLAN:\n{soap['plan']}"
        st.code(soap_text, language="text")

with tab5:
    st.markdown('<div class="section-header">Agent Reasoning Trace</div>', unsafe_allow_html=True)
    for i, step in enumerate(data["reasoning_trace"]):
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
        st.markdown('<div class="section-header" style="margin-top:1.5rem">📚 RAG Citations</div>', unsafe_allow_html=True)
        for i, citation in enumerate(data["rag_citations"]):
            st.markdown(f'<div class="citation-card"><strong style="color:{ACCENT}">Guideline {i+1}</strong><br><br>{citation}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    <span>MediCopilot v1.0 · {data['generated_at'][:10]}</span>
    <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents · A2A</span>
</div>
""", unsafe_allow_html=True)