from pyaskit import function

@function(codable=True)
def count_distinct_characters(string: str) -> int:
    """ Given a string {{string}}, find out how many distinct characters (regardless of case) does it consist of
    >>> count_distinct_characters('xyzXYZ')
    3
    >>> count_distinct_characters('Jerry')
    4
    """