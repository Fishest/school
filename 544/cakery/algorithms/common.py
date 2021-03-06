from cakery.utilities import all_same
from cakery.algorithms.utilities import get_total_value


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

    def is_proportional(self, slices):
        ''' Test that the proposed division is proportional

        :param slices: The proposed division of the resource
        :returns: True if proportional, False otherwise
        '''
        share  = slices.keys()[0].value_of(self.cake) / len(self.users)
        pieces = slices.values()
        for user, _ in slices.items():
            if not all(get_total_value(user, p) >= share for p in pieces):
                return False
        return True

    def is_equitable(self, slices):
        ''' Test that the proposed division is equitable

        :param slices: The proposed division of the resource
        :returns: True if equitable, False otherwise
        '''
        pieces = slices.values()
        for user, piece in slices.items():
            value = get_total_value(user, piece)
            if not all(get_total_value(user, p) == value for p in pieces):
                return False
        return True

    def is_envy_free(self, slices):
        ''' Test that the proposed division is envy-free

        :param slices: The proposed division of the resource
        :returns: True if envy-free, False otherwise
        '''
        pieces = slices.values()
        for user, piece in slices.items():
            envied = max(get_total_value(user, p) for p in pieces)
            if envied > get_total_value(user, piece):
                return False
        return True

    def is_optimal(self, slices):
        ''' Test that the proposed division is optimal

        :param slices: The proposed division of the resource
        :returns: True if envy-free, False otherwise
        '''
        raise NotImplementedError("is_optimal")

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
