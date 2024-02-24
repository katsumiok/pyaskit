import google.generativeai as genai
from . import config


def convert_role(role):
    if role == "assistant":
        return "model"
    return "user"


def convert_content(content):
    return [{"text": content}]


def convert_messages(messages):
    result = []
    for message in messages:
        role = convert_role(message["role"])
        content = convert_content(message["content"])
        result.append({"role": role, "parts": content})
    result.insert(1, {"role": "model", "parts": [{"text": "OK, I understand."}]})
    return result


model = genai.GenerativeModel(config.get_model())


def chat_with_retry(messages, max_retries=10):
    messages = convert_messages(messages)
    response = model.generate_content(messages)
    return response.text, response
