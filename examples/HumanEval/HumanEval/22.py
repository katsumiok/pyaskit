from pyaskit import function
from typing import List, Any

@function(codable=True)
def filter_integers(values: List[Any]) -> List[int]:
    """ Filter given list of any python values {{values}} only for integers
    >>> filter_integers(['a', 3.14, 5])
    [5]
    >>> filter_integers([1, 2, 3, 'abc', {}, []])
    [1, 2, 3]
    """