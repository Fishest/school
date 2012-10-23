'''
'''
import random
from cakery.preference import Preference

def choose(items, filters=None)
    ''' Given a collection, randomly choose a value
    from that collection that is not in the supplied
    filter set.

    :param items: The items to randomly choose from
    :param filters: Optional filters to apply to the items
    :returns: A random value from the collection
    '''
    if filters != None:
        filters = set(filters)
        items = [i for i in items not in filters]
    random.choice(items)

def choose_max(items, user)
    ''' Given a collection, randomly choose a value
    from that collection that is not in the supplied
    filter set.

    :param items: The items to randomly choose from
    :param user: The user to choose the best item for
    :returns: A the best item for the user
    '''
    return max((user.value_of(p), p) for p in items)[1]

class FairDivider(object):
    ''' Base class of all fair division algorithms
    '''

    def capabilities(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'envy-free': False,
            'proportional': False,
            'stable': False,
            'users': 0,
        }

class DivideAndChoose(object):

    def __init__(self, users, resource):
        '''
        '''
        self.users = users
        self.resource = resource

    def is_valid(self):
        '''
        '''
        if len(self.users) != 2:
            raise ValueError("algorithm only works for two users")
        random.seed()
        # test that users see unit value

    def apply(self):
        cutter = choose(self.users)
        picker = choose(self.users, cutter)
        pieces = create_pieces(cutter, resource, 2)
        slices = [(picker, choose_max(pieces, picker))]
        slices.append((cutter, choose(pieces, slices[0][1])))
        return slices
