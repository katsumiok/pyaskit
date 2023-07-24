import unittest
import pyaskit as ai
import pyaskit.types as t


class TestAskIt(unittest.TestCase):
    def test_define_ok(self):
        valid_examples = [
            {"input": {"x": 1}, "output": 2},
        ]
        ai.define(t.int, "add 1 to {{x}}", training_examples=valid_examples)

    def test_define_invalid_output_type(self):
        invalid_output_type_examples = [
            {"input": {"x": 1}, "output": "2"},
        ]
        # check if invalid examples are detected
        with self.assertRaises(ValueError):
            ai.define(
                int, "add 1 to {{x}}", training_examples=invalid_output_type_examples
            )

    def test_define_insufficient_parameters(self):
        # parameter is not specified
        insufficient_parameter_examples = [
            {"input": {}, "output": 2},
        ]
        with self.assertRaises(ValueError):
            ai.define(
                int, "add 1 to {{x}}", training_examples=insufficient_parameter_examples
            )

    def test_define_unknown_parameter(self):
        # unknown parameter is specified
        unknown_parameter_examples = [
            {"input": {"x": 1, "y": 1}, "output": 2},
        ]
        with self.assertRaises(ValueError):
            ai.define(
                int, "add 1 to {{x}}", training_examples=unknown_parameter_examples
            )


if __name__ == "__main__":
    unittest.main()
