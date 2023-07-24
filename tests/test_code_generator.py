import unittest
from pyaskit.code_generator import validate_python_code, extract_python_code
import pyaskit.types as t


class TestCodeGenerator(unittest.TestCase):
    def test_extract_python_code(self):
        valid_text = """
The following code is valid Python code:        
```python
def inc(x): return x + 1
```
"""
        self.assertEqual(extract_python_code(valid_text), "def inc(x): return x + 1")

        invalid_text = """
The following code is valid Python code:        
def inc(x): return x + 1
"""
        self.assertEqual(extract_python_code(invalid_text), "")

    def test_validate_python_code(self):
        valid_code = """
def inc(x): return x + 1
"""
        self.assertTrue(validate_python_code(valid_code, "inc", []))
        invalid_code = """
def inc(x):
"""
        self.assertFalse(validate_python_code(invalid_code, "inc", []))


if __name__ == "__main__":
    unittest.main()
