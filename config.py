# =============================================================
# config.py
# Central configuration file for the Local AI Chatbot project
#
# PURPOSE: This file stores ALL settings used across the
# application in one single place. If you need to change
# any setting — model name, folder path, database location —
# you only change it HERE and it applies everywhere.
# =============================================================

# -------------------------------------------------------------
# LLM MODEL SETTINGS
# These settings control which AI model is used and where
# Ollama is running on your local machine
# -------------------------------------------------------------

# The name of the LLM model loaded in Ollama
# Change this if you want to use a different model
# Example: "mistral", "llama3", "qwen2.5:1.5b"
MODEL_NAME = "qwen2.5:1.5b"

# The API endpoint where Ollama is running locally
# Default port for Ollama is 11434 — do not change unless
# you have configured Ollama to run on a different port
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Maximum seconds to wait for Ollama to respond before timing out
OLLAMA_TIMEOUT = 120

# -------------------------------------------------------------
# EMBEDDING MODEL SETTINGS
# Embeddings convert text into numbers so ChromaDB can
# perform semantic (meaning-based) search
# -------------------------------------------------------------

# The embedding model used to convert text into vectors
# nomic-embed-text is a lightweight and efficient embedding model
EMBEDDING_MODEL = "nomic-embed-text"

# -------------------------------------------------------------
# VECTOR DATABASE SETTINGS
# ChromaDB stores document embeddings for semantic search
# -------------------------------------------------------------

# Folder where ChromaDB stores your document embeddings
# This folder is created automatically when you run vector_store.py
CHROMA_PATH = "chroma_db"

# Number of relevant document chunks to retrieve per query
# Higher value = more context but slower response
# Lower value = faster response but less context
TOP_K_RESULTS = 2

# -------------------------------------------------------------
# DOCUMENT SETTINGS
# These settings control where your documents are stored
# and how they are split into chunks for processing
# -------------------------------------------------------------

# Folder where your PDF and TXT documents are stored
DOCUMENTS_PATH = "documents"

# Maximum size of each text chunk in characters
# Smaller chunks = more precise retrieval
# Larger chunks = more context per chunk
CHUNK_SIZE = 500

# Number of characters that overlap between consecutive chunks
# Overlap ensures important information is not lost at chunk boundaries
CHUNK_OVERLAP = 50

# -------------------------------------------------------------
# MEMORY SETTINGS
# Controls how much conversation history is remembered
# -------------------------------------------------------------

# Maximum number of messages stored in conversation memory
# Keeping this low saves tokens and improves response speed
MAX_HISTORY = 10