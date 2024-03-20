from pyaskit import function
from typing import List, Tuple

@function(codable=True)
def rolling_max(numbers: List[int]) -> List[int]:
    """ From a given list of {{numbers}}, generate a list of rolling maximum element found until given moment
    in the sequence.
    >>> rolling_max([1, 2, 3, 2, 3, 4, 2])
    [1, 2, 3, 3, 3, 4, 4]
    """