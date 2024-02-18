from typing import Union, Dict, List, Tuple

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
from . import types as t
from .types.converter import convert_type
import time
from contextlib import contextmanager
from .example import ExampleType
from .function import Function

ReturnType = Union[t.Type, Dict, List, Tuple, str, int, float, bool, TypedDict, None]
ParamType = ReturnType


def set_module_path(new_path):
    """Set the path where modules will be generated."""
    global module_path
    module_path = new_path


def ask(return_type: ReturnType, template: str, *args, **kwargs):
    f = define(return_type, template)
    return f(*args, **kwargs)


def define(return_type: ReturnType, template: str, training_examples: ExampleType = []):
    return Function(return_type, None, template, training_examples)


def defun(
    return_type: ReturnType,
    param_types: Dict[str, ParamType],
    template: str,
    training_examples: ExampleType = [],
    validate=None,
    params_order: List[str] = None,
):
    return Function(
        return_type, param_types, template, training_examples, order=params_order
    )


@contextmanager
def timer():
    start = time.perf_counter()  # Start the timer
    yield
    end = time.perf_counter()  # Stop the timer
    print(f"Elapsed time: {end - start} seconds")
