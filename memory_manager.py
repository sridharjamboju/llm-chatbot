# =============================================================
# memory_manager.py
# Manages conversation history for the AI chatbot
#
# PURPOSE: This file is responsible for storing, managing,
# and retrieving the conversation history between the user
# and the AI. This gives the chatbot memory so it can
# understand the context of the current conversation.
#
# HOW IT WORKS:
# 1. Every message (user or AI) is stored in a list
# 2. Each message is stored as a dictionary with two keys:
#    - "role"    : who sent the message ("user" or "assistant")
#    - "content" : the actual text of the message
# 3. History is automatically trimmed to MAX_HISTORY messages
#    to prevent token overload and keep responses fast
#
# EXAMPLE of stored history:
# [
#   {"role": "user",      "content": "What is RAG?"},
#   {"role": "assistant", "content": "RAG stands for..."},
#   {"role": "user",      "content": "How does it work?"}
# ]
# =============================================================

from config import MAX_HISTORY


class MemoryManager:
    """
    Manages conversation history for the AI chatbot.

    This class stores messages as structured dictionaries
    so they can be easily used by prompt_builder.py to
    build context-aware prompts for the LLM.
    """

    def __init__(self):
        """
        Initialize the MemoryManager with an empty history list.
        Called automatically when a new MemoryManager is created.
        """
        # Empty list to store all conversation messages
        # Each item will be a dictionary: {"role": ..., "content": ...}
        self.history = []
        print("[memory_manager] Memory initialized.")

    def add_message(self, role, content):
        """
        Add a new message to the conversation history.

        PURPOSE: Stores each message as a structured dictionary
        so it can be easily processed by the prompt builder.

        Args:
            role (str): Who sent the message
                        Use "user" for user messages
                        Use "assistant" for AI responses
            content (str): The actual text of the message

        Example:
            memory.add_message("user", "What is machine learning?")
            memory.add_message("assistant", "Machine learning is...")
        """
        # -------------------------------------------------------------
        # Store message as a dictionary with role and content
        # This format is consistent with how prompt_builder.py
        # expects the history to be structured
        # -------------------------------------------------------------
        message = {
            "role": role,
            "content": content
        }
        self.history.append(message)

        # -------------------------------------------------------------
        # TRIM HISTORY TO MAX_HISTORY LIMIT
        # We keep only the most recent MAX_HISTORY messages
        # This prevents the prompt from becoming too long
        # which would slow down responses and increase token usage
        # -------------------------------------------------------------
        if len(self.history) > MAX_HISTORY:
            # Remove the oldest message to make room for the new one
            self.history = self.history[-MAX_HISTORY:]
            print(f"[memory_manager] History trimmed to {MAX_HISTORY} messages.")

        print(f"[memory_manager] Message added. Total messages: {len(self.history)}")

    def get_history(self):
        """
        Return the full conversation history as a list.

        PURPOSE: Provides the conversation history to
        prompt_builder.py so it can build context-aware prompts.

        Returns:
            list: List of message dictionaries
                  Each dict has "role" and "content" keys
                  Returns empty list if no messages stored yet
        """
        return self.history

    def clear_history(self):
        """
        Clear all conversation history.

        PURPOSE: Resets the conversation when starting a new
        chat session so previous messages do not affect
        the new conversation.
        """
        self.history = []
        print("[memory_manager] Conversation history cleared.")

    def is_empty(self):
        """
        Check if the conversation history is empty.

        PURPOSE: Allows other parts of the application to check
        if there are any previous messages before trying to
        use the history.

        Returns:
            bool: True if no messages stored, False otherwise
        """
        return len(self.history) == 0
    
    