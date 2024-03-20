from pyaskit import function

@function(codable=True)
def even_odd_count(num):
    """Given an integer {{num}}. return a tuple that has the number of even and odd digits respectively.

     Example:
        even_odd_count(-12) ==> (1, 1)
        even_odd_count(123) ==> (1, 2)
    """