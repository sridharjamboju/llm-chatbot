# ollama_client.py
# Handles communication with the Ollama API

import requests
from config import MODEL_NAME, OLLAMA_API_URL

def generate_response(prompt):
    """
    Send prompt to Ollama and return the generated response.
    """

    response = requests.post(
        OLLAMA_API_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    # Check for successful response
    if response.status_code != 200:
        raise Exception(f"Ollama HTTP error: {response.status_code} - {response.text}")

    result = response.json()

    # Extract response text safely
    return result.get("response", "")