#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import list_best_pieces
from cakery.algorithms.utilities import list_worst_pieces

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
iterations = 10 # the number of rounds to run

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
xs = CollectionResource([chr(i) for i in range(ord('a'), ord('{'))])
us   = [
    lambda: ContinuousPreference.random(),
    lambda: CountedPreference.random(xs),
    lambda: CollectionPreference.random(xs),
    lambda: OrdinalPreference.random(xs),
    lambda: IntervalPreference.random(3)
]
cs = [
    lambda: ContinuousResource.random(),
    lambda: CountedResource.random(),
    lambda: CollectionResource.random(),
    lambda: CollectionResource.random(),
    lambda: IntervalResource.random(5)
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
print "\n","=" * 60
print "List Min/Max Pieces Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory().__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        users = [user_factory() for i in range(2)]
        cakes = [cake_factory() for i in range(size)]
        left  = list_worst_pieces(users, cakes)
        right = list_best_pieces(users, cakes)
        for ((u1, p1),(u2, p2)) in zip(left.items(), right.items()):
            lvalue, rvalue = u1.value_of(p1), u1.value_of(p2)
            print "left[%f]\t\t<= right[%f]" % (lvalue, rvalue)
            assert(p1 != p2)
            assert(u1 == u2)
            assert(lvalue <= rvalue)
