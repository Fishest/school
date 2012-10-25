#!/usr/bin/env python
import unittest
from fractions import Fraction
from cakery.resource import CollectionResource
from cakery.preference import CollectionPreference

class CollectionResourceTest(unittest.TestCase):
    '''
    This is the unittest for the CollectionResource
    code utilities.
    '''

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange']
        vals = dict((k, Fraction(1)) for k in keys)
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))

    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        keys = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        vals = dict((k, Fraction(1)) for k in keys)
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
        vals = dict((k, Fraction(1)) for k in keys)
        cake = CollectionResource(keys)
        user = CollectionPreference('mark', vals)
        piece = cake.find_piece(user, 3)
        actual = CollectionResource(['blue', 'purple', 'yellow'])
        self.assertEqual(piece, actual)

        vals = {'red':10, 'blue':20, 'green':30, 'yello':15, 'orange':25}
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

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
