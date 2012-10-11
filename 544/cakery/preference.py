'''
'''

class Preference(object):
    ''' Represents the preferences of a given user
    about a supplied resource(s). The preferences are
    represented as a dictionary of resource -> preference
    where the preference value is a fixed point value (no
    decimals).
    
    The preferences should be assigned as a percentage
    of the defined resolution (integers). We assume the
    preferences collectively add up to specified resolution
    (or slightly less, but never more).
    '''

    def __init__(self, user, values, resolution=100):
        ''' Initialize a new preference class

        :param user: The name or id of the participant
        :param values: The preference values of the user
        :param resolution: The fixed point max resolution (default 100)
        '''
        self.user = user
        self.values = values
        self.resolution = resolution

    def update(self, resources):
        ''' Given a list of resources, update the preferences
        by removing preferences for any non-existant resource,
        adding new resources with value of 0, and scaling the
        current resources to be valid.

        :param resources: The resources to update with

        .. note::

           To keep this in fixed point, the total sum may be
           slightly less than 100, but never more.
        '''
        current = dict((k, 0) for k in resources)
        current.update(dict((k,v) for k,v in self.values.items() if k in resources))
        total = sum(current.values())
        if (total != self.resolution) and (total != 0):
            scale = (float(self.resolution) - total) / total
            for k,v in current.items():
                current[k] = int(v * scale) + v
        self.values = current # atomic assign

    def is_valid(self):
        ''' A check to see if the user preferences are valid

        :returns: True if valid, false otherwise
        '''
        return (sum(self.values.values()) == self.resolution)

    def __str__(self):
        ''' Returns a string representation of the preference

        :returns: The string representation of this preference
        '''
        return "Preference(%s, %s)" % (self.user, str(self.values))

    __repr__ = __str__
