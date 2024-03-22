from pyaskit import function

@function(codable=True)
def fib(n: int):
    """Return {{n}}-th Fibonacci number.
    >>> fib(10)
    55
    >>> fib(1)
    1
    >>> fib(8)
    21
    """