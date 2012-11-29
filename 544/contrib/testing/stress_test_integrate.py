#!/usr/bin/env python
from cakery.preference import ContinuousPreference
from cakery.utilities import integrate

#------------------------------------------------------------ 
# settings
#------------------------------------------------------------ 
tolerance  = 0.005  # +/- off of 1 we accept
iterations = 1000   # the number of rounds to run
resolution = 1000   # higher means more precise integration

#------------------------------------------------------------ 
# initialize the test data
#------------------------------------------------------------ 
ps = [ContinuousPreference.random() for _ in range(iterations)]
ls = [integrate(p.function, 0.0, 0.5, resolution) for p in ps]
rs = [integrate(p.function, 0.5, 1.0, resolution) for p in ps]
ss = [l + r for l, r in zip(ls, rs)]

#------------------------------------------------------------ 
# test that the constraints hold
#------------------------------------------------------------ 
print "\n","=" * 60
print "Integration Stress Test"
print "=" * 60,"\n"

for left, right in zip(ls, rs):
    print "left[%f]\t<= right[%f]" % (left, right)
    assert(left != right)
    assert(left > right or left < right)
    assert(1.0 - tolerance < left + right < 1.0 + tolerance)
