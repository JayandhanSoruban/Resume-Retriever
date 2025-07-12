# reranker_llm.py
from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from typing import List
from langchain_core.documents import Document
import os
from dotenv import load_dotenv

def initialize_llm():
    """Initialize the Groq LLM with error handling."""
    env_path = "D:/AGENTIC AI/Resume Retrieval/.env"
    
    # Check if .env file exists
    if not os.path.exists(env_path):
        print(f"[ERROR] .env file not found at: {env_path}")
        api_key = input("🔑 Please enter your GROQ_API_KEY: ").strip()
        if not api_key:
            print("[ERROR] No API key provided. Exiting.")
            raise ValueError("No API key provided")
        os.environ["GROQ_API_KEY"] = api_key
    else:
        load_dotenv(dotenv_path=env_path)
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print(f"[ERROR] GROQ_API_KEY not found in {env_path}.")
            api_key = input("🔑 Please enter your GROQ_API_KEY: ").strip()
            if not api_key:
                print("[ERROR] No API key provided. Exiting.")
                raise ValueError("No API key provided")
            os.environ["GROQ_API_KEY"] = api_key

    # Debug
    print("[DEBUG] GROQ_API_KEY =", api_key)
    print("[DEBUG] GROQ_API_KEY length =", len(api_key))

    # Initialize LLM
    try:
        llm = ChatGroq(
            temperature=0.1,
            model_name="llama3-70b-8192",
            groq_api_key=api_key
        )
        print("[DEBUG] LLM initialized successfully")
        return llm
    except Exception as e:
        print("[ERROR] Failed to initialize LLM:", str(e))
        raise

def rerank_resumes(query: str, docs: List[Document]) -> str:
    """Rerank resumes using Groq LLM and return the best match."""
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

    # Initialize LLM
    llm = initialize_llm()

    # Chain: prompt -> LLM
    chain: Runnable = prompt_template | llm

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
        print("[ERROR] LLM call failed:", str(e))
        return "❗ Failed to rerank resumes due to LLM error."