#!/usr/bin/env python
import os
import unittest
from fractions import Fraction as F
from cakery.resource import IntervalResource
from cakery.preference import IntervalPreference

class IntervalResourceTest(unittest.TestCase):
    '''
    This is the unittest for the ContinuousResource
    code utilities.
    '''
    def test_resource_create(self):
        ''' test that the resource factory methods work '''
        cake1 = IntervalResource.random()
        cake2 = IntervalResource.random()
        self.assertNotEqual(cake1, cake2)

    def test_preference_create(self):
        ''' test that the preference factory methods work '''
        path  = os.path.join(os.path.abspath('contrib'), 'data')
        path  = os.path.join(path, 'interval')
        path  = os.path.join(path, 'uniform')
        user1 = IntervalPreference.from_file(path)
        user2 = IntervalPreference('user2', [(0.0, 1.0), (1.0, 1.0)])
        cake  = IntervalResource((F(0,1), F(1,1)))
        self.assertEqual(user1.value_of(cake), user2.value_of(cake))

        users = [IntervalPreference.random(10) for i in range(5)]
        for user in users:
            self.assertEqual(1.0, user.value_of(cake))

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        cake = IntervalResource((F(0,1), F(1,1)))
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))
        self.assertEqual(1, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

        cake = IntervalResource([(F(0,1), F(1,1))])
        self.assertEqual(1, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        cake = IntervalResource((F(0,1), F(1,1)))
        item = IntervalResource((F(0,1), F(1,2)))
        cake.remove(item)
        actual = IntervalResource((F(1,2), F(1,1)))
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,2)), (F(1,2), F(1,1))])
        item = IntervalResource((F(0,1), F(1,2)))
        cake.remove(item)
        actual = IntervalResource((F(1,2), F(1,1)))
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,2)), (F(1,2), F(1,1))])
        item = IntervalResource((F(0,1), F(3,4)))
        cake.remove(item)
        actual = IntervalResource((F(3,4), F(1,1)))
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,2)), (F(1,2), F(1,1))])
        item = IntervalResource((F(1,4), F(1,2)))
        cake.remove(item)
        actual = IntervalResource([(F(0,1), F(1,4)), (F(1,2), F(1,1))])
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,1))])
        item = IntervalResource((F(1,4), F(2,4)))
        cake.remove(item)
        actual = IntervalResource([(F(0, 1), F(1,4)), (F(1,2), F(1,1))])
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,2)), (F(1,2), F(1,1))])
        item = IntervalResource((F(1,4), F(3,4)))
        cake.remove(item)
        actual = IntervalResource([(F(0, 4), F(1,4)), (F(3,4), F(1,1))])
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,1), F(1,2))])
        item = IntervalResource((F(3,4), F(1,1)))
        self.assertRaises(ValueError, lambda: cake.remove(item))

    def test_resource_append(self):
        ''' test that the resource append works correctly '''
        cake = IntervalResource((F(1,2), F(1,1)))
        item = IntervalResource((F(0,1), F(1,2)))
        cake.append(item)
        actual = IntervalResource((F(0, 1), F(1,1)))
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(1,3), F(2,3))])
        item = IntervalResource([(F(0,3), F(1,3)), (F(2,3), F(3,3))])
        cake.append(item)
        self.assertEqual(actual.value, cake.value)

        cake = IntervalResource([(F(0,8), F(1,8))])
        item = IntervalResource([(F(1,8), F(2,8)), (F(3,4), F(1,1))])
        actual = IntervalResource([(F(0, 4), F(1,4)), (F(3,4), F(1,1))])
        cake.append(item)
        self.assertEqual(actual.value, cake.value)
        self.assertEqual(F(1, 2), cake.actual_value())

    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        user = IntervalPreference('user', [(0.0, 1.0), (1.0, 1.0)])
        cake = IntervalResource((F(0,1), F(1,1)))
        pieces = cake.create_pieces(user, 3)
        actual = [
            IntervalResource((F(0,3), F(1,3))),
            IntervalResource((F(1,3), F(2,3))),
            IntervalResource((F(2,3), F(3,3))),
        ]
        self.assertEqual(pieces, actual)

    def test_resource_find_piece(self):
        ''' test that we can find a piece in the cake '''
        user = IntervalPreference('user', [(0.0, 1.0), (1.0, 1.0)])
        cake = IntervalResource((F(0,1), F(1,1)))
        piece = cake.find_piece(user, F(1,2))
        actual = IntervalResource((F(0,1), F(1,2)))
        self.assertEqual(piece, actual)

        cake = IntervalResource([(F(0,1), F(1,4)), (F(1,4), F(3,4))])
        piece = cake.find_piece(user, F(1,2))
        actual = IntervalResource([(F(0,1), F(1,4)), (F(1,4), F(2,4))])
        self.assertEqual(piece, actual)

        cake = IntervalResource([(0.0, 0.25), (0.5, 0.75), (0.80, 1.0)])
        piece = cake.find_piece(user, 0.6)
        actual = IntervalResource([(0.0, 0.25), (0.5, 0.75), (0.80, 0.9)])
        self.assertEqual(piece, actual)

        self.assertRaises(ValueError, lambda: cake.find_piece(user, F(10)))

    def test_resource_as_collection(self):
        ''' test that we can convert a resource to a collection '''
        cake = IntervalResource((F(0), F(1)), resolution=5)
        pieces = cake.as_collection()
        actual = [
            IntervalResource((F(0,5), F(1,5))),
            IntervalResource((F(1,5), F(2,5))),
            IntervalResource((F(2,5), F(3,5))),
            IntervalResource((F(3,5), F(4,5))),
            IntervalResource((F(4,5), F(5,5)))
        ]
        for this,that in zip(pieces, actual):
            self.assertEqual(this.value, that.value)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
