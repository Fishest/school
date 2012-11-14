from cakery.algorithms.utilities import *
from cakery.algorithms.common import FairDivider


class LoneChooser(FairDivider):
    ''' This is an implementation of the lone chooser
    algorithm that works as follows:

    1. Perform divide and choose with two players
    2. Another player is added to the division
    3. Each current player divides their current share
    4. This should be 1/n (where n is the player count)
    5. The new player chooses the best slice from each player
    6. Repeat at 2 for each new player
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
        slices = {}
        count  = 1                                  # the current number of players
        users  = randomize_items(self.users)        # randomize to be somewhat fair
        cutter = choose_and_remove(users)           # randomly select the first chooser
        slices[cutter] = self.cake.clone()          # first user gets all of the cake
        while any(users):                           # until all the users have chosen
            picker = choose_and_remove(users)       # randomly select the next chooser
            count += 1                              # add another player to the game
            for cutter, piece in slices.items():    # each current player has to cut
                pieces = create_equal_pieces(cutter, piece, count)
                piece  = choose_best_piece(picker, pieces)  # picker finds the best piece for them
                slices[cutter].remove(piece)        # remove that piece from their share
                if not picker in slices:            # and add it to the picker's share
                    slices[picker] = piece
                else: slices[picker].append(piece)
        return slices
