# semantic_search.py
import sys
from pathlib import Path
from typing import List
from langchain_core.documents import Document

# Dynamically add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from resume_matcher.services.reranker_llm import rerank_resumes

def semantic_search(query: str, top_k: int = 5) -> List[Document]:
    """
    Placeholder for semantic search function.
    Replace with actual implementation from your resume_matcher.services.search module.
    """
    # Placeholder: Returns dummy documents for testing
    # Replace with your actual semantic_search implementation
    print("[INFO] Using placeholder semantic_search function.")
    dummy_resumes = [
        Document(
            page_content="John Doe\nSoftware Engineer\n6 years of experience in Python and machine learning\nProjects: AI chatbot, Recommendation system\nSkills: Python, TensorFlow, SQL",
            metadata={"id": "1", "source": "resume1.pdf"}
        ),
        Document(
            page_content="Jane Smith\nData Scientist\n4 years of experience in R and data analysis\nProjects: Predictive modeling, Data visualization\nSkills: R, Python, Tableau",
            metadata={"id": "2", "source": "resume2.pdf"}
        ),
        Document(
            page_content="Alice Johnson\nBackend Developer\n7 years of experience in Java and microservices\nProjects: Payment gateway, API development\nSkills: Java, Spring Boot, Docker",
            metadata={"id": "3", "source": "resume3.pdf"}
        )
    ]
    return dummy_resumes[:top_k]

def preview_doc(doc: Document, i: int):
    """Preview a document's metadata and content."""
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
    if not best_resume or best_resume.startswith("❗"):
        print("[DEBUG] GROQ_API_KEY =", os.getenv("GROQ_API_KEY"))
        print("❗ Reranker returned nothing or failed. Check the LLM prompt formatting or the model response.")
        print(best_resume)
    else:
        print(best_resume if isinstance(best_resume, str) else str(best_resume))