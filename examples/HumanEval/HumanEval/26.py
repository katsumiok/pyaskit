from pyaskit import function
from typing import List

@function(codable=True)
def remove_duplicates(numbers: List[int]) -> List[int]:
    """ From a list of integers {{numbers}}, remove all elements that occur more than once.
    Keep order of elements left the same as in the input.
    >>> remove_duplicates([1, 2, 3, 2, 4])
    [1, 3, 4]
    """