from .types.type_printer import TypePrinter
from typing import List, Dict, Union, Any


ExampleType = List[Dict[str, Union[Dict[str, Any], Any]]]


def _check_input(variables, input):
    if not isinstance(input, dict):
        raise ValueError(f"Input must be a dictionary: {input}")
    for variable in variables:
        if variable not in input:
            raise ValueError(f"Input must contain '{variable}' field")
    for variable, value in input.items():
        if variable not in variables:
            raise ValueError(f"Unknown variable '{variable}'")


def _check_output(return_type, output):
    if not return_type.validate(output):
        printer = TypePrinter()
        raise ValueError(f"Output must be of type {return_type.accept(printer)}")


def _check_example(return_type, variables, example):
    if "input" not in example:
        raise ValueError("Example must contain 'input' field")
    if "output" not in example:
        raise ValueError("Example must contain 'output' field")
    input = example["input"]
    _check_input(variables, input)
    output = example["output"]
    _check_output(return_type, output)


def check_examples(return_type, variables, examples):
    for example in examples:
        _check_example(return_type, variables, example)
