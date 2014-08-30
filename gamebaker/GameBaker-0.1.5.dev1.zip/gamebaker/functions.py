"""
A collection of functions for use in projects using GameBaker.
All angles are in degrees, anticlockwise from the right (the 3 o'clock position on a clock face).
The origin is at the top left.
Unlike in maths (but as is common for computer graphics), the y axis goes from top to bottom.
"""

import math

def distance(x1, y1, x2, y2):
    """
    Calculate the distance between two points.
    """
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)
    
def angle(x1, y1, x2, y2):
    """
    Calculate the angle between two points.
    """
    x_distance = abs(x1-x2)
    y_distance = abs(y1-y2)
    if x_distance == 0:
        angle = 90
    else:
        angle = math.degrees(math.atan(y_distance/x_distance))
    if x1 <= x2 and y1 >= y2:
        return angle
    elif x1 >= x2 and y1 >= y2:
        return 180 - angle
    elif x1 >= x2 and y1 <= y2:
        return 180 + angle
    elif x1 <= x2 and y1 <= y2:
        return 360 - angle
    else:
        raise ValueError("Angle between ({}, {}) and ({}, {}) could not be calculated".format(x1, y1, x2, y2))
        
def point_along_angle(x, y, angle, distance):
    """
    Return a point at a certain distance and angle from another point.
    """
    x_difference = distance * math.cos(math.radians(angle))
    y_difference = -1 * distance * math.sin(math.radians(angle))
    
    return (x + x_difference, y + y_difference)