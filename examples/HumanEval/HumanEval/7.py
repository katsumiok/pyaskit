from pyaskit import function
from typing import List

@function(codable=True)
def filter_by_substring(strings: List[str], substring: str) -> List[str]:
    """ Filter an input list of {{strings}} only for ones that contain given {{substring}}
    >>> filter_by_substring([], 'a')
    []
    >>> filter_by_substring(['abc', 'bacd', 'cde', 'array'], 'a')
    ['abc', 'bacd', 'array']
    """