from pyaskit import function
from typing import List

@function(codable=True)
def below_zero(operations: List[int]) -> bool:
    """ You're given a list of deposit and withdrawal operations {{operations}} on a bank account that starts with
    zero balance. Your task is to detect if at any point the balance of account falls below zero, and
    at that point function should return True. Otherwise it should return False.
    >>> below_zero([1, 2, 3])
    False
    >>> below_zero([1, 2, -4, 5])
    True
    """