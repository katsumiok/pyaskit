import unittest
import pyaskit.types as t


class TestTypeVisitor(unittest.TestCase):
    
    def setUp(self):
        self.visitor = t.types.TypeVisitor()
    
    def test_visit_literal_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_literal(None)
    
    def test_visit_dict_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_dict(None)

    def test_visit_int_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_int(None)

    def test_visit_float_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_float(None)
    
    def test_visit_string_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_string(None)

    def test_visit_bool_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_bool(None)
    
    def test_visit_list_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_list(None)
    
    def test_visit_union_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_union(None)

    def test_visit_tuple_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_tuple(None)
    
    def test_visit_code_raises_error(self):
        with self.assertRaises(NotImplementedError):
            self.visitor.visit_code(None)



class TestType(unittest.TestCase):
    def test_int(self):
        self.assertTrue(t.int.validate(5))
        self.assertFalse(t.int.validate("5"))

    def test_bool(self):
        self.assertTrue(t.bool.validate(True))
        self.assertFalse(t.bool.validate(5))

    def test_string(self):
        self.assertTrue(t.str.validate("5"))
        self.assertFalse(t.str.validate(5))

    def test_list(self):
        self.assertTrue(t.list(t.int).validate([1, 2, 3]))
        self.assertFalse(t.list(t.int).validate([1, 2, "3"]))

    def test_dict(self):
        self.assertTrue(
            t.dict({"a": t.int, "b": t.str}).validate({"a": 5, "b": "hello"})
        )
        self.assertTrue(t.dict({"a": t.list(t.int)}).validate({"a": [5, 6]}))
        self.assertFalse(t.dict({"a": t.int, "b": t.str}).validate({"a": 5, "b": 5}))

    def test_literal(self):
        self.assertTrue(t.literal(5).validate(5))
        self.assertFalse(t.literal(5).validate(6))
        self.assertTrue(t.literal("yes").validate("yes"))
        self.assertFalse(t.literal("yes").validate("no"))
        self.assertTrue(t.literal(True).validate(True))
        self.assertFalse(t.literal(True).validate(False))

    def test_union(self):
        self.assertTrue((t.literal("yes") | t.literal("no")).validate("yes"))
        self.assertTrue(t.union(t.literal("yes"), t.literal("no")).validate("no"))
        self.assertFalse((t.literal("yes", "no")).validate("maybe"))
        with self.assertRaises(TypeError):
            self.assertFalse((t.literal("yes") | "no"))


if __name__ == "__main__":
    unittest.main()
