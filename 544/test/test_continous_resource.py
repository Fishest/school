#!/usr/bin/env python
import unittest
from cakery.resource import ContinuousResource

class ContinuousResourceTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.resource.ContinuousResource
    '''

    def test_cloning(self):
        ''' test that the resource clones correctly '''
        resource = ContinuousResource(0, 100, 1)
        copied = resource.clone()
        self.assertEqual(str(resource), str(copied))
        self.assertEqual(repr(resource), repr(copied))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
