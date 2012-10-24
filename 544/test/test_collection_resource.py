#!/usr/bin/env python
import unittest
from cakery.resource import CollectionResource

class CollectionResourceTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.resource.CollectionResource
    '''

    def test_cloning(self):
        ''' test that the resource clones correctly '''
        items = ['red', 'blue', 'green', 'yello', 'orange']
        resource = CollectionResource(items)
        copied = resource.clone()
        self.assertEqual(str(resource), str(copied))
        self.assertEqual(repr(resource), repr(copied))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
