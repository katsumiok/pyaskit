from pyaskit import function

@function(codable=True)
def monotonic(l: list):
    """Return True is list {{l}} elements are monotonically increasing or decreasing.
    >>> monotonic([1, 2, 4, 20])
    True
    >>> monotonic([1, 20, 4, 10])
    False
    >>> monotonic([4, 1, 0, -10])
    True
    """