from collections import defaultdict
from cakery.utilities import all_unique
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class AdjustedWinner(FairDivider):
    ''' This algorithm takes turns between each user
    choosing their next favorite item from the resource.
    It runs as follows:

    1. Flatten the resource into a collection of choices
    2. At each round, have each user choose their best piece
    3. If the pieces are not the same, assign each user that piece
    4. Otherwise, put those pieces in the contested pile
    5. Repeat at 2 until the original pile is exhausted
    6. Now run the simple alternation choice on the contested pile
    7. Propose an object to exchange to make values equal
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
            'users':        2,
            'envy-free':    True,
            'proportional': True,
            'equitable':    True,
            'optimal':      False,
            'discrete':     True,
            'continuous':   True,
        }

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division. This algorithm also returns a dictionary of
        values for how to split a shared item to reduce any
        envy in the division:
        {
          'shared_item': the item to share
          'shared_rate': the rate at which to share the item
          'winner'     : the amount that the winner should receive
          'loser'      : the amount that the loser should receive
        }

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices  = defaultdict(list)                     # we will return N pieces per cutter
        pieces  = self.cake.as_collection()             # flatten the collection into choices
        cutters = self.strategy(self.users, pieces)     # create our alternation strategy
        contest = []                                    # initialize the contested pieces

        while any(pieces):                              # distribute the un-contested pieces
            choices = list_best_pieces(self.users, pieces)   # find each user's best piece
            settled = all_unique(choices.values())      # are any choices the same
            for cutter, piece in choices.items():       # if not assign, else put in contested
                if settled: slices[cutter].append(piece)
                else: contest.append(piece)             # both users want this piece
                pieces.remove(piece)                    # remove these from the choosing

        while any(contest):                             # distribute the contested pieces
            for cutter in cutters():                    # change users based on our strategy
                piece = choose_best_piece(cutter, pieces)
                slices[cutter].append(piece)            # give that user their next best piece
                                                        # find a piece to resolve envy with
        totals = {u: get_total_value(cs) for u, cs in slices.items()} # see what everyone got
        loser  = min((v, u) for u, v in totals.items())[1] # find the loser of the bidding
        winner = max((v, u) for u, v in totals.items())[1] # find the winner of the bidding
        shared = min((winner.value_of(v) / loser.value_of(v), v) for v in slices[winner])[1]
        rate = (totals[winner] - totals[loser]) / (loser.value_of(shared) + winner.value_of(shared))

        return slices, {
            'shared_item': shared,  # the contested item that should be shared
            'shared_rate': rate,    # the rate at which the item should be shared
            'winner'     : rate * -winner.value_of(shared), # how much the winner loses of shared
            'loser'      : rate * loser.value_of(shared),   # how much the loser gets of shared
        }
