#!/usr/bin/env python
import unittest
from fractions import Fraction as F
from cakery.preference import ContinuousPreference as Preference
from cakery.resource import ContinuousResource as Resource
from cakery.algorithms import DivideAndChoose

class DivideAndChooseTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithms.DivideAndChoose
    '''
    
    def setUp(self):
        ''' The common test setup code '''
        self.users = [
            Preference(None, lambda x: F(1,1)),
            Preference(None, lambda x: F(1,1)),
            Preference(None, lambda x: F(1,1)),
        ]
        self.cakes = [
            Resource(F(0,1), F(1,3)),
            Resource(F(0,1), F(1,3)),
            Resource(F(0,1), F(1,3)),
        ]
        self.cake = Resource(F(0,1), F(1,1))
        self.fair = DivideAndChoose(self.users, self.cake)
        self.shares = dict(zip(self.users, self.cakes))

    def test_is_proportional(self):
        ''' test that the is_proportional method works correctly '''
        result = self.fair.is_proportional(self.shares)
        self.assertTrue(result)

    def test_is_not_proportional(self):
        ''' test that the is_proportional method works correctly '''
        self.users[2].function = lambda x: F(1,3)
        result = self.fair.is_proportional(self.shares)
        self.assertFalse(result)

    def test_is_equitable(self):
        ''' test that the is_equitable method works correctly '''
        result = self.fair.is_equitable(self.shares)
        self.assertTrue(result)

    def test_is_not_equitable(self):
        ''' test that the is_equitable method works correctly '''
        self.cakes[2].value = (F(0,1), F(1,4))
        result = self.fair.is_equitable(self.shares)
        self.assertFalse(result)

    def test_is_envy_free(self):
        ''' test that the is_envy_free method works correctly '''
        result = self.fair.is_envy_free(self.shares)
        self.assertTrue(result)

    def test_is_not_envy_free(self):
        ''' test that the is_envy_free method works correctly '''
        self.cakes[2].value = (F(0,1), F(1,4))
        result = self.fair.is_envy_free(self.shares)
        self.assertTrue(result)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
