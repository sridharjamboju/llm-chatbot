# =============================================================
# prompt_builder.py
# Responsible for constructing structured prompts for the LLM
#
# PURPOSE: This file builds well structured prompts that are
# sent to the Ollama LLM. A good prompt has three parts:
#
# 1. SYSTEM PROMPT — tells the LLM how to behave, its role,
#    tone, and rules it must follow
#
# 2. CONVERSATION HISTORY — previous messages in the chat
#    so the LLM understands the context of the conversation
#
# 3. CURRENT QUESTION — the latest question from the user
#
# WHY THIS MATTERS:
# The quality of the prompt directly determines the quality
# of the LLM response. A well structured prompt produces
# accurate, relevant, and consistent answers.
# =============================================================

from config import MAX_HISTORY


# -------------------------------------------------------------
# SYSTEM PROMPT
# This is the instruction given to the LLM at the start of
# every conversation. It defines:
# - The role of the LLM (who it is)
# - The rules it must follow (what it can and cannot do)
# - The tone it should use (how it should respond)
# -------------------------------------------------------------
SYSTEM_PROMPT = """You are a helpful and precise AI assistant.

Your rules:
- Answer ONLY based on the context and conversation history provided
- Do NOT use any external or pretrained knowledge
- Keep your answers clear, concise, and factual
- If the answer is not found in the provided context, say: "I don't know based on the provided documents."
- Do NOT make up information or guess
- Always maintain a professional and helpful tone"""


def build_prompt(context, question, history=None):
    """
    Build a structured prompt combining system instructions,
    conversation history, retrieved context, and current question.

    PURPOSE: Creates a complete, well structured prompt that gives
    the LLM everything it needs to generate an accurate response.

    Args:
        context (str): Relevant document chunks retrieved from ChromaDB
        question (str): The current question from the user
        history (list): Optional list of previous conversation messages
                        Each item is a dict with 'role' and 'content' keys
                        Example: [{"role": "user", "content": "Hello"}]

    Returns:
        str: A complete structured prompt ready to be sent to the LLM
    """

    # -------------------------------------------------------------
    # STEP 1 — START WITH SYSTEM PROMPT
    # Always begin with the system instructions so the LLM
    # knows its role and rules before anything else
    # -------------------------------------------------------------
    prompt_parts = []
    prompt_parts.append(f"SYSTEM INSTRUCTIONS:\n{SYSTEM_PROMPT}")

    # -------------------------------------------------------------
    # STEP 2 — ADD CONVERSATION HISTORY (if available)
    # Including previous messages helps the LLM understand
    # the context of the current question
    # We limit history to MAX_HISTORY to save tokens
    # -------------------------------------------------------------
    if history:
        # Take only the most recent messages up to MAX_HISTORY limit
        recent_history = history[-MAX_HISTORY:]

        prompt_parts.append("\nCONVERSATION HISTORY:")

        for message in recent_history:
            # Format each message clearly showing who said what
            role = message.get("role", "unknown").upper()
            content = message.get("content", "")
            prompt_parts.append(f"{role}: {content}")

    # -------------------------------------------------------------
    # STEP 3 — ADD RETRIEVED DOCUMENT CONTEXT
    # This is the most important part for RAG
    # It gives the LLM the relevant information from your documents
    # so it can answer based on YOUR data, not general knowledge
    # -------------------------------------------------------------
    prompt_parts.append(f"\nRELEVANT CONTEXT FROM DOCUMENTS:\n{context}")

    # -------------------------------------------------------------
    # STEP 4 — ADD THE CURRENT QUESTION
    # Always end with the question so the LLM knows exactly
    # what it needs to answer
    # -------------------------------------------------------------
    prompt_parts.append(f"\nCURRENT QUESTION:\n{question}")
    prompt_parts.append("\nANSWER:")

    # -------------------------------------------------------------
    # STEP 5 — JOIN ALL PARTS TOGETHER
    # Combine all sections into one complete prompt string
    # Each section is separated by a blank line for clarity
    # -------------------------------------------------------------
    complete_prompt = "\n".join(prompt_parts)

    return complete_prompt

