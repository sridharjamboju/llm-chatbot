# memory_manager.py
# This module manages conversation history for the chatbot

from config import MAX_HISTORY

class MemoryManager:
    """
    Class responsible for storing and managing conversation history.
    """

    def __init__(self):
        # Initialize an empty list to store messages
        self.history = []

    def add_message(self, role, message):
        """
        Add a message to conversation history.
        role: 'User' or 'AI'
        message: text content
        """
        self.history.append(f"{role}: {message}")

        # Trim history to keep only the most recent messages
        self.history = self.history[-MAX_HISTORY:]

    def get_history(self):
        """
        Return the full conversation history as a list.
        """
        return self.history
    
    