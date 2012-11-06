from cakery.utilities import all_same


# ------------------------------------------------------------ 
# interfaces
# ------------------------------------------------------------ 
class FairDivider(object):
    ''' Base class of all fair division algorithms
    '''

    def is_valid(self):
        ''' Test that the parameters are valid for
        this algorithm.

        :returns: True if valid, False otherwise
        '''
        settings = self.settings()

        if len(self.users) < 2:
            raise ValueError("algorithm needs at least 2 users")
        if settings['users'] != 'n':
            if len(self.users) != settings['users']:
                raise ValueError("algorithm only works for % users" % settings['users'])
        if not all_same(u.value_of(self.cake) for u in self.users):
            raise ValueError("users don't all see unit value on the resource")
        return True

    def settings(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        raise NotImplementedError("settings")

    def divide(self):
        ''' Run the algorithm to perform a suggested
        division.

        :returns: A list of divisions of [(user, piece)]
        '''
        raise NotImplementedError("divide")
