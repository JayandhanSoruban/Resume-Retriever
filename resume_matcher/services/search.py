from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from resume_matcher.services.embedder import get_embedder

def load_vectorstore(persist_directory="data/vector_store"):
    embedding = get_embedder()
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embedding
    )
    return vectorstore

def semantic_search(query: str, top_k: int = 5) -> list[Document]:
    vectorstore = load_vectorstore()
    results = vectorstore.similarity_search(query, k=top_k)
    return results
