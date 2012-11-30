#!/usr/bin/env python
import unittest
from random import randint
from fractions import Fraction
from cakery.preference import ContinuousPreference
from cakery.resource import ContinuousResource
from cakery.algorithms import BanachKnaster

class BanachKnasterTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.BanachKnaster
    '''

    def test_initializes(self):
        ''' test that the algorithm initializes correctly '''
        cake  = ContinuousResource(Fraction(0,1), Fraction(1,1))
        pref  = lambda x: 1
        users = []
        users.append(ContinuousPreference('mark', pref))
        users.append(ContinuousPreference('john', pref))
        users.append(ContinuousPreference('anna', pref))
        users.append(ContinuousPreference('sara', pref))

        algorithm = BanachKnaster(users, cake)
        self.assertEqual(True, algorithm.is_valid())

        # test that the algorithm is not valid
        pref  = lambda x: randint(1, 100) # crazy person...
        users.append(ContinuousPreference('bill', pref))
        algorithm = BanachKnaster(users, cake)
        self.assertRaises(ValueError, lambda: algorithm.is_valid())

    def test_division(self):
        ''' test that the algorithm divides correctly '''
        cake  = ContinuousResource(Fraction(0,1), Fraction(1,1))
        pref  = lambda x: 1
        users = []
        users.append(ContinuousPreference('mark', pref))
        users.append(ContinuousPreference('john', pref))
        users.append(ContinuousPreference('anna', pref))
        users.append(ContinuousPreference('sara', pref))

        algorithm = BanachKnaster(users, cake)
        divisions = algorithm.divide()
        for user, piece in divisions.items():
            self.assertEqual(Fraction(1,4), user.value_of(piece))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
