from collections import defaultdict
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class KnasterSealedBids(FairDivider):
    ''' This algorithm works roughly like a simple
    sealed bids auction, however, at the end of the
    auction, money is distributed to make the parties
    equal.
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake  = cake

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
        N      = len(self.users)                                # The number of users competing
        slices = defaultdict(list)                              # initialize the user's assignments
        users  = randomize_items(self.users)                    # create a safe copy of the users
        fairs  = {u: u.value_of(self.cake) / N for u in users}  # each users fair share view of the cake
                                                                # simply run a sealed bids auction
        for piece in self.cake.as_collection():                 # project the cake into a collection
            cutter = choose_highest_bidder(users, piece)        # find the highest bidder for this piece
            slices[cutter].append(piece)                        # user that bid the most, gets the piece

        assign  = {u: get_total_value(u, slices[u]) for u in users}  # how much value each user got
        excess  = {u: assign[u] - fairs[u] for u in users}      # how much in excess of fair share we got
        surplus = sum(v for v in excess.values()) / N           # the total surplus share of value for each user
        adjusts = {u: fairs[u] + surplus for u in users}        # each user's assigned value adjusted by surplus
        settled = {u: assign[u] - adjusts[u] for u in users}    # how much each user should give and get from the pot
        return slices, {                                        # return the assignments and settlements
            'settlements': settled,
            'excesses'   : excess,
            'assignments': assign,
            'adjustments': adjusts,
            'surplus'    : surplus,
        }
