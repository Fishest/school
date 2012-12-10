from collections import defaultdict
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class TaylorRst(FairDivider):
    ''' This is an implementation of the taylor RST
    algorithm that works as follows:
    '''

    def __init__(self, users, cake, count=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake  = cake
        self.count = count or 10

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        'n',
            'envy-free':    False,
            'proportional': True,
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
        cutter, picker = randomize_items(self.users)[:2]
        pieces = create_equal_pieces(cutter, self.cake, self.count)
        pieces = sort_by_value(picker, pieces, reverse=True)
        pieces = [piece for value, piece in pieces]
        R,S,T  = pieces[0:-1:2], pieces[1::2], pieces[2::2]
        s_value, t_value = get_total_value(picker, S), get_total_value(picker, T)
        slices = {cutter: S, picker: T}
        cutters, pickers = R[0].create_pieces(picker, weight=s_value - t_value)
        slices[cutter].append(cutters)
        slices[picker].append(pickers)
        return slices
