from itertools import chain, combinations

def powerset(iterable):
    ''' Given an iterable, create the powerset

    :params iterable: The iterable to create a powerset of
    :returns: A powerset iterator
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def find_piece(resource, user, weight):
    ''' Given a collection of items and a user preference,
    propose an allocation meeting the specified weight.

    :param resource: The resource we can choose from
    :param user: The user preferences to weight with
    :param weight: The weight we are attempting to hit
    :returns: (weight, allocation dict)
    '''
    piece = (0, []) # a proposed slice in the resource
    items = dict((k, user.value_of(k)) for k in resource
        if 0 < user.value_of(k) <= weight)
    cakes = sorted(items, key=lambda k: items[k], reverse=True)

    for possible in powerset(cakes):
        value = sum(items[k] for k in possible)
        check = (value, list(possible))
        if   value == weight: return check
        elif value  < weight: piece = max(piece, check)
    return piece

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
    value to the stopping value with the supplied
    step size of any numeric type.

    :param start: The start of the range
    :param stop: The stop of the range
    :param step: The step size of the range
    '''
    current = start
    while current < stop:
        yield current
        current += step
