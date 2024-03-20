from pyaskit import function

@function(codable=True)
def triangle_area(a, h):
    """Given length of a side {{a}} and height {{h}} return area for a triangle.
    >>> triangle_area(5, 3)
    7.5
    """