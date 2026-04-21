# =============================================================
# ollama_client.py
# Handles all communication with the local Ollama LLM server
#
# PURPOSE: This file is responsible for sending questions to
# the locally running Ollama LLM and returning the generated
# response back to the application.
#
# HOW IT WORKS:
# 1. Receives document context and user question as input
# 2. Builds a strict RAG prompt that forces the LLM to answer
#    ONLY from the provided context
# 3. Sends the prompt to Ollama via HTTP POST request
# 4. Returns the generated answer to the caller
# =============================================================

import requests

# Import settings from central config file
# This ensures all settings are managed in one place
from config import MODEL_NAME, OLLAMA_API_URL, OLLAMA_TIMEOUT


def generate_response(context, question):
    """
    Generate a grounded response using retrieved document context.

    This function implements STRICT RAG (Retrieval Augmented Generation):
    - The LLM is instructed to answer ONLY from the provided context
    - It will NOT use any external or pretrained knowledge
    - This prevents hallucination and ensures factual accuracy

    Args:
        context (str): Relevant document chunks retrieved from ChromaDB
        question (str): The user's question to be answered

    Returns:
        str: The LLM generated answer based strictly on the context
             Returns an error message if something goes wrong
    """

    try:
        # -------------------------------------------------------------
        # BUILD THE RAG PROMPT
        # This prompt is carefully designed to:
        # 1. Force the LLM to use ONLY the provided context
        # 2. Prevent hallucination by blocking external knowledge
        # 3. Keep answers short, precise, and factual
        # -------------------------------------------------------------
        prompt = f"""
You are a strict question-answering system.

Rules:
- Answer ONLY from the context provided below
- Do NOT use any external or pretrained knowledge
- Keep the answer short, precise, and factual
- If the answer is not found in the context, respond with: "I don't know based on the provided documents."

Context:
{context}

Question:
{question}

Answer:
"""

        # -------------------------------------------------------------
        # SEND REQUEST TO OLLAMA
        # We send the prompt to the locally running Ollama server
        # stream=False means we wait for the complete response
        # temperature=0 means deterministic responses (no randomness)
        # -------------------------------------------------------------
        print(f"\n[ollama_client] Sending request to Ollama...")
        print(f"[ollama_client] Model: {MODEL_NAME}")

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,        # Wait for complete response
                "options": {
                    "temperature": 0    # 0 = factual, consistent responses
                                        # 1 = creative, varied responses
                }
            },
            timeout=OLLAMA_TIMEOUT      # Maximum seconds to wait for response
        )

        # -------------------------------------------------------------
        # HANDLE ERRORS
        # Check if Ollama returned a successful response (HTTP 200)
        # If not, raise an exception with the error details
        # -------------------------------------------------------------
        if response.status_code != 200:
            raise Exception(
                f"Ollama returned error {response.status_code}: {response.text}"
            )

        # -------------------------------------------------------------
        # EXTRACT AND RETURN THE ANSWER
        # The response is a JSON object
        # The actual answer text is inside the "response" key
        # .strip() removes any extra whitespace from beginning and end
        # -------------------------------------------------------------
        result = response.json()
        answer = result.get("response", "").strip()

        print(f"[ollama_client] Response received successfully.")

        return answer

    except requests.exceptions.Timeout:
        # This happens if Ollama takes too long to respond
        error_msg = "Error: Ollama request timed out. Please check if Ollama is running."
        print(f"[ollama_client] TIMEOUT ERROR: {error_msg}")
        return error_msg

    except requests.exceptions.ConnectionError:
        # This happens if Ollama is not running on your machine
        error_msg = "Error: Cannot connect to Ollama. Please make sure Ollama is running."
        print(f"[ollama_client] CONNECTION ERROR: {error_msg}")
        return error_msg

    except Exception as e:
        # This catches any other unexpected errors
        error_msg = f"Error: {str(e)}"
        print(f"[ollama_client] UNEXPECTED ERROR: {error_msg}")
        return error_msg