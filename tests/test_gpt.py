import unittest
import pyaskit.gpt as gpt


class TestGPT(unittest.TestCase):
    def test_extract_json(self):
        self.assertEqual(1, gpt.extract_json("...```json 1 ```..."))
        data = gpt.extract_json('{ "reason": "ok"}')
        self.assertEqual("ok", data["reason"])
        # expect raise
        with self.assertRaises(ValueError):
            gpt.extract_json("...```json 1 ```...```")

if __name__ == "__main__":
    unittest.main()
