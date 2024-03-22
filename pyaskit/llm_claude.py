import anthropic
from . import config


def convert_role(role):
    if role == "system":
        return "user"
    return role


def convert_messages(messages):
    result = []
    for message in messages:
        role = convert_role(message["role"])
        result.append({"role": role, "content": message["content"]})
    result.insert(1, {"role": "assistant", "content": "OK, I understand."})
    return result


def chat_with_retry(messages):
    messages = convert_messages(messages)

    response = anthropic.Anthropic().messages.create(
        model=config.get_model(), max_tokens=1024, messages=messages
    )

    return response.content[0].text, response
