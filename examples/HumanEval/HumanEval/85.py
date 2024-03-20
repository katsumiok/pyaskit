from pyaskit import function

@function(codable=True)
def add(lst):
    """Given a non-empty list of integers {{lst}}. Add the even elements that are at odd indices.

    Examples:
        add([4, 2, 6, 7]) ==> 2
    """