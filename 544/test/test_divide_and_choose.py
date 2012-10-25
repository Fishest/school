#!/usr/bin/env python
import unittest
from cakery.preference import CollectionPreference
from cakery.resource import CollectionResource
from cakery.algorithm import DivideAndChoose, InverseDivideAndChoose

class DivideAndChooseTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.DivideAndChoose
    '''

    def test_initializes(self):
        ''' test that the algorithm initializes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', vals))
        users.append(CollectionPreference('john', vals))

        algorithm = DivideAndChoose(users, cake)
        self.assertEqual(True, algorithm.is_valid())

        users.append(CollectionPreference('bill', vals))
        algorithm = DivideAndChoose(users, cake)
        self.assertRaises(ValueError, lambda: algorithm.is_valid())

    def test_division(self):
        ''' test that the algorithm divides correctly '''
        vals = {'red':10, 'blue':20, 'green':30, 'yello':15, 'orange':25}
        keys = vals.keys()
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', vals))
        users.append(CollectionPreference('john', vals))

        algorithm = DivideAndChoose(users, cake)
        divisions = algorithm.divide()
        for user, piece in divisions.items():
            self.assertEqual(50, user.value_of(piece))

    def test_inverse_division(self):
        ''' test that the inverse algorithm divides correctly '''
        vals = {'red':10, 'blue':20, 'green':30, 'yello':15, 'orange':25}
        keys = vals.keys()
        cake = CollectionResource(keys)
        users = []
        users.append(CollectionPreference('mark', vals))
        users.append(CollectionPreference('john', vals))

        algorithm = InverseDivideAndChoose(users, cake)
        divisions = algorithm.divide()
        for user, piece in divisions.items():
            self.assertEqual(50, user.value_of(piece))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
