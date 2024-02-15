from typing import Set
from . import types as t


class TypePrinter(t.TypeVisitor):
    def __init__(self) -> None:
        super().__init__()
        self.imports: Set[str] = set()
        self.type_defs: Set[str] = set()

    def get_type_name(self):
        return "Type" + str(len(self.type_defs))

    def visit_literal(self, type):
        self.imports.add("Literal")
        return f"Literal[{repr(type.value)}]"

    def visit_dict(self, type):
        self.imports.add("TypedDict")
        type_name = self.get_type_name()
        fields_str = "".join(
            [
                f"    {field_name}: {field_type.accept(self)}\n"
                for field_name, field_type in type.props.items()
            ]
        )
        typedef = f"""
class {type_name}(TypedDict):
{fields_str}"""
        self.type_defs.add(typedef)
        return type_name

    def visit_int(self, type):
        return "int"

    def visit_float(self, type):
        return "float"

    def visit_bool(self, type):
        return "bool"

    def visit_string(self, type):
        return "str"

    def visit_list(self, type: t.ListType):
        self.imports.add("List")
        return f"List[{type.type.accept(self)}]"

    def visit_union(self, type):
        self.imports.add("Union")
        return f'Union[{", ".join([t.accept(self) for t in type.types])}]'

    def visit_tuple(self, type):
        self.imports.add("Tuple")
        return f'Tuple[{", ".join([t.accept(self) for t in type.types])}]'

    def visit_record(self, type):
        self.imports.add("Dict")
        return f"Dict[{type.key_type.accept(self)}, {type.value_type.accept(self)}]"

    def visit_ref(self, type):
        return type.name

    def visit_none(self, type):
        return "None"
