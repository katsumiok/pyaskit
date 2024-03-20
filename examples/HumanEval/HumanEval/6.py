from pyaskit import function
from typing import List

@function(codable=True)
def parse_nested_parens(paren_string: str) -> List[int]:
    """ Input to this function is a string {{paren_string}} represented multiple groups for nested parentheses separated by spaces.
    For each of the group, output the deepest level of nesting of parentheses.
    E.g. (()()) has maximum two levels of nesting while ((())) has three.

    >>> parse_nested_parens('(()()) ((())) () ((())()())')
    [2, 3, 1, 3]
    """