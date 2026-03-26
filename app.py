"""
MediCopilot — Streamlit Demo UI
Polished demo for hackathon judges.
"""
import streamlit as st
import httpx
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="MediCopilot",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE = os.getenv("API_BASE", "https://medicopilot.onrender.com")

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: 700; color: #1a1a2e; }
    .sub-header  { font-size: 0.95rem; color: #6b7280; margin-top: -8px; }
    .anomaly-critical { background:#fee2e2; border-left:4px solid #ef4444; padding:12px; border-radius:6px; }
    .anomaly-urgent   { background:#fef3c7; border-left:4px solid #f59e0b; padding:12px; border-radius:6px; }
    .anomaly-warning  { background:#fffbeb; border-left:4px solid #fbbf24; padding:12px; border-radius:6px; }
    .anomaly-normal   { background:#d1fae5; border-left:4px solid #10b981; padding:12px; border-radius:6px; }
    .trace-step  { background:#f8fafc; border:1px solid #e2e8f0; border-radius:8px; padding:10px; margin:4px 0; }
    .tier-critical { color:#dc2626; font-weight:600; }
    .tier-high     { color:#ea580c; font-weight:600; }
    .tier-moderate { color:#d97706; font-weight:600; }
    .tier-low      { color:#16a34a; font-weight:600; }
    .soap-section  { background:#f0f9ff; border-radius:8px; padding:14px; margin:6px 0; }
    .risk-bar-container { background:#f1f5f9; border-radius:20px; height:12px; margin:4px 0; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🏥 MediCopilot")
    st.markdown("*AI Clinical Copilot*")
    st.divider()

    st.markdown("**Select Patient**")
    patient_options = {
        # Original
        "P001 — John Doe (62M, Diabetes + HTN + CKD)": "P001",
        "P002 — Sarah Chen (45F, AFib + Hypothyroidism)": "P002",
        "P003 — Marcus Johnson (71M, COPD + Heart Failure)": "P003",
        # Oncology
        "P004 — Patricia Williams (54F, Breast Cancer HER2+)": "P004",
        "P005 — Robert Nguyen (67M, Lung Cancer Stage IV)": "P005",
        # Pediatric
        "P006 — Aiden Patel (8M, T1 Diabetes + Asthma)": "P006",
        "P007 — Lily Thompson (5F, ALL Leukemia)": "P007",
        # Mental Health
        "P008 — Diana Foster (34F, Bipolar I + Anxiety)": "P008",
        "P009 — Carlos Rivera (28M, Schizophrenia + SUD)": "P009",
        # Rare / Complex
        "P010 — Eleanor Voss (41F, Lupus + Antiphospholipid)": "P010",
        "P011 — Samuel Okafor (19M, Cystic Fibrosis)": "P011",
        "P012 — Ingrid Larsson (37F, Multiple Sclerosis)": "P012",
        "P013 — Theo Blackwood (52M, ALS)": "P013",
    }
    selected_label = st.selectbox("Patient", list(patient_options.keys()), label_visibility="collapsed")
    patient_id = patient_options[selected_label]

    st.divider()
    st.markdown("**SHARP Context (Simulated)**")
    sharp_token = st.text_input("SHARP Token", value="demo-sharp-token-xxx", type="password")
    fhir_token = st.text_input("FHIR Token", value="demo-fhir-bearer-xxx", type="password")

    st.divider()
    run_btn = st.button("Generate Briefing", type="primary", use_container_width=True)

    st.divider()
    st.markdown("**Agents Active**")
    agents = ["FHIR", "Memory", "Anomaly", "RAG", "Diagnosis", "Drug Safety", "Risk", "2nd Opinion", "SOAP"]
    for agent in agents:
        st.markdown(f"● {agent}")


# ── Main Content ──────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">MediCopilot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-powered pre-visit clinical briefing · Multi-agent · RAG · FHIR-ready</div>', unsafe_allow_html=True)
st.divider()

if not run_btn:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("**Step 1** — Select a patient from the sidebar")
    with col2:
        st.info("**Step 2** — Click 'Generate Briefing'")
    with col3:
        st.info("**Step 3** — Review the AI clinical report")
    st.stop()

# ── API Call ──────────────────────────────────────────────────────────────────
with st.spinner("Running MediCopilot agents..."):
    try:
        response = httpx.post(
            f"{API_BASE}/invoke",
            json={"patient_id": patient_id, "sharp_token": sharp_token, "fhir_token": fhir_token},
            timeout=120.0
        )
        response.raise_for_status()
        data = response.json()
    except httpx.ConnectError:
        st.error("Cannot connect to API. Make sure the Render backend is running.")
        st.stop()
    except Exception as e:
        st.error(f"API error: {e}")
        st.stop()

# ── Render Report ─────────────────────────────────────────────────────────────
anomaly = data["anomaly_flag"]
level = anomaly["level"]
level_class = f"anomaly-{level.lower()}"
level_emoji = {"CRITICAL": "🚨", "URGENT": "⚠️", "WARNING": "🔶", "NORMAL": "✅"}.get(level, "ℹ️")

if anomaly["triggered"]:
    reasons_html = "".join(f"<li>{r}</li>" for r in anomaly["reasons"])
    st.markdown(
        f'<div class="{level_class}"><strong>{level_emoji} {level} — Anomaly Detected</strong><ul>{reasons_html}</ul></div>',
        unsafe_allow_html=True
    )
else:
    st.markdown('<div class="anomaly-normal">✅ Vitals within acceptable ranges</div>', unsafe_allow_html=True)

st.markdown(f"### {data['patient_name']}")
st.markdown(f"*{data['summary']}*")

if data.get("memory_trend"):
    with st.expander("📈 Patient Memory Trends"):
        st.code(data["memory_trend"])

st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔬 Diagnosis", "💊 Drug Safety", "📊 Risk Scores", "📝 SOAP Note", "🔍 Reasoning Trace"
])

with tab1:
    st.markdown("#### Differential Diagnosis")
    for i, dx in enumerate(data["diagnoses"]):
        tier = dx["tier"]
        tier_class = f"tier-{tier}"
        conf = dx["confidence"]
        conf_bar = "█" * (conf // 10) + "░" * (10 - conf // 10)
        with st.container():
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.markdown(f"**{i+1}. {dx['condition']}**")
                st.caption(dx["reasoning"])
            with col_b:
                st.markdown(f'<span class="{tier_class}">{tier.upper()}</span>', unsafe_allow_html=True)
                st.markdown(f"`{conf}%` {conf_bar}")
        st.divider()

    if data.get("second_opinion"):
        st.markdown("#### 🧐 Second Opinion")
        op = data["second_opinion"]
        with st.expander("View second opinion analysis"):
            st.markdown(f"**Challenge:** {op['challenge']}")
            st.markdown(f"**Counter-evidence:** {op['counter_evidence']}")
            st.success(f"**Final Recommendation:** {op['final_recommendation']}")

with tab2:
    st.markdown("#### Drug Interaction Matrix")
    warnings = data["drug_warnings"]
    if not warnings:
        st.success("No significant drug interactions detected.")
    else:
        severity_colors = {"critical": "🔴", "major": "🟠", "moderate": "🟡", "minor": "🟢"}
        for w in warnings:
            emoji = severity_colors.get(w["severity"], "⚪")
            with st.container():
                st.markdown(f"{emoji} **{w['drug_a']}** + **{w['drug_b']}** — `{w['severity'].upper()}`")
                st.caption(f"Recommendation: {w['recommendation']}")
            st.divider()

with tab3:
    st.markdown("#### Risk Score Assessment")
    for r in data["risk_scores"]:
        score = r["score"]
        color = "#ef4444" if score >= 70 else ("#f59e0b" if score >= 40 else "#10b981")
        st.markdown(f"**{r['condition']}**")
        st.progress(score / 100, text=f"{score}% risk")
        with st.expander("Contributing factors & recommendation"):
            for factor in r["factors"]:
                st.markdown(f"- {factor}")
            st.info(r["recommendation"])

with tab4:
    st.markdown("#### SOAP Note")
    soap = data["soap_note"]
    sections = [
        ("S — Subjective", soap["subjective"], "🗣️"),
        ("O — Objective", soap["objective"], "🔬"),
        ("A — Assessment", soap["assessment"], "🧠"),
        ("P — Plan", soap["plan"], "📋"),
    ]
    for label, content, emoji in sections:
        st.markdown(f'<div class="soap-section"><strong>{emoji} {label}</strong><br><br>{content}</div>', unsafe_allow_html=True)
        st.markdown("")

    if st.button("Copy SOAP Note to Clipboard"):
        soap_text = f"S: {soap['subjective']}\nO: {soap['objective']}\nA: {soap['assessment']}\nP: {soap['plan']}"
        st.code(soap_text, language="text")

with tab5:
    st.markdown("#### Agent Reasoning Trace")
    st.caption("How the agents collaborated to produce this briefing")
    for i, step in enumerate(data["reasoning_trace"]):
        agent_colors = {
            "FHIRAgent": "🟦",
            "MemoryAgent": "🟪",
            "AnomalyDetector": "🟥",
            "RAGAgent": "🟩",
            "DiagnosisAgent": "🟦",
            "DrugSafetyAgent": "🟧",
            "RiskScoringAgent": "🟥",
            "SecondOpinionAgent": "🟫",
            "SOAPNoteGenerator": "⬛",
        }
        emoji = agent_colors.get(step["agent"], "⚪")
        st.markdown(
            f'<div class="trace-step">'
            f'<strong>{emoji} [{i+1}] {step["agent"]}</strong><br>'
            f'<small>Action: {step["action"]}</small><br>'
            f'<small>Finding: <em>{step["finding"]}</em></small>'
            f'</div>',
            unsafe_allow_html=True
        )

    if data.get("rag_citations"):
        st.markdown("#### 📚 RAG Citations")
        for i, citation in enumerate(data["rag_citations"]):
            with st.expander(f"Guideline chunk {i+1}"):
                st.markdown(citation)

# ── Footer ────────────────────────────────────────────────────────────────────
st.divider()
st.caption(f"Generated at {data['generated_at']} UTC · MediCopilot v1.0 · Powered by Groq llama-3.1-8b-instant · RAG: FAISS + Medical Guidelines")