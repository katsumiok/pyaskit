import builtins


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
    


class Type:
    # override | operator
    def __or__(self, other):
        return UnionType(self, other)

    def validate(self, value):
        raise NotImplementedError("validate method not implemented")

    def accept(self, visitor):
        raise NotImplementedError("accept method not implemented")
   
    
class CodeType(Type):
    def __init__(self, language: str) -> None:
        self.language = language
    
    def validate(self, value):
        return isinstance(value, builtins.str)
    
    def accept(self, visitor):
        return visitor.visit_code(self)


def code(language: str):
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
            isinstance(value, builtins.list)
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
