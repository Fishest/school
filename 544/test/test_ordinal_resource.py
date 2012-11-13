#!/usr/bin/env python
import os
import unittest
from fractions import Fraction as F
from cakery.resource import CollectionResource
from cakery.preference import OrdinalPreference
from cakery.preference import CollectionPreference

class OrdinalResourceTest(unittest.TestCase):
    '''
    This is the unittest for the OrdinalResource
    code utilities.
    '''

    def test_resource_create(self):
        ''' test that the resource is created correctly '''
        vals  = {'a': 4, 'b': 3, 'c': 2, 'd': 1}
        keys  = sorted(vals.keys())
        user1 = CollectionPreference('mark', vals)
        user2 = OrdinalPreference('john', keys)
        cake  = CollectionResource(keys)
        self.assertEqual(user1.value_of(cake), user2.value_of(cake))


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
