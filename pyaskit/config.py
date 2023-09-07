import os


def get_model():
    return os.getenv("ASKIT_MODEL", "gpt-3.5-turbo-16k")
