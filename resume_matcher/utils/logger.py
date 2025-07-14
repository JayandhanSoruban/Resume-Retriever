import sys
from pathlib import Path

# Dynamically add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from resume_matcher.services.search import semantic_search
from resume_matcher.services.reranker_llm import rerank_resumes
from dotenv import load_dotenv
load_dotenv()


def preview_doc(doc, i):
    print(f"\n--- RESULT {i+1} ---")
    print("📄 Metadata:", doc.metadata)
    content = doc.page_content.strip() if doc.page_content else ""
    if content:
        print("🧠 Content Preview:", content[:300], "...")
    else:
        print("❗ Empty content!")


if __name__ == "__main__":
    query = input("🔍 Enter job description or query: ").strip()
    if not query:
        print("❗ No query provided. Exiting.")
        sys.exit(1)

    # Step 1: Semantic Search
    try:
        results = semantic_search(query, top_k=5)
    except Exception as e:
        print(f"[ERROR] Semantic search failed: {e}")
        sys.exit(1)

    print(f"\n[DEBUG] Number of results retrieved: {len(results)}")

    if not results:
        print("❗ No results found. Check if your vector DB is populated correctly.")
        sys.exit(1)

    print("\n📄 Top-K Semantic Search Results:")
    for i, doc in enumerate(results):
        preview_doc(doc, i)

    # Step 2: Rerank with LLM
    print("\n🔁 Reranking with Groq LLM...")
    try:
        best_resume = rerank_resumes(query, results)
    except Exception as e:
        print(f"[ERROR] Reranking failed: {e}")
        sys.exit(1)

    print("\n🎯 Best Matched Resume:\n")
    if not best_resume:
        print("[DEBUG] GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))        
        print("❗ Reranker returned nothing. Check the LLM prompt formatting or the model response.")
    else:
        print(best_resume if isinstance(best_resume, str) else str(best_resume))






from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

# Load explicitly
load_dotenv(dotenv_path="D:/AGENTIC AI/Resume Retrieval/.env")

# Debug
print("[DEBUG] GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))

# Load Groq LLM (LLaMA3 70B)
llm = ChatGroq(
    temperature=0.1,
    model_name="llama3-70b-8192",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Prompt template
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

# Chain: prompt -> LLM
chain: Runnable = prompt_template | llm


def rerank_resumes(query: str, docs: List[Document]) -> str:
    if not docs:
        print("[ERROR] No documents provided to rerank.")
        return "❗ No resumes to rerank."

    # Build resume string
    resumes_str = "\n\n".join([
        f"Resume {i+1}:\n{doc.page_content.strip()}" 
        for i, doc in enumerate(docs) 
        if doc.page_content and doc.page_content.strip()
    ])

    if not resumes_str:
        print("[ERROR] All documents are empty or invalid.")
        return "❗ All resumes were empty."

    print("\n[DEBUG] Prompt being sent to LLM:\n")
    print(prompt_template.format(query=query, resumes=resumes_str[:1000]), "...\n")  # partial print

    try:
        result = chain.invoke({"query": query, "resumes": resumes_str})
        if hasattr(result, "content"):
            return result.content.strip()
        elif isinstance(result, str):
            return result.strip()
        else:
            print("[WARN] Unexpected LLM response format:", type(result))
            return str(result)
    except Exception as e:
        print("[ERROR] LLM call failed:", e)
        return "❗ Failed to rerank resumes due to LLM error."



# content[:300], "...")