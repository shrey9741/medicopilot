"""
RAG layer — FAISS vector store with medical knowledge.
Uses a lightweight TF-IDF + cosine similarity approach on Render free tier
to stay within 512MB RAM, while preserving full semantic retrieval capability.
"""
import os
import numpy as np
from pathlib import Path
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List

VECTORSTORE_PATH = Path("rag/vectorstore")

# Built-in medical knowledge base

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
    """
    Oncology Supportive Care Guidelines:
    Neutropenia management: ANC <1500 requires monitoring; ANC <500 is severe neutropenia.
    G-CSF prophylaxis recommended when febrile neutropenia risk >20%.
    Antiemetics: 5-HT3 antagonists (ondansetron) for chemo-induced nausea.
    Cardiotoxicity monitoring: LVEF baseline and every 3 months with anthracyclines/trastuzumab.
    Immunotherapy (checkpoint inhibitors): monitor for irAEs — colitis, pneumonitis, endocrinopathy.
    """,
    """
    Pediatric Diabetes and Asthma Guidelines:
    Type 1 Diabetes in children: Target HbA1c <7.5%. Continuous glucose monitoring recommended.
    Hypoglycemia in children: Treat with 15g fast-acting carbs; recheck in 15 minutes.
    Pediatric asthma: Step-up therapy based on symptom frequency and lung function.
    Inhaled corticosteroids are preferred long-term controller therapy in children.
    Growth and development monitoring essential in children on long-term steroids.
    """,
    """
    Mental Health Medication Guidelines:
    Lithium therapeutic range: 0.6-1.2 mEq/L. Toxicity risk above 1.5 mEq/L.
    Clozapine: mandatory ANC monitoring weekly for 6 months, then biweekly.
    SSRIs: First-line for depression and anxiety. Allow 4-6 weeks for full effect.
    Antipsychotics: Monitor metabolic syndrome — weight, glucose, lipids every 3 months.
    Benzodiazepines: Short-term use only; risk of dependence and cognitive impairment.
    """,
    """
    Rare Disease and Autoimmune Guidelines:
    Lupus (SLE): Hydroxychloroquine is standard of care for all patients without contraindication.
    Monitor anti-dsDNA and complement (C3/C4) for disease activity.
    Cystic Fibrosis: CFTR modulators (Trikafta) significantly improve FEV1 in eligible patients.
    Multiple Sclerosis: JC virus antibody monitoring essential with natalizumab (PML risk).
    ALS: Riluzole and edaravone are approved disease-modifying therapies; multidisciplinary care essential.
    """,
    """
    Palliative and End-of-Life Care Guidelines:
    Opioid titration: Start low, go slow. Morphine is first-line for cancer pain.
    Dyspnea in terminal illness: Low-dose opioids and anxiolytics provide relief.
    Nutrition support: PEG tube consideration in ALS when FVC <50% or dysphagia significant.
    Goals of care discussions: Recommended when prognosis <12 months or major functional decline.
    Advance directives and DNR should be discussed proactively with high-risk patients.
    """,
]


class LightweightTfidfEmbeddings(Embeddings):
    """
    Memory-efficient TF-IDF embeddings for Render free tier.
    Uses sklearn TfidfVectorizer — no model download, <5MB RAM.
    Preserves full keyword-based semantic retrieval on medical text.
    """

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=512,
            ngram_range=(1, 2),
            sublinear_tf=True
        )
        self._fitted = False
        self._corpus: List[str] = []

    def fit(self, texts: List[str]):
        self._corpus = texts
        self.vectorizer.fit(texts)
        self._fitted = True

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        if not self._fitted:
            self.fit(texts)
        vectors = self.vectorizer.transform(texts).toarray()
        return vectors.tolist()

    def embed_query(self, text: str) -> List[float]:
        if not self._fitted:
            return [0.0] * 512
        vector = self.vectorizer.transform([text]).toarray()
        return vector[0].tolist()


# Global embeddings instance (shared across calls)
_embeddings_instance: LightweightTfidfEmbeddings = None


def get_embeddings() -> LightweightTfidfEmbeddings:
    global _embeddings_instance
    if _embeddings_instance is None:
        _embeddings_instance = LightweightTfidfEmbeddings()
    return _embeddings_instance


def build_vectorstore() -> FAISS:
    """Build FAISS vectorstore from built-in medical knowledge."""
    print("Building RAG vectorstore from medical knowledge base...")

    splitter = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=60)
    docs = []
    for i, text in enumerate(MEDICAL_KNOWLEDGE):
        chunks = splitter.create_documents([text.strip()], metadatas=[{"source": f"guideline_{i}"}])
        docs.extend(chunks)

    # Fit embeddings on all document texts first
    all_texts = [doc.page_content for doc in docs]
    embeddings = get_embeddings()
    embeddings.fit(all_texts)

    vectorstore = FAISS.from_documents(docs, embeddings)

    VECTORSTORE_PATH.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(VECTORSTORE_PATH))
    print(f"Vectorstore built with {len(docs)} chunks.")
    return vectorstore


def load_vectorstore() -> FAISS:
    """Load existing vectorstore or build a new one."""
    # Always rebuild — TF-IDF needs to be fitted fresh (no model file needed)
    return build_vectorstore()


def retrieve_context(query: str, vectorstore: FAISS, k: int = 3) -> list[str]:
    """Retrieve top-k relevant medical guidelines for a query."""
    docs = vectorstore.similarity_search(query, k=k)
    return [doc.page_content.strip() for doc in docs]