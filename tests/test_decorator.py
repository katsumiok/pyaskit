import unittest
import pytest
from pyaskit.decorator import function, make_examples


def test_func():
    assert func(1, 1) == 2
    assert func(2, 2) == 4


def test_func_bad():
    assert 4 == func(2, 2)


def func(x, y):
    return x + y


def dummy_defun_hinted(return_type, arg_types, description, training_examples=None):
    # This is a mock version of defun_hinted for testing purposes
    def decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Tests for make_examples
def test_make_examples_success():
    examples = make_examples(test_func, func)
    expected_examples = [
        {"input": {"x": 1, "y": 1}, "output": 2},
        {"input": {"x": 2, "y": 2}, "output": 4},
    ]
    assert (
        examples == expected_examples
    ), "make_examples should extract correct examples"


def test_make_examples_failure():
    with pytest.raises(SyntaxError):
        # Assume test_func_bad is defined with incorrect assert statements
        make_examples(test_func_bad, func)


def t_sample_func():
    assert sample_func(1, 1) == 2
    assert sample_func(2, 2) == 4


def e_sample_func():
    assert sample_func(1, 1) == 2
    assert sample_func(2, 2) == 4


@function(codable=True, example=e_sample_func, test=t_sample_func)
def sample_func(x: int, y: int) -> int:
    """add {{x}} and {{y}}"""
