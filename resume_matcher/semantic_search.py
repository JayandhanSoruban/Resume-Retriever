import sys
from pathlib import Path
from typing import List
from langchain_core.documents import Document

# Dynamically add project root to sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from resume_matcher.search import load_vectorstore
from services.reranker_llm import rerank_resumes

def semantic_search(query: str, top_k: int = 5) -> List[Document]:
    vectorstore = load_vectorstore()
    return vectorstore.similarity_search(query, k=top_k)

if __name__ == "__main__":
    query = input("🔍 Enter job description or query: ").strip()
    if not query:
        print("❗ No query provided. Exiting.")
        sys.exit(1)

    try:
        results = semantic_search(query, top_k=5)
        if not results:
            print("❗ No results found in vector DB.")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Semantic search failed: {e}")
        sys.exit(1)

    print("\n🔁 Reranking with Groq LLM...")
    try:
        best_resume = rerank_resumes(query, results)
    except Exception as e:
        print(f"[ERROR] Reranking failed: {e}")
        sys.exit(1)

    print("\n🎯 Best Matched Resume:\n")
    print(best_resume if isinstance(best_resume, str) else str(best_resume))
