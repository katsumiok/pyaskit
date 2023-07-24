import os
import json
import re
import time
import random
import openai
from .types.schema import generate_schema
from .example import ExampleType

openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_json(text: str):
    json_text = text
    json_regex = r"```json(.*)```"
    json_match = re.search(json_regex, text, re.DOTALL)
    if json_match:
        json_text = json_match.group(1)
    try:
        return json.loads(json_text)
    except:
        return None


def chat_with_retry(model, messages, max_retries=5):
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
            jitter = wait_time / 2
            time.sleep(wait_time + random.uniform(-jitter, jitter))
    raise Exception(f"Failed to get response after {max_retries} attempts")


def make_qa(task, example):
    input = example["input"]
    output = example["output"]
    q = make_question(task, input)
    a = make_answer(output)
    return q, a


def make_answer(output):
    return f"""```json
{{
    "reason": "..."
    "answer": {json.dumps(output)}
}}
```"""


def make_example_chat_messages(task, examples: ExampleType):
    messages = []
    for example in examples:
        q, a = make_qa(task, example)
        messages.append({"role": "user", "content": q})
        messages.append({"role": "assistant", "content": a})
    return messages


def parse(text: str, return_type):
    data = extract_json(text)
    if data is None:
        raise ValueError("Answer is not in a single JSON block")
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")
    if "answer" not in data:
        raise ValueError('JSON must contain "answer" field')
    format_is_ok = return_type.validate(data["answer"])
    if not format_is_ok:
        schema = generate_schema(return_type)
        raise ValueError(
            f"""The type of answer" field must be the following type:
```ts
{schema}
```
"""
        )
    return data["answer"]


def chat(task: str, var_map: dict, return_type, training_examples: ExampleType):
    messages = make_messages(task, return_type, var_map, training_examples)

    while True:
        completion = chat_with_retry(
            "gpt-3.5-turbo-16k",
            messages,
        )
        content = completion.choices[0].message.content
        try:
            data = parse(content, return_type)
            return data
        except ValueError as e:
            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": str(e)})
            # print(str(e))
            # print(content)
            # print(content)
            # print('retrying...')
            pass


def make_messages(task, return_type, varMap, training_examples):
    system = make_system_message(return_type)
    question = make_question(task, varMap)
    example_messages = make_example_chat_messages(task, training_examples)
    messages = [
        {"role": "system", "content": system},
        *example_messages,
        {"role": "user", "content": question},
    ]
    # print(messages)
    return messages


def make_system_message(return_type):
    system_template = """You are a helpful assistant that generates responses in JSON format enclosed with ```json and ``` like:
```json
{ "reason": "Reason for the answer", "answer": "Final answer or result" }
```

The answer inside the JSON code block should be given in the type defined as follows:
```ts
{ reason: string; answer: {{type}} }
```
"""
    type = generate_schema(return_type)
    return re.sub(r"{{type}}", type, system_template)


def make_question(task: str, varMap: dict):
    # print("make_question: ", task)
    question = task + "\n\n"
    if len(varMap) > 0:
        question += "where\n"
        for key in varMap:
            question += f"  '{key}' = {json.dumps(varMap[key])}\n"
    return question
