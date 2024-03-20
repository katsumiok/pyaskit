from pyaskit import function

@function(codable=True)
def is_palindrome(text: str):
    """
    Checks if given string {{text}} is a palindrome
    >>> is_palindrome('')
    True
    >>> is_palindrome('aba')
    True
    >>> is_palindrome('aaaaa')
    True
    >>> is_palindrome('zbcd')
    False
    """