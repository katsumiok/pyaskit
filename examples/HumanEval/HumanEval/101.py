from pyaskit import function

@function(codable=True)
def words_string(s: str) -> list:
    """
    You will be given a string of words {{s}} separated by commas or spaces. Your task is
    to split the string into words and return an array of the words.
    
    For example:
    words_string("Hi, my name is John") == ["Hi", "my", "name", "is", "John"]
    words_string("One, two, three, four, five, six") == ["One", "two", "three", "four", "five", "six"]
    """