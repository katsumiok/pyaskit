import unittest
from pyaskit.prompt import make_coding_prompt
import pyaskit.types as t


class TestPrompt(unittest.TestCase):
    def test_make_conding_prompt(self):
        prompt = make_coding_prompt(t.int, {"x": t.int}, "Add 'x' + 'y'", "add", ["x", "y"])
        self.assertTrue(prompt.find("def add(x: int, y) -> int:") >= 0)
        prompt = make_coding_prompt(
            t.dict({"dirname": t.str, "basename": t.str, "ext": t.str}),
            None,
            "Split a file path 'path' into its components",
            "split",
            ["path"],
        )
        print(prompt)


if __name__ == "__main__":
    unittest.main()
