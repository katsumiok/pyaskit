import unittest
import pyaskit.template as template


class TestTemplate(unittest.TestCase):
    def test_extract_variables(self):
        self.assertEqual(template.extract_variables("{{a }} {{a }}"), ["a"])
        self.assertEqual(template.extract_variables("{{ a }} {{ b }}"), ["a", "b"])
        with self.assertRaises(ValueError):
            template.extract_variables("{{ a + b }}")

    def test_convert_template(self):
        self.assertEqual(template.convert_template("{{ a }}"), "'a'")
        self.assertEqual(template.convert_template("{{ a }} {{ b }}"), "'a' 'b'")


if __name__ == "__main__":
    unittest.main()
