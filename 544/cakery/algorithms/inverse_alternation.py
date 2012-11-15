from collections import defaultdict
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class InverseAlternatingChoice(FairDivider):
    '''
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
        slices  = defaultdict(list)
        pieces  = self.cake.as_collection()
        cutters = self.strategy(self.users, pieces)
        while any(pieces):
            for cutter in cutters():
                piece = choose_worst_piece(cutter, pieces)
                slices[cutter].append(piece)
        return slices
