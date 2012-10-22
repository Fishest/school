#!/usr/bin/env python
import unittest
from cakery.preference import Preference
from cakery.utilities import find_piece, create_pieces

class UtilitiesTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.utilities.maximum_cut
    '''

    def test_find_piece(self):
        ''' test that the finding a single piece works correctly '''
        vals = {'red':10, 'blue':20, 'green':30, 'yello':15, 'orange':25}
        keys = vals.keys()
        pref = Preference('mark', vals, 100)
        self.assertEqual(50, find_piece(keys, pref, 50)[0])
        self.assertEqual(60, find_piece(keys, pref, 60)[0])
        self.assertEqual(70, find_piece(keys, pref, 70)[0])

        vals = {'red':10, 'blue':20, 'green':30, 'orange':40}
        keys = vals.keys()
        pref = Preference('mark', vals, 100)
        self.assertEqual(50, find_piece(keys, pref, 50)[0])
        self.assertEqual(60, find_piece(keys, pref, 60)[0])
        self.assertEqual(70, find_piece(keys, pref, 70)[0])
        
    def test_create_pieces(self):
        ''' test that the creating n pieces works correctly '''
        pass

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
