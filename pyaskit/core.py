from . import config
from .models import models

model_name = config.get_model()
models_infos = [model for model in models if model["model_name"] == model_name]
model_info = models_infos[0] if models_infos else None
if model_info and model_info["api_name"] == "Gemini API":
    from .llm_gemini import chat_with_retry
else:
    from .llm_openai import chat_with_retry

chat_function = chat_with_retry
history = []


def get_history():
    return history


def clear_history():
    history.clear()


def set_chat_function(func):
    """Allows the user to set a custom chat function."""
    global chat_function
    chat_function = func


def chat(messages):
    content, completion = chat_function(messages)
    history.append(messages + [{"role": "assistant", "content": content}])
    return content, completion
