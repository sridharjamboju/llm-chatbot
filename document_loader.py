# document_loader.py
# Improved document loading + better chunking for accurate retrieval

from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():

    documents = []

    # Load text file
    text_loader = TextLoader("data/sample.txt")
    documents.extend(text_loader.load())

    # Load PDF file
    pdf_loader = PyPDFLoader("data/sample.pdf")
    documents.extend(pdf_loader.load())

    # 🔥 IMPROVED SPLITTING (VERY IMPORTANT)
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,     # bigger chunks → more complete info
        chunk_overlap=200    # overlap → avoids losing definitions
    )

    chunks = splitter.split_documents(documents)

    print(f"Loaded {len(chunks)} document chunks")

    # 🔥 DEBUG: print chunks
    for i, chunk in enumerate(chunks):
        print(f"\n--- Chunk {i} ---\n{chunk.page_content}")

    return chunks


if __name__ == "__main__":
    load_documents()