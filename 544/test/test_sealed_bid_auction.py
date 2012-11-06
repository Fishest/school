#!/usr/bin/env python
import unittest
from cakery.preference import CollectionPreference
from cakery.resource import CollectionResource
from cakery.algorithms import SealedBidAuction

class SealedBidAuctionTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.SealedBidAuction
    '''

    def test_initializes(self):
        ''' test that the algorithm initializes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', vals))
        users.append(CollectionPreference('john', vals))

        algorithm = SealedBidAuction(users, cake)
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

        algorithm = SealedBidAuction(users, cake)
        divisions = algorithm.divide()
        for user, piece in divisions.items():
            self.assertEqual(30, user.value_of(piece))


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
