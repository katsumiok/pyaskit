from pyaskit import function
from typing import List

@function(codable=True)
def all_prefixes(string: str) -> List[str]:
    """ Return list of all prefixes from shortest to longest of the input {{string}}
    >>> all_prefixes('abc')
    ['a', 'ab', 'abc']
    """