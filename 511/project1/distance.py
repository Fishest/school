'''
Distances
-----------------------------------------------------------

A collection of distance functions that can be used to
determine the distance between two points.
'''
import math

def manhattan(s, e):
    ''' Returns the manhattan distance between two points

    >>> manhattan((2,2),(4,4))
    4

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    return abs(s[0] - e[0]) + abs(s[1] - e[1])

cityblock = manhattan

def euclidean(s, e):
    ''' Returns the euclidean distance between two points

    >>> int(euclidean((2,2),(4,4)) + 0.5)
    3

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    return math.sqrt((s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2)

def euclideanSquared(s, e):
    ''' Returns the euclidean squared distance between two points

    >>> euclideanSquared((2,2),(4,4))
    8

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    return (s[0] - e[0]) ** 2 + (s[1] - e[1]) ** 2

def chebyshev(s, e):
    ''' Returns the chebyshev distance between two points

    >>> chebyshev((2,2),(4,4))
    2

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    return max(abs(s[0] - e[0]), abs(s[1] - e[1]))

def canberra(s, e):
    ''' Returns the canberra distance between two points

    >>> canberra((2,2),(4,4))
    0

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    left  = abs(s[0] - e[0]) / (abs(s[0]) + abs(e[0]))
    right = abs(s[1] - e[1]) / (abs(s[1]) + abs(e[1]))
    return left + right

def braycurtis(s, e):
    ''' Returns the braycurtis distance between two points

    >>> braycurtis((2,2),(4,4))
    0

    :param s: The starting position to measure
    :param e: The ending position to measure
    :returns: The distance between the two points
    '''
    left  = abs(s[0] - e[0]) + abs(s[1] - e[1])
    right = abs(s[0] + e[0]) + abs(s[1] + e[1])
    return left / right
