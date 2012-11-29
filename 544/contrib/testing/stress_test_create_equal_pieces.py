#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import create_equal_pieces

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
iterations = 5 # the number of rounds to run

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
def counted_factory():
    ''' Otherwise it doesn't look like the
    resource is split, this makes it roughly
    look like a collection resource
    '''
    cake = CountedResource.random(10)
    cake.value = {k: 1 for k in cake.value}
    return cake 

xs = CollectionResource([chr(i) for i in range(ord('a'), ord('{'))])
us   = [
    lambda: ContinuousPreference.random(),
    lambda: CountedPreference.random(xs),
    lambda: CollectionPreference.random(xs),
    lambda: OrdinalPreference.random(xs),
    lambda: IntervalPreference.random(3)
]
cs = [      # skew, resource
    lambda: (0.05, ContinuousResource(F(0), F(1))),
    lambda: (0.25, counted_factory()),
    lambda: (0.20, CollectionResource.random(10)),
    lambda: (0.20, CollectionResource.random(10)),
    lambda: (0.10, IntervalResource((F(0), F(1))))
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
print "\n","=" * 60
print "Create Equal Pieces Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory()[1].__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        skew, cake = cake_factory()
        user   = user_factory()
        total  = user.value_of(cake)
        value  = F(1, size) * total
        pieces = create_equal_pieces(user, cake, size)
        values = [user.value_of(piece) for piece in pieces]
        print "needed[%f]\t<= found:%s" % (value, values)

        assert(abs(sum(values) - total) < (total * 0.01))               # should roughly sum to 1
        #assert(all(abs(v - value) < (value * skew) for v in values))   # should all be ~ equal
