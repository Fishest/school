#!/usr/bin/env python
import unittest
from fractions import Fraction
from cakery.resource import ContinuousResource
from cakery.preference import ContinuousPreference

class ContinuousResourceTest(unittest.TestCase):
    '''
    This is the unittest for the ContinuousResource
    code utilities.
    '''

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        cake = ContinuousResource(Fraction(0), Fraction(100))
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))

    def test_resource_create_pieces(self):
        user = ContinuousPreference('mark', lambda x: Fraction(1))
        cake = ContinuousResource(Fraction(0), Fraction(1))
        pieces = cake.create_pieces(user, 3)
        actual = [
            ContinuousResource(Fraction(0, 1), Fraction(1, 3)),
            ContinuousResource(Fraction(1, 3), Fraction(2, 3)),
            ContinuousResource(Fraction(2, 3), Fraction(3, 3))
        ]
        self.assertEqual(pieces, actual)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
