from . import config
from .models import models

model_name = config.get_model()
models_infos = [model for model in models if model["model_name"] == model_name]
model_info = models_infos[0] if models_infos else None
if model_info is None:
    raise ValueError(f"Model {model_name} not found in models")
if model_info and model_info["api_name"] == "Gemini API":
    from .llm_gemini import chat_with_retry
elif model_info and model_info["api_name"] == "Claude API":
    from .llm_claude import chat_with_retry
elif model_info and model_info["api_name"] == "Cohere API":
    from .llm_cohere import chat_with_retry
elif model_info and model_info["api_name"] == "groq API":
    from .llm_gloq import chat_with_retry
else:
    from .llm_openai import chat_with_retry

chat_function = chat_with_retry


def set_chat_function(func):
    """Allows the user to set a custom chat function."""
    global chat_function
    chat_function = func


def chat(messages):
    content, completion = chat_function(messages)
    return content, completion
