import unittest
import pyaskit.types as t
from pyaskit.types.schema import generate_schema, SchemaGenerator


class TestGenerateSchema(unittest.TestCase):
    def test_int(self):
        self.assertEqual(generate_schema(t.int), "number")

    def test_bool(self):
        self.assertEqual(generate_schema(t.bool), "boolean")

    def test_string(self):
        self.assertEqual(generate_schema(t.str), "string")

    def test_code(self):
        self.assertEqual(generate_schema(t.code("python")), "string")

    def test_list(self):
        self.assertEqual(generate_schema(t.list(t.int)), "Array(number)")

    def test_dict(self):
        self.assertEqual(
            generate_schema(t.dict({"a": t.int, "b": t.str})),
            "{ a: number; b: string }",
        )

    def test_unknown_type(self):
        with self.assertRaises(AttributeError):
            generate_schema(None)

    def test_literal(self):
        self.assertEqual(generate_schema(t.literal(5)), "5")
        self.assertEqual(generate_schema(t.literal("yes")), '"yes"')
        self.assertEqual(generate_schema(t.literal(True)), "true")

    def test_union(self):
        self.assertEqual(
            generate_schema(t.literal("yes") | t.literal("no")), '"yes" | "no"'
        )

    def test_tuple(self):
        self.assertEqual(generate_schema(t.tuple(t.int, t.float)), "[number, number]")

    def test_ref(self):
        generator = SchemaGenerator()
        Tree = t.dict({"name": t.str, "children": t.list(t.ref("Tree"))})
        self.assertEqual(t.ref("Tree").accept(generator), "Tree")
        self.assertEqual(
            generator.type_defs, {"Tree": "{ name: string; children: Array(Tree) }"}
        )


if __name__ == "__main__":
    unittest.main()
