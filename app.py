# app.py

from flask import Flask, render_template, request, jsonify
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from ollama_client import generate_response

CHROMA_PATH = "chroma_db"

embedding_model = OllamaEmbeddings(model="nomic-embed-text")

vector_db = Chroma(
    persist_directory=CHROMA_PATH,
    embedding_function=embedding_model
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("chat.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data["message"]

        print("\nUSER:", user_message)

        # Retrieve docs
        results = vector_db.similarity_search(user_message, k=2)

        print("DEBUG docs:", len(results))

        if len(results) == 0:
            return jsonify({"reply": "I don't know"})

        # Build context
        context = "\n".join([doc.page_content for doc in results])

        print("CONTEXT:\n", context)

        # 🔥 CORRECT CALL
        reply = generate_response(context, user_message)

        print("AI:", reply)

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"reply": f"Error: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)