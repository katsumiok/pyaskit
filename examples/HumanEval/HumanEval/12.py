from pyaskit import function
from typing import List, Optional

@function(codable=True)
def longest(strings: List[str]) -> Optional[str]:
    """ Out of list of {{strings}}, return the longest one. Return the first one in case of multiple
    strings of the same length. Return None in case the input list is empty.
    >>> longest([])

    >>> longest(['a', 'b', 'c'])
    'a'
    >>> longest(['a', 'bb', 'ccc'])
    'ccc'
    """