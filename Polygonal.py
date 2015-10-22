__author__ = 'mario'

import random
from math import pi, sqrt, cos, sin

#
# Checks if a point (x,y) is inside a polygon
# @param x Integer
# @param x Integer
# @param poly List of tuples with coordinates [(a,b),(c,d)].
#
# @returns True if point is within the polygon, False otherwise
#
def point_in_poly(x,y,poly):

    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def points_in_poly(coordinates, poly):
    for x,y in coordinates:
        if point_in_poly(x,y, poly) is False:
            return False

    return True
#
# Converts a number in Centimeters to a number in Decimal degrees.
# If needed, consult https://en.wikipedia.org/wiki/Decimal_degrees
#
# @param cm an input Float in Centimeters
#
# @returns Float with the converted value in Decimal degrees
#
def centimetersToDecimalDegrees(cm):
    conversionFactor = 8.983111749910169e-08
    return conversionFactor * cm


#
# Generate uniformly distributed random points in a circle of radius 'r'
#
# @param r the radius of the circle
# @param n the number of points to be generated
#
# @returns a list with random coordinates (x,y)
#
def random_coordinates(center, r, n):
    ret = []
    for i in range(0, n):
        x, y = center
        xx, yy = random_coordinate(r)
        ret.append((x+xx, y+yy))

    return ret

#
# Generate uniformly distributed random points in a circle of radius 'r'
# Info here http://mathworld.wolfram.com/DiskPointPicking.html
#
# @param r the radius of the circle
#
# @returns a random coordinate (x,y) around the center (0,0)
#
def random_coordinate(r):
    angle = 2 * pi * random.random()
    radius = random.random()

    x = r * sqrt(radius) * cos(angle)
    y = r * sqrt(radius) * sin(angle)

    return (x,y)
