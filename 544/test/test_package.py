#!/usr/bin/env python
import unittest
from cakery.version import version

class PackageTest(unittest.TestCase):
    '''
    This is the unittest for the cakery.utilities.maximum_cut
    '''

    def test_version(self):
        ''' test that the powerset method works correctly '''
        short = version.short()
        total = str(version).split(' ')[-1][:-1]
        self.assertEqual(total, short)

#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    unittest.main()
