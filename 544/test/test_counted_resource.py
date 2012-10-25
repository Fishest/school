#!/usr/bin/env python
import unittest
from cakery.resource import CountedResource

class CountedResourceTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.resource.CountedResource
    '''

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        items = {'red':2, 'blue':3, 'green':4, 'yello':5, 'orange':6}
        cake = CountedResource(items)
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        items = {'red':2, 'blue':3, 'green':4, 'yello':5, 'orange':6}
        cake = CountedResource(items)
        copy = cake.clone()
        item = CountedResource({'red': 2, 'orange':6})
        copy.remove(item)
        actual = CountedResource({'blue':3, 'green':4, 'yello':5})
        self.assertEqual(copy, actual)

        copy = cake.clone()
        item = CountedResource(items.keys())
        copy.remove(item)
        actual = CountedResource(dict((k,v - 1) for k,v in items.items()))
        self.assertEqual(copy, actual)

        item = CountedResource('cyan')
        self.assertRaises(ValueError, lambda: cake.remove(item))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
