from typing import Dict
from . import types as t
import json


class SchemaGenerator(t.TypeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.type_defs: Dict[str, str] = {}

    def visit_literal(self, type):
        return json.dumps(type.value)

    def visit_dict(self, type):
        if type.name != None:
            if type.name not in self.type_defs:
                self.type_defs[type.name] = None
                props = [
                    f"{key}: {value.accept(self)}" for key, value in type.props.items()
                ]
                self.type_defs[type.name] = f'{{ {"; ".join(props)} }}'
            return type.name
        else:
            props = [
                f"{key}: {value.accept(self)}" for key, value in type.props.items()
            ]
            return f'{{ {"; ".join(props)} }}'

    def visit_int(self, type):
        return "number"

    def visit_float(self, type):
        return "number"

    def visit_bool(self, type):
        return "boolean"

    def visit_string(self, type):
        return "string"

    def visit_list(self, type: t.ListType):
        typeString = type.type.accept(self)
        return f"Array({typeString})"

    def visit_union(self, type):
        types = [t.accept(self) for t in type.types]
        return " | ".join(types)

    def visit_tuple(self, type):
        types = [t.accept(self) for t in type.types]
        return f'[{", ".join(types)}]'

    def visit_code(self, type):
        return "string"

    def visit_record(self, type):
        k = type.key_type.accept(self)
        v = type.value_type.accept(self)
        return f"{{[key: {k}]: {v}}}]"

    def visit_ref(self, type: t.RefType):
        if type.name not in self.type_defs:
            self.type_defs[type.name] = None
            self.type_defs[type.name] = type.access().accept(self)
        return type.name

    def visit_none(self, type):
        return "null"


# export function generateSchema<T>(type: any): string {
def generate_schema(type) -> str:
    return type.accept(SchemaGenerator())
