#!/usr/bin/env python
import random
import unittest
from cakery.algorithms.utilities import *
from cakery.preference import CollectionPreference
from cakery.resource import CollectionResource

class AlgorithmUtilitiesTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.utility
    '''

    def test_randomize_items(self):
        ''' test the random items utility '''
        random.seed(1) # to ensure same result
        items = ['a', 'b', 'c', 'd']
        takes = [randomize_items(items) for i in range(2)]
        self.assertNotEqual(takes, sorted(takes))

    def test_choose_and_remove(self):
        ''' test the choose and remove utility '''
        random.seed(1) # to ensure same result
        items = ['a', 'b', 'c', 'd']
        item = choose_and_remove(items)
        self.assertEqual(item, 'a')
        self.assertEqual(items, ['b', 'c', 'd'])

    def test_choose_highest_bidder(self):
        ''' test the choose highest bidder utility '''
        cake = CollectionResource(['cake'])
        users = [
            CollectionPreference('mark', {'cake':1}),
            CollectionPreference('john', {'cake':0})
        ]
        actual = choose_highest_bidder(users, cake)
        self.assertEqual(actual, users[0])

        users[0].values['cake'] = 0
        actual = choose_highest_bidder(users, cake)
        self.assertEqual(actual, users[0])

    def test_choose_lowest_bidder(self):
        ''' test the choose lowest bidder utility '''
        cake = CollectionResource(['cake'])
        users = [
            CollectionPreference('mark', {'cake':1}),
            CollectionPreference('john', {'cake':0})
        ]
        actual = choose_lowest_bidder(users, cake)
        self.assertEqual(actual, users[1])

        users[0].values['cake'] = 0
        actual = choose_lowest_bidder(users, cake)
        self.assertEqual(actual, users[0])

    def test_choose_best_piece(self):
        ''' test the choose best piece utility '''
        prefs = {'a': 1, 'b': 2, 'c': 3}
        cakes = [CollectionResource([k]) for k in prefs.keys()]
        user  = CollectionPreference('mark', prefs)
        actual = choose_best_piece(user, cakes)
        self.assertEqual(actual.value, ['c'])

        user.values['b'] = 3
        actual = choose_best_piece(user, cakes)
        self.assertEqual(actual.value, ['c'])

    def test_choose_worst_piece(self):
        ''' test the choose worst piece utility '''
        prefs = {'a': 1, 'b': 2, 'c': 3}
        cakes = [CollectionResource([k]) for k in prefs.keys()]
        user  = CollectionPreference('mark', prefs)
        actual = choose_worst_piece(user, cakes)
        self.assertEqual(actual.value, ['a'])

        user.values['a'] = 3
        actual = choose_worst_piece(user, cakes)
        self.assertEqual(actual.value, ['b'])

    def test_create_equal_pieces(self):
        ''' test the create equal pieces utility '''
        pref = {'a': 1, 'b': 1, 'c': 1}
        cake = CollectionResource(pref.keys())
        user = CollectionPreference('mark', pref)
        actual = create_equal_pieces(user, cake, 3)
        pieces = [CollectionResource([k]) for k in pref.keys()]
        self.assertEqual(actual, pieces)

    def test_list_best_pieces(self):
        ''' test the list best pieces utility '''
        cakes = [
            CollectionResource(['a']),
            CollectionResource(['b'])
        ]
        users = [
            CollectionPreference('mark', {'a':1, 'b':0}),
            CollectionPreference('john', {'a':0, 'b':1})
        ]
        actual = list_best_pieces(users, cakes)
        expect = {users[0]: cakes[1], users[1]: cakes[0]}
        self.assertEqual(actual, expect)

        users[0].values = {'a':1, 'b':0}
        users[1].values = {'a':1, 'b':0}
        actual = list_best_pieces(users, cakes)
        expect = {users[0]: cakes[0], users[1]: cakes[0]}
        self.assertEqual(actual, expect)

    def test_list_worst_pieces(self):
        ''' test the list worst pieces utility '''
        cakes = [
            CollectionResource(['a']),
            CollectionResource(['b'])
        ]
        users = [
            CollectionPreference('mark', {'a':1, 'b':0}),
            CollectionPreference('john', {'a':0, 'b':1})
        ]
        actual = list_worst_pieces(users, cakes)
        expect = {users[0]: cakes[0], users[1]: cakes[1]}
        self.assertEqual(actual, expect)

        users[0].values = {'a':1, 'b':0}
        users[1].values = {'a':1, 'b':0}
        actual = list_worst_pieces(users, cakes)
        expect = {users[0]: cakes[1], users[1]: cakes[1]}
        self.assertEqual(actual, expect)

    def test_choose_next_piece(self):
        ''' test the choose next piece utility '''
        cake  = CollectionResource(['a', 'b', 'c'])
        users = [
            CollectionPreference('mark', {'a':0.5, 'b':.50}),
            CollectionPreference('john', {'a':0.25, 'b':.75})
        ]
        user, piece = choose_next_piece(users, cake)
        self.assertEqual(user, users[0])
        self.assertEqual(piece, CollectionResource(['a']))

    def test_trim_and_replace(self):
        ''' test the trim and replace utility '''
        cake = CollectionResource(['c'])
        trim = CollectionResource(['a', 'b'])
        user = CollectionPreference('mark', {'a':1, 'b':5, 'c':10})
        piece = trim_and_replace(user, cake, trim, 1)
        self.assertEqual(cake, CollectionResource(['a', 'b']))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
