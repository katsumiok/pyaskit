import inspect
from .py_askit import defun

import ast
import inspect
import astor


def make_examples(func, tested_func):
    def safe_eval(node_or_string):
        """Safely evaluate Python expressions from AST nodes or strings."""
        try:
            if isinstance(node_or_string, ast.AST):
                return ast.literal_eval(astor.to_source(node_or_string))
            return ast.literal_eval(node_or_string)
        except ValueError:
            raise ValueError(f"Unable to safely evaluate expression: {node_or_string}")

    # Extract the source code and parse it into an AST
    source = inspect.getsource(func)
    parsed_ast = ast.parse(source)

    # Obtain the signature of the tested function
    signature = inspect.signature(tested_func)
    param_names = list(signature.parameters.keys())

    examples = []
    for node in parsed_ast.body[0].body:
        if not (
            isinstance(node, ast.Assert)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.ops[0], ast.Eq)
        ):
            raise SyntaxError(
                "Expected an assert statement with an equality comparison."
            )

        lhs = node.test.left
        if not isinstance(lhs, ast.Call):
            raise SyntaxError(
                "Left-hand side of the assert statement must be a function call."
            )

        # Map function call arguments to their names based on the signature
        args = {}
        for i, arg in enumerate(lhs.args):
            arg_val = safe_eval(arg)
            param_name = param_names[i] if i < len(param_names) else f"arg{i}"
            args[param_name] = arg_val

        # Extract and evaluate the expected output
        rhs = safe_eval(node.test.comparators[0])

        # Store the example
        examples.append({"input": args, "output": rhs})

    return examples


def function(codable: bool, example=None, test=None):
    def decorator(func):
        signature = inspect.signature(func)
        arg_types = {
            name: param.annotation for name, param in signature.parameters.items()
        }
        order = [name for name, _ in signature.parameters.items()]
        return_type = signature.return_annotation
        description = func.__doc__
        kwargs = {}
        kwargs["params_order"] = order
        if example is not None:
            examples = make_examples(example, func)
            kwargs["training_examples"] = examples
        elif test is not None:
            kwargs["test_examples"] = test
        func = defun(return_type, arg_types, description, **kwargs)
        return func.compile() if codable else func

    return decorator
