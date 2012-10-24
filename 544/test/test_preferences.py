#!/usr/bin/env python
import unittest
from cakery.preference import Preference

class PreferenceTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.preference.Preference
    '''

    def test_initializes(self):
        ''' test that the preference initializes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        pref = Preference('mark', vals) # uniform
        self.assertEqual(str(pref), repr(pref))
        self.assertEqual(pref.sees_unit_value(), True)

    def test_normalize(self):
        ''' test that the preference normalizes correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        pref = Preference('mark', vals, 1000)
        self.assertEqual(pref.sees_unit_value(), False)
        pref.normalize()
        self.assertEqual(pref.sees_unit_value(), True)

    def test_update(self):
        ''' test that the preference updates correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        pref = Preference('mark', vals, 100)
        self.assertEqual(pref.sees_unit_value(), True)

        pref.update(keys + ['purple', 'black'])
        self.assertEqual(pref.sees_unit_value(), True)
        self.assertEqual(len(pref.values), 7)

        pref.update(keys[1:], remove=True)
        self.assertEqual(pref.sees_unit_value(), True)
        self.assertEqual(len(pref.values), 4)

    def test_value_of(self):
        ''' test that the preference gets the resource(s) value correctly '''
        keys = ['red', 'blue', 'green', 'yello', 'orange']
        vals = dict((k, 100/len(keys)) for k in keys)
        pref = Preference('mark', vals, 100)
        self.assertEqual(pref.value_of('red'), 20)
        self.assertEqual(pref.value_of(['red']), 20)
        self.assertEqual(pref.value_of(['red', 'blue']), 40)
        self.assertEqual(pref.value_of(['red', 'cyan']), 20)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
