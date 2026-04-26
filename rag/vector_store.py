from langchain_chroma import Chroma
from rag.embeddings import get_embeddings

DB_PATH = "vector_db"

def get_vector_store():

    embeddings = get_embeddings()

    vectordb = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings
    )
    return vectordb