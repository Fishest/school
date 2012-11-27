import sys
import os
import logging

#--------------------------------------------------------------------------------#
# initialize logging
#--------------------------------------------------------------------------------#
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log.debug(sys.argv) # log command line arguments

#--------------------------------------------------------------------------------#
# initialize library path
#--------------------------------------------------------------------------------#
if __name__ == '__main__': pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

import cakery.algorithms
from cakery.resource import *
from cakery.preference import *
from fractions import Fraction as F


#--------------------------------------------------------------------------------#
# helper methods
#--------------------------------------------------------------------------------#
def get_algorithm(name):
    ''' Given an algorithm name, return a factory
    for that algorithm.

    :param name: The name of the algorithm to create
    :returns: The type factory for that algorithm
    '''
    if not hasattr(cakery.algorithms, name):
        raise Exception("no matching algorithm available")
    return getattr(cakery.algorithms, name)


def get_users(paths):
    ''' Given a collection of preference files,
    generate a collection of users.

    :param paths: The paths to create users from
    :returns: The collection of users to operate with
    '''
    preferences = [
        IntervalPreference,
        CollectionPreference,
        CountedPreference,
        ContinuousPreference,
    ]

    for preference in preferences:
        try:
            log.debug("trying user %s" % preference.__name__)
            return [preference.from_file(path) for path in paths]
        except Exception, e:
            log.exception("Preference cannot be parsed")
    raise Exception("no matching user preference available")


def get_cake(user):
    ''' Given a collection of preference files,
    generate a collection of users.

    :param user: The type of user to create a cake for
    :returns: The collection of users to operate with
    '''
    resource = resources = {
        'IntervalPreference'  : lambda: IntervalResource((F(0, 1), F(1, 1))),
        'CollectionPreference': lambda: CollectionResource(user.values.keys()),
        'ContinuousPreference': lambda: ContinuousResource(F(0, 1), F(1, 1)),
    }[user.__class__.__name__]
    return resource()

def print_results(divider, results, extras):
    ''' Given an algorithm and its results,
    print a nice report to the console.

    :param divider: The algorithm we divided with
    :param results: The division results
    :param extras: Any extra results to report
    '''
    header  = "-" * 50
    print "\nAlgorithm Information\n", header
    for key, value in divider.settings().items():
        print "*", key, "\t:", value

    print "\nAlgorithm Results\n", header
    for user, shares in results.items():
        print "* share for", user
        print " ", shares, "\n"

    if isinstance(extras, dict):
        print "Extra Results\n", header
        for key, value in extras.items():
            print key, "\t:", value
        print

    print "Algorithm Result Validation\n", header
    print "* users\t\t:", len(results.keys())
    print "* optimal\t:", divider.is_optimal(results)
    print "* envy free\t:", divider.is_envy_free(results)
    print "* equitable\t:", divider.is_equitable(results)
    print "* proportional\t:", divider.is_proportional(results)


#--------------------------------------------------------------------------------#
# algorithm main
#--------------------------------------------------------------------------------#
def run_algorithm(name):
    ''' Given an algorithm, run it with the supplied
    command line parameters.

    :param name: The name of the algorithm to run
    '''
    users   = get_users(sys.argv[1:])
    cake    = get_cake(users[0])
    factory = get_algorithm(name)
    divider = factory(users, cake)
    results = divider.divide()
    extras  = None

    if isinstance(results, tuple):
        results, extras = results
    print_results(divider, results, extras)
