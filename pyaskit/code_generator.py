import re
import os
import importlib
import tempfile
from timeout_decorator import timeout, TimeoutError
from .example import ExampleType
from .gpt import chat_with_retry
from .logging_config import setup_logger
from .path import add_to_sys_path
from . import config


logger = setup_logger(__name__)

TMP_MOD_PATH = tempfile.mktemp(suffix=".py")
TMP_MOD_DIR = os.path.dirname(TMP_MOD_PATH)
TMP_MOD_NAME, _ = os.path.splitext(os.path.basename(TMP_MOD_PATH))


def extract_python_code(text: str) -> str:
    # extract ```python...``` from text
    json_regex = r"```python\n(.*)\n```"
    json_match = re.search(json_regex, text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    return ""


@timeout(60)
def test_example(func, example: dict) -> bool:
    input = example["input"]
    output = example["output"]
    result = func(**input)
    logger.debug("input:", input)
    logger.debug("output:", output)
    logger.debug("result:", result)
    return func(**input) == output


def test(func, examples: ExampleType) -> bool:
    try:
        return all(test_example(func, example) for example in examples)
    except TimeoutError:
        return False


def validate_python_code(code: str, func_name):
    # save code in a file
    with open(TMP_MOD_PATH, "w") as f:
        f.write(code)
    with add_to_sys_path(TMP_MOD_DIR):
        try:
            module = importlib.import_module(TMP_MOD_NAME)
            importlib.reload(module)
        except ImportError:
            logger.debug(f"Module {TMP_MOD_NAME} not found")
            return None
        except Exception as e:
            logger.debug(f"An error occurred: {e}")
            return None
    if not hasattr(module, func_name):
        logger.debug(f"Function {func_name} not found")
        return None
    func = getattr(module, func_name)
    return func


def make_messages(skeleton: str):
    return [
        {
            "role": "system",
            "content": "You are a Python programmer. Your task is to implement the body of the function with the given name and parameters. The function should return the given type.",
        },
        {
            "role": "user",
            "content": """```python
def add(x, y) -> int:
    # add 'x' and 'y'
    pass
```""",
        },
        {
            "role": "assistant",
            "content": """```python
def add(x, y) -> int:
    # add 'x' and 'y'
    return x + y
```""",
        },
        {
            "role": "user",
            "content": skeleton,
        },
    ]


def implement_body(
    function_name: str,
    skeleton: str,
    test_examples: ExampleType = [],
):
    # print("skelton:", skeleton)
    messages = make_messages(skeleton)
    # print(messages)
    test_failed_count = 0
    for i in range(10):
        completion = chat_with_retry(model=config.get_model(), messages=messages)
        code = extract_python_code(completion.choices[0].message.content)
        func = validate_python_code(code, function_name)
        if func is None:
            continue
        ok = test(func, test_examples)
        if ok:
            return code, test_failed_count
        else:
            test_failed_count += 1
            # print("Test failed")
            # print("Code:", code)
    raise ValueError("Failed to generate valid code")
