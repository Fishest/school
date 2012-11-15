from itertools import chain, combinations


def powerset(iterable):
    ''' Given an iterable, create the powerset

    :params iterable: The iterable to create a powerset of
    :returns: A powerset iterator
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def all_same(iterable):
    ''' Given an iterable, check if all the values
    in that iterable are the same value.

    :param iterable: The iterable to check for equality
    :returns: True if all the values are the same, False otherwise
    '''
    return len(set(iterable)) == 1


def all_unique(iterable):
    ''' Given an iterable, check if all the values
    in that iterable are unique

    :param iterable: The iterable to check for uniqueness
    :returns: True if all the values are the unique, False otherwise
    '''
    values = list(iterable)
    return len(set(values)) == len(values)


def integrate(fx, x0, x1, ns):
    ''' Approximates the integral of the supplied
    function by using the trapezoidal rule.

    :param fx: The function to integrate
    :param x0: The starting point of the integral
    :param x1: The ending point of the integral
    :param ns: The number of subinterval steps to take
    '''
    h = (x1 - x0) / ns
    s = fx(x0) + fx(x1)
    for i in xrange(1, ns):
        s += 2 * fx(x0 + i * h)
    return s * h / 2


def any_range(start, stop, step=1):
    ''' Generates a range from the starting
    value to the stopping value (exclusive) with the
    supplied step size of any numeric type.

    :param start: The start of the range
    :param stop: The stop of the range
    :param step: The step size of the range
    '''
    current = start
    while current < stop:
        yield current
        current += step


class Interval(object):
    ''' Represents a single linear interval
    '''

    @staticmethod
    def create(points):
        ''' Given a list of points, create a collection
        of intervals.

        :param points: The points to create intervals for
        :returns: The collection of intervals
        '''
        intervals = []
        ox, oy = 0, 0
        for x, y in points:
            if x != 0:
                interval = Interval((ox, oy), (x, y))
                intervals.append(interval)
                ox, oy = x, y
            else: oy = y
        if ox < 1:
            intervals.append(Interval((ox, oy), (1, 0)))
        return intervals

    def __init__(self, start, stop):
        '''
        :param start: The starting (x1, y1)
        :param stop: The ending (x2, y2)
        '''
        self.x1, self.y1 = start
        self.x2, self.y2 = stop

        if self.x1 >= self.x2:
            raise ValueError("invalid interval range")

        # constants for y = mx + b
        self.m  = (self.y2 - self.y1) / (self.x2 - self.x1)
        self.b  = (self.y1 - (self.m * self.x1))

    def _integrate(self, x):
        ''' Integrate based on the linear equation
        y = mx + b

        :param x: The x point to integrate with
        :returns: The integral of this interval
        '''
        return self.m * x * x / 2 + self.b * x

    def area(self, a, b):
        ''' Calculate the area of this interval from a to b.
        The area is valid only between the left and right boundaries
        of this interval.

        :param a: The starting point of the area
        :param b: The ending point of the area
        :returns: The area of the specified range
        '''
        l, r = max(self.x1, a), min(self.x2, b)
        if (l > self.x2) or (r < self.x1):
            return 0
        return self._integrate(r) - self._integrate(l)

    def __str__(self):
        ''' Returns a string representation of this interval

        :returns: The string representation
        '''
        return "%s - %s" % ((self.x1, self.y1), (self.x2, self.y2))
