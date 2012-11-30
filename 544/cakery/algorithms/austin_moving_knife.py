from fractions import Fraction as F
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class AustinMovingKnife(FairDivider):
    '''
    '''

    def __init__(self, users, cake, value=F(1, 2), shift=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param value: The agreed value to find
        :param shift: The amount off of value to allow
        '''
        self.users = users
        self.cake  = cake
        self.value = value
        self.shift = shift or F(1, 10) * self.value

        if value <= 0:
            raise ValueError("cannot split resource to less than 0 value")

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

        If a piece of the requesed value cannot be found,
        this will throw.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        swaps  = 0                                          # so we don't just swap forever
        users  = randomize_items(self.users)
        cake   = self.cake.clone()
        cutter = choose_and_remove(users)                   # randomly choose first cutter
        picker = choose_and_remove(users)                   # randomly choose first picker
        while cake.actual_value() > 0:                      # unless we cannot find a piece
            piece = cake.find_piece(cutter, self.value)     # propose a 1/N piece
            value = picker.value_of(piece)                  # see if other user agrees
            if abs(value - self.value) <= self.shift:       # if so we are done
                slices = {u:piece for u in self.users}      # both users 'get' this piece
                break
            elif value > self.value:                        # else other trims to be 1/N
                swaps, value = 0, value - self.value        # determine amount off of 1/N
                trimming = cake.find_piece(picker, value)   # find a piece that is that value
                cake.remove(trimming)                       # reduce the cake to said value
            elif value < self.value:                        # other user saw a bigger piece
                cutter, picker = picker, cutter             # swap users and try again
                swaps += 1
            if swaps == len(self.users):                    # we are just suggesting the same piece
                cake.remove(piece)                          # so just remove it and start fresh
        return slices
