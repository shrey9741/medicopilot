"""
MediCopilot — Streamlit Demo UI
Premium clinical interface design.
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
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Playfair+Display:wght@600;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, .stApp {
    background: #0a0f1e !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem !important; max-width: 1400px !important; }

[data-testid="stSidebar"] {
    background: #0d1425 !important;
    border-right: 1px solid #1e2d4a !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSelectbox > div > div {
    background: #131d35 !important;
    border: 1px solid #1e2d4a !important;
    color: #e2e8f0 !important;
    border-radius: 8px !important;
}

.logo-area { padding: 1.5rem 0 1rem; border-bottom: 1px solid #1e2d4a; margin-bottom: 1.5rem; }
.logo-title { font-family: 'Playfair Display', serif; font-size: 1.6rem; font-weight: 700; color: #ffffff !important; letter-spacing: -0.5px; }
.logo-sub { font-size: 0.75rem; color: #4a7fa5 !important; letter-spacing: 2px; text-transform: uppercase; margin-top: 2px; }
.patient-label { font-size: 0.7rem; letter-spacing: 2px; text-transform: uppercase; color: #4a7fa5 !important; margin-bottom: 8px; font-weight: 600; }

.stButton > button {
    background: linear-gradient(135deg, #1a6b9a 0%, #0e4d7a 100%) !important;
    color: #ffffff !important; border: none !important; border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important; font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important; font-size: 0.9rem !important; letter-spacing: 0.5px !important;
    transition: all 0.2s ease !important; box-shadow: 0 4px 15px rgba(26,107,154,0.3) !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 20px rgba(26,107,154,0.5) !important; }

.agent-pill { display: inline-block; background: #131d35; border: 1px solid #1e2d4a; border-radius: 20px; padding: 3px 10px; font-size: 0.7rem; color: #4a7fa5 !important; margin: 2px; font-family: 'DM Mono', monospace; }

.main-hero { background: linear-gradient(135deg, #0d1425 0%, #111827 100%); border: 1px solid #1e2d4a; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.main-hero::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(26,107,154,0.08) 0%, transparent 70%); pointer-events: none; }
.hero-title { font-family: 'Playfair Display', serif; font-size: 2.2rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1.2; }
.hero-title span { color: #1a6b9a; }
.hero-sub { font-size: 0.85rem; color: #4a7fa5; margin-top: 6px; letter-spacing: 0.5px; }
.hero-badges { margin-top: 12px; display: flex; gap: 8px; flex-wrap: wrap; }
.badge { background: #131d35; border: 1px solid #1e2d4a; border-radius: 20px; padding: 4px 12px; font-size: 0.7rem; color: #4a7fa5; font-family: 'DM Mono', monospace; letter-spacing: 0.5px; }

.step-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.step-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.2rem 1.5rem; transition: border-color 0.2s; }
.step-card:hover { border-color: #1a6b9a; }
.step-num { font-family: 'DM Mono', monospace; font-size: 0.65rem; color: #1a6b9a; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 6px; }
.step-text { font-size: 0.85rem; color: #94a3b8; }

.anomaly-critical { background: linear-gradient(135deg, #1a0a0a, #2d0f0f); border: 1px solid #ef4444; border-left: 4px solid #ef4444; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-urgent { background: linear-gradient(135deg, #1a1200, #2d1f00); border: 1px solid #f59e0b; border-left: 4px solid #f59e0b; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-warning { background: linear-gradient(135deg, #1a1200, #2d1f00); border: 1px solid #fbbf24; border-left: 4px solid #fbbf24; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-normal { background: linear-gradient(135deg, #001a0f, #002d1a); border: 1px solid #10b981; border-left: 4px solid #10b981; border-radius: 10px; padding: 14px 18px; margin-bottom: 1rem; }
.anomaly-title { font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; }
.anomaly-item { font-size: 0.82rem; color: #94a3b8; margin: 3px 0 3px 12px; }

.patient-summary { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.5rem; margin-bottom: 1rem; }
.patient-name { font-family: 'Playfair Display', serif; font-size: 1.4rem; color: #ffffff; margin-bottom: 6px; }
.patient-desc { font-size: 0.85rem; color: #64748b; line-height: 1.6; }

.stTabs [data-baseweb="tab-list"] { background: #0d1425 !important; border-radius: 10px !important; padding: 4px !important; border: 1px solid #1e2d4a !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { background: transparent !important; color: #64748b !important; border-radius: 8px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.82rem !important; font-weight: 500 !important; padding: 8px 16px !important; border: none !important; }
.stTabs [aria-selected="true"] { background: #131d35 !important; color: #e2e8f0 !important; border: 1px solid #1e2d4a !important; }
.stTabs [data-baseweb="tab-panel"] { background: transparent !important; padding: 1rem 0 !important; }

.dx-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; transition: border-color 0.2s; }
.dx-card:hover { border-color: #2a4a6a; }
.dx-condition { font-size: 0.95rem; font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.dx-reasoning { font-size: 0.8rem; color: #64748b; line-height: 1.5; }
.dx-meta { display: flex; gap: 10px; align-items: center; margin-top: 10px; }
.tier-critical { background: #2d0f0f; color: #ef4444; border: 1px solid #ef4444; border-radius: 6px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-high { background: #2d1500; color: #f97316; border: 1px solid #f97316; border-radius: 6px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-moderate { background: #2d2000; color: #f59e0b; border: 1px solid #f59e0b; border-radius: 6px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.tier-low { background: #002d1a; color: #10b981; border: 1px solid #10b981; border-radius: 6px; padding: 2px 10px; font-size: 0.72rem; font-weight: 700; font-family: 'DM Mono', monospace; }
.conf-bar-bg { background: #131d35; border-radius: 20px; height: 6px; flex: 1; overflow: hidden; }
.conf-bar-fill { height: 100%; border-radius: 20px; background: linear-gradient(90deg, #1a6b9a, #38bdf8); }
.conf-label { font-family: 'DM Mono', monospace; font-size: 0.75rem; color: #4a7fa5; min-width: 36px; }

.drug-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; }
.drug-pair { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; margin-bottom: 6px; }
.drug-rec { font-size: 0.8rem; color: #64748b; line-height: 1.5; }
.sev-critical { color: #ef4444; } .sev-major { color: #f97316; } .sev-moderate { color: #f59e0b; } .sev-minor { color: #10b981; }

.risk-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.2rem 1.5rem; margin-bottom: 10px; }
.risk-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.risk-name { font-size: 0.9rem; font-weight: 600; color: #e2e8f0; }
.risk-pct { font-family: 'DM Mono', monospace; font-size: 1.1rem; font-weight: 700; }
.risk-bar-bg { background: #131d35; border-radius: 20px; height: 8px; margin-bottom: 10px; overflow: hidden; }
.risk-factor { font-size: 0.78rem; color: #64748b; margin: 3px 0; padding-left: 12px; }
.risk-rec { font-size: 0.78rem; color: #4a7fa5; margin-top: 8px; padding: 8px 12px; background: #131d35; border-radius: 8px; border-left: 3px solid #1a6b9a; }

.soap-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 12px; padding: 1.5rem; margin-bottom: 12px; }
.soap-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; text-transform: uppercase; color: #1a6b9a; margin-bottom: 10px; font-weight: 600; }
.soap-content { font-size: 0.85rem; color: #94a3b8; line-height: 1.7; }

.trace-card { background: #0d1425; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 8px; display: grid; grid-template-columns: auto 1fr; gap: 12px; align-items: start; }
.trace-num { font-family: 'DM Mono', monospace; font-size: 0.7rem; color: #1a6b9a; background: #131d35; border: 1px solid #1e2d4a; border-radius: 6px; padding: 4px 8px; font-weight: 600; min-width: 32px; text-align: center; }
.trace-agent { font-size: 0.82rem; font-weight: 600; color: #e2e8f0; margin-bottom: 4px; }
.trace-action { font-size: 0.76rem; color: #64748b; }
.trace-finding { font-size: 0.76rem; color: #4a7fa5; margin-top: 3px; font-style: italic; }

.opinion-card { background: #0d1425; border: 1px solid #2a4a2a; border-radius: 12px; padding: 1.5rem; margin-top: 1rem; }
.opinion-label { font-family: 'DM Mono', monospace; font-size: 0.65rem; letter-spacing: 3px; color: #10b981; text-transform: uppercase; margin-bottom: 10px; }

.section-header { font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #ffffff; margin-bottom: 1rem; padding-bottom: 8px; border-bottom: 1px solid #1e2d4a; }

.citation-card { background: #0a0f1e; border: 1px solid #1e2d4a; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; font-size: 0.78rem; color: #64748b; font-family: 'DM Mono', monospace; line-height: 1.6; }

.stProgress > div > div { background: #1e2d4a !important; }
.stProgress > div > div > div { background: linear-gradient(90deg, #1a6b9a, #38bdf8) !important; }

.footer-bar { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #1e2d4a; font-size: 0.72rem; color: #334155; font-family: 'DM Mono', monospace; display: flex; justify-content: space-between; }

hr { border-color: #1e2d4a !important; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
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
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Generate Briefing", type="primary", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="patient-label">Active Agents</div>', unsafe_allow_html=True)
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    pills_html = "".join(f'<span class="agent-pill">{a}</span>' for a in agents)
    st.markdown(pills_html, unsafe_allow_html=True)


# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-hero">
    <div class="hero-title">Medi<span>Copilot</span></div>
    <div class="hero-sub">AI-powered pre-visit clinical briefing system</div>
    <div class="hero-badges">
        <span class="badge">MULTI-AGENT</span>
        <span class="badge">RAG · FAISS</span>
        <span class="badge">FHIR-READY</span>
        <span class="badge">GROQ · LLAMA 3.1</span>
        <span class="badge">SOAP NOTES</span>
        <span class="badge">DRUG SAFETY</span>
    </div>
</div>
""", unsafe_allow_html=True)

if not run_btn:
    st.markdown("""
    <div class="step-grid">
        <div class="step-card">
            <div class="step-num">Step 01</div>
            <div class="step-text">Select a patient from the sidebar</div>
        </div>
        <div class="step-card">
            <div class="step-num">Step 02</div>
            <div class="step-text">Click Generate Briefing</div>
        </div>
        <div class="step-card">
            <div class="step-num">Step 03</div>
            <div class="step-text">Review the AI clinical report</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── API Call ──────────────────────────────────────────────────────────────────
with st.spinner("Running MediCopilot agents..."):
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
anomaly_class = f"anomaly-{level.lower()}"

if anomaly["triggered"]:
    items = "".join(f'<div class="anomaly-item">→ {r}</div>' for r in anomaly["reasons"])
    st.markdown(f"""
    <div class="{anomaly_class}">
        <div class="anomaly-title">{level_emoji} {level} — Vital Anomaly Detected</div>
        {items}
    </div>""", unsafe_allow_html=True)
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
            <div class="dx-condition">{i+1}. {dx['condition']}</div>
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
            <div class="opinion-label">🧐 Second Opinion Analysis</div>
            <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:8px"><strong style="color:#e2e8f0">Challenge:</strong> {op['challenge']}</div>
            <div style="font-size:0.82rem;color:#94a3b8;margin-bottom:8px"><strong style="color:#e2e8f0">Counter-evidence:</strong> {op['counter_evidence']}</div>
            <div style="font-size:0.82rem;color:#10b981"><strong>Final Recommendation:</strong> {op['final_recommendation']}</div>
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
            sev_class = f"sev-{w['severity']}"
            st.markdown(f"""
            <div class="drug-card">
                <div class="drug-pair">{icon} {w['drug_a']} <span style="color:#334155">+</span> {w['drug_b']} <span class="{sev_class}" style="font-size:0.72rem;font-family:'DM Mono',monospace;margin-left:8px">{w['severity'].upper()}</span></div>
                <div class="drug-rec">{w['recommendation']}</div>
            </div>""", unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Risk Score Assessment</div>', unsafe_allow_html=True)
    for r in data["risk_scores"]:
        score = r["score"]
        risk_color = "#ef4444" if score >= 70 else ("#f59e0b" if score >= 40 else "#10b981")
        factors_html = "".join(f'<div class="risk-factor">→ {f}</div>' for f in r["factors"])
        st.markdown(f"""
        <div class="risk-card">
            <div class="risk-header">
                <div class="risk-name">{r['condition']}</div>
                <div class="risk-pct" style="color:{risk_color}">{score}%</div>
            </div>
            <div class="risk-bar-bg"><div style="width:{score}%;height:100%;border-radius:20px;background:linear-gradient(90deg,{risk_color}88,{risk_color})"></div></div>
            {factors_html}
            <div class="risk-rec">{r['recommendation']}</div>
        </div>""", unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="section-header">SOAP Clinical Note</div>', unsafe_allow_html=True)
    soap = data["soap_note"]
    soap_sections = [
        ("S — SUBJECTIVE", soap["subjective"], "🗣️"),
        ("O — OBJECTIVE", soap["objective"], "🔬"),
        ("A — ASSESSMENT", soap["assessment"], "🧠"),
        ("P — PLAN", soap["plan"], "📋"),
    ]
    for label, content, emoji in soap_sections:
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
            st.markdown(f'<div class="citation-card"><strong style="color:#4a7fa5">Guideline {i+1}</strong><br><br>{citation}</div>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="footer-bar">
    <span>MediCopilot v1.0 · Generated {data['generated_at'][:10]} UTC</span>
    <span>Groq · Llama 3.1-8b · FAISS RAG · 9 Agents</span>
</div>
""", unsafe_allow_html=True)