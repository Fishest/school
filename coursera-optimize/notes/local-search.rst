==============================================================
Local Search
==============================================================

Works by moving from configuration to configuration by making
small local moves. Thus, it works with a complete assignment
to the decision variables and then modifies them. This differs
from constraint programming which works with partial assignment
and then extends the assignments.

Local search can abstracly be viewed as a graph exploration. In
performing this exploration, it seeks to find a local minima
such that (every new move results in a worse configuration).
This does not gurantee that we will find the global minima::

    \all n \in N(c): f(n) >= f(c)

    c = configuration
    N = neighborhood
    n = neighboring move
    f = optimization function

    f(c) > 0 = an infeasible solution
    f(c) = 0 = a feasible solution (not the optimal)
    f(x) -> 0/1  = a binary constraint
    f(x) -> 0..1 = a degree based constraint

    // the basic kernel of local search can then be
    do {
      I = { n for N(C) | f(n) < f(c) };
      c = select a configuration from I;
    } while (|I| > 0);

Local search can be performed in three different ways:

* **Satisfaction**

   This starts with an infeasable solution and slowly move
   towards a feasible one by changing the assignments. This
   is generally implemented by converting it into an
   optimization problem.
   
   The method is to model how many constraints are violated
   by any configuration and then move towards a configuration
   that minimizes those violations. Moving towards another
   configuration is performed by changing an assignment to a
   local variable. The variable to move/change can be decided
   in many ways, but max/min conflict is a good method.

   This works by choosing a variable that appears in the most
   conflicts and changing it to a value that minimizes its
   violations. In case of ties for max/min, randomly choose
   one of the items to prevent bouncing between movements.

* **Pure Optimization**

   This starts with a suboptimal solution and then refines it
   into the optimal solution.

* **Constrained Optimization**

   There are many variations on this theme.

--------------------------------------------------------------
N-Queens
--------------------------------------------------------------

The constraints for N-Queens can be modeled as the following::

    range R = 1..8;
    var {int} for row[R] in R;
    solve {
      foralll r(i in R; j in R; i < j) {
        row[i] != row[j];
        row[i] != row[j] + (j - 1);
        row[i] != row[j] - (j - 1);
      }
    }

--------------------------------------------------------------
Car Sequencing
--------------------------------------------------------------

The general strategy for solving this problem is to swap
neiboring car configurations to minimize the current number of
violations. So, find a car configuration in violation and swap
it with another one. We so swaps instead of assignments as this
maintains a large number of constraints from the beginning of
the problem that don't have to be checked again (hard constraint
vs soft constraint).


--------------------------------------------------------------
Magic Square
--------------------------------------------------------------

The constraints for a magic square can be modeled as followins::

    range R = 1..n;
    range D = 1..n^2;
    int   T = n * (n^2 - 1) / 2;
    var {int} s[R,R] in D;
    solve {
      foralll (i in R) {
        sum (j in R) s[i, j] = T;
        sum (j in R) s[j, i] = T;
      }
      sum (i in R) s[i, i] = T;
      sum (i in R) s[i, n-i + 1] = T;
      alldifferent(all(i in R, j in R) s[i,j]);
    }

Here the `alldifferent` is the hard constraint while the
inequalities are the soft constraints. We can solve the
hard constraint from the beginning by simply assigning
all the numbers randomly and then swapping until the soft
constraints are met.

If we just use neighboring swaps in this situation, then
we only have 0/1 violations which adds no extra information
to our search and devolves into a purely random walk. So,
for an equation `l = r`, we can use `abs(l - r)` as a 
measure of the violations. This will drive the search
much more efficiently.
