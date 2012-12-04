from fractions import Fraction as F
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class InverseDubinsSpanier(FairDivider):
    '''
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param value: The value to split the cake into
        '''
        self.users = users
        self.cake = cake
        self.value = None or F(1, len(users))

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        'n',
            'envy-free':    True,
            'proportional': True,
            'equitable':    True,
            'optimal':      False,
            'discrete':     True,
            'continuous':   True,
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
            (cutter, piece) = choose_last_piece(users, cake, self.value)
            slices[cutter]  = piece         # user that said stop gets the piece
            users.remove(cutter)            # remove that user from the division
        slices[users.pop()] = cake          # last user gets remainder
        return slices
