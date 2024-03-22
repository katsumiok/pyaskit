from pyaskit import function

def digitSum(s: str) -> int:
    @function(codable=True)
    """Task
    Write a function that takes a string {{s}} as input and returns the sum of the upper characters only'
    ASCII codes.

    Examples:
        digitSum("") => 0
        digitSum("abAB") => 131
        digitSum("abcCd") => 67
        digitSum("helloE") => 69
        digitSum("woArBld") => 131
        digitSum("aAaaaXa") => 153
    """