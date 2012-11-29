from collections import defaultdict
from cakery.utilities import all_unique
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class BalancedAlternatingChoice(FairDivider):
    ''' This algorithm takes turns between each user
    choosing their next favorite item from the resource.
    It runs as follows:

    1. Flatten the resource into a collection of choices
    2. At each round, have each user choose their best piece
    3. If the pieces are not the same, assign each user that piece
    4. Otherwise, put those pieces in the contested pile
    5. Repeat at 2 until the original pile is exhausted
    6. Now run the simple alternation choice on the contested pile
    '''

    def __init__(self, users, cake, strategy=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        :param strategy: The alternation strategy to use
        '''
        self.users = users
        self.cake  = cake
        self.strategy = strategy or AlternationStrategy.balanced

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
        slices  = defaultdict(list)                     # we will return N pieces per cutter
        pieces  = self.cake.as_collection()             # flatten the collection into choices
        cutters = self.strategy(self.users, pieces)     # create our alternation strategy
        contest = []                                    # initialize the contested pieces

        while any(pieces):                              # distribute the un-contested pieces
            choices = list_best_pieces(self.users, pieces)   # find each user's best piece
            settled = all_unique(choices.values())      # are any choices the same
            for cutter, piece in choices.items():       # check all the chosen items
                if settled: slices[cutter].append(piece)# if not contested, give each user that piece
                elif piece not in pieces: continue      # this piece has already been contested
                else: contest.append(piece)             # both users want this piece
                pieces.remove(piece)                    # remove these from the choosing

        while any(contest):                             # distribute the contested pieces
            for cutter in cutters():                    # change users based on our strategy
                piece = choose_best_piece(cutter, contest)
                slices[cutter].append(piece)            # give that user their next best piece
                if not any(contest): break              # exit early in case of odd pieces
        return slices
