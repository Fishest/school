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

def create_pieces(resource, user, count=2, weight=None):
    ''' Given a resource, split it into count many pieces
    with the specified weight (or user.resolution / count)
    depending on the supplied user preference.

    :param resource: The resource to split
    :param user: The user preference to split by
    :param count: The number of pieces to split
    :param weight: The weight to split into
    '''
    pieces = []
    weight = weight or int(user.resolution / count)
    resource = set(resource)
    for n in range(count - 1):
        piece = find_piece(resource, user, weight)
        pieces.append(piece[1])
        resource = resource.difference(piece[1])
    pieces.append(list(resource)) # the rest is a single slice
    return pieces

def integrate(fx, xa, xb, ns):
    ''' Approximates the integral of the supplied
    function by using the trapezoidal rule.

    :param fx: The function to integrate
    :param xa: The starting point of the integral
    :param xb: The ending point of the integral
    :param ns: The number of subinterval steps to take
    '''
    h = (xb - xa) / ns
    s = fx(xa) + fx(xb)
    for i in xrange(1, ns):
        s += 2 * fx(xa + i * h)
    return s * h / 2

def frange(start, stop, step=1):
    ''' Generates a range from the starting
    value to the stopping value with the supplied
    step size.

    :param start: The start of the range
    :param stop: The stop of the range
    :param step: The step size of the range
    '''
    current = start
    while current < stop:
        yield current
        current += step
