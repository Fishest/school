#!/usr/bin/env python
import os
import unittest
from fractions import Fraction as F
from cakery.resource import CollectionResource
from cakery.preference import CollectionPreference

class CollectionResourceTest(unittest.TestCase):
    '''
    This is the unittest for the CollectionResource
    code utilities.
    '''

    def test_resource_create(self):
        ''' test that the resource factory methods work '''
        cake1 = CollectionResource.random(5)
        cake2 = CollectionResource.random(5)
        cake3 = CollectionResource.random()
        self.assertEqual(cake1.actual_value(), cake2.actual_value())
        self.assertNotEqual(cake1.value, cake2.value)
        self.assertNotEqual(cake1.value, cake3.value)

    def test_preference_create(self):
        ''' test that the preference factory methods work '''
        path  = os.path.join(os.path.abspath('contrib'), 'data')
        path  = os.path.join(path, 'collection')
        path  = os.path.join(path, 'uniform')
        user1 = CollectionPreference.from_file(path)
        keys  = user1.values.keys()
        prefs = dict((p, 0.25) for p in keys)
        user2 = CollectionPreference('user2', prefs)
        cake  = CollectionResource(keys)
        self.assertEqual(user1.value_of(cake), user2.value_of(cake))

        users = [CollectionPreference.random(cake) for i in range(5)]
        for user in users:
            self.assertTrue(0.95 <= user.value_of(cake) <= 1.05)

    def test_resource_clone(self):
        ''' test that the resource clone works correctly '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange']
        vals = dict((k, F(1,1)) for k in keys)
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))

        self.assertEqual(5, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

        self.assertEqual(CollectionResource('a'), CollectionResource(['a']))

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange']
        cake = CollectionResource(keys)
        item = CollectionResource(keys[2:])
        cake.remove(item)
        actual = CollectionResource(keys[:2])
        self.assertEqual(actual, cake)

    def test_resource_append(self):
        ''' test that the resource append works correctly '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange']
        cake = CollectionResource(keys[:-2])
        item = CollectionResource(keys[-2:])
        cake.append(item)
        actual = CollectionResource(keys)
        self.assertEqual(actual.value, cake.value)

    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        vals = dict((k, F(1,1)) for k in keys)
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        pieces = cake.create_pieces(user, 3)
        actual = [
            CollectionResource(['red', 'blue']),
            CollectionResource(['green', 'yellow']),
            CollectionResource(['orange', 'purple'])
        ]
        for this,that in zip(pieces, actual):
            self.assertEqual(this.value, that.value)

    def test_resource_find_pieces(self):
        ''' test that we can find a piece in the cake '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        vals = dict((k, F(1,1)) for k in keys)
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        piece = cake.find_piece(user, 3)
        actual = CollectionResource(['red', 'blue', 'green'])
        self.assertEqual(piece.value, actual.value)

        vals = {'red':10, 'blue':20, 'green':30, 'yellow':15, 'orange':25}
        keys = vals.keys()
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        self.assertEqual(50, user.value_of(cake.find_piece(user, 50)))
        self.assertEqual(60, user.value_of(cake.find_piece(user, 60)))
        self.assertEqual(70, user.value_of(cake.find_piece(user, 70)))

        vals = {'red':10, 'blue':20, 'green':30, 'orange':40}
        keys = vals.keys()
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        self.assertEqual(50, user.value_of(cake.find_piece(user, 50)))
        self.assertEqual(60, user.value_of(cake.find_piece(user, 60)))
        self.assertEqual(70, user.value_of(cake.find_piece(user, 70)))

        self.assertRaises(ValueError, lambda: cake.find_piece(user, 150))

    def test_resource_as_collection(self):
        ''' test that we can convert a resource to a collection '''
        keys = ['red', 'blue', 'green']
        cake = CollectionResource(keys)
        pieces = cake.as_collection()
        actual = [CollectionResource(key) for key in keys]
        for this,that in zip(pieces, actual):
            self.assertEqual(this.value, that.value)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
