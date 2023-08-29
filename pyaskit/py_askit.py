from . import types as t
import time
from contextlib import contextmanager
from .example import ExampleType
from .function import Function


def set_module_path(new_path):
    """Set the path where modules will be generated."""
    global module_path
    module_path = new_path


def ask(return_type: t.Type, template: str, *args, **kwargs):
    f = define(return_type, template)
    return f(*args, **kwargs)


def define(return_type: t.Type, template: str, training_examples: ExampleType = []):
    return Function(return_type, template, training_examples)


@contextmanager
def timer():
    start = time.perf_counter()  # Start the timer
    yield
    end = time.perf_counter()  # Stop the timer
    print(f"Elapsed time: {end - start} seconds")
