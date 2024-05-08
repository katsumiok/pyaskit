from pyaskit import function

@function(codable=True)
def right_angle_triangle(a, b, c):
    '''
    Given the lengths of the three sides {{a}}, {{b}}, and {{c}} of a triangle. Return True if the three
    sides form a right-angled triangle, False otherwise.
    A right-angled triangle is a triangle in which one angle is right angle or 
    90 degree.
    Example:
    right_angle_triangle(3, 4, 5) == True
    right_angle_triangle(1, 2, 3) == False
    '''
