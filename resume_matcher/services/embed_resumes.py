import sys
import os
from pathlib import Path

# 🛣️ Set up ROOT path to import utils and services
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR)) if str(ROOT_DIR) not in sys.path else None

# ✅ Standard imports
from utils.loader import load_resumes_from_folder
from services.embedder import get_embedder
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

def embed_and_store_resumes():
    # 1️⃣ Load resumes
    resume_data = load_resumes_from_folder("data/resumes")

    # 2️⃣ Convert to LangChain documents
    documents = [
        Document(page_content=entry["content"], metadata=entry["metadata"])
        for entry in resume_data
    ]

    # 3️⃣ Load embedder model
    embedder = get_embedder()

    # 4️⃣ Store in Chroma vector database
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedder,
        persist_directory="data/vector_store"
    )

    # 5️⃣ Vectorstore is auto-persisted in latest Chroma
    print(f"✅ Embedded and stored {len(documents)} resumes.")

if __name__ == "__main__":
    embed_and_store_resumes()
