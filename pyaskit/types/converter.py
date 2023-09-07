from typing import List, Tuple, Type, Dict, Literal, get_origin, get_args, TypedDict, Union, Any, _GenericAlias, _SpecialForm
import inspect
import pyaskit.types as t


def convert_type(x):
    if x == int:
        return t.int
    elif x == float:
        return t.float
    elif x == bool:
        return t.bool
    elif x == str:
        return t.str
    if inspect.isclass(x) and getattr(x, '__bases__', [])[0].__name__ == "dict":
        return t.dict({k: convert_type(v) for k, v in x.__annotations__.items()})
    origin = get_origin(x)
    if origin is list:
        return t.list(convert_type(get_args(x)[0]))
    elif origin is tuple:
        return t.tuple(*[convert_type(item_type) for item_type in get_args(x)])
    elif origin is Union:
        args = get_args(x)
        return t.union(*[convert_type(arg) for arg in args])
    elif origin is Literal:
        return t.literal(*get_args(x))
    elif origin is dict:
        return t.record(convert_type(get_args(x)[0]), convert_type(get_args(x)[1]))
    return x
