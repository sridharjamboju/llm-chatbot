# ollama_client.py
# Stable + working version (STRICT RAG, no chat mode)

import requests
from config import MODEL_NAME, OLLAMA_API_URL


def generate_response(context, question):
    """
    Generate grounded response using context + question
    """

    try:
        # Strong grounding prompt
        prompt = f"""
You are a strict question-answering system.

Rules:
- Answer ONLY from the context below
- Do NOT use any external knowledge
- Keep the answer short and exact
- If answer is not in context, say: I don't know

Context:
{context}

Question:
{question}

Answer:
"""

        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0
                }
            },
            timeout=120
        )

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.status_code} - {response.text}")

        result = response.json()

        return result.get("response", "").strip()

    except Exception as e:
        return f"Error: {str(e)}"