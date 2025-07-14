# Resume-Retriever
AI-powered microservice that retrieves, ranks, and selects the most relevant resumes based on a given job query using semantic search and LLM-based reranking.


### ✅ Step 1: Set Up Virtual Environment

It's recommended to use a virtual environment to isolate project dependencies.

#### 🔹 For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

#### 🔹 For macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### ✅ Step 2: Install Requirements

Make sure you're in the project root directory (where `requirements.txt` is located), then run:

```bash
pip install -r requirements.txt
```

### ✅ Step 3: Embed Resumes and Create Vector Store

Once dependencies are installed, run the following script to:

* Load resume files (PDF or TXT) from `data/Resumes`
* Convert them into LangChain-compatible documents
* Generate embeddings using a transformer model
* Store those embeddings in a persistent local vector store

#### 🔹 Command:

```bash
python resume_matcher/services/embed_resumes.py
```

Make sure your resume files are placed in the following folder structure:

```
resume_matcher/
├── data/
│   └── Resumes/
│       ├── resume1.pdf
│       ├── resume2.txt
│       └── ...
```

> ✅ This step will create a persistent vector store under the `resume_matcher/vectorstore/` folder.

---

Let me know if you also want to include instructions for running a search, deleting the vector store, or preventing duplicates.


### ✅ Step 4: Reset Vector Store (Optional – Use With Caution)
If you're planning to update the vector store with new or modified resumes, it's important to first delete the existing embeddings to prevent duplicates or inconsistencies.

🔹 Command:
bash

python resume_matcher/vector_store/reset_vector_store.py

⚠️ Caution: This will permanently delete all existing embeddings in the resume_matcher/vectorstore/ directory.
✅ Run this only when you're adding or updating resumes.
❌ Do not run this if you're only performing a search, as it will remove all existing vector data.

After resetting, re-run Step 3 to embed the updated resumes.

### ✅ Step 5: Run Semantic Search + LLM Reranking
Use this script to:

Search the top matching resumes based on semantic similarity

Rerank them using LLM to return the best match

🔹 Command:

bash
Copy
Edit
python semantic_search.py
🧠 You'll be prompted to enter the job description.

🎯 The LLM will evaluate and return the single best matching resume.




