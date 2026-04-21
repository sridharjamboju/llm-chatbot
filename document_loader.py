# =============================================================
# document_loader.py
# Loads and splits documents for the RAG pipeline
#
# PURPOSE: This file is responsible for:
# 1. Automatically finding all documents in the documents folder
# 2. Loading PDF and TXT files into memory
# 3. Splitting documents into smaller chunks for storage
#    in ChromaDB so semantic search works accurately
#
# HOW IT WORKS:
# 1. Scans the documents folder for all PDF and TXT files
# 2. Loads each file using the appropriate loader
# 3. Splits loaded content into chunks using
#    RecursiveCharacterTextSplitter
# 4. Returns all chunks ready to be stored in ChromaDB
#
# WHY CHUNKING IS IMPORTANT:
# LLMs have a token limit — they cannot process very large
# documents at once. Splitting into chunks allows us to
# retrieve only the MOST RELEVANT parts of a document
# for each question, making responses faster and more accurate.
# =============================================================

import os

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Import settings from central config file
from config import DOCUMENTS_PATH, CHUNK_SIZE, CHUNK_OVERLAP


def load_documents():
    """
    Automatically load all PDF and TXT documents from the
    documents folder and split them into chunks.

    PURPOSE: Prepares documents for storage in ChromaDB by
    loading and splitting them into manageable chunks that
    can be retrieved efficiently during semantic search.

    Returns:
        list: A list of document chunks ready for ChromaDB storage
              Returns empty list if no documents found or error occurs
    """

    # -------------------------------------------------------------
    # STEP 1 — CHECK IF DOCUMENTS FOLDER EXISTS
    # Before trying to load files, verify the folder exists
    # This prevents crashes and gives a helpful error message
    # -------------------------------------------------------------
    if not os.path.exists(DOCUMENTS_PATH):
        print(f"[document_loader] ERROR: Documents folder not found: {DOCUMENTS_PATH}")
        print(f"[document_loader] Please create the folder and add your documents.")
        return []

    # -------------------------------------------------------------
    # STEP 2 — SCAN FOLDER FOR SUPPORTED FILES
    # Automatically find all PDF and TXT files in the folder
    # This is better than hardcoding specific filenames because
    # it works with ANY documents you add to the folder
    # -------------------------------------------------------------
    all_files = os.listdir(DOCUMENTS_PATH)

    # Filter only supported file types
    supported_files = [
        f for f in all_files
        if f.endswith(".pdf") or f.endswith(".txt")
    ]

    if not supported_files:
        print(f"[document_loader] WARNING: No PDF or TXT files found in {DOCUMENTS_PATH}")
        print(f"[document_loader] Please add your documents to the folder.")
        return []

    print(f"[document_loader] Found {len(supported_files)} document(s): {supported_files}")

    # -------------------------------------------------------------
    # STEP 3 — LOAD EACH DOCUMENT
    # Use the appropriate loader based on the file type:
    # - PyPDFLoader for PDF files
    # - TextLoader for TXT files
    # -------------------------------------------------------------
    all_documents = []

    for filename in supported_files:
        filepath = os.path.join(DOCUMENTS_PATH, filename)

        try:
            if filename.endswith(".pdf"):
                # PyPDFLoader extracts text from each page of the PDF
                loader = PyPDFLoader(filepath)
                print(f"[document_loader] Loading PDF: {filename}")

            elif filename.endswith(".txt"):
                # TextLoader reads plain text files
                loader = TextLoader(filepath, encoding="utf-8")
                print(f"[document_loader] Loading TXT: {filename}")

            # Load the document and add to our list
            documents = loader.load()
            all_documents.extend(documents)
            print(f"[document_loader] Successfully loaded: {filename}")

        except Exception as e:
            # If one file fails, skip it and continue with others
            print(f"[document_loader] ERROR loading {filename}: {str(e)}")
            continue

    if not all_documents:
        print(f"[document_loader] ERROR: No documents could be loaded.")
        return []

    print(f"[document_loader] Total documents loaded: {len(all_documents)}")

    # -------------------------------------------------------------
    # STEP 4 — SPLIT DOCUMENTS INTO CHUNKS
    # RecursiveCharacterTextSplitter splits text intelligently:
    # - It tries to split at paragraph breaks first
    # - Then sentence breaks
    # - Then word breaks
    # - This preserves the natural flow and meaning of the text
    #
    # CHUNK_SIZE: Maximum characters per chunk (from config.py)
    # CHUNK_OVERLAP: Characters shared between adjacent chunks
    #               This ensures information at chunk boundaries
    #               is not lost during retrieval
    # -------------------------------------------------------------
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(all_documents)

    print(f"[document_loader] Total chunks created: {len(chunks)}")
    print(f"[document_loader] Chunk size: {CHUNK_SIZE} | Overlap: {CHUNK_OVERLAP}")

    return chunks


# -------------------------------------------------------------
# DIRECT EXECUTION — FOR TESTING ONLY
# Run this file directly to test document loading:
# python document_loader.py
# -------------------------------------------------------------
if __name__ == "__main__":
    print("[document_loader] Running in test mode...")
    chunks = load_documents()
    print(f"\n[document_loader] Test complete. {len(chunks)} chunks ready for ChromaDB.")
    