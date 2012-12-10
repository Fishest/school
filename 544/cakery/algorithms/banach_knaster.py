from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class BanachKnaster(FairDivider):
    ''' This is an implementation of the banach knaster
    last diminisher algorithm that works as follows:

    1. The first player proposes a trimming
    2. The next users in the line are allowed to reduce the trimming
    3. This continues until the last player in the line
    4. The last user that trimmed the piece receives it and exits
    5. This continues until all the players have exited the division
    '''

    def __init__(self, users, cake, weight=None):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake = cake
        self.weight = weight or cake.actual_value() / len(users)

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

        If a piece of the requesed value cannot be found,
        this will throw.

        :returns: A dictionary of divisions of {user: piece}
        '''
        slices = {}
        users  = randomize_items(self.users)
        cake   = self.cake.clone()
        while len(users) > 1:                   # single user shouldn't divide
            cutter = users[0]                   # create the initial trimming
            piece  = cake.find_piece(cutter, self.weight)
            for user in users[1:]:              # skip initial cutter
                value = user.value_of(piece)    # what this users thinks is 1/n
                if value > self.weight:         # user thinks piece is too big
                    piece  = trim_and_replace(user, cake, piece, self.weight)
                    cutter = user               # update last trimmer
            cake.remove(piece)                  # remove piece from cake
            users.remove(cutter)                # remove assigned user
            slices[cutter] = piece              # give the last trimmer their piece
        slices[users.pop()] = cake              # last user gets remainder
        return slices
