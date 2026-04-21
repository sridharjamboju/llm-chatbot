# =============================================================
# app.py
# Main Flask web application — Entry point of the chatbot
#
# PURPOSE: This is the main file that runs the entire chatbot
# application. It brings together ALL other modules:
# - vector_store / ChromaDB — for document retrieval
# - memory_manager — for conversation history
# - prompt_builder — for building structured prompts
# - ollama_client — for generating LLM responses
#
# HOW IT WORKS:
# 1. User types a question in the browser
# 2. Flask receives the question via the /chat route
# 3. ChromaDB searches for relevant document chunks
# 4. Memory manager adds the question to history
# 5. Prompt builder creates a structured prompt
# 6. Ollama client sends prompt to LLM and gets response
# 7. Response is sent back to the browser
#
# HOW TO RUN:
# python app.py
# Then open: http://127.0.0.1:5000
# =============================================================

from flask import Flask, render_template, request, jsonify
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Import our custom modules
from ollama_client import generate_response
from memory_manager import MemoryManager
from prompt_builder import build_prompt

# Import settings from central config file
from config import CHROMA_PATH, EMBEDDING_MODEL, TOP_K_RESULTS

# -------------------------------------------------------------
# INITIALISE FLASK APPLICATION
# Flask is the web framework that handles browser requests
# and serves the chat interface
# -------------------------------------------------------------
app = Flask(__name__)

# -------------------------------------------------------------
# INITIALISE CHROMADB CONNECTION
# Connect to the existing ChromaDB vector database
# This must be created first by running: python vector_store.py
#
# OllamaEmbeddings converts user questions into vectors
# so ChromaDB can find the most relevant document chunks
# -------------------------------------------------------------
print("[app] Initialising ChromaDB connection...")

embedding_model = OllamaEmbeddings(model=EMBEDDING_MODEL)

vector_db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

print(f"[app] ChromaDB connected successfully at: {CHROMA_PATH}")

# -------------------------------------------------------------
# INITIALISE MEMORY MANAGER
# Creates a single memory manager instance for the session
# This stores the conversation history throughout the session
# -------------------------------------------------------------
memory = MemoryManager()
print("[app] Memory manager initialised.")


# -------------------------------------------------------------
# ROUTE 1 — HOME PAGE
# Serves the chat HTML interface when user opens the browser
# render_template looks for chat.html in the templates folder
# -------------------------------------------------------------
@app.route("/")
def home():
    """Serve the main chat interface."""
    return render_template("chat.html")


# -------------------------------------------------------------
# ROUTE 2 — CHAT ENDPOINT
# This is the main route that handles all chat messages
# It receives POST requests from the browser with user messages
# and returns AI generated responses as JSON
# -------------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    """
    Handle incoming chat messages and return AI responses.

    PURPOSE: This is the core function of the chatbot. It
    orchestrates the entire RAG pipeline:
    1. Receives user message from browser
    2. Validates the input
    3. Retrieves relevant document chunks from ChromaDB
    4. Builds a structured prompt with context and history
    5. Generates a response using the Ollama LLM
    6. Stores the exchange in memory
    7. Returns the response to the browser

    Returns:
        JSON: {"reply": "AI response text"}
    """

    try:
        # -------------------------------------------------------------
        # STEP 1 — RECEIVE AND VALIDATE USER MESSAGE
        # Get the JSON data sent from the browser
        # Validate that message exists and is not empty
        # -------------------------------------------------------------
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"reply": "Error: No message received."})

        user_message = data["message"].strip()

        if not user_message:
            return jsonify({"reply": "Please type a message before sending."})

        print(f"\n[app] User message received: {user_message}")

        # -------------------------------------------------------------
        # STEP 2 — RETRIEVE RELEVANT DOCUMENT CHUNKS
        # ChromaDB performs semantic search to find the most
        # relevant chunks from your documents for this question
        # TOP_K_RESULTS controls how many chunks are retrieved
        # -------------------------------------------------------------
        print(f"[app] Searching ChromaDB for relevant context...")

        results = vector_db.similarity_search(user_message, k=TOP_K_RESULTS)

        if not results:
            return jsonify({
                "reply": "I could not find relevant information in the documents. Please make sure your documents are loaded."
            })

        print(f"[app] Found {len(results)} relevant document chunks.")

        # -------------------------------------------------------------
        # STEP 3 — BUILD CONTEXT FROM RETRIEVED CHUNKS
        # Join all retrieved chunks into a single context string
        # This context will be injected into the prompt so the
        # LLM can answer based on YOUR documents
        # -------------------------------------------------------------
        context = "\n\n".join([doc.page_content for doc in results])

        # -------------------------------------------------------------
        # STEP 4 — BUILD STRUCTURED PROMPT
        # Use prompt_builder to create a well structured prompt
        # that includes system instructions, conversation history,
        # retrieved context, and the current question
        # -------------------------------------------------------------
        conversation_history = memory.get_history()

        prompt = build_prompt(
            context=context,
            question=user_message,
            history=conversation_history
        )

        # -------------------------------------------------------------
        # STEP 5 — GENERATE AI RESPONSE
        # Send the structured prompt to Ollama LLM
        # and get the generated response back
        # -------------------------------------------------------------
        print(f"[app] Generating response from LLM...")

        reply = generate_response(context, user_message)

        print(f"[app] Response generated successfully.")

        # -------------------------------------------------------------
        # STEP 6 — STORE EXCHANGE IN MEMORY
        # Save both the user message and AI response to memory
        # so future questions can reference this conversation
        # -------------------------------------------------------------
        memory.add_message("user", user_message)
        memory.add_message("assistant", reply)

        # -------------------------------------------------------------
        # STEP 7 — RETURN RESPONSE TO BROWSER
        # Send the AI response back as JSON
        # The browser JavaScript will display it in the chat UI
        # -------------------------------------------------------------
        return jsonify({"reply": reply})

    except Exception as e:
        # Catch any unexpected errors and return a helpful message
        print(f"[app] ERROR: {str(e)}")
        return jsonify({"reply": f"An error occurred: {str(e)}"})


# -------------------------------------------------------------
# ROUTE 3 — CLEAR CONVERSATION
# Allows the user to reset the conversation history
# Called when user clicks a "Clear Chat" button in the UI
# -------------------------------------------------------------
@app.route("/clear", methods=["POST"])
def clear_chat():
    """Clear the conversation history and start fresh."""
    memory.clear_history()
    print("[app] Conversation history cleared.")
    return jsonify({"status": "Conversation cleared successfully."})


# -------------------------------------------------------------
# APPLICATION ENTRY POINT
# This block runs when you execute: python app.py
# debug=True enables auto-reload when you change code
# Set debug=False when deploying to production
# -------------------------------------------------------------
if __name__ == "__main__":
    print("[app] Starting Local AI Chatbot...")
    print("[app] Make sure Ollama is running before starting.")
    print("[app] Open your browser at: http://127.0.0.1:5000")
    app.run(debug=True)