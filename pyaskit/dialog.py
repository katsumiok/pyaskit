import json
import re
from .types.schema import SchemaGenerator
from .example import ExampleType
import pyaskit.types as t
from .llm import chat


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


def parse_code(text: str, return_type):
    # extract ```python...``` from text
    #     json_text = text
    pattern = r"```\w+\n(.*?)\n```"
    python_code = re.findall(pattern, text, re.DOTALL)
    if len(python_code) > 0:
        return python_code[0]
    raise ValueError("Code block is not found")


def parse(text: str, return_type):
    if isinstance(return_type, t.CodeType):
        # print("parse_code")
        # print(text)
        return parse_code(text, return_type), ""
    data = extract_json(text)
    if data is None:
        raise ValueError("Answer is not in a single JSON block")
    if not isinstance(data, dict):
        raise ValueError("JSON must be an object")
    if "answer" not in data:
        raise ValueError('JSON must contain "answer" field')
    format_is_ok = return_type.validate(data["answer"])
    if not format_is_ok:
        schema, decls = generate_schema(return_type)
        raise ValueError(
            f"""The type of answer" field must be the following type:
```ts
{decls}

{schema}
```
"""
        )
    return data["answer"], data["reason"] if "reason" in data else ""


def query(
    task: str, var_map: dict, return_type, training_examples: ExampleType, validator
):
    messages = make_messages(task, return_type, var_map, training_examples)
    data, reason, errors, completion = ask_and_parse(return_type, messages)
    for _ in range(10):
        if validator is None:
            break
        if validator.is_valid(data):
            break
        new_messages = messages.copy()
        new_messages.append({"role": "assistant", "content": make_answer(data)})
        new_messages.append(
            {
                "role": "user",
                "content": f"Correct the answer in JSON again to solve the following error: {validator.feedback}\nProvide the whole answer.",
            }
        )
        data, reason, errors, completion = ask_and_parse(return_type, new_messages)
    return data, reason, errors, completion


def chat_raw(return_type, messages):
    merged_messages = merge_messages(messages, return_type)
    return ask_and_parse(return_type, merged_messages)


def ask_and_parse(return_type, messages):
    retry = False
    errors = []

    for _ in range(10):
        content, completion = chat(messages)
        try:
            # print(content)
            data, reason = parse(content, return_type)
            return data, reason, errors, completion
        except ValueError as e:
            if retry:
                messages = messages[:-2]
                retry = False
            else:
                s = make_retry_message(return_type)
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": s})
                retry = True
            errors.append(str(e))
    return None, "Retry limit exceeded", errors, completion


def generate_schema(return_type):
    generator = SchemaGenerator()
    schema = return_type.accept(generator)
    decls = "\n".join(
        [f"type {name} = {type}" for name, type in generator.type_defs.items()]
    )
    return schema, decls


def make_retry_message(return_type):
    if isinstance(return_type, t.CodeType):
        return f"Generates code in {return_type.language} enclosed with ```{return_type.language} and ```"
    else:
        schema, decls = generate_schema(return_type)
        s = """Generates responses again in JSON format enclosed with ```json and ``` like:
```json
{ "reason": "Reason for the answer", "answer": "Final answer or result" }
```
The type of response in the JSON code block should be the JsonType defined as follows:
```ts
{{decls}}
interface JsonType { reason: string; answer: {{type}} }
```
""".replace(
            "{{type}}", schema
        ).replace(
            "{{decls}}", decls
        )
        return s


def make_messages(task, return_type, varMap, training_examples):
    system = (
        make_system_message(return_type)
        if not isinstance(return_type, t.CodeType)
        else make_system_message_for_code(return_type)
    )
    question = make_question(task, varMap)
    example_messages = make_example_chat_messages(task, training_examples)
    messages = [
        {"role": "system", "content": system},
        *example_messages,
        {"role": "user", "content": question},
    ]
    # print('\n'.join([message["content"] for message in messages]))
    return messages


def merge_messages(base_messages, return_type):
    system = make_system_message(return_type)
    messages = [{"role": "system", "content": system}, *base_messages]
    return messages


def make_system_message(return_type):
    system_template = """You are a helpful assistant that generates responses in JSON format enclosed with ```json and ``` like:
```json
{ "reason": "Step-by-step reason for the answer", "answer": "Final answer or result" }
```

The type of response in the JSON code block should be the JsonType defined as follows:
```ts
{{decls}}
type JsonType = { reason: string; answer: {{type}} }
```
Explain your answer step-by-step in the 'reason' field."""
    if isinstance(return_type, t.StringType):
        system_template += (
            "\nNo additional text should be part of the value in the 'answer' field."
        )

    type, decls = generate_schema(return_type)
    # Use replace instead of re.sub because of the following error when handling unicode characters:
    # bad escape \u at position 1
    return system_template.replace("{{type}}", type).replace("{{decls}}", decls)


def make_system_message_for_code(return_type):
    system_template = """You are a helpful assistant that generates code in written in {{language}} enclosed with ```{{language}} and ``` like:
```{{language}}
Program written in {{language}}:
```
Let's think step-by-step!
"""
    # Use replace instead of re.sub because of the following error when handling unicode characters:
    # bad escape \u at position 1
    return system_template.replace("{{language}}", return_type.language)


def make_question(task: str, varMap: dict):
    # print("make_question: ", task)
    question = task + "\n\n"
    if len(varMap) == 0:
        return question
    var_list = [f"  '{key}' = {json.dumps(varMap[key])}" for key in varMap]
    return question + "where\n" + "\n".join(var_list)
