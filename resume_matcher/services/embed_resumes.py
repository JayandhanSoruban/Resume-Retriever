import sys
import os
import json
import hashlib
from pathlib import Path

# ✅ Add ROOT dir to sys.path before any local imports
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
print("✅ sys.path root set to:", ROOT_DIR)

# ✅ Local imports (after sys.path is set)
from utils.loader import load_resumes_from_folder
from services.embedder import get_embedder
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

# 📦 Path to store known hashes
HASH_FILE_PATH = ROOT_DIR / "data" / "resume_hashes.json"
VECTOR_STORE_DIR = ROOT_DIR / "D:/AGENTIC  AI/Resume Retrieval/resume_matcher/vector_store"
RESUME_FOLDER = ROOT_DIR / "data" / "Resumes"

def load_existing_hashes():
    if HASH_FILE_PATH.exists():
        with open(HASH_FILE_PATH, "r") as f:
            return set(json.load(f))
    return set()

def save_hashes(hashes):
    with open(HASH_FILE_PATH, "w") as f:
        json.dump(list(hashes), f, indent=2)

def compute_hash(content: str) -> str:
    return hashlib.md5(content.encode('utf-8')).hexdigest()

def embed_and_store_resumes():
    # 1️⃣ Load resumes
    resume_data = load_resumes_from_folder(str(RESUME_FOLDER))
    print("📄 Loaded resumes:", len(resume_data))

    # 2️⃣ Load existing hashes
    existing_hashes = load_existing_hashes()
    new_hashes = set()
    new_documents = []

    # 3️⃣ Filter new unique resumes
    for entry in resume_data:
        content = entry["content"]
        doc_hash = compute_hash(content)
        if doc_hash not in existing_hashes:
            new_hashes.add(doc_hash)
            new_documents.append(Document(page_content=content, metadata=entry["metadata"]))

    if not new_documents:
        print("✅ No new resumes to embed. All already processed.")
        return

    print(f"🆕 New resumes to embed: {len(new_documents)}")

    # 4️⃣ Embed and store
    embedder = get_embedder()
    vectorstore = Chroma.from_documents(
        documents=new_documents,
        embedding=embedder,
        persist_directory=str(VECTOR_STORE_DIR)
    )

    # 5️⃣ Update known hashes
    all_hashes = existing_hashes.union(new_hashes)
    save_hashes(all_hashes)

    print(f"✅ Embedded and stored {len(new_documents)} new resumes.")

if __name__ == "__main__":
    embed_and_store_resumes()
