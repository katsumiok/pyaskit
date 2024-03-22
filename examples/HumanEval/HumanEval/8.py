from pyaskit import function
from typing import List, Tuple

@function(codable=True)
def sum_product(numbers: List[int]) -> Tuple[int, int]:
    """ For a given list of {{numbers}}, return a tuple consisting of a sum and a product of all the integers in a list.
    Empty sum should be equal to 0 and empty product should be equal to 1.
    >>> sum_product([])
    (0, 1)
    >>> sum_product([1, 2, 3, 4])
    (10, 24)
    """