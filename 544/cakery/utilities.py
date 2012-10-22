from itertools import chain, combinations

def powerset(iterable):
    ''' Given an iterable, create the powerset

    :params iterable: The iterable to create a powerset of
    :returns: A powerset iterator
    '''
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def find_piece(resources, pref, weight):
    ''' Given a collection of items and a user preference,
    propose an allocation meeting the specified weight.

    :param resources: The resource we can choose from
    :param pref: The user preferences to weight with
    :param weight: The weight we are attempting to hit
    :returns: (weight, allocation dict)
    '''
    piece = (0, []) # a proposed slice in the resources
    items = dict((k, pref.value_of(k)) for k in resources
        if 0 < pref.value_of(k) <= weight)
    cakes = sorted(items, key=lambda k: items[k], reverse=True)

    for possible in powerset(cakes):
        value = sum(items[k] for k in possible)
        check = (value, list(possible))
        if   value == weight: return check
        elif value  < weight: piece = max(piece, check)
    return piece

def create_pieces(resources, pref, count=2, weight=None):
    ''' Given a resource, split it into count many pieces
    with the specified weight (or user.resolution / count)
    depending on the supplied user preference.

    :param resources: The resource to split
    :param pref: The preference to split by
    :param count: The number of pieces to split
    :param weight: The weight to split into
    '''
    pieces = []
    weight = weight or int(pref.resolution / count)
    resources = set(resources)
    for n in range(count - 1):
        piece = find_piece(resources, pref, weight)
        pieces.append(piece[1])
        resources = resources.difference(piece[1])
    pieces.append(resources) # the rest is a single slice
    return pieces
