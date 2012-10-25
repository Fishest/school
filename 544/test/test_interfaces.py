#!/usr/bin/env python
import unittest
from cakery.preference import Preference
from cakery.resource import Resource

class InterfacesTest(unittest.TestCase):
    '''
    This is the unittest for the cakery interfaces
    '''

    def test_preference_interface(self):
        ''' test the basic methods on the preference interface '''
        cake = None
        user = Preference()
        self.assertRaises(NotImplementedError, lambda: user.value_of(cake))

    def test_resource_interface(self):
        ''' test the basic methods on the preference interface '''
        user = None
        item = None
        size = 0.5
        cake = Resource()
        self.assertRaises(NotImplementedError, lambda: cake.actual_value())
        self.assertRaises(NotImplementedError, lambda: cake.clone())
        self.assertRaises(NotImplementedError, lambda: cake.remove(item))
        self.assertRaises(NotImplementedError, lambda: cake.find_piece(user, size))
        self.assertRaises(NotImplementedError, lambda: cake.compare(item))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
