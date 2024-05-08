from pyaskit import function

@function(codable=True)
def is_nested(string):
    '''
    Create a function that takes a string {{string}} as input which contains only square brackets.
    The function should return True if and only if there is a valid subsequence of brackets 
    where at least one bracket in the subsequence is nested.

    is_nested('[[]]') ➜ True
    is_nested('[]]]]]]][[[[[]') ➜ False
    is_nested('[][]') ➜ False
    is_nested('[]') ➜ False
    is_nested('[[][]]') ➜ True
    is_nested('[[]][[') ➜ True
    '''