import unittest
import pyaskit.types as t


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
        self.assertTrue((t.literal("yes") | t.literal("no")).validate("no"))
        self.assertFalse((t.literal("yes") | t.literal("no")).validate("maybe"))


if __name__ == "__main__":
    unittest.main()
