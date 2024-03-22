from pyaskit import function
from typing import List

@function(codable=True)
def factorize(n: int) -> List[int]:
    """ Return list of prime factors of given integer {{n}} in the order from smallest to largest.
    Each of the factors should be listed number of times corresponding to how many times it appears in factorization.
    Input number should be equal to the product of all factors
    >>> factorize(8)
    [2, 2, 2]
    >>> factorize(25)
    [5, 5]
    >>> factorize(70)
    [2, 5, 7]
    """