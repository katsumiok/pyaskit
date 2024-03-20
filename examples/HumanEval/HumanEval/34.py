from pyaskit import function

@function(codable=True)
def unique(l: list):
    """Return sorted unique elements in a list {{l}}
    >>> unique([5, 3, 5, 2, 3, 3, 9, 0, 123])
    [0, 2, 3, 5, 9, 123]
    """