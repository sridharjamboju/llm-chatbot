# prompt_builder.py
# Responsible for constructing the prompt sent to the AI model

def build_prompt(history):
    """
    Convert conversation history list into a single prompt string.
    """
    return "\n".join(history)