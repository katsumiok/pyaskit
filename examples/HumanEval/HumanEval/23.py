from pyaskit import function

@function(codable=True)
def strlen(string: str) -> int:
    """ Return length of given {{string}}
    >>> strlen('')
    0
    >>> strlen('abc')
    3
    """