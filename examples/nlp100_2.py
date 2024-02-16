from pyaskit import function


# 00. Reversed string
@function(codable=True)
def func00(s: str) -> str:
    """Obtain the string that arranges letters of the string {{s}} in reverse order (tail to head)."""


assert func00("stressed") == "desserts"


# 01. “schooled”
@function(codable=True)
def func01(s: str) -> str:
    """Obtain the string that concatenates the 1st, 3rd, 5th, and 7th letters in the string {{s}}."""


assert func01("schooled") == "shoe"
