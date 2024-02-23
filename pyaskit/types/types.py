import builtins
import inspect


class TypeVisitor:
    def visit_literal(self, type):
        raise NotImplementedError("visit_literal method not implemented")

    def visit_dict(self, type):
        raise NotImplementedError("visit_dict method not implemented")

    def visit_int(self, type):
        raise NotImplementedError("visit_int method not implemented")

    def visit_float(self, type):
        raise NotImplementedError("visit_float method not implemented")

    def visit_string(self, type):
        raise NotImplementedError("visit_string method not implemented")

    def visit_bool(self, type):
        raise NotImplementedError("visit_bool method not implemented")

    def visit_list(self, type):
        raise NotImplementedError("visit_list method not implemented")

    def visit_union(self, type):
        raise NotImplementedError("visit_union method not implemented")

    def visit_tuple(self, type):
        raise NotImplementedError("visit_tuple method not implemented")

    def visit_code(self, type):
        raise NotImplementedError("visit_code method not implemented")

    def visit_record(self, type):
        raise NotImplementedError("visit_record method not implemented")

    def visit_ref(self, type):
        raise NotImplementedError("visit_ref method not implemented")

    def visit_none(self, type):
        raise NotImplementedError("visit_none method not implemented")


class Type:
    # override | operator
    def __or__(self, other):
        return UnionType([self, other])

    def validate(self, value):
        raise NotImplementedError("validate method not implemented")

    def accept(self, visitor):
        raise NotImplementedError("accept method not implemented")


class NoneType(Type):
    def validate(self, value):
        return value is None

    def accept(self, visitor):
        return visitor.visit_none(self)


none = NoneType()


class CodeType(Type):
    def __init__(self, language: builtins.str) -> None:
        self.language = language

    def validate(self, value):
        return isinstance(value, builtins.str)

    def accept(self, visitor):
        return visitor.visit_code(self)


def code(language: builtins.str):
    return CodeType(language)


class LiteralType(Type):
    def __init__(self, value) -> None:
        self.value = value

    def validate(self, value):
        return value == self.value

    def accept(self, visitor):
        return visitor.visit_literal(self)


def literal(*values):
    if len(values) == 1:
        return LiteralType(values[0])
    else:
        return UnionType([LiteralType(value) for value in values])


class DictType(Type):
    def __init__(self, props) -> None:
        # Check that all values in fields are of type Type
        if not all(isinstance(value, Type) for value in props.values()):
            raise TypeError("All values in fields must be of type Type")
        # Check that all keys in fields are of type str
        if not all(isinstance(key, builtins.str) for key in props.keys()):
            raise TypeError("All keys in fields must be of type str")
        self.props = props
        self.name = None

    def validate(self, value):
        if not isinstance(value, builtins.dict):
            return False
        if not set(self.props.keys()).issubset(set(value.keys())):
            return False
        return all(self.props[key].validate(value[key]) for key in self.props.keys())

    def accept(self, visitor):
        return visitor.visit_dict(self)


def dict(props):
    return DictType(props)


class IntType(Type):
    def validate(self, value):
        return isinstance(value, builtins.int)

    def accept(self, visitor):
        return visitor.visit_int(self)


int = IntType()


class FloatType(Type):
    def validate(self, value):
        return isinstance(value, builtins.float) or isinstance(value, builtins.int)

    def accept(self, visitor):
        return visitor.visit_float(self)


float = FloatType()


class StringType(Type):
    def validate(self, value):
        return isinstance(value, builtins.str)

    def accept(self, visitor):
        return visitor.visit_string(self)


str = StringType()


class BoolType(Type):
    def validate(self, value):
        return isinstance(value, builtins.bool)

    def accept(self, visitor):
        return visitor.visit_bool(self)


bool = BoolType()


class ListType(Type):
    def __init__(self, type) -> None:
        if not isinstance(type, Type):
            raise TypeError("Argument must be of type Type")
        self.type = type

    def validate(self, value):
        return isinstance(value, builtins.list) and all(
            self.type.validate(item) for item in value
        )

    def accept(self, visitor):
        return visitor.visit_list(self)


def list(type):
    return ListType(type)


class TupleType(Type):
    def __init__(self, types):
        self.types = types

    def validate(self, value):
        return (
            (isinstance(value, builtins.list) or isinstance(value, builtins.tuple))
            and len(value) == len(self.types)
            and all(type.validate(item) for item, type in zip(value, self.types))
        )

    def accept(self, visitor):
        return visitor.visit_tuple(self)


def tuple(*types):
    return TupleType(types)


class UnionType(Type):
    def __init__(self, types) -> None:
        if not all(isinstance(type, Type) for type in types):
            raise TypeError("All arguments must be of type Type")
        self.types = types

    def validate(self, value):
        return any(type.validate(value) for type in self.types)

    def accept(self, visitor):
        return visitor.visit_union(self)


def union(*types):
    return UnionType(types)


class RecordType(Type):
    def __init__(self, key_type, value_type) -> None:
        self.key_type = key_type
        self.value_type = value_type

    def validate(self, value):
        return isinstance(value, builtins.dict) and all(
            self.key_type.validate(key) and self.value_type.validate(value)
            for key, value in value.items()
        )

    def accept(self, visitor):
        return visitor.visit_record(self)


def record(key_type, value_type):
    return RecordType(key_type, value_type)


class RefType(Type):
    def __init__(self, locals, globals, name) -> None:
        self.locals = locals
        self.globals = globals
        self.name = name

    def access(self):
        if self.name in self.locals:
            return self.locals[self.name]
        elif self.name in self.globals:
            return self.globals[self.name]
        else:
            raise NameError(f"Name {self.name} is not defined")

    def validate(self, value):
        return self.access().validate(value)

    def accept(self, visitor):
        return visitor.visit_ref(self)


def ref(name):
    return RefType(
        inspect.currentframe().f_back.f_locals,
        inspect.currentframe().f_back.f_globals,
        name,
    )
