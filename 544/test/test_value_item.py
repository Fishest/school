#!/usr/bin/env python
import unittest
from cakery.utilities import ValueItem as V

class ValueItemTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.utilities.ValueItem
    '''

    def test_rich_comparison(self):
        ''' test the rich comparison methods work correctly '''
        hat = V('hat', 250)
        car = V('car', 25000)
        self.assertTrue(hat == hat)
        self.assertTrue(car == car)
        self.assertTrue(car != hat)
        self.assertTrue(car >= car)
        self.assertTrue(car <= car)
        self.assertTrue(car >= hat)
        self.assertTrue(car  > hat)
        self.assertTrue(hat <= car)
        self.assertTrue(hat  < car)

    def test_item_hashing(self):
        ''' test the hashing methods work correctly '''
        hat = V('hat', 250)
        car = V('car', 25000)
        items = {hat: hat.value, car: car.value}
        self.assertNotEqual(hash(hat), hash(car))
        for key in [car, hat]:
            self.assertEqual(key.value, items[key])

    def test_item_strings(self):
        ''' test the string methods work correctly '''
        hat = V('hat', 250)
        self.assertEqual('hat($250)', str(hat))
        self.assertEqual('hat($250)', repr(hat))

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
