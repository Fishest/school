#!/usr/bin/env python
import unittest
from cakery.preference import Preference
from cakery.utilities import find_piece, create_pieces
from cakery.utilities import integrate

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

    def test_integrate(self):
        ''' test that integrate method works correctly '''
        self.assertEqual( 5, int(integrate(lambda x:   1, 0.0, 5.0, 100)))
        self.assertEqual(25, int(integrate(lambda x: 2*x, 0.0, 5.0, 100)))
        self.assertEqual(41, int(integrate(lambda x: x*x, 0.0, 5.0, 100)))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
