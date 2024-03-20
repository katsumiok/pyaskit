from pyaskit import function

def count_upper(s: str) -> int:
    @function(codable=True)
    """
    Given a string {{s}}, count the number of uppercase vowels in even indices.
    
    For example:
    count_upper('aBCdEf') returns 1
    count_upper('abcdefg') returns 0
    count_upper('dBBE') returns 0
    """