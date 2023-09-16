from .llm_openai import chat_with_retry
import importlib
from typing import Optional
import warnings

chat_function = chat_with_retry


def set_chat_function(func):
    """Allows the user to set a custom chat function."""
    global chat_function
    chat_function = func


def chat(messages):
    return chat_function(messages)


def use_llama(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    llama = importlib.import_module("llama")
    generator = llama.Llama.build(
        ckpt_dir=ckpt_dir,
        tokenizer_path=tokenizer_path,
        max_seq_len=max_seq_len,
        max_batch_size=max_batch_size,
    )

    def chat(messages):
        results = generator.chat_completion(
            [messages],  # type: ignore
            max_gen_len=max_gen_len,
            temperature=temperature,
            top_p=top_p,
        )
        return results[0]["generation"]["content"], results[0]

    set_chat_function(chat)
