#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import choose_next_piece

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
    #lambda: CountedPreference.random(xs),
    #lambda: CollectionPreference.random(xs),
    #lambda: OrdinalPreference.random(xs),
    lambda: IntervalPreference.random(3)
]
cs = [
    #lambda: ContinuousResource.random(),
    #lambda: CountedResource.random(),
    #lambda: CollectionResource.random(),
    #lambda: CollectionResource.random(),
    #lambda: IntervalResource.random(5)

    lambda: ContinuousResource(F(0), F(1)),
    #lambda: CountedResource.random(10),
    #lambda: CollectionResource.random(10),
    #lambda: CollectionResource.random(10),
    lambda: IntervalResource((F(0), F(1)))
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
print "\n","=" * 60
print "Choose Next Piece Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory().__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        value = F(1, size)
        users = [user_factory() for _ in range(size)]
        cake  = cake_factory()
        (user, piece)  = choose_next_piece(users, cake)
        values = {u: u.value_of(piece) for u in users}
        closer = min((abs(value - v), k) for k,v in values.items())[1]
        print "needed[%f]\t\t<= found[%f]" % (value, values[user])
        assert(user == closer)
