# 🤖 Local AI Chatbot using RAG + Flask + Ollama + ChromaDB

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.3-black.svg)
![LangChain](https://img.shields.io/badge/LangChain-1.2.10-green.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-1.5.2-orange.svg)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-purple.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📌 Project Overview

This project is a **Local AI Chatbot** built using **Retrieval-Augmented Generation (RAG).**

Instead of relying on generic AI knowledge, this chatbot answers user questions
**strictly based on your own private documents** — making it ideal for
enterprise knowledge bases, private document Q&A, and domain-specific AI assistants.

All processing happens **100% locally** on your machine — no external API calls,
no data sent to the cloud, complete privacy.

---

## 🧠 Key Features

- ✅ **100% Local** — No external API required, complete data privacy
- ✅ **RAG Pipeline** — Answers from your own documents, not generic AI knowledge
- ✅ **Vector Search** — Semantic similarity search using ChromaDB
- ✅ **Local LLM** — Powered by Ollama running on your machine
- ✅ **PDF + TXT Support** — Ingests and processes multiple document formats
- ✅ **Flask Web Interface** — Clean browser-based chat UI
- ✅ **Hallucination Control** — Responses grounded strictly in document context
- ✅ **Modular Architecture** — Clean, maintainable, and extensible codebase

---

## 🏗️ Architecture

User Query (Browser)
│
▼
Flask Web App (app.py)
│
▼
Vector Search — ChromaDB
(Finds most relevant document chunks)
│
▼
Context Injection — LangChain
(Injects retrieved context into prompt)
│
▼
Local LLM — Ollama
(Generates answer based strictly on context)
│
▼
Response → Browser

---

## 📂 Project Structure
llm-chatbot/
│
├── app.py                 # Flask web application — main entry point
├── ollama_client.py       # Handles communication with local Ollama LLM
├── document_loader.py     # Loads and splits documents into chunks
├── vector_store.py        # Creates embeddings and stores them in ChromaDB
├── memory_manager.py      # Manages conversation history and memory
├── prompt_builder.py      # Builds structured prompts for the LLM
├── config.py              # Central configuration settings
├── main.py                # Alternative CLI entry point
│
├── data/                  # Sample input documents (TXT format)
├── documents/             # Additional documents (PDF format)
├── templates/
│   └── chat.html          # Browser chat UI
│
├── requirements.txt       # Project dependencies
├── LICENSE                # MIT License
└── .gitignore             # Files excluded from Git tracking

---

## ⚙️ Setup Instructions

### 1. Prerequisites
- Python 3.10 or higher
- [Ollama](https://ollama.com) installed and running locally
- Git

### 2. Clone Repository
```bash
git clone https://github.com/sridharjamboju/llm-chatbot.git
cd llm-chatbot
```

### 3. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Pull Required Ollama Models
```bash
ollama pull mistral
ollama pull nomic-embed-text
```

### 6. Add Your Documents
Place your `.pdf` or `.txt` files inside the `documents/` folder.

### 7. Build Vector Store
```bash
python vector_store.py
```

### 8. Start the Application
```bash
python app.py
```

### 9. Open in Browser
http://127.0.0.1:5000

---

## 💡 Example Queries

Once you load your own documents, you can ask questions like:

- *"What are the key responsibilities mentioned in this document?"*
- *"Summarize the main points from the uploaded PDF."*
- *"What does the document say about [specific topic]?"*
- *"List all the technical skills mentioned in the document."*

---

## 🎯 Key Learnings & Concepts Demonstrated

- ✅ End-to-end **RAG pipeline** design and implementation
- ✅ **Semantic search** using vector embeddings
- ✅ **Hallucination control** through context grounding
- ✅ **Local LLM** deployment using Ollama
- ✅ **Vector database** management using ChromaDB
- ✅ **Modular Python** application architecture
- ✅ **Prompt engineering** with structured templates
- ✅ **Flask web application** development

---

## 🚀 Future Enhancements

- [ ] File upload support directly from browser
- [ ] Multi-document selection and filtering
- [ ] Source citation display with page numbers
- [ ] Conversation memory across sessions
- [ ] Deployment on AWS using Amazon Bedrock
- [ ] Streamlit UI version

---

## 👨‍💻 Author

**Sridhar Jamboju**
Aspiring AI/ML Engineer | GenAI | RAG | LLM Applications

[![GitHub](https://img.shields.io/badge/GitHub-sridharjamboju-black.svg)](https://github.com/sridharjamboju)


