# Example of programming by example (PBE) in pyaskit
from pyaskit import function


def training_examples():
    assert add_binary("1", "0") == "1"
    assert add_binary("1", "1") == "10"
    assert add_binary("101", "11") == "1000"
    assert add_binary("1001", "110") == "1111"
    assert add_binary("1111", "1") == "10000"


def test_examples():
    assert add_binary("0", "1") == "1"
    assert add_binary("10", "0") == "10"
    assert add_binary("110", "10") == "1000"


@function(codable=True, example=training_examples, test=test_examples)
def add_binary(x: str, y: str) -> str:
    """Add {{x}} and {{y}}"""


sum = add_binary(x="101", y="11")
print(sum)
