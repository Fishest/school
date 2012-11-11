#!/usr/bin/env python
import os
import unittest
from cakery.resource import CountedResource
from cakery.preference import CountedPreference

class CountedResourceTest(unittest.TestCase):
    '''
    This is the unittest for the CountedResource
    code utilities.
    '''

    def test_resource_create(self):
        ''' test that the resource factory methods work '''
        path  = os.path.join(os.path.abspath('data'), 'collection')
        path  = os.path.join(path, 'uniform')
        user1 = CountedPreference.from_file(path)
        keys  = user1.values.keys()
        prefs = dict((p, 0.25) for p in keys)
        user2 = CountedPreference('user2', prefs)
        cake  = CountedResource(dict((k, 1) for k in keys))
        self.assertEqual(user1.value_of(cake), user2.value_of(cake))

        users = [CountedPreference.random(cake) for i in range(5)]
        for user in users:
            self.assertTrue(0.95 <= user.value_of(cake) <= 1.05)

    def test_resource_clone(self):
        ''' test that the resource clones correctly '''
        items = {'red':2, 'blue':3, 'green':4, 'yello':5, 'orange':6}
        cake = CountedResource(items)
        copy = cake.clone()
        self.assertEqual(str(cake), str(copy))
        self.assertEqual(repr(cake), repr(copy))
        self.assertEqual(20, cake.actual_value(),)
        self.assertEqual(cake.actual_value(), copy.actual_value())

    def test_resource_remove(self):
        ''' test that the resource remove works correctly '''
        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        keys = vals.keys()
        cake = CountedResource(vals)
        copy = cake.clone()
        item = CountedResource({'red': 2, 'orange':6})
        copy.remove(item)
        actual = CountedResource({'blue':3, 'green':4, 'yellow':5})
        self.assertEqual(copy.value, actual.value)

        copy = cake.clone()
        item = CountedResource(keys)
        copy.remove(item)
        actual = CountedResource(dict((k,v - 1) for k,v in vals.items()))
        self.assertEqual(copy, actual)

        item = CountedResource('cyan')
        self.assertRaises(ValueError, lambda: cake.remove(item))

    def test_resource_append(self):
        ''' test that the resource append works correctly '''
        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        cake = CountedResource({'blue':3, 'green':2, 'yellow':5})
        item = CountedResource({'red': 2, 'orange':6, 'green':2})
        cake.append(item)
        actual = CountedResource(vals)
        self.assertEqual(cake.value, actual.value)

    # TODO
    @unittest.skip("fixing")
    def test_resource_create_pieces(self):
        ''' test that we can create n pieces of the cake '''
        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        pref = {'red':1, 'blue':1, 'green':1, 'yellow':1, 'orange':1}
        cake = CountedResource(vals)
        user = CountedPreference('mark', pref)
        pieces = cake.create_pieces(user, 3)
        actual = [
            CountedResource({'red':1, 'blue':1}),
            CountedResource({'green':1, 'yellow':1}),
            CountedResource({'orange':1, 'purple':1})
        ]
        for this,that in zip(pieces, actual):
            self.assertEqual(this.value, that.value)

    def test_resource_find_pieces(self):
        ''' test that we can find a piece in the cake '''
        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        pref = {'red':1, 'blue':1, 'green':1, 'yellow':1, 'orange':1}
        cake = CountedResource(vals)
        user = CountedPreference('mark', pref)
        piece = cake.find_piece(user, 3)
        actual = CountedResource({'blue':1, 'orange':1, 'green':1})
        self.assertEqual(piece.value, actual.value)

        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        pref = {'red':10, 'blue':20, 'green':30, 'yellow':15, 'orange':25}
        cake = CountedResource(vals)
        user = CountedPreference('mark', pref)
        self.assertEqual(50, user.value_of(cake.find_piece(user, 50)))
        self.assertEqual(60, user.value_of(cake.find_piece(user, 60)))
        self.assertEqual(70, user.value_of(cake.find_piece(user, 70)))

        vals = {'red':2, 'blue':3, 'green':4, 'yellow':5, 'orange':6}
        pref = {'red':10, 'blue':20, 'green':30, 'yellow':15, 'orange':25}
        cake = CountedResource(vals)
        user = CountedPreference('mark', pref)
        self.assertEqual(50, user.value_of(cake.find_piece(user, 50)))
        self.assertEqual(60, user.value_of(cake.find_piece(user, 60)))
        self.assertEqual(70, user.value_of(cake.find_piece(user, 70)))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
