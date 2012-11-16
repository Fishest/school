#!/usr/bin/env python
import unittest
from fractions import Fraction as F
from cakery.resource import ContinuousResource
from cakery.preference import ContinuousPreference

class ContinuousResourceTest(unittest.TestCase):
    '''
    This is the unittest for the ContinuousResource
    code utilities.
    '''

    def test_resource_create(self):
        ''' test that the resource factory methods work '''
        cake1 = ContinuousResource.random()
        cake2 = ContinuousResource.random()
        self.assertNotEqual(cake1, cake2)

    def test_preference_create(self):
        ''' test that the preference factory methods work '''
        cake  = ContinuousResource(0.0, 1.0)
        users = [ContinuousPreference.random() for i in range(5)]
        for user in users:
            self.assertTrue(0.95 <= user.value_of(cake) <= 1.05)

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        cake = ContinuousResource(F(0), F(100))
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))
        self.assertEqual(100, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        cake = ContinuousResource(F(0,1), F(1,1))
        item = ContinuousResource(F(1,2), F(1,2))
        cake.remove(item)
        actual = ContinuousResource(F(0, 1), F(1,2))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(F(0,1), F(1,1))
        item = ContinuousResource(F(0,1), F(1,2))
        cake.remove(item)
        actual = ContinuousResource(F(1, 2), F(1,2))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(F(0,1), F(1,1))
        item = ContinuousResource(F(0,1), F(2,1))
        self.assertRaises(ValueError, lambda: cake.remove(item))

    def test_resource_append(self):
        ''' test that the resource append works correctly '''
        cake = ContinuousResource(F(1,2), F(1,2))
        item = ContinuousResource(F(0,1), F(1,2))
        cake.append(item)
        actual = ContinuousResource(F(0, 1), F(1,1))
        self.assertEqual(actual.value, cake.value)

        cake = ContinuousResource(F(0,1), F(1,2))
        item = ContinuousResource(F(1,2), F(1,2))
        cake.append(item)
        actual = ContinuousResource(F(0, 1), F(1,1))
        self.assertEqual(actual.value, cake.value)

    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        user = ContinuousPreference('mark', lambda x: F(1))
        cake = ContinuousResource(F(0), F(1))
        pieces = cake.create_pieces(user, 3)
        actual = [
            ContinuousResource(F(0, 1), F(1, 3)),
            ContinuousResource(F(1, 3), F(1, 3)),
            ContinuousResource(F(2, 3), F(1, 3))
        ]
        self.assertEqual(pieces, actual)

    def test_resource_find_piece(self):
        ''' test that we can find a piece in the cake '''
        user = ContinuousPreference('mark', lambda x: F(1))
        cake = ContinuousResource(F(0), F(1))
        piece = cake.find_piece(user, F(1,3))
        actual = ContinuousResource(F(0, 1), F(1, 3))
        self.assertEqual(piece, actual)

        self.assertRaises(ValueError, lambda: cake.find_piece(user, F(10)))

    def test_resource_as_collection(self):
        ''' test that we can convert a resource to a collection '''
        cake = ContinuousResource(F(0), F(1), resolution=5)
        pieces = cake.as_collection()
        actual = [
            ContinuousResource(F(0,5), F(1,5)),
            ContinuousResource(F(1,5), F(1,5)),
            ContinuousResource(F(2,5), F(1,5)),
            ContinuousResource(F(3,5), F(1,5)),
            ContinuousResource(F(4,5), F(1,5))
        ]
        for this,that in zip(pieces, actual):
            self.assertEqual(this.value, that.value)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
