import unittest
import pyaskit.example as example
import pyaskit.types as t


class TestExample(unittest.TestCase):
    def test_check_examples(self):
        example.check_examples(t.int, ["x", "y"], [{"input": {"x": 1, "y": 2}, "output": 3}])
        with self.assertRaises(ValueError):
            example.check_examples(t.int, ["x", "y"], [{"input": 1, "output": 3}])        
        with self.assertRaises(ValueError):
            example.check_examples(t.int, ["x", "y"], [{"input": {"x": 1}, "output": 3}])
        with self.assertRaises(ValueError):
            example.check_examples(t.int, ["x", "y"], [{"input": {"x": 1, "y": 2, "z": 3}, "output": 3}])
        with self.assertRaises(ValueError):
            example.check_examples(t.int, ["x", "y"], [{"input": {"x": 1, "y": 2}, "output": "3"}])
        with self.assertRaises(ValueError):
             example.check_examples(t.int, ["x", "y"], [{"output": 3}])
        with self.assertRaises(ValueError):
             example.check_examples(t.int, ["x", "y"], [{"input": {"x": 1, "y": 2}}])
