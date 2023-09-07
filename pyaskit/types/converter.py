from typing import Union
#from typing import Literal
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
    #origin = get_origin(x)
    #args = get_args(x)
    origin = getattr(x, '__origin__', None)
    args = getattr(x, '__args__', ())
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
    return x
