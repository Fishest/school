#!/usr/bin/env python
import unittest
from fractions import Fraction
from cakery.utilities import Interval


class IntervalTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.utilities.Interval
    '''

    def test_initializes(self):
        ''' test that the utility initializes correctly '''
        self.assertRaises(ValueError, lambda: Interval((1,1), (0,0)))

        interval = Interval((0,0), (1, 1.0))
        self.assertEqual("(0, 0) - (1, 1.0)", str(interval))
        self.assertEqual(1, interval.m)
        self.assertEqual(0, interval.b)
        self.assertEqual(0.5, interval.area(0, 1))
        self.assertEqual(0.0, interval.area(2, 0))

        interval = Interval((0, 0), (1, Fraction(1, 2)))
        self.assertEqual("(0, 0) - (1, Fraction(1, 2))", str(interval))
        self.assertEqual(Fraction(1, 2), interval.m)
        self.assertEqual(0, interval.b)
        self.assertEqual(Fraction(0, 1), interval.area(0, 0))
        self.assertEqual(Fraction(1, 4), interval.area(0, 1))

    def test_create(self):
        ''' test that the factory method works correctly '''
        intervals = [(0,0), (1,1)]
        interval  = Interval.create(intervals)[0]
        self.assertEqual("(0, 0) - (1, 1)", str(interval))

        intervals = [(0,0), (0.5,0.5)]
        interval  = Interval.create(intervals)[-1]
        self.assertEqual("(0.5, 0.5) - (1, 0)", str(interval))


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
