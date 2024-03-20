from pyaskit import function

@function(codable=True)
def max_element(l: list):
    """Return maximum element in the list {{l}}.
    >>> max_element([1, 2, 3])
    3
    >>> max_element([5, 3, -5, 2, -3, 3, 9, 0, 123, 1, -10])
    123
    """