#!/usr/bin/env python
import unittest
from cakery.resource import CountedResource

class CountedResourceTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.resource.CountedResource
    '''

    def test_cloning(self):
        ''' test that the resource clones correctly '''
        items = {'red':2, 'blue':3, 'green':4, 'yello':5, 'orange':6}
        resource = CountedResource(items)
        copied = resource.clone()
        self.assertEqual(str(resource), str(copied))
        self.assertEqual(repr(resource), repr(copied))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
