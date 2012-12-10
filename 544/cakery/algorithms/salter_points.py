from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class SalterPoints(FairDivider):
    '''
    '''

    def __init__(self, users, cake, count=None):
        ''' Initializes a new instance of the algorithm.
        It should be noted that the first player is the
        bidder and the second player is the chooser.

        :param users: The users to operate with
        :param cake: The cake to divide
        :param count: The number of pieces to suggest
        '''
        self.users = users[:2]
        self.cake  = cake
        self.count = count or 2

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        2,
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
        cutter, picker = self.users
        slices  = {}
        pieces  = create_equal_pieces(cutter, self.cake, self.count)
        removed = choose_best_piece(picker, pieces)
        cleaned = self.cake.clone()
        cleaned.remove(removed)
        slices[picker] = removed
        slices[cutter] = cleaned
        return slices
