# main.py
# Main entry point of the chatbot application

from memory_manager import MemoryManager
from prompt_builder import build_prompt
from ollama_client import generate_response

# Create memory manager instance
memory = MemoryManager()

print("AI Chatbot with Memory Started (type 'exit' to quit)\n")

while True:

    # Read user input
    user_input = input("You: ")

    # Exit condition
    if user_input.lower().strip() == "exit":
        print("Chatbot stopped.")
        break

    # Store user message
    memory.add_message("User", user_input)

    # Build prompt from conversation history
    prompt = build_prompt(memory.get_history())

    try:
        # Get response from the AI model
        ai_reply = generate_response(prompt)

        print("\nAI:", ai_reply, "\n")

        # Store AI response
        memory.add_message("AI", ai_reply)

    except Exception as error:
        print("\n[ERROR]", error)