import os
from pyaskit import function, define
import json


examples = [
    {
        "input": {
            "code": """from typing import List


def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\" Check if in given list of numbers, are any two numbers closer to each other than
    given threshold.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"
"""
        },
        "output": """from pyaskit import function
from typing import List


@function(codable=True)
def has_close_elements(numbers: List[float], threshold: float) -> bool:
    \"\"\" Check if in given list of {{numbers}}, are any two numbers closer to each other than
    given {{threshold}}.
    >>> has_close_elements([1.0, 2.0, 3.0], 0.5)
    False
    >>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)
    True
    \"\"\"""",
    },
    {
        "input": {
            "code": """from typing import List

def separate_paren_groups(paren_string: str) -> List[str]:
    \"\"\" Input to this function is a string containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    \"\"\""""
        },
        "output": """from pyaskit import function
from typing import List

@function(codable=True)
def separate_paren_groups(paren_string: str) -> List[str]:
    \"\"\" Input to this function is a string {{paren_string}} containing multiple groups of nested parentheses. Your goal is to
    separate those group into separate strings and return the list of those.
    Separate groups are balanced (each open brace is properly closed) and not nested within each other
    Ignore any spaces in the input string.
    >>> separate_paren_groups('( ) (( )) (( )( ))')
    ['()', '(())', '(()())']
    \"\"\"""",
    },
]


convert = define(
    str,
    """Convert given {{code}}.
    Add "from pyaskit import function" to the top of the code.
    Add "@function(codable=True)" to the function definition.
    Refer all the parameters in the docstring with double curly braces.
    """,
    training_examples=examples,
)


with open("HumanEval.jsonl") as f:
    lines = f.readlines()

entries = [json.loads(line) for line in lines]
for entry in entries:
    id = entry["task_id"]
    filename = id + ".py"
    code = convert(entry["prompt"])
    # make the parent directory
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(code)
