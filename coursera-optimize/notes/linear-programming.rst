==============================================================
Linear and Integer Programming
==============================================================

--------------------------------------------------------------
Summary and Geometric View
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

A *face* is the intersection of finitely many hyperplanes. Given
`N` dimensions:

* dimension `N - 1` is a facet
* dimension 0 is a vertex
* every point in a polytope is a convex combination of its vertices
* at least one of the points where the objective is minimal is a vertex

Thus to solve a linear program geometrically, simply enumerate all the
vertices and test each one for the optimal value (minimal / maximal).

----------------------------------------------------------------------------------
Algebraic View
----------------------------------------------------------------------------------

The Simplex Algorithm is the method of solving algebraiclly. The goal of the
algorithm is to be "on top of the world:"

1. The top of the world is the top of a mountain
2. The top of the mountain is a beautiful fantastic spot (BFS)
3. You can move from one BFS to a neighboring BFS
4. When you are on top of the world, you know you are there
5. When you are on a BFS, you can move to a higher BFS

Converted away from the ELI5 version: the goal is to solve a linear program:

1. An optimal solution is located at a vertex
2. A vertex is a Basic Feasible Solution (BFS)
3. You can move from one BFS to a neighboring BFS
4. You can detect whether a BFS is optimal
5. From any BFS, you can move to another BFS with a higher / lower cost

To solve a linear program, first represent each of the linear equations in
terms of the others. We then attempt to set the `non-basic-variables` to `0`
and the `basic-variables` to `b`::

    x_1 = b_1 + \sum{i = m + 1} a_1i x_i
    x_m = b_m + \sum{i = m + 1} a_mi x_i
    |           | non-basic variables
    | basic variables

    { x_i = b_i | 1 <= i <= m } U { x_i = 0 | m + 1 <= i <= n }
    feasible if { \forall i \in 1..m : b_i >= 0 }

So to find a solution:

1. Re-express the constraints as equations by adding *slack variables*
2. Select `m` variables (these will be the basic variables)
3. Re-express them in terms of the non-baisc variables only (*Gaussian Elimination*)
4. Check if all the `b` are non-negative

----------------------------------------------------------------------------------
The Simplex Algorithm
----------------------------------------------------------------------------------
