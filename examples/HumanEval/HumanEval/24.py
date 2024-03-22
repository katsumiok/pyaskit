from pyaskit import function

@function(codable=True)
def largest_divisor(n: int) -> int:
    """ For a given number {{n}}, find the largest number that divides {{n}} evenly, smaller than {{n}}
    >>> largest_divisor(15)
    5
    """