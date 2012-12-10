from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


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
        self.users = users[:2]
        self.cake  = cake

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        2,
            'envy-free':    True,
            'proportional': True,
            'equitable':    True,
            'optimal':      True,
            'discrete':     True,
            'continuous':   True,
        }

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        cutter, picker = randomize_items(self.users)
        pieces = create_equal_pieces(cutter, self.cake, 2)
        slices[picker] = choose_worst_piece(picker, pieces)
        slices[cutter] = choose_and_remove(pieces)
        return slices
