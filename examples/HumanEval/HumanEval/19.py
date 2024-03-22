from pyaskit import function
from typing import List

@function(codable=True)
def sort_numbers(numbers: str) -> str:
    """ Input is a space-delimited string {{numbers}} of numberals from 'zero' to 'nine'.
    Valid choices are 'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight' and 'nine'.
    Return the string with numbers sorted from smallest to largest
    >>> sort_numbers('three one five')
    'one three five'
    """