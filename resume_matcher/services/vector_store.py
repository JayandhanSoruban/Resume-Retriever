# services/vector_store.py
from langchain.vectorstores import Chroma
from langchain.schema.document import Document
import os

def init_vector_store(persist_directory: str, embedding):
    return Chroma(persist_directory=persist_directory, embedding_function=embedding)

def add_documents_to_store(docs: list[dict], store):
    documents = [Document(page_content=doc["content"], metadata=doc["metadata"]) for doc in docs]
    store.add_documents(documents)
    store.persist()
