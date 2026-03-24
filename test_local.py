"""
MediCopilot — Local test script.
Run this BEFORE deploying to catch any issues early.
Usage: python test_local.py
"""
import os
import sys
import json
from dotenv import load_dotenv

load_dotenv()

PASS = "✅"
FAIL = "❌"
WARN = "⚠️"

results = []

def check(label, fn):
    try:
        result = fn()
        print(f"  {PASS} {label}: {result}")
        results.append(True)
    except Exception as e:
        print(f"  {FAIL} {label}: {e}")
        results.append(False)


print("\n" + "="*55)
print("  MediCopilot — Pre-flight Test Suite")
print("="*55)

# ── 1. Environment ────────────────────────────────────────────
print("\n[1] Environment")
check("GROQ_API_KEY set", lambda: "OK" if os.getenv("GROQ_API_KEY") else (_ for _ in ()).throw(ValueError("Not set — copy .env.example to .env and add your key")))

# ── 2. Imports ────────────────────────────────────────────────
print("\n[2] Imports")
check("models.schemas", lambda: __import__("models.schemas") and "OK")
check("fhir.mock_client", lambda: __import__("fhir.mock_client") and "OK")
check("agents.anomaly_detector", lambda: __import__("agents.anomaly_detector") and "OK")
check("agents.memory", lambda: __import__("agents.memory") and "OK")
check("rag.retriever", lambda: __import__("rag.retriever") and "OK")

# ── 3. FHIR mock data ─────────────────────────────────────────
print("\n[3] FHIR Mock Client")
from fhir.mock_client import get_patient_bundle, get_patient_history

check("Fetch P001", lambda: get_patient_bundle("P001").name)
check("Fetch P002", lambda: get_patient_bundle("P002").name)
check("Fetch P003", lambda: get_patient_bundle("P003").name)
check("History P001", lambda: f"{len(get_patient_history('P001'))} records")

# ── 4. Anomaly detector ───────────────────────────────────────
print("\n[4] Anomaly Detector")
from agents.anomaly_detector import detect_anomalies

p1 = get_patient_bundle("P001")
p3 = get_patient_bundle("P003")

check("P001 anomaly level", lambda: detect_anomalies(p1).level)
check("P003 anomaly (critical patient)", lambda: f"{detect_anomalies(p3).level} — {len(detect_anomalies(p3).reasons)} flags")

# ── 5. Memory module ──────────────────────────────────────────
print("\n[5] Temporal Memory")
from agents.memory import load_history, update_memory, analyze_trends

check("Load history P001", lambda: load_history("P001", get_patient_history("P001")) or "OK")
check("Update memory", lambda: update_memory(p1) or "OK")
check("Analyze trends", lambda: analyze_trends("P001")[:60] + "..." if analyze_trends("P001") else "No trends yet (need 2+ visits)")

# ── 6. RAG vectorstore ────────────────────────────────────────
print("\n[6] RAG Vectorstore")
from rag.retriever import load_vectorstore, retrieve_context

print(f"  {WARN} Building vectorstore (first run takes ~30 seconds)...")
try:
    vs = load_vectorstore()
    check("Vectorstore loaded", lambda: f"{vs.index.ntotal} vectors")
    check("Retrieve diabetes guidelines", lambda: retrieve_context("Type 2 Diabetes Metformin", vs, k=2)[0][:60] + "...")
    check("Retrieve drug interactions", lambda: retrieve_context("Warfarin NSAIDs interaction", vs, k=1)[0][:60] + "...")
except Exception as e:
    print(f"  {FAIL} Vectorstore: {e}")
    results.append(False)
    vs = None

# ── 7. Groq API ───────────────────────────────────────────────
print("\n[7] Groq API (LLM)")
try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": "Reply with just: OK"}],
        max_tokens=5,
        temperature=0
    )
    check("Groq API call", lambda: resp.choices[0].message.content.strip())
except Exception as e:
    print(f"  {FAIL} Groq API: {e}")
    results.append(False)

# ── 8. Full orchestrator (if vectorstore built) ───────────────
if vs:
    print("\n[8] Full Orchestrator (end-to-end)")
    print(f"  {WARN} Running full pipeline for P001 (takes 10-20 seconds)...")
    try:
        from agents.orchestrator import run_medicopilot
        result = run_medicopilot("P001", vs)

        check("Response has diagnoses",    lambda: f"{len(result.diagnoses)} diagnoses")
        check("Response has drug warnings",lambda: f"{len(result.drug_warnings)} warnings")
        check("Response has risk scores",  lambda: f"{len(result.risk_scores)} scores")
        check("SOAP note generated",       lambda: result.soap_note.subjective[:50] + "...")
        check("Reasoning trace length",    lambda: f"{len(result.reasoning_trace)} steps")
        check("Second opinion present",    lambda: result.second_opinion.challenge[:50] + "...")
        check("Anomaly flag",              lambda: f"{result.anomaly_flag.level} — {len(result.anomaly_flag.reasons)} flags")
        check("Memory trend",              lambda: result.memory_trend[:60] + "..." if result.memory_trend else "No prior visits (first run)")

    except Exception as e:
        print(f"  {FAIL} Orchestrator: {e}")
        results.append(False)
else:
    print(f"\n[8] Full Orchestrator — {WARN} Skipped (vectorstore failed)")

# ── Summary ───────────────────────────────────────────────────
print("\n" + "="*55)
passed = sum(results)
total = len(results)
status = PASS if passed == total else (WARN if passed >= total * 0.8 else FAIL)
print(f"  {status} {passed}/{total} checks passed")

if passed == total:
    print("\n  All systems go! You can now run:")
    print("    uvicorn main:app --reload")
    print("    streamlit run app.py")
elif passed >= total * 0.8:
    print("\n  Minor issues — check failures above before deploying.")
else:
    print("\n  Critical issues found — fix failures before running.")

print("="*55 + "\n")
