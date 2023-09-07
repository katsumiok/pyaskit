import unittest
import pyaskit.types as t
from pyaskit.types.type_printer import TypePrinter


class TestTypePrinter(unittest.TestCase):
    def test_int(self):
        printer = TypePrinter()
        self.assertEqual(t.int.accept(printer), "int")

    def test_bool(self):
        printer = TypePrinter()
        self.assertEqual(t.bool.accept(printer), "bool")

    def test_string(self):
        printer = TypePrinter()
        self.assertEqual(t.str.accept(printer), "str")

    def test_list(self):
        printer = TypePrinter()
        self.assertEqual(t.list(t.int).accept(printer), "List[int]")
        self.assertEqual(printer.imports, {"List"})

    def test_dict(self):
        printer = TypePrinter()
        self.assertEqual(t.dict({"a": t.int, "b": t.str}).accept(printer), "Type0")
        self.assertEqual(
            printer.type_defs, {"\nclass Type0(TypedDict):\n    a: int\n    b: str\n"}
        )
        self.assertEqual(printer.imports, {"TypedDict"})

    def test_literal(self):
        printer = TypePrinter()
        self.assertEqual(t.literal(5).accept(printer), "Literal[5]")
        self.assertEqual(printer.imports, {"Literal"})

    def test_union(self):
        printer = TypePrinter()
        self.assertEqual(
            (t.literal("yes") | t.literal("no")).accept(printer),
            "Union[Literal['yes'], Literal['no']]",
        )
        self.assertEqual(printer.imports, {"Union", "Literal"})
        
    def test_tuple(self):
        printer = TypePrinter()
        self.assertEqual(
            t.tuple(t.int, t.float).accept(printer),
            "Tuple[int, float]",
        )
        self.assertEqual(printer.imports, {"Tuple"})
        
    def test_code(self):
        printer = TypePrinter()





if __name__ == "__main__":
    unittest.main()
