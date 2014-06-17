==============================================================
Linear and Integer Programming
==============================================================

--------------------------------------------------------------
Summary
--------------------------------------------------------------

A linear program can be described by the following model::

    minimize   { c1 * x1 + ... + cn * xn }
    subject to {
      a11 * x1 + ... + a1n * xn <= b1
      am1 * x1 + ... + amn * xn <= bm
    } with {
      all(xi >= 0 for i in 1..n)
    }

Along with the following caveats:

* `n` = variables   - all must be non-negative
* `m` = constraints - must be inequality based constraints
* to mazimize       - `minimize  -{ c1 * x1 + ... + cn * xn }`
* to have a negative variables - replace all `xi` with `xi_p - xi_n`
* to have an equality constraint - use two inequalities
* if your variable takes an integer value - you must use a MIP

A convex set (geometrically) is one where any two points in
the geometric object can be connected with a line whose points
are also in the object: a circle is such a set, a star is not::

    is_a_convex_combination {
      l1 * v1 + ... + ln * vn, for v1...vn
    } subject to {
      l1 + ... + ln = 1
      all(li >= 0 for i in 1..n)
    }

    A set S in R^n is convex if it contains all the convex
    combinations of the points in S.

The following are given without proofs:

* The intersection of convex sets is a convex sets
* A half space is a convex set
* The intersection of a set of half spaces is convex
* It is called a polyhedron unless it is finite it which case
  it is called a polytope.

VIDEO 5.1
    

