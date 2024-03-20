from pyaskit import function

@function(codable=True)
def digits(n):
    """Given a positive integer {{n}}, return the product of the odd digits.
    Return 0 if all digits are even.
    For example:
    digits(1)  == 1
    digits(4)  == 0
    digits(235) == 15
    """