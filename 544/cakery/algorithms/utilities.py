'''
------------------------------------------------------------
Algorithm Utilities
------------------------------------------------------------

These are a collection of simple helper methods that make
the code easier to read (basically a simple DSL).
'''
import random
from math import ceil, sqrt


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


def choose_highest_bidder(users, item):
    ''' Given an item, return the user that bid
    the higest amount for said item.

    :param users: The users bidding on the item
    :param item: The item to be bid upon
    :returns: The user with the highest bid
    '''
    return max((user.value_of(item), user) for user in users)[1]


def choose_lowest_bidder(users, item):
    ''' Given an item, return the user that bid
    the lowest amount for said item.

    :param users: The users bidding on the item
    :param item: The item to be bid upon
    :returns: The user with the highest bid
    '''
    return min((user.value_of(item), user) for user in users)[1]


def list_best_pieces(users, pieces):
    ''' Given a collection of users and pieces
    return the favorite pieces for each user.
    
    :param users: The users to search with
    :param pieces: The pieces to search in
    :returns: dict of {user: best-pieces}
    '''
    choices = {}
    for user in users:
        choice = max((user.value_of(p),p) for p in pieces)
        choices[user] = choice[1]
    return choices

def list_worst_pieces(users, pieces):
    ''' Given a collection of users and pieces
    return the worst pieces for each user.
    
    :param users: The users to search with
    :param pieces: The pieces to search in
    :returns: dict of {user: worst-pieces}
    '''
    choices = {}
    for user in users:
        choice = min((user.value_of(p),p) for p in pieces)
        choices[user] = choice[1]
    return choices


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
# classes
# ------------------------------------------------------------
class AlternationStrategy(object):
    ''' A collection of predefined alternation strategies
    that can be used to supply a user ordering for choosing
    resources.
    '''

    @staticmethod
    def ordinal(users, pieces):
        ''' Simply rotate the users in order
        from start to finish.

        :param users: The users to rotate between
        :param pieces: The items to choose between
        :returns: The next user to choose
        '''
        return lambda: list(users)

    @staticmethod
    def random(users, pieces):
        ''' Return a random ordering each time.

        :param users: The users to rotate between
        :param pieces: The items to choose between
        :returns: The next user to choose
        '''
        return lambda: randomize_items(users)

    @staticmethod
    def balanced(users, pieces):
        ''' Perform a balanced alternation that
        attepmts to catch up the latter choosers.

        ab
        abba
        abbabaab
        abbabaabbaababba

        :param users: The users to rotate between
        :param pieces: The items to choose between
        :returns: The next user to choose
        '''
        turns = list(users)
        sizes = int(ceil(sqrt(len(pieces))))
        for i in range(1, sizes):
            n = len(turns) / 2
            turns = turns + turns[n:] + turns[:n]
        return lambda: turns
