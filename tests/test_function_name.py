import unittest
from pyaskit.function_name import generate_unique_function_name


class TestFunctionName(unittest.TestCase):
    def test_generate_unique_function_name(self):
        english = generate_unique_function_name("Calculate 'x' + 'y'")
        self.assertTrue(english.startswith("calculate_x_y"))
        japanese = generate_unique_function_name("'x'に'y'を足す")
        self.assertTrue(japanese.startswith("x_ni_y_wo"))


if __name__ == "__main__":
    unittest.main()
