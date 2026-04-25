from langchain_community.document_loaders import DirectoryLoader
# from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma


# from rag.embeddings import get_embeddings


# from rag.embeddings import get_embeddings
from  embeddings import get_embeddings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_PATH = os.path.join(BASE_DIR, "data", "insurance_docs")
DB_PATH = os.path.join(BASE_DIR, "vector_db")

# DATA_PATH = "data/insurance_docs"
# DB_PATH = "vector_db"

def ingest_documents():

    loader = DirectoryLoader(DATA_PATH, glob="**/*.txt")
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(docs)

    embeddings = get_embeddings()

    vectordb = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory=DB_PATH
    )

    vectordb.persist()

    print("✅ Documents stored in vector DB")
    
    

if __name__ == "__main__":
    ingest_documents()