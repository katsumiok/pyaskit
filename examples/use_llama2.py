from pyaskit import define, use_llama
import pyaskit.types as t
from typing import Optional
import fire


def main(
    ckpt_dir: str,
    tokenizer_path: str,
    temperature: float = 0.6,
    top_p: float = 0.9,
    max_seq_len: int = 512,
    max_batch_size: int = 8,
    max_gen_len: Optional[int] = None,
):
    use_llama(
        ckpt_dir,
        tokenizer_path,
        temperature,
        top_p,
        max_seq_len,
        max_batch_size,
        max_gen_len,
    )
    add = define(t.int, "add {{x}} and {{y}}")
    sum = add(-1, 2)
    print(sum)


if __name__ == "__main__":
    fire.Fire(main)
