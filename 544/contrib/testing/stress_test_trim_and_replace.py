#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import trim_and_replace

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
iterations = 20 # the number of rounds to run

#------------------------------------------------------------ 
# helper factories
#------------------------------------------------------------ 
# These are here so we can generate two clean halves so we
# can focus on optimizing the trim function (and not have
# to worry about noise from other methods).
#------------------------------------------------------------ 
def generate_continuous():
    return [
        ContinuousResource(F(0,2), F(1,2)),
        ContinuousResource(F(1,2), F(2,2))
    ]

def generate_interval():
    return [
        IntervalResource((F(0,2), F(1,2))),
        IntervalResource((F(1,2), F(2,2)))
    ]

def generate_collection():
    cake1 = CollectionResource.random(10)
    cake2 = cake1.clone()
    cake1.value = cake1.value[:5]
    cake2.value = cake2.value[5:]
    return [cake1, cake2]

def generate_counted():
    cake1 = CountedResource.random(10)
    cake1.value = {k: 1 for k in cake1.value}
    cake2 = cake1.clone()
    cake1.value = dict(cake1.value.items()[:5])
    cake2.value = dict(cake2.value.items()[5:])
    return [cake1, cake2]

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
xs = CollectionResource([chr(i) for i in range(ord('a'), ord('{'))])
us   = [
    #lambda: (1.00, ContinuousPreference.random()),
    lambda: (0.05, CountedPreference.random(xs)),
    lambda: (0.05, CollectionPreference.random(xs)),
    lambda: (20.00, OrdinalPreference.random(xs)), # these values get large
    lambda: (0.02, IntervalPreference.random(3))
]
cs = [
    #lambda: generate_continuous(), TODO this is broke!
    lambda: generate_counted(),
    lambda: generate_collection(),
    lambda: generate_collection(),
    lambda: generate_interval()
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
print "\n","=" * 60
print "Trim and Replace Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory()[0].__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        skew, user = user_factory()
        cake, trim = cake_factory()
        cvalue = user.value_of(cake)    # original cake
        tvalue = user.value_of(trim)    # the trimming to reduce
        pvalue = F(1, size) * tvalue    # the size we want the trimming to be
        piece  = trim_and_replace(user, cake, trim, pvalue)
        cvalue2 = user.value_of(cake)   # the cake with trimming added back
        tvalue2 = user.value_of(piece)  # the reduced trimming
        before, after = cvalue + tvalue, cvalue2 + tvalue2
        arguments = (cvalue, tvalue, pvalue, cvalue2, tvalue2)
        print "head[c:%f, t:%f]\t: need[t:%f]\t: tail[c:%f, t:%f]" % arguments
        assert(abs(before - after) < before * 0.01)
        assert(abs(pvalue - tvalue2) < skew)
