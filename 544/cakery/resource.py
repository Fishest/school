'''
'''

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

    def __str__(self):
        ''' Returns a string representation of the
        underlying resource.

        :returns: A string representation of the resoruce
        '''
        return str(self.value)

    __repr__ = __str__

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

    def __init__(self, start, stop, step=1):
        ''' Initializes a new instance of the resource

        :param items: The items representing this resource
        '''
        self.start = start
        self.stop  = stop
        self.step  = step
        self.value = (start, stop)

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        return self.stop - self.start

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        return ContinuousResource(self.start, self.stop, self.step)

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        :param piece: The piece to remove from this
        '''
        (ostart, oend) = piece.value


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
