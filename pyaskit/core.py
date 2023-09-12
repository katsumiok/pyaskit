from .llm_openai import chat_with_retry

chat_function = chat_with_retry


def set_chat_function(func):
    """Allows the user to set a custom chat function."""
    global chat_function
    chat_function = func


def chat(messages, max_retries=10):
    return chat_function(messages, max_retries)
