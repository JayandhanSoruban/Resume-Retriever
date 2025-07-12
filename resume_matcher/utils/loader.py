# utils/loader.py
from pathlib import Path
import fitz

folder_path= "D:\AGENTIC  AI\Resume Retrieval\resume_matcher\data\Resumes"

def load_resumes_from_folder(folder_path: str):
    resumes = []
    for file in Path(folder_path).glob("*"):
        if file.suffix == ".txt":
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
        elif file.suffix == ".pdf":
            doc = fitz.open(file)
            content = "\n".join([page.get_text() for page in doc])
            doc.close()
        else:
            continue
        
        resumes.append({
            "content": content,
            "metadata": {"filename": file.name}
        })

    return resumes
