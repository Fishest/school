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
        self.assertEqual(100, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        cake = ContinuousResource(Fraction(0,1), Fraction(1,1))
        item = ContinuousResource(Fraction(1,2), Fraction(1,2))
        cake.remove(item)
        actual = ContinuousResource(Fraction(0, 1), Fraction(1,2))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(Fraction(0,1), Fraction(1,1))
        item = ContinuousResource(Fraction(0,1), Fraction(1,2))
        cake.remove(item)
        actual = ContinuousResource(Fraction(1, 2), Fraction(1,2))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(Fraction(0,1), Fraction(1,1))
        item = ContinuousResource(Fraction(0,1), Fraction(2,1))
        self.assertRaises(ValueError, lambda: cake.remove(item))

    def test_resource_append(self):
        ''' test that the resource append works correctly '''
        cake = ContinuousResource(Fraction(1,2), Fraction(1,2))
        item = ContinuousResource(Fraction(0,1), Fraction(1,2))
        cake.append(item)
        actual = ContinuousResource(Fraction(0, 1), Fraction(1,1))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(Fraction(0,1), Fraction(1,2))
        item = ContinuousResource(Fraction(1,2), Fraction(1,2))
        cake.append(item)
        actual = ContinuousResource(Fraction(0, 1), Fraction(1,1))
        self.assertEqual(actual.value, cake.value)

    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        user = ContinuousPreference('mark', lambda x: Fraction(1))
        cake = ContinuousResource(Fraction(0), Fraction(1))
        pieces = cake.create_pieces(user, 3)
        actual = [
            ContinuousResource(Fraction(0, 1), Fraction(1, 3)),
            ContinuousResource(Fraction(1, 3), Fraction(1, 3)),
            ContinuousResource(Fraction(2, 3), Fraction(1, 3))
        ]
        self.assertEqual(pieces, actual)

    def test_resource_find_piece(self):
        ''' test that we can find a piece in the cake '''
        user = ContinuousPreference('mark', lambda x: Fraction(1))
        cake = ContinuousResource(Fraction(0), Fraction(1))
        piece = cake.find_piece(user, Fraction(1,3))
        actual = ContinuousResource(Fraction(0, 1), Fraction(1, 3))
        self.assertEqual(piece, actual)

        self.assertRaises(ValueError, lambda: cake.find_piece(user, Fraction(10)))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
