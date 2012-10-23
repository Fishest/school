
class BasePreference(object):
    ''' Represents the preferences of a given user
    about a given abstract resource.
    '''

    def normalize(self):
        ''' Noramlize the current preferences to match
        the current resolution.

        .. note::

           To keep this in fixed point, the total sum may be
           slightly less than 100, but never more.
        '''
        raise NotImplementedError("normalize")

    def is_valid(self):
        ''' A check to see if the user preferences are valid

        :returns: True if valid, false otherwise
        '''
        raise NotImplementedError("is_valid")

    def value_of(self, items):
        ''' Given one or more items, return the total value
        to this user.

        :params items: The item(s) to get the value of
        :returns: The total value of the items
        '''
        raise NotImplementedError("value_of")

class ContinuousPreference(BasePreference):
    ''' Represents the preference of a given user about a continuous
    resource. This preference is supplied by a function over a given
    interval.
    '''

    def __init__(self, user, function, resolution=100, tolerance=0.05):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param function: The function that describes the user's preference
        :param resolution: The number of steps we will take in the integral
        :param tolerance: The amount we are allowed to be off from unit value
        '''
        self.user = user
        self.function = function
        self.resolution = resolution
        self.tolerance = int(resolution * tolerance)

    def normalize(self):
        ''' Noramlize the current preferences to match
        the current resolution.
        '''
        # we need to scale the function?
        pass

    def is_valid(self):
        ''' A check to see if the user preferences are valid

        :returns: True if valid, false otherwise
        '''
        # is the resource unit value
        raise NotImplementedError("is_valid")

    def value_of(self, resource):
        ''' Given a resource, return its total value
        to this user.

        :params resource: The resource to get the value of
        :returns: The total value of the items
        '''
        # integrate over the resource range
        raise NotImplementedError("value_of")

class Preference(BasePreference):
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

    def __init__(self, user, values, resolution=100, tolerance=0.05):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param values: The preference values of the user
        :param resolution: The fixed point max resolution (default 100)
        :param tolerance: The amount we are allowed to be off from unit value
        '''
        self.user = user
        self.values = values or {}
        self.resolution = resolution
        self.tolerance = int(resolution * tolerance)

    def update(self, resources, remove=False):
        ''' Given a list of resources, update the preferences
        by removing preferences for any non-existant resource,
        adding new resources with value of 0, and scaling the
        current resources to be valid (by calling normalize).

        :param resources: Any resources to update with
        :param remove: Set to True to remove values not in resources

        .. note::

           To keep this in fixed point, the total sum may be
           slightly less than 100, but never more.
        '''
        updated = dict((k, 0) for k in resources)
        for key, value in self.values.items():
            if (key in resources) or (not remove):
                updated[key] = value
        self.values = updated
        self.normalize()

    def normalize(self):
        ''' Noramlize the current preferences to match
        the current resolution.

        .. note::

           To keep this in fixed point, the total sum may be
           slightly less than 100, but never more.
        '''
        total = sum(self.values.values())
        if (total != self.resolution) and (total != 0):
            fixed = {}
            scale = (float(self.resolution) - total) / total
            for k,v in self.values.items():
                fixed[k] = int(v * scale) + v
            self.values = fixed

    def is_valid(self):
        ''' A check to see if the user preferences are valid

        :returns: True if valid, false otherwise
        '''
        total = sum(self.values.values())
        return ((total <= self.resolution)
            and (total + self.tolerance >= self.resolution))

    def value_of(self, items):
        ''' Given one or more items, return the total value
        to this user.

        :params items: The item(s) to get the value of
        :returns: The total value of the items
        '''
        if not hasattr(items, '__iter__'):
            return self.values.get(items, 0)
        return sum(v for k,v in self.values.items() if k in items)

    def __str__(self):
        ''' Returns a string representation of the preference

        :returns: The string representation of this preference
        '''
        return "Preference(%s, %s)" % (self.user, str(self.values))

    __repr__ = __str__
