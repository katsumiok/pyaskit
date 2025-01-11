import os


def get_model():
    return os.getenv("ASKIT_MODEL", "gpt-4o-mini")
