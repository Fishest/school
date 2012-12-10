#!/usr/bin/env python
from fractions import Fraction as F
from cakery.preference import *
from cakery.resource import *
from cakery.algorithms import *
from cakery.algorithms.utilities import get_total_value

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
# [A] This algorithm will not work well for discrete items
#     with many users unless there are many items as well.
# [B] This algorithm is currently broke
#------------------------------------------------------------ 
iterations = 10 # the number of rounds to run
algorithms = [
#    AustinMovingKnife,
#    BanachKnaster,             # [A]
#    InverseBanachKnaster,      # [A]
#    DivideAndChoose,
    DubinsSpanier,             # [A]
#    InverseDubinsSpanier,      # [A]
#    SealedBidsAuction,
#    InverseDivideAndChoose,
#    LoneChooser,               # [A]
#    InverseLoneChooser,        # [A]
#    AlternatingChoice,
#    InverseAlternatingChoice,
#    BalancedAlternatingChoice,
#    InverseBalancedAlternatingChoice,
#    KnasterSealedBids,
#    AdjustedWinner,
#    OneCutSuffices,
#    GuyConwaySelfridge,        # [B]
#    InverseGuyConwaySelfridge, # [B]
#    LensEpsteinPoints,
#    SalterPoints,
#    TaylorRst,
]

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
us   = [
    #lambda xs: ContinuousPreference.random(),
    #lambda xs: CountedPreference.random(xs),
    #lambda xs: CollectionPreference.random(xs),
    #lambda xs: OrdinalPreference.random(xs),
    lambda xs: IntervalPreference.random(3)
]
cs = [
    #lambda: ContinuousResource(F(0), F(1)),
    #lambda: CountedResource.random(10),
    #lambda: CollectionResource.random(10),
    #lambda: CollectionResource.random(10),
    lambda: IntervalResource((F(0), F(1)))
]

#------------------------------------------------------------ 
# test that the methods work
#------------------------------------------------------------ 
print "\n","=" * 60
print "Algorithms Stress Test"
print "=" * 60,"\n"

for user_factory, cake_factory in zip(us, cs):
    print "-" * 60
    print cake_factory().__class__.__name__
    print "-" * 60
    for algorithm_factory in algorithms:
        print "* %s" % algorithm_factory.__name__
        for size in range(2, iterations):
            size  = 2 # override number of users here
            value = F(1, size)
            cake  = cake_factory()
            users = [user_factory(cake) for _ in range(size)]
            algorithm = algorithm_factory(users, cake)    
            extras, results = None, algorithm.divide()
            if isinstance(results, tuple):
                results, extras = results
            for user, shares in results.items():
                print "  - share for %s: value(%s)" % (str(user), get_total_value(user, shares))
            if extras:
                for k, v in extras.items(): print "  ~", k, v
            print
