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
        self.assertEqual(pieces, actual)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
