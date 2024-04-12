import google.generativeai as genai
import time
import random
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
    base_wait_time = 1  # wait time in seconds
    for i in range(max_retries):
        try:
            response = model.generate_content(messages)
            return response.text, response
        except Exception as e:
            wait_time = base_wait_time * 2**i
            wait_time = min(wait_time, 30)
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))
    raise Exception(f"Failed to get response after {max_retries} attempts")
