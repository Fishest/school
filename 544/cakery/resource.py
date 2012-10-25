'''
'''
from cakery.utilities import any_range, find_piece

#------------------------------------------------------------
# interface
#------------------------------------------------------------
class Resource(object):
    ''' Represents a basic resource that is to be
    divided among a number of users.

    .. attribute:: value
    
       The current value of this resource in which
       the type may be unique to the resource in
       question.
    '''

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        raise NotImplementedError("value_of")

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        raise NotImplementedError("value_of")

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        :param piece: The piece to remove from this
        '''
        raise NotImplementedError("value_of")

    def create_pieces(self, user, count=2, weight=None):
        ''' Split the current resource it into count many pieces
        with the specified weight depending on the supplied user
        preference (or user.value_of(resource) / count).

        :param user: The user preference to split by
        :param count: The number of pieces to split
        :param weight: The weight to split into
        '''
        raise NotImplementedError("value_of")

    #------------------------------------------------------------
    # the magic methods
    #------------------------------------------------------------
    def __repr__(self):     return str(self.value)
    def __str__(self):      return str(self.value)
    def __ne__(self, that): return self.value != that.value
    def __eq__(self, that): return self.value == that.value
    def __lt__(self, that): return self.value  < that.value
    def __gt__(self, that): return self.value  > that.value
    def __le__(self, that): return self.value <= that.value
    def __ge__(self, that): return self.value >= that.value


#------------------------------------------------------------
# implementations
#------------------------------------------------------------
class ContinuousResource(Resource):
    ''' Represents a continuous resource that exists
    over a range from 0 to 1 (beach front property
    for example).

    This is represented internally as a
    range(start, end).
    '''

    def __init__(self, start, stop):
        ''' Initializes a new instance of the resource

        :param items: The items representing this resource
        '''
        if start > stop:
            raise ValueError("start value is greater than stop value")
        self.value = (start, stop)

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        (start, stop) = self.value
        return stop - start

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        (start, stop) = self.value
        return ContinuousResource(start, stop)

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        It should be noted that we can only remove from
        one end or another from a continuous resource. If you need
        to remove from the middle, you will have to split.

        :param piece: The piece to remove from this
        '''
        (this_x0, this_x1) = self.value
        (that_x0, that_x1) = piece.value
        if   that_x0 > this_x0: this_x0 = that_x0
        elif that_x1 < this_x1: this_x1 = that_x1
        self.value = (this_x0, this_x1)

    def create_pieces(self, user, count=2, weight=None):
        ''' Split the current resource it into count many pieces
        with the specified weight depending on the supplied user
        preference (or user.value_of(resource) / count).

        :param user: The user preference to split by
        :param count: The number of pieces to split
        :param weight: The weight to split into
        '''
        weight = weight or user.value_of(self) / count
        (x0, x1) = self.value
        x0s = list(any_range(x0, x1, weight))
        x1s = x0s[1:] + [x1] # remove start, add ending
        return [ContinuousResource(a, b) for a,b in zip(x0s, x1s)]


class CountedResource(Resource):
    ''' Represents a discrete resource that may
    have 1 or more of the same item available (class
    slots for example).

    This is represented internally as a dictionary.
    '''

    def __init__(self, items):
        ''' Initializes a new instance of the resource

        :param items: The items representing this resource
        '''
        if not isinstance(items, dict):
            items = dict((item, 1) for item in items)
        self.value = items

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        return sum(self.value.values())

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        return CountedResource(dict(self.value))

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        :param piece: The piece to remove from this
        '''
        if not isinstance(piece, dict):
            piece = dict((item, 1) for item in piece)

        for key, value in piece:
            if self.value.get(key, -1) - value < 0:
                raise ValueError("not enough supply to remove")
            self.value[key] -= value

        for key, value in self.value:
            if self.value[key] == 0:
                del self.value[key]


class CollectionResource(Resource):
    ''' Represents a discrete resource that has only
    one instance of each item (team member selection
    for example).

    This is represented internally as a list.
    '''

    def __init__(self, items):
        ''' Initializes a new instance of the resource

        :param items: The items representing this resource
        '''
        if not hasattr(items, '__iter__'):
            items = [items]
        self.value = list(items)

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        return len(self.value)

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        return CollectionResource(list(self.value))

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        :param piece: The piece to remove from this
        '''
        self.value = [v for v in self.value if v not in piece]

    def create_pieces(self, user, count=2, weight=None):
        ''' Split the current resource it into count many pieces
        with the specified weight depending on the supplied user
        preference (or user.value_of(resource) / count).

        :param user: The user preference to split by
        :param count: The number of pieces to split
        :param weight: The weight to split into
        '''
        pieces = []
        weight = weight or user.value_of(self) / count
        resource = set(self.value) # TODO what about repeats?
        for n in range(count - 1):
            piece = find_piece(resource, user, weight)
            pieces.append(piece[1])
            resource = resource.difference(piece[1])
        pieces.append(list(resource)) # the rest is a single slice
        return pieces
