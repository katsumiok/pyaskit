from . import types as t
import json


# export function generateSchema<T>(type: any): string {
def generate_schema(type) -> str:
    if isinstance(type, t.IntType):
        return "number"
    if isinstance(type, t.FloatType):
        return "number"    
    elif isinstance(type, t.BoolType):
        return "boolean"
    elif isinstance(type, t.StringType):
        return "string"
    elif isinstance(type, t.LiteralType):
        return json.dumps(type.value)
    elif isinstance(type, t.UnionType):
        types = [generate_schema(type) for type in type.types]
        return " | ".join(types)
    elif isinstance(type, t.DictType):
        props = [
            f"{key}: {generate_schema(value)}" for key, value in type.props.items()
        ]
        return f'{{ {"; ".join(props)} }}'
    elif isinstance(type, t.ListType):
        typeString = generate_schema(type.type)
        return f"Array({typeString})"
    elif isinstance(type, t.TupleType):
        types = [generate_schema(type) for type in type.types]
        return f'[{", ".join(types)}]'
    elif isinstance(type, t.CodeType):
        return "string"

    raise TypeError(f"Unknown type: {type}")
