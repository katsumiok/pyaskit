import cohere
from . import config


def convert_role(role):
    if role == "assistant":
        return "CHATBOT"
    return "USER"


def convert_messages(messages):
    result = []
    for message in messages:
        role = convert_role(message["role"])
        result.append({"role": role, "message": message["content"]})
    result.insert(1, {"role": "CHATBOT", "message": "OK, I understand."})
    return result


co = cohere.Client()


def chat_with_retry(messages):
    messages = convert_messages(messages)
    response = co.chat(
        model=config.get_model(),
        chat_history=messages[:-1],
        message=messages[-1]["message"],
    )
    return response.text, response
