#!/usr/bin/env python
import random
import unittest
from cakery.algorithms.utilities import AlternationStrategy

class AlternationStrategyTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.algorithm.AlternationStrategy
    '''

    def test_ordinal_strategy(self):
        ''' test the ordinal alternation strategy '''
        users = ['a', 'b']
        cakes = [None] * 16
        strategy = AlternationStrategy.ordinal(users, cakes)
        self.assertEquals(users, strategy())

    def test_random_strategy(self):
        ''' test the random alternation strategy '''
        random.seed(1) # to ensure same result
        users = ['a', 'b']
        cakes = [None] * 16
        strategy = AlternationStrategy.random(users, cakes)
        turns = [strategy() for i in range(4)]
        self.assertNotEqual(turns, sorted(turns))

    def test_balanced_strategy(self):
        ''' test the random alternation strategy '''
        users = ['a', 'b']
        turns = {1: 'ab', 4:'abba', 8:'abbabaab', 16:'abbabaabbaababba'}
        # TODO check ranges between
        for size, expected in turns.items():
            cake = [None] * size
            strategy = AlternationStrategy.balanced(users, cake)
            actual = ''.join(strategy())
            self.assertEqual(actual, expected)


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
