from pyaskit import function

@function(codable=True)
def is_multiply_prime(a):
    """Write a function that returns true if the given number {{a}} is the multiplication of 3 prime numbers
    and false otherwise.
    Knowing that ({{a}}) is less then 100. 
    Example:
    is_multiply_prime(30) == True
    30 = 2 * 3 * 5
    """