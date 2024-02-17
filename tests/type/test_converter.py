import unittest
from typing import Tuple, Union, List, Tuple, Dict

try:
    from typing import TypedDict
except ImportError:
    from typing_extensions import TypedDict
import pyaskit.types as t
from pyaskit.types.converter import convert_type


class TestConvert(unittest.TestCase):
    def test_int(self):
        self.assertEqual(convert_type(int), t.int)

    def test_float(self):
        self.assertEqual(convert_type(float).validate(5.5), t.float.validate(5.5))

    def test_bool(self):
        self.assertEqual(convert_type(bool), t.bool)

    def test_str(self):
        self.assertEqual(convert_type(str), t.str)

    def test_list(self):
        self.assertTrue(convert_type(List[int]).validate([1, 2, 3]))

    def test_tuple(self):
        self.assertTrue(convert_type(Tuple[int, float]).validate([1, 2.0]))

    def test_union(self):
        self.assertTrue(convert_type(Union[int, str]).validate("hello"))

    def test_typed_dict(self):
        class Point(TypedDict):
            x: int
            y: int

        self.assertTrue(convert_type(Point).validate({"x": 1, "y": 2}))

    # def test_literal(self):
    #     self.assertTrue(convert_type(Literal[5]).validate(5))
    #     self.assertTrue(convert_type(Literal["hello"]).validate("hello"))
    #     self.assertTrue(convert_type(Literal[True]).validate(True))

    def test_record(self):
        self.assertTrue(convert_type(Dict[str, int]).validate({"x": 1, "y": 2}))
