#!/usr/bin/env python
import unittest
from cakery.preference import Preference
from cakery.algorithm import DivideAndChoose

class DivideAndChooseTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.preference.Preference
    '''

    def test_initializes(self):
        ''' test that the preference initializes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        users = []
        users.append(Preference('mark', vals))
        users.append(Preference('john', vals))

        algorithm = DivideAndChoose(users, keys)
        self.assertEqual(True, algorithm.is_valid())

        users.append(Preference('bill', vals))
        algorithm = DivideAndChoose(users, keys)
        self.assertRaises(ValueError, lambda: algorithm.is_valid())

    def test_division(self):
        ''' test that the preference initializes correctly '''
        vals = {'red':10, 'blue':20, 'green':30, 'yello':15, 'orange':25}
        keys = vals.keys()
        users = []
        users.append(Preference('mark', vals))
        users.append(Preference('john', vals))

        algorithm = DivideAndChoose(users, keys)
        divisions = algorithm.divide()
        for user, piece in divisions.items():
            self.assertEqual(50, user.value_of(piece))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
