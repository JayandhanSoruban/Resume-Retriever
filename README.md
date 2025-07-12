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

* Load resume files (PDF or TXT) from `data/resumes`
* Convert them into LangChain-compatible documents
* Generate embeddings using a transformer model
* Store those embeddings in a persistent local vector store

#### 🔹 Command:

```bash
python resume_matcher/scripts/embed_resumes.py
```

Make sure your resume files are placed in the following folder structure:

```
resume_matcher/
├── data/
│   └── resumes/
│       ├── resume1.pdf
│       ├── resume2.txt
│       └── ...
```

> ✅ This step will create a persistent vector store under the `data/vectorstore/` folder.

---

Let me know if you also want to include instructions for running a search, deleting the vector store, or preventing duplicates.
