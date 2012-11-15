from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import choose_highest_bidder
from cakery.algorithms.utilities import choose_lowest_bidder

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
iterations = 10 # the number of rounds to run

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
xs = CollectionResource(['a', 'b', 'c', 'd', 'e'])
us   = [
    lambda: ContinuousPreference.random(),
    lambda: CountedPreference.random(xs),
    lambda: CollectionPreference.random(xs),
    lambda: OrdinalPreference.random(xs),
    lambda: IntervalPreference.random(10)
]
cs = [
    lambda: ContinuousResource(F(0,1), F(1,2)),
    lambda: CountedResource({'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}),
    lambda: CollectionResource(['c', 'd']),
    lambda: CollectionResource(['c', 'd']),
    lambda: IntervalResource((F(0,1), F(1,2)))
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
for user_factory, cake_factory in zip(us, cs):
    cake = cake_factory()
    print "-" * 60
    print cake.__class__.__name__, cake
    print "-" * 60
    for size in range(2, iterations):
        users = [user_factory() for _ in range(size)]
        left  = choose_lowest_bidder(users, cake)
        right = choose_highest_bidder(users, cake)
        lvalue, rvalue = left.value_of(cake), right.value_of(cake)
        print "left[%f]\t<=\tright[%f]" % (lvalue, rvalue)
        assert(left != right)
        assert(lvalue <= rvalue)
