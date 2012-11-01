import random
from cakery.utilities import all_same


# ------------------------------------------------------------ 
# helpers
# ------------------------------------------------------------ 
def randomize_items(items):
    ''' Given a collection, create a clone of it and
    randomize the elements before returning it.

    :param items: The items to randomly choose from
    :returns: The randomized collection
    '''
    items = list(items)
    random.shuffle(items)
    return items

def choose_and_remove(items):
    ''' Given a collection, randomly choose a value
    from that collection and then remove it from the
    collection so it can't be selected again.

    :param items: The items to randomly choose from
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

def trim_and_replace(user, cake, piece, weight):
    ''' Given a resource and a user, trim the given
    piece to be of the supplied value and reattach the
    trimming to the total cake.

    :param user: The user to split the resource with
    :param cake: The cake to re-attach trimmings to
    :param piece: The piece to trim with the given user
    :returns: The newly trimmed piece
    '''
    (piece, trimming) = piece.create_pieces(user, weight=weight)
    cake.append(trimming)
    return piece

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
        if not all_same(u.value_of(self.cake) for u in self.users):
            raise ValueError("users don't all see unit value on the resource")
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
# fair division algorithms
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
        slices = {}
        users  = randomize_items(self.users)
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.cake, 2)
        slices[picker] = choose_best_piece(picker, pieces)
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
        users  = randomize_items(self.users)
        cake   = self.cake.clone()
        while len(users) > 1:               # single user shouldn't divide
            (cutter, piece) = choose_next_piece(users, cake)
            slices[cutter]  = piece         # user that said stop gets the piece
        slices[users[0]] = cake             # last user gets remainder
        return slices


class AustinMovingKnife(FairDivider):
    '''
    '''

    def __init__(self, users, cake, value):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param value: The agreed value to find
        '''
        self.users = users
        self.cake = cake
        self.value = value

        if value < 0:
            raise ValueError("cannot split resource to less than 0 value")

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

        If a piece of the requesed value cannot be found,
        this will throw.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        users  = randomize_items(self.users)
        cake   = self.cake.clone()
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        while cake.actual_value() > 0:
            piece = cutter.find_piece(cake)
            value = picker.value_of(item)
            if value == self.value:
                slices[cutter] = piece
                slices[picker] = piece
                break
            elif value > self.value:
                value = value - self.value
                trimming = picker.find_value(trim)
                cake.remove(trimming)
            # elif value < self.value: swap and let other try
            cutter, picker = picker, cutter
        return slices


class BanachKnaster(FairDivider):
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

        If a piece of the requesed value cannot be found,
        this will throw.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        users  = randomize_items(self.users)
        cake   = self.cake.clone()
        weight = cake.actual_value() / len(users) # TODO not right for collection
        while len(users) > 1:                   # single user shouldn't divide
            cutter = users[0]                   # create the initial trimming
            piece  = cake.find_piece(cutter, weight)
            for user in users[1:]:              # skip initial cutter
                value = user.value_of(piece)    # what this users thinks is 1/n
                if value > weight:              # user thinks piece is too big
                    piece  = trim_and_replace(user, cake, piece, weight)
                    cutter = user               # update last trimmer
            cake.remove(piece)                  # remove piece from cake
            users.remove(cutter)                # remove assigned user
            slices[cutter] = piece              # give the last trimmer their piece
        slices[users[0]] = cake                 # last user gets remainder
        return slices


# ------------------------------------------------------------ 
# chore division algorithms
# ------------------------------------------------------------ 
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
        slices = {}
        users  = randomize_items(self.users)
        cutter = choose_and_remove(users)
        picker = choose_and_remove(users)
        pieces = create_equal_pieces(cutter, self.cake, 2)
        slices[picker] = choose_worst_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices
