from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms.utilities import choose_best_piece
from cakery.algorithms.utilities import choose_worst_piece

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
for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory().__class__.__name__
    print "-" * 60
    for size in range(2, iterations):
        user  = user_factory()
        cakes = [cake_factory() for i in range(size)]
        left  = choose_worst_piece(user, cakes)
        right = choose_best_piece(user, cakes)
        lvalue, rvalue = user.value_of(left), user.value_of(right)
        print "left[%f]\t<=\tright[%f]" % (lvalue, rvalue)
        assert(left   != right)
        assert(lvalue <= rvalue)
