from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_groq import ChatGroq
from typing import List
from langchain_core.documents import Document
import os

# Load LLM (e.g., Mixtral or LLaMA3)
llm = ChatGroq(temperature=0.1, model_name="llama3-70b-8192")

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["query", "resumes"],
    template="""
You are a recruitment expert. Based on the query: "{query}", analyze the following resumes and rank them by relevance.

Return the **best matching resume only**, without any explanation.

Resumes:
{resumes}
"""
)

# Create runnable chain
chain: Runnable = prompt_template | llm

# Function to rerank resumes using Groq LLM
def rerank_resumes(query: str, docs: List[Document]) -> str:
    resume_contents = "\n\n".join([f"Resume {i+1}:\n{doc.page_content}" for i, doc in enumerate(docs)])
    result = chain.invoke({"query": query, "resumes": resume_contents})
    return result.content
