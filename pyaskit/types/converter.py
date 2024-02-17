from typing import Union

try:
    from typing import (
        Literal,
        _TypedDictMeta,
        get_origin,
        get_args,
        get_type_hints,
    )
except ImportError:
    from typing_extensions import (
        Literal,
        _TypedDictMeta,
        get_origin,
        get_args,
        get_type_hints,
    )
import pyaskit.types as t


def is_typed_dict(type_hint) -> bool:
    if isinstance(type_hint, _TypedDictMeta):
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
    if origin is list:
        return t.list(convert_type(args[0]))
    elif origin is tuple:
        return t.tuple(*[convert_type(item_type) for item_type in args])
    elif origin is Union:
        return t.union(*[convert_type(arg) for arg in args])
    elif origin is Literal:
        return t.literal(*get_args(x))
    elif origin is dict:
        return t.record(convert_type(args[0]), convert_type(args[1]))
    elif is_typed_dict(x):
        annotations = get_type_hints(x)
        return t.dict({key: convert_type(value) for key, value in annotations.items()})
    elif origin is None:
        return t.none
    return x
