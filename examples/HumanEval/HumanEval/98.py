from pyaskit import function

@function(codable=True)
def count_upper(s: str) -> int:
    """
    Given a string {{s}}, count the number of uppercase vowels in even indices.
    
    For example:
    count_upper('aBCdEf') returns 1
    count_upper('abcdefg') returns 0
    count_upper('dBBE') returns 0
    """