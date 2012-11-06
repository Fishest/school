from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class BanachKnaster(FairDivider):
    '''
    '''

    def __init__(self, users, cake):
        ''' Initializes a new instance of the algorithm

        :param users: The users to operate with
        :param cake: The cake to divide
        '''
        self.users = users
        self.cake = cake

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'users':        'n',
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
        weight = cake.actual_value() / len(users) # TODO not right for collection
        while len(users) > 1:                   # single user shouldn't divide
            cutter = users[0]                   # create the initial trimming
            piece  = cake.find_piece(cutter, weight)
            for user in users[1:]:              # skip initial cutter
                value = user.value_of(piece)    # what this users thinks is 1/n
                if value > weight:              # user thinks piece is too big
                    piece  = trim_and_replace(user, cake, piece, weight)
                    cutter = user               # update last trimmer
            cake.remove(piece)                  # remove piece from cake
            users.remove(cutter)                # remove assigned user
            slices[cutter] = piece              # give the last trimmer their piece
        slices[users[0]] = cake                 # last user gets remainder
        return slices
