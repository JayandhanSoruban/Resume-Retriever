from resume_matcher.services.search import semantic_search
from resume_matcher.services.reranker_llm import rerank_resumes
import sys
from pathlib import Path

# Ensure root path is in sys.path
root_path = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_path))


if __name__ == "__main__":
    query = input("🔍 Enter job description or query: ")
    
    # Step 1: Do semantic search
    results = semantic_search(query, top_k=5)

    print("\n📄 Top-K Semantic Search Results:")
    for i, doc in enumerate(results):
        print(f"\n--- RESULT {i+1} ---")
        print("📄 Metadata:", doc.metadata)
        print("🧠 Content:", doc.page_content[:300], "...")  # preview

    # Step 2: Rerank with Groq LLM
    print("\n🔁 Reranking with Groq LLM...")
    best_resume = rerank_resumes(query, results)

    print("\n🎯 Best Matched Resume:\n")
    print(best_resume)
