from typing import Union

try:
    from typing import TypedDict, _TypedDictMeta, get_origin, get_args, get_type_hints

    python_38 = True
except ImportError:
    from typing_extensions import (
        TypedDict,
        _TypedDictMeta,
        get_origin,
        get_args,
        get_type_hints,
    )

    python_38 = False

# from typing import Literal
import pyaskit.types as t


def is_typed_dict(type_hint) -> bool:
    """
    Check whether the provided type hint is a TypedDict.

    Args:
    - type_hint: The type hint to check.

    Returns:
    - bool: True if the type_hint is a TypedDict, False otherwise.
    """
    # Check for Python 3.8 and newer
    if python_38 and isinstance(type_hint, _TypedDictMeta):
        return True
    # Check for compatibility with older versions using typing_extensions
    if (
        not python_38
        and isinstance(type_hint, type)
        and issubclass(type_hint, TypedDict)
    ):
        return True
    return False


def convert_type(x):
    if x == int:
        return t.int
    elif x == float:
        return t.float
    elif x == bool:
        return t.bool
    elif x == str:
        return t.str
    origin = get_origin(x)
    args = get_args(x)
    # origin = getattr(x, "__origin__", None)
    # args = getattr(x, "__args__", ())
    if origin is list:
        return t.list(convert_type(args[0]))
    elif origin is tuple:
        return t.tuple(*[convert_type(item_type) for item_type in args])
    elif origin is Union:
        return t.union(*[convert_type(arg) for arg in args])
    # elif origin is Literal:
    #     return t.literal(*get_args(x))
    elif origin is dict:
        return t.record(convert_type(args[0]), convert_type(args[1]))
    elif is_typed_dict(x):
        annotations = get_type_hints(x)
        return t.dict({key: convert_type(value) for key, value in annotations.items()})
    elif origin is None:
        return t.none
    return x
