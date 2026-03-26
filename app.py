"""
MediCopilot — Streamlit Demo UI
Premium clinical interface — clean white, emerald accents, medical aesthetic.
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

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #f7f8fa !important;
    color: #1a1f2e !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px !important; }

[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #e4e8ef !important; }
[data-testid="stSidebar"] * { color: #1a1f2e !important; }
[data-testid="stSidebar"] .stSelectbox > div > div { background: #f7f8fa !important; border: 1px solid #e4e8ef !important; color: #1a1f2e !important; border-radius: 8px !important; }

.sidebar-logo { padding: 1.2rem 0 1.4rem; border-bottom: 1px solid #e4e8ef; margin-bottom: 1.5rem; }
.sidebar-cross { font-size: 2rem; line-height: 1; color: #2d7a4f; }
.sidebar-title { font-family: 'Libre Baskerville', serif; font-size: 1.3rem; font-weight: 700; color: #0a2e1a !important; margin-top: 6px; letter-spacing: -0.3px; }
.sidebar-sub { font-size: 0.68rem; letter-spacing: 2.5px; text-transform: uppercase; color: #2d7a4f !important; margin-top: 3px; font-weight: 600; }
.sidebar-label { font-size: 0.65rem; letter-spacing: 2px; text-transform: uppercase; color: #8a9bb0 !important; margin-bottom: 8px; font-weight: 600; }

.stButton > button { background: #0a2e1a !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; padding: 0.7rem 1.5rem !important; font-family: 'DM Sans', sans-serif !important; font-weight: 600 !important; font-size: 0.875rem !important; letter-spacing: 0.3px !important; transition: all 0.2s ease !important; }
.stButton > button:hover { background: #2d7a4f !important; transform: translateY(-1px) !important; }

.agent-pill { display: inline-block; background: #f0f7f4; border: 1px solid #c8e6d4; border-radius: 20px; padding: 3px 10px; font-size: 0.68rem; color: #2d7a4f !important; margin: 2px; font-family: 'DM Mono', monospace; font-weight: 500; }

.hero-wrap { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero-wrap::before { content: '+'; position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); font-size: 8rem; color: #e8f5ee; font-family: 'DM Sans', sans-serif; font-weight: 300; line-height: 1; pointer-events: none; }
.hero-eyebrow { font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #2d7a4f; font-weight: 600; margin-bottom: 8px; }
.hero-title { font-family: 'Libre Baskerville', serif; font-size: 2.4rem; font-weight: 700; color: #0a2e1a; letter-spacing: -1px; line-height: 1.15; }
.hero-title em { font-style: italic; color: #2d7a4f; }
.hero-desc { font-size: 0.875rem; color: #6b7a90; margin-top: 8px; max-width: 500px; line-height: 1.6; }
.hero-badges { margin-top: 14px; display: flex; gap: 8px; flex-wrap: wrap; }
.badge { background: #f0f7f4; border: 1px solid #c8e6d4; border-radius: 20px; padding: 4px 12px; font-size: 0.68rem; color: #2d7a4f; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; font-weight: 500; }

.step-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.step-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.2rem 1.5rem; }
.step-num { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #2d7a4f; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; font-weight: 500; }
.step-text { font-size: 0.85rem; color: #6b7a90; }

.anomaly-critical { background: #fff5f5; border: 1px solid #fca5a5; border-left: 4px solid #ef4444; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-urgent { background: #fffbeb; border: 1px solid #fcd34d; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-warning { background: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #fbbf24; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-normal { background: #f0fdf4; border: 1px solid #86efac; border-left: 4px solid #22c55e; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-title { font-weight: 700; font-size: 0.875rem; margin-bottom: 6px; color: #1a1f2e; }
.anomaly-item { font-size: 0.8rem; color: #6b7a90; margin: 3px 0 3px 12px; }

.patient-summary { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
.patient-name { font-family: 'Libre Baskerville', serif; font-size: 1.5rem; color: #0a2e1a; margin-bottom: 6px; }
.patient-desc { font-size: 0.85rem; color: #6b7a90; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { background: #ffffff !important; border-radius: 10px !important; padding: 4px !important; border: 1px solid #e4e8ef !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #6b7a90 !important; border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; padding: 8px 16px !important; border: none !important; }
.stTabs [aria-selected="true"] { background: #f0f7f4 !important; color: #0a2e1a !important; border: 1px solid #c8e6d4 !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding: 1rem 0 !important; }

.dx-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; transition: border-color 0.2s; }
.dx-card:hover { border-color: #2d7a4f; }
.dx-rank { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #8a9bb0; margin-bottom: 4px; letter-spacing: 1px; }
.dx-condition { font-family: 'Libre Baskerville', serif; font-size: 1rem; font-weight: 700; color: #0a2e1a; margin-bottom: 6px; }
.dx-reasoning { font-size: 0.8rem; color: #6b7a90; line-height: 1.6; }
.dx-meta { display: flex; gap: 10px; align-items: center; margin-top: 12px; }
.tier-critical { background: #fff5f5; color: #dc2626; border: 1px solid #fca5a5; border-radius: 6px; padding: 2px 10px; font-size: 0.7rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-high { background: #fff7ed; color: #ea580c; border: 1px solid #fdba74; border-radius: 6px; padding: 2px 10px; font-size: 0.7rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-moderate { background: #fffbeb; color: #d97706; border: 1px solid #fcd34d; border-radius: 6px; padding: 2px 10px; font-size: 0.7rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-low { background: #f0fdf4; color: #16a34a; border: 1px solid #86efac; border-radius: 6px; padding: 2px 10px; font-size: 0.7rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.conf-bar-bg { background: #f0f7f4; border-radius: 20px; height: 6px; flex: 1; overflow: hidden; }
.conf-bar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #2d7a4f, #4ade80); }
.conf-label { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #2d7a4f; min-width: 36px; font-weight: 500; }

.drug-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; }
.drug-pair { font-size: 0.9rem; font-weight: 600; color: #0a2e1a; margin-bottom: 6px; }
.drug-rec { font-size: 0.8rem; color: #6b7a90; line-height: 1.6; margin-top: 6px; padding: 8px 12px; background: #f7f8fa; border-radius: 6px; }
.sev-critical { color: #dc2626; font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 700; }
.sev-major { color: #ea580c; font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 700; }
.sev-moderate { color: #d97706; font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 700; }
.sev-minor { color: #16a34a; font-family: 'DM Mono', monospace; font-size: 0.7rem; font-weight: 700; }

.risk-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.5rem; margin-bottom: 10px; }
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; }
.risk-name { font-family: 'Libre Baskerville', serif; font-size: 0.95rem; font-weight: 700; color: #0a2e1a; }
.risk-pct { font-family: 'DM Mono', monospace; font-size: 1.4rem; font-weight: 700; }
.risk-bar-bg { background: #f0f7f4; border-radius: 20px; height: 8px; margin-bottom: 12px; overflow: hidden; }
.risk-factor { font-size: 0.78rem; color: #6b7a90; margin: 4px 0; padding-left: 14px; position: relative; }
.risk-factor::before { content: 'middot'; position: absolute; left: 4px; color: #2d7a4f; }
.risk-rec { font-size: 0.78rem; color: #2d7a4f; margin-top: 10px; padding: 10px 14px; background: #f0f7f4; border-radius: 8px; border-left: 3px solid #2d7a4f; line-height: 1.5; }

.soap-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 12px; padding: 1.5rem; margin-bottom: 12px; }
.soap-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 3px; text-transform: uppercase; color: #2d7a4f; margin-bottom: 10px; font-weight: 600; }
.soap-content { font-size: 0.85rem; color: #4a5568; line-height: 1.8; }

.trace-card { background: #ffffff; border: 1px solid #e4e8ef; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 8px; display: grid; grid-template-columns: auto 1fr; gap: 14px; align-items: start; }
.trace-num { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #2d7a4f; background: #f0f7f4; border: 1px solid #c8e6d4; border-radius: 6px; padding: 4px 8px; font-weight: 600; min-width: 32px; text-align: center; }
.trace-agent { font-size: 0.85rem; font-weight: 600; color: #0a2e1a; margin-bottom: 4px; }
.trace-action { font-size: 0.76rem; color: #6b7a90; }
.trace-finding { font-size: 0.76rem; color: #2d7a4f; margin-top: 4px; font-style: italic; }

.opinion-card { background: #f0fdf4; border: 1px solid #86efac; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }
.opinion-label { font-family: 'DM Mono', monospace; font-size: 0.62rem; letter-spacing: 3px; color: #16a34a; text-transform: uppercase; margin-bottom: 12px; font-weight: 600; }
.opinion-item { font-size: 0.82rem; color: #374151; margin-bottom: 8px; line-height: 1.6; }
.opinion-final { font-size: 0.82rem; color: #16a34a; font-weight: 600; margin-top: 10px; padding: 10px 14px; background: #dcfce7; border-radius: 8px; line-height: 1.5; }

.section-header { font-family: 'Libre Baskerville', serif; font-size: 1.05rem; font-weight: 700; color: #0a2e1a; margin-bottom: 1rem; padding-bottom: 10px; border-bottom: 2px solid #e4e8ef; }
.citation-card { background: #ffffff; border: 1px solid #e4e8ef; border-left: 3px solid #2d7a4f; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; font-size: 0.78rem; color: #6b7a90; font-family: 'DM Mono', monospace; line-height: 1.7; }
.footer-bar { margin-top: 2.5rem; padding-top: 1rem; border-top: 2px solid #e4e8ef; font-size: 0.7rem; color: #a0aec0; font-family: 'DM Mono', monospace; display: flex; justify-content: space-between; align-items: center; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-cross">✚</div>
        <div class="sidebar-title">MediCopilot</div>
        <div class="sidebar-sub">Clinical AI System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-label">Select Patient</div>', unsafe_allow_html=True)
    patient_options = {
        "P001 — John Doe (62M · Diabetes + HTN + CKD)": "P001",
        "P002 — Sarah Chen (45F · AFib + Hypothyroidism)": "P002",
        "P003 — Marcus Johnson (71M · COPD + Heart Failure)": "P003",
    }
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("✚ Generate Briefing", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">Active Agents</div>', unsafe_allow_html=True)
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    pills_html = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
    st.markdown(pills_html, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="sidebar-label">SHARP Context</div>', unsafe_allow_html=True)
    st.text_input("SHARP Token", value="demo-sharp-token", type="password", label_visibility="collapsed")
    st.text_input("FHIR Token", value="demo-fhir-token", type="password", label_visibility="collapsed")


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">✚ Pre-Visit Clinical Intelligence</div>
    <div class="hero-title">Medi<em>Copilot</em></div>
    <div class="hero-desc">AI-powered briefing system that reads patient history, flags risks, checks drug interactions, and generates SOAP notes — before the doctor walks in.</div>
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
        <div class="step-card">
            <div class="step-num">Step 01</div>
            <div class="step-text">Select a patient from the sidebar panel</div>
        </div>
        <div class="step-card">
            <div class="step-num">Step 02</div>
            <div class="step-text">Click Generate Briefing to run all 9 agents</div>
        </div>
        <div class="step-card">
            <div class="step-num">Step 03</div>
            <div class="step-text">Review diagnosis, drug safety, SOAP note and trace</div>
        </div>
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
        st.error("Cannot connect to API. Make sure the backend is running.")
        st.stop()
    except Exception as e:
        st.error(f"API error: {e}")
        st.stop()


# ── Anomaly Banner ────────────────────────────────────────────────────────────
anomaly = data["anomaly_flag"]
level = anomaly["level"]
level_emoji = {"CRITICAL": "🚨", "URGENT": "⚠️", "WARNING": "🔶", "NORMAL": "✅"}.get(level, "i")

if anomaly["triggered"]:
    items = "".join(f'<div class="anomaly-item">- {r}</div>' for r in anomaly["reasons"])
    st.markdown(f"""
    <div class="anomaly-{level.lower()}">
        <div class="anomaly-title">{level_emoji} {level} - Vital Anomaly Detected</div>
        {items}
    </div>""", unsafe_allow_html=True)
else:
    st.markdown('<div class="anomaly-normal"><div class="anomaly-title">All vitals within acceptable ranges</div></div>', unsafe_allow_html=True)


# ── Patient Summary ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="patient-summary">
    <div class="patient-name">{data['patient_name']}</div>
    <div class="patient-desc">{data['summary']}</div>
</div>
""", unsafe_allow_html=True)

if data.get("memory_trend"):
    with st.expander("Patient Memory Trends"):
        st.code(data["memory_trend"], language="text")


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Diagnosis", "Drug Safety", "Risk Scores", "SOAP Note", "Reasoning Trace"
])

with tab1:
    st.markdown('<div class="section-header">Differential Diagnosis</div>', unsafe_allow_html=True)
    for i, dx in enumerate(data["diagnoses"]):
        tier = dx["tier"]
        conf = dx["confidence"]
        st.markdown(f"""
        <div class="dx-card">
            <div class="dx-rank">DIAGNOSIS {i+1:02d}</div>
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
            <div class="opinion-item"><strong>Challenge:</strong> {op['challenge']}</div>
            <div class="opinion-item"><strong>Counter-evidence:</strong> {op['counter_evidence']}</div>
            <div class="opinion-final">Final Recommendation: {op['final_recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Drug Interaction Matrix</div>', unsafe_allow_html=True)
    warnings = data["drug_warnings"]
    if not warnings:
        st.markdown('<div class="anomaly-normal"><div class="anomaly-title">No significant drug interactions detected</div></div>', unsafe_allow_html=True)
    else:
        sev_icons = {"critical": "🔴", "major": "🟠", "moderate": "🟡", "minor": "🟢"}
        for w in warnings:
            icon = sev_icons.get(w["severity"], "o")
            st.markdown(f"""
            <div class="drug-card">
                <div class="drug-pair">{icon} {w['drug_a']} x {w['drug_b']} &nbsp;<span class="sev-{w['severity']}">{w['severity'].upper()}</span></div>
                <div class="drug-rec">{w['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Risk Score Assessment</div>', unsafe_allow_html=True)
    for r in data["risk_scores"]:
        score = r["score"]
        risk_color = "#dc2626" if score >= 70 else ("#d97706" if score >= 40 else "#16a34a")
        factors_html = "".join(f'<div class="risk-factor">{f}</div>' for f in r["factors"])
        st.markdown(f"""
        <div class="risk-card">
            <div class="risk-header">
                <div class="risk-name">{r['condition']}</div>
                <div class="risk-pct" style="color:{risk_color}">{score}%</div>
            </div>
            <div class="risk-bar-bg">
                <div style="width:{score}%;height:100%;border-radius:20px;background:{risk_color};opacity:0.85"></div>
            </div>
            {factors_html}
            <div class="risk-rec">{r['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">SOAP Clinical Note</div>', unsafe_allow_html=True)
    soap = data["soap_note"]
    soap_sections = [
        ("S - SUBJECTIVE", soap["subjective"]),
        ("O - OBJECTIVE", soap["objective"]),
        ("A - ASSESSMENT", soap["assessment"]),
        ("P - PLAN", soap["plan"]),
    ]
    for label, content in soap_sections:
        st.markdown(f"""
        <div class="soap-card">
            <div class="soap-label">{label}</div>
            <div class="soap-content">{content}</div>
        </div>""", unsafe_allow_html=True)

    if st.button("Export SOAP Note"):
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
        st.markdown('<div class="section-header" style="margin-top:1.5rem">RAG Citations</div>', unsafe_allow_html=True)
        for i, citation in enumerate(data["rag_citations"]):
            st.markdown(f'<div class="citation-card"><strong style="color:#2d7a4f">Guideline {i+1}</strong><br><br>{citation}</div>', unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    <span>MediCopilot v1.0 · Generated {data['generated_at'][:10]}</span>
    <span style="color:#c8e6d4">✚</span>
    <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents · A2A</span>
</div>
""", unsafe_allow_html=True)