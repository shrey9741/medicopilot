"""
RAG layer — FAISS vector store with medical knowledge.
Uses sentence-transformers for embeddings (no API key needed for embeddings).
"""
import os
import pickle
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

VECTORSTORE_PATH = Path("rag/vectorstore")
EMBEDDINGS_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Built-in medical knowledge (used when no PDFs are provided)
MEDICAL_KNOWLEDGE = [
    """
    Type 2 Diabetes Management Guidelines (WHO/ADA):
    Target HbA1c: <7% for most adults. Metformin is first-line therapy.
    Avoid Metformin if eGFR <30 mL/min (CKD Stage 4+). Monitor renal function every 3-6 months.
    Combination therapy with SGLT2 inhibitors or GLP-1 agonists recommended when HbA1c >9%.
    Blood pressure target in diabetics: <130/80 mmHg. ACE inhibitors preferred for renal protection.
    """,
    """
    Hypertension Treatment Guidelines (JNC 8 / ACC/AHA 2017):
    Stage 1: SBP 130-139 or DBP 80-89. Lifestyle modifications first.
    Stage 2: SBP ≥140 or DBP ≥90. Initiate pharmacotherapy.
    Hypertensive crisis: SBP >180 and/or DBP >120. Immediate evaluation required.
    ACE inhibitors or ARBs recommended for patients with diabetes or CKD.
    """,
    """
    Chronic Kidney Disease (CKD) Management:
    Stage 2: eGFR 60-89. Monitor annually, control BP and blood sugar.
    Avoid nephrotoxic drugs including NSAIDs and contrast agents when possible.
    Metformin dose reduction or discontinuation may be needed in CKD.
    ACE inhibitors/ARBs slow CKD progression but monitor potassium and creatinine.
    Refer to nephrology if eGFR <45 or rapid decline.
    """,
    """
    Drug Interaction Guidelines:
    Metformin + contrast dye: Hold Metformin 48 hours before/after iodinated contrast.
    Warfarin interactions: NSAIDs, antibiotics, and many medications affect INR. Monitor closely.
    ACE inhibitors + NSAIDs: Increases risk of acute kidney injury. Avoid combination.
    Statins + certain antibiotics (clarithromycin): Increased myopathy risk.
    Furosemide + NSAIDs: Reduced diuretic effect, risk of renal impairment.
    """,
    """
    Cardiovascular Risk Assessment (Framingham / ACC/AHA Pooled Cohort):
    Major risk factors: Age, hypertension, diabetes, smoking, dyslipidemia, family history.
    High risk: 10-year ASCVD risk ≥20%. Statin therapy strongly recommended.
    Intermediate: 7.5-20%. Consider statin + lifestyle modification.
    BP control reduces cardiovascular events by 25-30%.
    Aspirin: Not recommended for primary prevention; use for secondary prevention.
    """,
    """
    Heart Failure Management (ACC/AHA HF Guidelines):
    HFrEF (EF <40%): ACE inhibitor/ARB + beta-blocker + aldosterone antagonist.
    Monitor daily weights, restrict sodium <2g/day and fluid <2L/day.
    Loop diuretics (Furosemide) for fluid overload. Titrate to dry weight.
    Symptoms of decompensation: orthopnea, PND, increased edema, worsening dyspnea.
    SGLT2 inhibitors reduce hospitalizations in HFrEF regardless of diabetes status.
    """,
    """
    COPD Management (GOLD Guidelines):
    Bronchodilators are cornerstone of treatment (LABA/LAMA).
    Short-acting bronchodilators for rescue use.
    Inhaled corticosteroids for patients with frequent exacerbations.
    Oxygen therapy if SpO2 <88% at rest (target 88-92% in COPD to avoid CO2 retention).
    Smoking cessation is most effective intervention to slow progression.
    Pulmonary rehabilitation improves exercise tolerance and quality of life.
    """,
    """
    Atrial Fibrillation Management:
    Rate control target: HR <80 bpm at rest (lenient: <110 bpm acceptable).
    Anticoagulation: CHA2DS2-VASc score guides warfarin or DOAC therapy.
    INR target for warfarin: 2.0-3.0. Subtherapeutic INR increases stroke risk.
    Ibuprofen and NSAIDs contraindicated with anticoagulation (bleeding risk).
    Thyroid function testing recommended in all new AF cases.
    """,
]


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDINGS_MODEL,
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def build_vectorstore() -> FAISS:
    """Build FAISS vectorstore from built-in medical knowledge."""
    print("Building RAG vectorstore from medical knowledge base...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
    docs = []
    for i, text in enumerate(MEDICAL_KNOWLEDGE):
        chunks = splitter.create_documents([text.strip()], metadatas=[{"source": f"guideline_{i}"}])
        docs.extend(chunks)

    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_PATH))
    print(f"Vectorstore built with {len(docs)} chunks.")
    return vectorstore


def load_vectorstore() -> FAISS:
    """Load existing vectorstore or build a new one."""
    embeddings = get_embeddings()
    if VECTORSTORE_PATH.exists() and any(VECTORSTORE_PATH.iterdir()):
        try:
            return FAISS.load_local(str(VECTORSTORE_PATH), embeddings, allow_dangerous_deserialization=True)
        except Exception:
            pass
    return build_vectorstore()


def retrieve_context(query: str, vectorstore: FAISS, k: int = 3) -> list[str]:
    """Retrieve top-k relevant medical guidelines for a query."""
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content.strip() for doc in docs]
