# =============================================================
# vector_store.py
# Creates and manages the ChromaDB vector database
#
# PURPOSE: This file is responsible for:
# 1. Loading all document chunks from document_loader.py
# 2. Converting each chunk into a vector (embedding)
#    using the Ollama embedding model
# 3. Storing all vectors in ChromaDB for fast semantic search
#
# HOW EMBEDDINGS WORK:
# An embedding is a list of numbers that represents the
# MEANING of a piece of text. Similar texts will have
# similar numbers. This allows ChromaDB to find the most
# relevant document chunks for any given question.
#
# EXAMPLE:
# "What is machine learning?" and "Define ML" will have
# very similar embeddings even though they use different words
#
# HOW TO RUN THIS FILE:
# Run once to build the vector database:
# python vector_store.py
# You only need to re-run it when you add new documents
# =============================================================

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from document_loader import load_documents

# Import settings from central config file
from config import CHROMA_PATH, EMBEDDING_MODEL


def create_vector_store():
    """
    Create ChromaDB vector store from loaded documents.

    PURPOSE: Converts all document chunks into vector embeddings
    and stores them in ChromaDB so they can be retrieved
    efficiently during semantic search.

    HOW IT WORKS:
    1. Loads all document chunks from document_loader.py
    2. Initialises the Ollama embedding model
    3. Converts each chunk into a vector embedding
    4. Stores all embeddings in ChromaDB
    5. ChromaDB automatically saves to disk for future use

    Returns:
        Chroma: The created vector database object
                Returns None if creation fails
    """

    # -------------------------------------------------------------
    # STEP 1 — LOAD DOCUMENT CHUNKS
    # Get all document chunks from document_loader.py
    # These are the text pieces that will be converted to vectors
    # -------------------------------------------------------------
    print("[vector_store] Starting vector store creation...")
    print("[vector_store] Loading documents...")

    documents = load_documents()

    # -------------------------------------------------------------
    # STEP 2 — VALIDATE DOCUMENTS
    # Check if any documents were loaded before proceeding
    # If no documents found, we cannot create the vector store
    # -------------------------------------------------------------
    if not documents:
        print("[vector_store] ERROR: No documents loaded.")
        print("[vector_store] Please add PDF or TXT files to the documents folder.")
        print("[vector_store] Then run this file again: python vector_store.py")
        return None

    print(f"[vector_store] Successfully loaded {len(documents)} document chunks.")

    # -------------------------------------------------------------
    # STEP 3 — INITIALISE EMBEDDING MODEL
    # OllamaEmbeddings converts text into numerical vectors
    # We use nomic-embed-text — a lightweight embedding model
    # that runs locally through Ollama
    # -------------------------------------------------------------
    print(f"[vector_store] Initialising embedding model: {EMBEDDING_MODEL}")

    try:
        embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)
        print(f"[vector_store] Embedding model ready.")

    except Exception as e:
        print(f"[vector_store] ERROR: Could not initialise embedding model: {str(e)}")
        print(f"[vector_store] Please make sure Ollama is running and {EMBEDDING_MODEL} is installed.")
        print(f"[vector_store] Run: ollama pull {EMBEDDING_MODEL}")
        return None

    # -------------------------------------------------------------
    # STEP 4 — CREATE CHROMADB VECTOR STORE
    # Chroma.from_documents() does three things:
    # 1. Takes each document chunk
    # 2. Converts it to a vector using the embedding model
    # 3. Stores the vector in ChromaDB at CHROMA_PATH
    #
    # persist_directory tells ChromaDB where to save the database
    # on your disk so it is available next time you run the app
    # -------------------------------------------------------------
    print(f"[vector_store] Creating ChromaDB at: {CHROMA_PATH}")
    print(f"[vector_store] This may take a few minutes for large documents...")

    try:
        db = Chroma.from_documents(
            documents=documents,
            embedding=embedding_model,
            persist_directory=CHROMA_PATH
        )

        print(f"[vector_store] ✅ Vector store created successfully!")
        print(f"[vector_store] Total vectors stored: {len(documents)}")
        print(f"[vector_store] Database saved at: {CHROMA_PATH}")

        return db

    except Exception as e:
        print(f"[vector_store] ERROR: Could not create vector store: {str(e)}")
        return None


# -------------------------------------------------------------
# DIRECT EXECUTION — Run this file to build the vector store
# python vector_store.py
#
# You need to run this:
# 1. When setting up the project for the first time
# 2. When you add new documents to the documents folder
# -------------------------------------------------------------
if __name__ == "__main__":
    print("[vector_store] Running vector store builder...")
    db = create_vector_store()

    if db:
        print("\n[vector_store] ✅ Setup complete! You can now run the chatbot.")
        print("[vector_store] Start the app with: python app.py")
    else:
        print("\n[vector_store] ❌ Setup failed. Please check the errors above.")