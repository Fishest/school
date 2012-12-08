from collections import defaultdict
from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class GuyConwaySelfridge(FairDivider):
    '''
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake  = cake
        self.count = len(self.users)

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
        slices = defaultdict(list)                                      # initialize each users results
        cutter, marker, picker = randomize_items(self.users)            # randomize each user role
        pieces = create_equal_pieces(cutter, self.cake, self.count)     # the cutter makes N pieces
        values = sort_by_value(marker, pieces)                          # the marker choose the top two pieces
        value1, piece1 = values.pop()                                   # the biggest piece and value
        value2, piece2 = values.pop()                                   # the second biggest piece and value

        if value1 != value2:                                            # we must create a tie between these two
            trimmed, trimming = piece1.create_pieces(marker, weight=value2) # so make value(piece1) == value2
            replace_first_item(pieces, piece1, trimmed)                 # we then replace with the trimmed piece

        for user in [picker, marker, cutter]:                           # the users choose in this order
            if user is marker and trimmed in pieces:                    # if the trimmed piece still exists
                slices[user] = trimmed                                  # then the marker must choose it
                pieces.remove(trimmed)                                  # and remove it from the list
            else: slices[user].append(choose_best_piece(user, pieces))  # otherwise, pick the best user piece

        if trimming:                                                    # if there was a trimming
            trimmer, chooser = randomize_items(picker, marker)          # we create new user roles
            pieces = create_equal_pieces(trimmer, trimming, self.count) # divide the trimming into N pieces
            for user in [chooser, trimmer, cutter]:                     # the users choose in this order
                slices[user].append(choose_best_piece(user, pieces))    # the best piece that each user sees
        return slices
