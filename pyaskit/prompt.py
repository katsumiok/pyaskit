from typing import List, Union, Dict
from .example import ExampleType
from .types.type_printer import TypePrinter
from . import types as t


def make_single_example_code(function_name: str, example):
    input = example["input"]
    output = example["output"]
    code = f"""```python
{function_name}(**{repr(input)})
# {repr(output)}
```"""
    return code


def make_example_code(function_name: str, examples: ExampleType):
    if len(examples) == 0:
        return ""
    code = "\nExamples:\n"
    for example in examples:
        code += make_single_example_code(function_name, example) + "\n"
    return code


def make_parameter(
    variable: str, param_types: Union[Dict[str, t.Type], None], printer: TypePrinter
):
    if param_types is None or variable not in param_types:
        return variable
    else:
        return f"{variable}: {param_types[variable].accept(printer)}"


def make_coding_prompt(
    return_type: t.Type,
    param_types: Union[Dict[str, t.Type], None],
    task_description: str,
    function_name: str,
    variables: List[str],
    training_examples: ExampleType = [],
):
    printer = TypePrinter()
    param_list = ", ".join(
        [make_parameter(variable, param_types, printer) for variable in variables]
    )
    return_type_str = return_type.accept(printer)
    type_defs = "|n".join(printer.type_defs)
    import_stmt = (
        "from typing import " + ", ".join([name for name in printer.imports])
        if len(printer.imports) > 0
        else ""
    )
    examples = make_example_code(function_name, training_examples)

    prompt = f"""
```python
{import_stmt}
{type_defs}

def {function_name}({param_list}) -> {return_type_str}:
    # {task_description}
    pass
```
{examples}
"""
    # print("Prompt:", prompt)
    return prompt
