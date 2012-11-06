from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class DubinsSpanier(FairDivider):
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
