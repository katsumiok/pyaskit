# Example of programming by example (PBE) in pyaskit
from pyaskit import define
import pyaskit.types as t

training_examples = [
    {"input": {"x": "1", "y": "0"}, "output": "1"},
    {"input": {"x": "1", "y": "1"}, "output": "10"},
    {"input": {"x": "101", "y": "11"}, "output": "1000"},
    {"input": {"x": "1001", "y": "110"}, "output": "1111"},
    {"input": {"x": "1111", "y": "1"}, "output": "10000"},
]

add_binary = define(t.str, "Add {{x}} and {{y}}", training_examples=training_examples)
sum = add_binary(x="101", y="11")
print(sum)

test_examples = [
    {"input": {"x": "0", "y": "1"}, "output": "1"},
    {"input": {"x": "10", "y": "0"}, "output": "10"},
    {"input": {"x": "110", "y": "10"}, "output": "1000"},
]
f = add_binary.compile(test_examples=test_examples)
sum = f(x="101", y="11")
print(sum)
