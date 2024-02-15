import os
import time
import random
import openai
from . import config


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=10, timeout=10)


def chat_with_retry(messages, max_retries=10):
    model = config.get_model()
    response = client.chat.completions.create(
        model=model,
        response_format={"type": "json_object"},
        messages=messages,
    )
    return response.choices[0].message.content, response
