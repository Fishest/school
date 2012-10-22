'''
'''
from cakery.preference import Preference

class FairDivider(object):
    ''' Base class of all fair division algorithms
    '''

    def capabilities(self):
        ''' Retieves a capability listing of this algorithm

        :returns: A dictionary of the algorithm features
        '''
        return {
            'envy-free': False,
            'proportional': False,
            'stable': False,
            'users': 0,
        }
