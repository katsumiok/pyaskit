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
        json_text = json_match.group(1).strip()
    try:
        return json.loads(json_text)
    except Exception as e:
        raise ValueError(f"Failed to parse JSON: {e}")


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


def make_qa(task, example):
    input = example["input"]
    output = example["output"]
    q = make_question(task, input)
    a = make_answer(output)
    return q, a


def make_answer(output):
    return f"""```json
{{
    "reason": "...",
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
    return data["answer"], data["reason"] if "reason" in data else ""


def chat(task: str, var_map: dict, return_type, training_examples: ExampleType):
    messages = make_messages(task, return_type, var_map, training_examples)
    return ask_and_parse(return_type, messages)


def chat_raw(return_type, messages):
    merged_messages = merge_messages(messages, return_type)
    return ask_and_parse(return_type, merged_messages)


def ask_and_parse(return_type, messages):
    retry = False

    while True:
        completion = chat_with_retry(
            "gpt-3.5-turbo-16k",
            #            "gpt-4",
            messages,
        )
        content = completion.choices[0].message.content
        try:
            data, reason = parse(content, return_type)
            return data, reason
        except ValueError as e:
            if retry:
                messages = messages[:-2]
                retry = False
            else:
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": str(e)})
                retry = True
            # print(str(e))
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


def merge_messages(base_messages, return_type):
    system = make_system_message(return_type)
    messages = [{"role": "system", "content": system}, *base_messages]
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
Explain your answer in the `reason` field step by step.
No additional text should be part of the value of `answer` field.
"""
    type = generate_schema(return_type)
    # Use replace instead of re.sub because of the following error when handling unicode characters:
    # bad escape \u at position 1
    return system_template.replace("{{type}}", type)


def make_question(task: str, varMap: dict):
    # print("make_question: ", task)
    question = task + "\n\n"
    if len(varMap) > 0:
        question += "where\n"
        for key in varMap:
            question += f"  '{key}' = {json.dumps(varMap[key])}\n"
    return question
