import random
from cakery.utilities import create_pieces, find_piece


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

def choose_next_piece(users, resource):
    ''' Given a resource and a collection of users,
    return the next user who would have said 'Stop'
    first and the piece they would have stopped for.

    :param users: The users to split the resource with
    :param resource: The resource to split
    :returns: (user, piece)
    '''
    weight = 1.0 / len(users)
    pieces = ((find_piece(resource, u, weight), u) for u in users)
    (piece, user) = min(pieces) # random choice
    resource.remove(piece)
    return (user, piece)

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
        settings = self.settings()

        if len(self.users) < 2:
            raise ValueError("algorithm needs at least 2 users")
        if settings['users'] != 'n':
            if len(self.users) != settings['users']:
                raise ValueError("algorithm only works for % users" % settings['users'])
        if not all(u.sees_unit_value() for u in self.users):
            raise ValueError("users don't see unit value on the resource")
        return True

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        raise NotImplementedError("settings")

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
    '''
    '''

    def __init__(self, users, resource):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param resource: The resouce to divide
        '''
        self.users = users
        self.resource = resource

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        2,
            'envy-free':    True,
            'proportional': True,
        }

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A dictionary of divisions of {user: piece}
        '''
        users  = list(self.users) # defensive copy
        slices = {}
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.resource, 2)
        slices[picker] = choose_best_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices

class DubinsAndSpanier(FairDivider):
    '''
    '''

    def __init__(self, users, resource):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param resource: The resouce to divide
        '''
        self.users = users
        self.resource = resource

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        2,
            'envy-free':    True,
            'proportional': True,
            # equitable, stable
        }

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        users  = list(self.users)
        resource = self.resource.clone()
        while len(users) > 1:
            (cutter, piece) = choose_next_piece(users, resource)
            slices[cutter]  = piece
        slices[users[0]] = resource # last user gets last
        return slices
