import random


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

def choose_worst_piece(user, pieces):
    ''' Given a collection of resources, choose the 
    one that is the least preferred by the supplied
    user.

    :param user: The user to choose the best item for
    :param pieces: The pieces to choose the least liked from
    :returns: A the worst item for the user
    '''
    choice = min((user.value_of(p), p) for p in pieces)[1]
    pieces.remove(choice)
    return choice

def create_equal_pieces(user, cake, count):
    ''' Given a resource, split it into count many
    pieces equal in value to the supplied user.

    :param user: The user to split the resource with
    :param cake: The cake to split
    :param count: The number of pieces to create
    :returns: A list of the split pieces
    '''
    return cake.create_pieces(user, count)

def choose_next_piece(users, cake):
    ''' Given a resource and a collection of users,
    return the next user who would have said 'Stop'
    first and the piece they would have stopped for.

    :param users: The users to split the resource with
    :param cake: The cake to split
    :returns: (user, piece)
    '''
    weight = 1.0 / len(users)
    pieces = ((cake.find_piece(user, weight), user) for user in users)
    (piece, user) = min(pieces) # random choice
    cake.remove(piece)
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
        #if not all(u.is_unit_value(self.cake) for u in self.users):
        #    raise ValueError("users don't see unit value on the resource")
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
    ''' This is an implementation of the divide and choose
    algorithm that works as follows:

    1. A cutting user is randomly chosen
    2. The other user is labled as the chooser
    3. The cutter divides the cake into two pieces
    4. The chooser picks the piece they like the best
    5. The cutter gets the remaining piece
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake  = cake

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
        users  = list(self.users) # defensive copy
        slices = {}
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.cake, 2)
        slices[picker] = choose_best_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices


class InverseDivideAndChoose(FairDivider):
    ''' This is an implementation of the divide and choose
    algorithm that can be used to divide chores and it
    works as follows:

    1. A cutting user is randomly chosen
    2. The other user is labled as the chooser
    3. The cutter divides the cake into two pieces
    4. The chooser picks the piece they like the least
    5. The cutter gets the remaining piece
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake  = cake

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
        users  = list(self.users) # defensive copy
        slices = {}
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.cake, 2)
        slices[picker] = choose_worst_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices


class DubinsAndSpanier(FairDivider):
    '''
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake = cake

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        'n',
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
        cake = self.cake.clone()
        while len(users) > 1:
            (cutter, piece) = choose_next_piece(users, cake)
            slices[cutter]  = piece
        slices[users[0]] = cake # last user gets last
        return slices
