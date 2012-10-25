'''
'''
from fractions import Fraction
from cakery.utilities import any_range, powerset

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

    def find_piece(self, user, weight):
        ''' Attempt to find a piece of the current resource
        that meets the requested weight according to the
        given user.

        :param user: The user preferences to weight with
        :param weight: The weight we are attempting to hit
        :returns: The first piece matching that weight
        '''
        raise NotImplementedError("find_piece")

    def compare(this, that):
        ''' A utility method used to provide rich
        comparison operations on the resource.

        :param that: The other resource to compare
        :returns: -1: less than, 0: equal to, 1: greater than
        '''
        raise NotImplementedError("compare")

    #------------------------------------------------------------
    # common methods
    #------------------------------------------------------------
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
        cake = self.clone()
        for n in range(count - 1):
            piece = cake.find_piece(user, weight)
            pieces.append(piece)
            cake.remove(piece)
        pieces.append(cake) # the rest is a single slice
        return pieces

    #------------------------------------------------------------
    # the magic methods
    #------------------------------------------------------------
    def __repr__(self):     return str(self.value)
    def __str__(self):      return str(self.value)
    def __ne__(self, that): return self.compare(that) !=  0
    def __eq__(self, that): return self.compare(that) ==  0
    def __lt__(self, that): return self.compare(that) == -1
    def __gt__(self, that): return self.compare(that) ==  1
    def __le__(self, that): return self.compare(that) <=  0
    def __ge__(self, that): return self.compare(that) >=  0


#------------------------------------------------------------
# implementations
#------------------------------------------------------------
class ContinuousResource(Resource):
    ''' Represents a continuous resource that exists
    over a range from 0 to 1 (beach front property
    for example).

    This is represented internally as a (start, span).
    Also, all math is internally performed using
    rational values (fractions.Fraction).
    '''

    def __init__(self, start, span):
        ''' Initializes a new instance of the resource

        :param start: The starting point on the x-axis
        :param span: The span from the starting point
        '''
        self.value = (start, span)

    def actual_value(self):
        ''' Return an actual value that we can use for
        comparison for the algorithm.

        :returns: The actual value of the object
        '''
        return self.value[1]

    def clone(self):
        ''' Return a clone of this resource that is
        identical to the original.

        :returns: A clone of the current resource
        '''
        (start, span) = self.value
        return ContinuousResource(start, span)

    def remove(self, piece):
        ''' Update this resource by removing the
        specified piece.

        It should be noted that we can only remove from
        one end or another from a continuous resource. If you need
        to remove from the middle, you will have to split.

        :param piece: The piece to remove from this
        '''
        (this_x0, this_span) = self.value
        (that_x0, that_span) = piece.value
   
        # we are removing from the front
        # (0/1, 1/1) - (0/1, 1/4) = (1/4, 3/4)
        if this_x0 == that_x0:
            this_x0   += that_span
            this_span -= that_span
        # we are removing from the front
        # (0/1, 1/1) - (3/4, 1/4) = (0/1, 3/4)
        else: this_span -= that_span
        self.value = (this_x0, this_span)

    def find_piece(self, user, weight):
        ''' Attempt to find a piece of the current resource
        that meets the requested weight according to the
        given user.

        This is implemented with a Stern-Brocot tree.

        :param user: The user preferences to weight with
        :param weight: The weight we are attempting to hit
        :returns: The first piece matching that weight
        '''
        shift = 1.0 / user.resolution
        cake, value = self.clone(), user.value_of(self)
        if value < weight:
            raise ValueError("cannot find a piece with this weight")

        l, h = Fraction(0,1), cake.value[1]
        while (value < weight - shift) or (value > weight + shift):
            m = Fraction(l.numerator + h.numerator, l.denominator + h.denominator)
            cake.value = (cake.value[0], m)
            value = user.value_of(cake)
            if   value > weight: h = m
            elif value < weight: l = m
        return cake

    def compare(this, that):
        ''' A utility method used to provide rich
        comparison operations on the resource.

        :param that: The other resource to compare
        :returns: -1: less than, 0: equal to, 1: greater than
        '''
        return cmp(this.value[1], that.value[1])


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
        for key, value in piece.value.items():
            if self.value.get(key, -1) - value < 0:
                raise ValueError("not enough supply to remove")
            self.value[key] -= value

        for key, value in self.value.items():
            if self.value[key] == 0:
                del self.value[key]

    def find_piece(self, user, weight):
        ''' Attempt to find a piece of the current resource
        that meets the requested weight according to the
        given user.

        :param user: The user preferences to weight with
        :param weight: The weight we are attempting to hit
        :returns: The first piece matching that weight
        '''
        raise NotImplementedError("find_piece")


    def compare(this, that):
        ''' A utility method used to provide rich
        comparison operations on the resource.

        :param that: The other resource to compare
        :returns: -1: less than, 0: equal to, 1: greater than
        '''
        if this.value == that.value: return 0
        return cmp(sum(this.value.values()), sum(that.value.values()))


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
        self.value = [v for v in self.value if v not in piece.value]

    def find_piece(self, user, weight):
        ''' Attempt to find a piece of the current resource
        that meets the requested weight according to the
        given user.

        :param user: The user preferences to weight with
        :param weight: The weight we are attempting to hit
        :returns: The first piece matching that weight
        '''
        piece = (0, []) # a proposed slice in the resource
        items = []

        # sort the values by weight to make the least amount of
        # cuts possible, otherwise keep them ordered by the 
        # original resource ordering
        for item in self.value:
            cake = CollectionResource([item])
            value = user.value_of(cake)
            if 0 < value <= weight: items.append((item, value))
        cakes = sorted(items, key=lambda k: k[1], reverse=True)
        cakes = [item[0] for item in items]
        items = dict(items)

        # try all possible combinations of resources until we
        # find one that matches the weight we are looking for
        for possible in powerset(cakes):
            value = sum(items[k] for k in possible)
            check = (value, list(possible))
            if   value == weight: piece = check; break
            elif value  < weight: piece = max(piece, check)
        return CollectionResource(piece[1])

    def compare(this, that):
        ''' A utility method used to provide rich
        comparison operations on the resource.

        :param that: The other resource to compare
        :returns: -1: less than, 0: equal to, 1: greater than
        '''
        if this.value == that.value: return 0
        return cmp(len(this.value), len(that.value))
