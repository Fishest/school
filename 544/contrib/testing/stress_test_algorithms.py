#!/usr/bin/env python
from functions import Functions
from random import randint
from fractions import Fraction
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms import *

class AlgorithmTester(object):

    def __init__(self, algorithm):
        '''
        '''
        self.algorithm = algorithm
        self.settings  = algorithm([], None).settings()

    def _create_users(self, count):
        '''
        '''
        users = []
        for idx in range(count):
            negat = -1 if idx % 2 == 0 else 1
            slope = Fraction(negat, randint(1, 10))
            shift = 1 - Fraction(1, 2) * slope
            value = Functions.linear(slope, shift)
            prefs = ContinuousPreference(None, value)
            print "[%s] = %f * x + %f" % (prefs.user, slope, shift)
            users.append(prefs)
        return users

    def _validate(self, algorithm, divisions):
        '''
        '''
        results = []

        if (self.settings['proportional']
            and not algorithm.is_proportional(divisions)):
            results.append('proportional')

        if (self.settings['equitable']
            and not algorithm.is_equitable(divisions)):
            results.append('equitable')

        if (self.settings['envy-free']
            and not algorithm.is_envy_free(divisions)):
            results.append('envy-free')

        if (self.settings['optimal']
            and not algorithm.is_optimal(divisions)):
            pass

        if any(results):
            print "errors:\t\t", results
            print "users:\t\t", algorithm.users
            print "divisions:\t", divisions

    def _iterate(self):
        ''' Given an algorithm, verify that it meets the
        settings that it states it does
        '''
        resource  = ContinuousResource(Fraction(0,1), Fraction(1,1))
        players   = [None]
        algorithm = self.algorithm(players, resource)
    
        while len(players) < self.settings['users']:
            players   = self._create_users(len(players) + 1)
            algorithm = self.algorithm(players, resource)

            try:
                algorithm.is_valid()
                divisions = algorithm.divide()
                self._validate(algorithm, divisions)
            except Exception, ex: print ex

    def test(self, iterations):
        for i in range(iterations):
            print "\nperforming iteration %i" % i
            print "-" * 60
            self._iterate()


#---------------------------------------------------------------------------#
# Main
#---------------------------------------------------------------------------#
if __name__ == "__main__":
    
    tester = AlgorithmTester(DivideAndChoose)
    tester.test(10)
