import math, sys
from cakery.utilities import integrate

#------------------------------------------------------------
# interface
#------------------------------------------------------------
class Preference(object):
    ''' Represents the preferences of a given user
    about a given resource.
    
    It should be noted, that the implementation of each
    preference type is strongly coupled to the underlying
    resource type. Trying to use mismatched types (Counted
    with Collection for example) will result in runtime errors.
    '''

    def value_of(self, resource):
        ''' Given a resource, return the total value
        of this resource to the current user.

        :params resource: The resource to get the value of
        :returns: The total value of the items
        '''
        raise NotImplementedError("value_of")

    def __str__(self):
        ''' Returns a string representation of the preference

        :returns: The string representation of this preference
        '''
        return "Preference(%s)" % self.user

    __repr__ = __str__


#------------------------------------------------------------
# implementations
#------------------------------------------------------------
class ContinuousPreference(Preference):
    ''' Represents the preference of a given user about a continuous
    resource. This preference is supplied by a function over a given
    interval.
    '''

    def __init__(self, user, function, resolution=1000):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param function: The function that describes the user's preference
        :param resolution: The number of steps we will take in the integral
        '''
        self.user = user
        self.function = function
        self.resolution = resolution

    def value_of(self, resource):
        ''' Given a resource, return the total value
        of this resource to the current user.

        :params resource: The resource to get the value of
        :returns: The total value of the items
        '''
        (x0, span) = resource.value
        return integrate(self.function, x0, x0 + span, self.resolution)


class CountedPreference(Preference):
    ''' Represents the preference of a given user about a collection
    of items that can be requested more than once.

    Here, a value is given to each item and a count filter can
    optionally be specified that suggests how many of each item
    we care to retrieve (defaults to as many as possible).
    '''

    def __init__(self, user, values, counts=None):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param values: The preference values of the user
        :param counts: Listing of how many of each item is wanted
        '''
        self.user = user
        self.values = values or {}
        self.counts = counts or dict((k, 1) for k in self.values)
        #self.counts = counts or dict((k, sys.maxint) for k in self.values)

    def value_of(self, resource):
        ''' Given a resource, return the total value
        of this resource to the current user.

        :params resource: The resource to get the value of
        :returns: The total value of the items
        '''
        total = 0
        for item, count in resource.value.items():
            value = self.values.get(item, 0)
            wants = self.counts.get(item, 0)
            total += value * min(wants, count)
        return total


class CollectionPreference(Preference):
    ''' Represents the discrete preferences of a given user
    about a supplied resource(s). The preferences are
    represented as a dictionary of resource -> preference
    where the preference value is a fixed point value (no
    decimals).
    
    The preferences should be assigned as a percentage
    of the defined resolution (integers). We assume the
    preferences collectively add up to specified resolution
    (or slightly less, but never more).
    '''

    def __init__(self, user, values):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param values: The preference values of the user
        '''
        self.user = user
        self.values = values or {}

    def value_of(self, resource):
        ''' Given a resource, return its total value
        to this user.

        :params resource: The resource to get the value of
        :returns: The total value of the items
        '''
        return sum(value for item, value in self.values.items()
            if item in resource.value)
