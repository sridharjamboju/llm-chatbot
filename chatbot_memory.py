# Import the requests library to make HTTP calls to the Ollama API
import requests

# Define the model name that Ollama will use
MODEL_NAME = "qwen2.5:1.5b"

# Define the Ollama API endpoint
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# List to store conversation history
conversation_history = []

# Display startup message
print("AI Chatbot with Memory Started (type 'exit' to quit)\n")

# Infinite loop so the chatbot keeps running
while True:

    # Get user input
    user_input = input("You: ")

    # Stop the chatbot if user types 'exit'
    if user_input.lower().strip() == "exit":
        print("Chatbot stopped.")
        break

    # Add user message to conversation history
    conversation_history.append(f"User: {user_input}")

    # Keep only the last 10 entries to prevent very long prompts
    conversation_history = conversation_history[-10:]

    # Build the prompt using conversation history
    prompt = "\n".join(conversation_history)

    try:
        # Send request to Ollama API
        response = requests.post(
            OLLAMA_API_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        # Check if HTTP request succeeded
        if response.status_code == 200:

            # Convert response into JSON dictionary
            result = response.json()

            # Extract AI response safely
            ai_reply = result.get("response")

            # If response field exists
            if ai_reply:
                print("\nAI:", ai_reply, "\n")

                # Save AI response in conversation history
                conversation_history.append(f"AI: {ai_reply}")

            else:
                # Handle unexpected API response structure
                print("\n[ERROR] API response missing 'response' field:")
                print(result)

        else:
            # Handle HTTP errors
            print("\n[ERROR] HTTP error from Ollama:", response.status_code)
            print(response.text)

    # Handle case where Ollama server is not reachable
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Cannot connect to Ollama. Make sure it is running.")

    # Handle timeout situations
    except requests.exceptions.Timeout:
        print("\n[ERROR] The request timed out.")

    # Catch any unexpected Python errors
    except Exception as error:
        print("\n[ERROR] Unexpected error:", error)
        