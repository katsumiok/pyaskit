from pyaskit import ask, define
import pyaskit
import pyaskit.types as t
from typing import Optional
import fire
from llama import Llama


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    generator = Llama.build(
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

    pyaskit.core.set_chat_function(chat)
    sum = ask(t.int, "add 1 + 2")
    print(sum)


if __name__ == "__main__":
    fire.Fire(main)
