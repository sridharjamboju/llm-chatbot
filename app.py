# Import Flask and render_template
# render_template allows Flask to load HTML files from the templates folder
from flask import Flask, render_template, request, jsonify
from ollama_client import generate_response

# Create Flask application instance
app = Flask(__name__)


# Route for the homepage
# When user opens http://127.0.0.1:5000 this function runs
@app.route("/")
def home():

    # Load chat.html from the templates folder
    return render_template("chat.html")

@app.route("/chat", methods=["POST"])
def chat():

    # Get message sent from browser
    data = request.get_json()
    user_message = data["message"]

    # Temporary response (we will connect the AI later)
    reply = generate_response(user_message)

    # Send response back to browser
    return jsonify({"reply": reply})

# Start the Flask web server
if __name__ == "__main__":

    # Run the server locally
    app.run(debug=True)