# 🚀 Local AI Chatbot (RAG) using Flask + Ollama + ChromaDB

## 📌 Project Overview

This project is a **Local AI Chatbot** built using Retrieval-Augmented Generation (RAG).
It answers user questions based strictly on custom documents instead of relying on generic AI knowledge.

---

## 🧠 Key Features

* ✅ Local LLM using Ollama (No external API required)
* ✅ Retrieval-Augmented Generation (RAG)
* ✅ Vector database using ChromaDB
* ✅ Document ingestion (PDF + TXT)
* ✅ Flask-based web interface
* ✅ Context-aware responses (no hallucination)
* ✅ Clean and modular architecture

---

## 🏗️ Architecture

User Query → Flask API → Vector Search (ChromaDB) → Context Injection → LLM (Ollama) → Response

---

## 📂 Project Structure

```
llm-chatbot/
│
├── app.py                 # Flask web app
├── ollama_client.py       # LLM interaction
├── document_loader.py     # Load & split documents
├── vector_store.py        # Create embeddings & DB
│
├── data/                  # Sample input documents
├── documents/             # Additional documents
├── templates/
│   └── chat.html          # UI
│
└── chroma_db/             # Vector DB (ignored in Git)
```

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```
git clone https://github.com/sridharjamboju/llm-chatbot.git
cd llm-chatbot
```

### 2. Install Dependencies

```
pip install flask langchain chromadb langchain-community langchain-ollama pypdf
```

### 3. Run Vector Store

```
python vector_store.py
```

### 4. Start Application

```
python app.py
```

### 5. Open in Browser

```
http://127.0.0.1:5000
```

---

## 💡 Example Queries

* What is AI?
* What is AWS?

---

## 🎯 Key Learnings

* Implemented end-to-end RAG pipeline
* Controlled LLM hallucination using context grounding
* Built local AI system without external APIs
* Hands-on with embeddings, vector DB, and prompt engineering

---

## 🚀 Future Enhancements

* File upload support
* Chat memory (conversation context)
* Source citation display
* Deployment on cloud

---

## 👨‍💻 Author

Sridhar Jamboju
