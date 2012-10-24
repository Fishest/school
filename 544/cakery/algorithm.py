import random
from cakery.utilities import create_pieces


# ------------------------------------------------------------ 
# helpers
# ------------------------------------------------------------ 
def choose_and_remove(items):
    ''' Given a collection, randomly choose a value
    from that collection and then remove it from the
    collection so it can't be selected again.

    :param items: The items to randomly choose from
    :param filters: Optional filters to apply to the items
    :returns: A random value from the collection
    '''
    choice = random.choice(items)
    items.remove(choice)
    return choice


def choose_best_piece(user, pieces):
    ''' Given a collection of resources, choose the 
    one that is the most preferred by the supplied
    user.

    :param user: The user to choose the best item for
    :param pieces: The pieces to choose the most liked from
    :returns: A the best item for the user
    '''
    choice = max((user.value_of(p), p) for p in pieces)[1]
    pieces.remove(choice)
    return choice

def create_equal_pieces(user, resource, count):
    ''' Given a resource, split it into count many
    pieces equal in value to the supplied user.

    :param user: The user to split the resource with
    :param resource: The resource to split
    :param count: The number of pieces to create
    :returns: A list of the split pieces
    '''
    return create_pieces(resource, user, count)


# ------------------------------------------------------------ 
# interfaces
# ------------------------------------------------------------ 
class FairDivider(object):
    ''' Base class of all fair division algorithms
    '''

    def is_valid(self):
        ''' Test that the parameters are valid for
        this algorithm.

        :returns: True if valid, False otherwise
        '''
        return False

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

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A list of divisions of [(user, piece)]
        '''
        raise NotImplementedError("divide")


# ------------------------------------------------------------ 
# algorithms
# ------------------------------------------------------------ 
class DivideAndChoose(FairDivider):

    def __init__(self, users, resource):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param resource: The resouce to divide
        '''
        self.users = users
        self.resource = resource

    def capabilities(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'envy-free': True,
            'proportional': True,
            'stable': True,
            'users': 2,
        }

    def is_valid(self):
        ''' Test that the parameters are valid for
        this algorithm.

        :returns: True if valid, False otherwise
        '''
        if len(self.users) != 2:
            raise ValueError("algorithm only works for two users")
        if not all(u.sees_unit_value() for u in self.users):
            raise ValueError("users don't see unit value on the resource")
        return True

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A dictionary of divisions of {user: piece}
        '''
        users  = list(self.users) # defensive copy
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.resource, 2)
        slices = {}
        slices[picker] = choose_best_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices
