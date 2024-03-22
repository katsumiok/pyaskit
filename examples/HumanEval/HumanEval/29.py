from pyaskit import function
from typing import List

@function(codable=True)
def filter_by_prefix(strings: List[str], prefix: str) -> List[str]:
    """ Filter an input list of {{strings}} only for ones that start with a given {{prefix}}.
    >>> filter_by_prefix([], 'a')
    []
    >>> filter_by_prefix(['abc', 'bcd', 'cde', 'array'], 'a')
    ['abc', 'array']
    """