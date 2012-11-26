from fractions import Fraction as F
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class AustinMovingKnife(FairDivider):
    '''
    '''

    def __init__(self, users, cake, value=F(1, 2)):
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
