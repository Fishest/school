#!/usr/bin/env python
import os
import unittest
import random
from fractions import Fraction as F
from cakery.resource import CollectionResource
from cakery.preference import OrdinalPreference
from cakery.preference import CollectionPreference

class OrdinalResourceTest(unittest.TestCase):
    '''
    This is the unittest for the OrdinalResource
    code utilities.
    '''

    def test_preference_create(self):
        ''' test that the preference is created correctly '''
        vals  = {'a': 4, 'b': 3, 'c': 2, 'd': 1}
        keys  = sorted(vals.keys())
        cake  = CollectionResource(keys)
        user1 = CollectionPreference('mark', vals)
        user2 = OrdinalPreference('john', keys)
        self.assertEqual(user1.value_of(cake), user2.value_of(cake))

        random.seed(1) # to ensure same test
        cake  = CollectionResource(['a'])
        user3 = OrdinalPreference.random(cake)
        self.assertNotEqual(user2.value_of(cake), user3.value_of(cake))


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
