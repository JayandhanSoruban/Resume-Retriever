import sys
from pathlib import Path
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from services.embedder import get_embedder

# -------------------------
# ✅ Setup Paths & Environment
# -------------------------
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
print("✅ sys.path root set to:", ROOT_DIR)

load_dotenv(dotenv_path=ROOT_DIR / ".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("GROQ_MODEL", "llama3-70b-8192")  # Default fallback

if not GROQ_API_KEY:
    raise EnvironmentError("❌ GROQ_API_KEY not found in .env file")

VECTOR_STORE_DIR = ROOT_DIR / "resume_matcher/vector_store"

# -------------------------
# ✅ Initialize LLM
# -------------------------
def initialize_llm():
    try:
        llm = ChatGroq(
            temperature=0.1,
            model_name=MODEL_NAME,
            groq_api_key=GROQ_API_KEY
        )
        print(f"[✅] LLM '{MODEL_NAME}' initialized successfully")
        return llm
    except Exception as e:
        print("[ERROR] Failed to initialize LLM:", str(e))
        raise

# -------------------------
# ✅ Rerank Resumes with LLM
# -------------------------
def rerank_resumes(query: str, docs: list[Document]) -> str:
    if not docs:
        return "❗ No resumes found for the query."

    resumes_str = "\n\n".join([
        f"Resume {i+1}:\n{doc.page_content.strip()}"
        for i, doc in enumerate(docs)
        if doc.page_content and doc.page_content.strip()
    ])

    if not resumes_str:
        return "❗ All resumes were empty."

    prompt_template = PromptTemplate(
        input_variables=["query", "resumes"],
        template="""
You are a recruitment expert. Based on the job description below, evaluate the given resumes and **select the best matching one only**.

Job Description:
"{query}"

Resumes:
{resumes}

Return the **full content** of the best matching resume ONLY — no explanation, no numbering.
"""
    )

    llm = initialize_llm()
    chain: Runnable = prompt_template | llm

    try:
        result = chain.invoke({"query": query, "resumes": resumes_str})
        return result.content.strip() if hasattr(result, "content") else str(result).strip()
    except Exception as e:
        return f"❗ LLM Error: {str(e)}"

# -------------------------
# ✅ Retrieve & Rerank
# -------------------------
def retrieve_and_rerank(query: str, top_k: int = 5):
    embedder = get_embedder()
    vectorstore = Chroma(
        embedding_function=embedder,
        persist_directory=str(VECTOR_STORE_DIR)
    )
    print(f"[INFO] Searching top {top_k} resumes for query: {query}")
    docs = vectorstore.similarity_search(query, k=top_k)
    best_match = rerank_resumes(query, docs)
    print("\n🎯 Best Matching Resume:\n")
    print(best_match)

# -------------------------
# ✅ Entry Point
# -------------------------
if __name__ == "__main__":
    user_query = input("💼 Enter job description or query: ").strip()
    if user_query:
        retrieve_and_rerank(user_query)
    else:
        print("❗ Query cannot be empty.")
