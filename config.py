# config.py
# This file stores configuration variables used across the application

# Name of the LLM model used by Ollama
MODEL_NAME = "qwen2.5:1.5b"

# Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# Maximum number of messages stored in conversation memory
MAX_HISTORY = 10
