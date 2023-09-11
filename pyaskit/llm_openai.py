import os
import time
import random
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_with_retry(model, messages, max_retries=10):
    base_wait_time = 1  # wait time in seconds
    for i in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=messages,
            )
            return response
        except (
            openai.error.APIError,
            openai.error.Timeout,
            openai.error.APIConnectionError,
            openai.error.RateLimitError,
            openai.error.ServiceUnavailableError,
        ):
            # https://platform.openai.com/docs/guides/error-codes/python-library-error-types
            wait_time = base_wait_time * 2**i
            wait_time = min(wait_time, 30)
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))
    raise Exception(f"Failed to get response after {max_retries} attempts")
