from pyaskit import function
from typing import List


@function(codable=True)
def concatenate(strings: List[str]) -> str:
    """ Concatenate list of {{strings}} into a single string
    >>> concatenate([])
    ''
    >>> concatenate(['a', 'b', 'c'])
    'abc'
    """