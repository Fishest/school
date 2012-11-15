#!/usr/bin/env python
import unittest
from fractions import Fraction
from cakery.utilities import integrate, powerset
from cakery.utilities import all_same, any_range
from cakery.utilities import all_unique

class UtilitiesTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.utilities.maximum_cut
    '''

    def test_powerset(self):
        ''' test that the powerset method works correctly '''
        actual = list(powerset([1,2,3]))
        expect = [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
        self.assertEqual(actual, expect)

    def test_integrate(self):
        ''' test that integrate method works correctly '''
        self.assertEqual( 5, int(integrate(lambda x:   1, 0.0, 5.0, 100)))
        self.assertEqual(25, int(integrate(lambda x: 2*x, 0.0, 5.0, 100)))
        self.assertEqual(41, int(integrate(lambda x: x*x, 0.0, 5.0, 100)))

    def test_any_range(self):
        ''' test that the any_range method works correctly '''
        actual = list(any_range(Fraction(0), Fraction(4,3), Fraction(1,3)))
        expect = [Fraction(0,1), Fraction(1,3), Fraction(2,3), Fraction(3,3)]  
        self.assertEqual(actual, expect)

    def test_all_same(self):
        ''' test that the all_same method works correctly '''
        self.assertTrue(all_same([1,1,1,1,1,1]))
        self.assertTrue(all_same(['a', 'a', 'a']))
        self.assertTrue(all_same(1 for _ in range(10)))
        self.assertFalse(all_same([1,1,1,2,1,1]))
        self.assertFalse(all_same(range(10)))

    def test_all_unique(self):
        ''' test that the all_same method works correctly '''
        self.assertTrue(all_unique(['a', 'b', 'c']))
        self.assertFalse(all_unique([1,1,1,2,1,1]))
        self.assertTrue(all_unique(range(10)))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
