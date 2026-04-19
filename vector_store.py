# vector_store.py
# Creates vector database from documents

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from document_loader import load_documents

CHROMA_PATH = "chroma_db"

def create_vector_store():

    # Load documents
    documents = load_documents()

    print("DEBUG: Documents loaded:", len(documents))

    # Initialize embedding model
    embedding_model = OllamaEmbeddings(model="nomic-embed-text")

    # Create vector DB (auto persists)
    db = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=CHROMA_PATH
    )

    print("Vector DB created successfully!")


if __name__ == "__main__":
    create_vector_store()