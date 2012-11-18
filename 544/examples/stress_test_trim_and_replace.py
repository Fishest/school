#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import trim_and_replace

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
print "Trim and Replace Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory().__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        user   = user_factory()
        cake   = cake_factory()
        trim   = cake_factory()
        cvalue = user.value_of(cake)
        tvalue = user.value_of(trim)
        pvalue = F(1, size) * tvalue
        piece  = trim_and_replace(user, cake, trim, pvalue)
        arguments = (cvalue, tvalue, pvalue, user.value_of(cake), user.value_of(piece))
        print "head[c:%f, t:%f]\t: need[t:%f]\t: tail[c:%f, t:%f]" % arguments
        #assert(abs(value - user.value_of(piece)) < value * 0.10)
