from pyaskit import function

@function(codable=True)
def flip_case(string: str) -> str:
    """ For a given {{string}}, flip lowercase characters to uppercase and uppercase to lowercase.
    >>> flip_case('Hello')
    'hELLO'
    """