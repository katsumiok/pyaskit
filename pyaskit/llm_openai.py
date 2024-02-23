import os
import time
import random
import openai
from . import config
from .models import models

model_name = os.getenv("ASKIT_MODEL")

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"), max_retries=0)


def chat_with_retry(messages, max_retries=10):
    model = config.get_model()
    base_wait_time = 1  # wait time in seconds
    for i in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content, response
        except (
            openai.APIError,
            openai.APITimeoutError,
            openai.APIConnectionError,
            openai.RateLimitError,
            openai.InternalServerError,
        ):

            # https://platform.openai.com/docs/guides/error-codes/python-library-error-types
            wait_time = base_wait_time * 2**i
            wait_time = min(wait_time, 30)
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))
    raise Exception(f"Failed to get response after {max_retries} attempts")


models_infos = [model for model in models if model["model_name"] == model_name]
model_info = models_infos[0] if models_infos else None
if model_info and model_info["api_name"] == "Gemini API":
    from .llm_gemini import chat_with_retry
