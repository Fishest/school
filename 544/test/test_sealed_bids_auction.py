#!/usr/bin/env python
import unittest
from cakery.preference import CollectionPreference
from cakery.resource import CollectionResource
from cakery.algorithms import SealedBidsAuction
from cakery.algorithms.utilities import get_total_value

class SealedBidsAuctionTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.SealedBidsAuction
    '''

    def test_initializes(self):
        ''' test that the algorithm initializes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', vals))
        users.append(CollectionPreference('john', vals))

        algorithm = SealedBidsAuction(users, cake)
        self.assertEqual(True, algorithm.is_valid())

    def test_division(self):
        ''' test that the algorithm divides correctly '''
        vals = {'red':10, 'blue':20, 'green':30}
        keys = vals.keys()
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', {'red':10, 'blue':20, 'green':30}))
        users.append(CollectionPreference('john', {'red':10, 'blue':30, 'green':20}))
        users.append(CollectionPreference('anna', {'red':30, 'blue':20, 'green':10}))

        algorithm = SealedBidsAuction(users, cake)
        divisions = algorithm.divide()
        for user, pieces in divisions.items():
            self.assertEqual(30, get_total_value(user, pieces))


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
