import sys
from pathlib import Path

# ✅ Set ROOT_DIR for local imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
print("✅ sys.path root set to:", ROOT_DIR)

# ✅ Local imports
from utils.loader import load_resumes_from_folder
from services.embedder import get_embedder
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# 📁 Paths
VECTOR_STORE_DIR = ROOT_DIR / "D:/AGENTIC  AI/Resume Retrieval/resume_matcher/vector_store"
RESUME_FOLDER = ROOT_DIR / "data" / "Resumes"

def embed_and_store_resumes():
    # 1️⃣ Load all resumes
    resume_data = load_resumes_from_folder(str(RESUME_FOLDER))
    print("📄 Loaded resumes:", len(resume_data))

    # 2️⃣ Convert to LangChain Documents
    documents = [
        Document(page_content=entry["content"], metadata=entry["metadata"])
        for entry in resume_data
    ]

    # 3️⃣ Embed and store in Chroma
    embedder = get_embedder()
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedder,
        persist_directory=str(VECTOR_STORE_DIR)
    )

    print(f"✅ Embedded and stored {len(documents)} resumes.")

if __name__ == "__main__":
    embed_and_store_resumes()
