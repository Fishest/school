#!/usr/bin/env python
import unittest
from fractions import Fraction
from cakery.utilities import integrate, powerset, any_range

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

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
