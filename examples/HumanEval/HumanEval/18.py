from pyaskit import function

@function(codable=True)
def how_many_times(string: str, substring: str) -> int:
    """ Find how many times a given {{substring}} can be found in the original {{string}}. Count overlapping cases.
    >>> how_many_times('', 'a')
    0
    >>> how_many_times('aaa', 'a')
    3
    >>> how_many_times('aaaa', 'aa')
    3
    """