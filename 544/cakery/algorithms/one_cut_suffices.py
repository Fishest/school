from copy import copy
from collections import defaultdict
from fractions import Fraction as F
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class OneCutSuffices(FairDivider):
    ''' Given a collection of items, divide them
    into two platters of value and total - value
    by using only one item division.
    '''

    def __init__(self, users, cake, value=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param value: The value of the first platter
        '''
        self.users = users
        self.cake  = cake
        self.value = value or self.users[0].value_of(cake) * F(1, 2)

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        1,
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
        extra  = {}
        slices = defaultdict(list)
        picker = randomize_items(self.users).pop()
        pieces = self.cake.as_collection()
        valued = sorted((picker.value_of(p), p) for p in pieces)
        split, total, value = None, 0, 0

        while total < self.value:
            value, split = valued.pop(0)
            if total + value <= self.value:
                slices[picker].append(split)
            elif total + value > self.value:
                extra['left-value']  = self.value - total
                extra['right-value'] = value - self.value + total
                extra['spilt-piece'] = split
            total += value

        picker = copy(picker)                           # treat one user as two
        picker.user = picker.user + "-right"            # so we know who is the right pile
        slices[picker] = [piece for _, piece in valued] # everything else goes to the right
        return slices, extra
