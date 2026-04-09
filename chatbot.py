# Import the 'requests' library, which allows us to send HTTP requests (like POST, GET)
# This is a third-party library, so it must be installed via: pip install requests
import requests

# Define the AI model name to use with Ollama
# "mistral" is the name of the locally running LLM model served by Ollama
model = "mistral"

# Print a welcome message to the console when the chatbot starts
# The '\n' at the end adds a blank line for better readability
print("AI Chatbot Started (type 'exit' to quit)\n")

# Start an infinite loop so the chatbot keeps running until the user decides to quit
while True:

    # Prompt the user to type their message and store the input as a string
    # The 'input()' function pauses the program and waits for the user to press Enter
    user_input = input("You: ")

    # Check if the user typed 'exit' (case-insensitive using .lower())
    # .lower() converts the input to lowercase so 'EXIT', 'Exit', etc. also work
    if user_input.lower() == "exit":

        # Exit the while loop, which ends the chatbot session
        break

    # Send a POST request to the Ollama API running locally on port 11434
    # This is the endpoint that Ollama exposes to interact with AI models
    response = requests.post(

        # The URL of the locally running Ollama API endpoint for text generation
        "http://localhost:11434/api/generate",

        # Send the request body as JSON with the required parameters
        json={

            # Specify which AI model to use (defined earlier as "mistral")
            "model": model,

            # Pass the user's message as the prompt for the AI to respond to
            "prompt": user_input,

            # Disable streaming so we get the full response at once
            # If True, the response would come in chunks (like a typewriter effect)
            "stream": False
        }
    )

    # Parse the HTTP response body from JSON format into a Python dictionary
    # The Ollama API returns a JSON object, so .json() converts it for easy access
    result = response.json()

    # Print the AI's response to the console
    # result["response"] accesses the 'response' key from the returned JSON dictionary
    # '\n' before 'AI:' adds a blank line above for better readability
    print("\nAI:", result["response"])

    # Print an empty line after the AI's response for visual spacing between exchanges
    print()