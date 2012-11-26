from collections import defaultdict
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class InverseAlternatingChoice(FairDivider):
    ''' This is a simple algorithm that just lets
    each available user take turns choosing their next
    worst piece. The choosing order is dependent on
    the supplied alternation strategy which simply
    defaults to ordinal.
    '''

    def __init__(self, users, cake, strategy=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param strategy: The alternation strategy to use
        '''
        self.users = users
        self.cake  = cake
        self.strategy = strategy or AlternationStrategy.ordinal

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        'n',
            'envy-free':    False,
            'proportional': False,
            'equitable':    False,
            'optimal':      False,
            'discrete':     True,
            'continuous':   True,
        }

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices  = defaultdict(list)                 # initialize each user to an empty list
        pieces  = self.cake.as_collection()         # project our collection to a list
        cutters = self.strategy(self.users, pieces) # initialize our alternation strategy
        while any(pieces):                          # while there are still pieces
            for cutter in cutters():                # choose users based on our strategy
                piece = choose_worst_piece(cutter, pieces)   # they remove their worst piece
                slices[cutter].append(piece)        # and add it to their list
                if not any(pieces): break           # exit early in case of odd piece
        return slices
