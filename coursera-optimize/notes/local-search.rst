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

--------------------------------------------------------------
Warehouse Location
--------------------------------------------------------------

Find which warehouses to open to minimize the fixed and
transportation costs given:

* a set of warehouses `W`, each warehouse with a fixed cost `fw`
* a set of customers `C`
* a transportation cost `t_w,c` from warehouse `w` to customer `c`

This can be modeled as:

* `o_w` - whether the warehouse is open (0/1)
* `a[c]` - the warehouse assigned to customer c
* there are no constraints
* the objective is::
  
    minimize sum(f_w * o_w)_{w : W}
           + sum(t_{a[c], c})_{c : C}

* once the locations have been chosen, the problem becomes easy
* just assign the customer to the nearest warehouse::

    minimize sum(f_w * o_w)_{w : W}
           + sum(min_{w : W, o_w = 1} t_{w,c})_{c : C}

* there are many possibilities of neighborhoods:

  - open and close warehouses based on coin flip for `o_w`
  - open and close warehouses by swapping open and closed

--------------------------------------------------------------
Traveling Salesman Problem
--------------------------------------------------------------

Find a tour of minimal cost visitin each city exactly once
given:

* a set of `C` cities to visit
* a symmetric distance matrix `d` between every two cities

A simple model of this problem is::

    range Cities = 1..n;
    int distance[Cities, Cities] = ...;
    var{int} next[Cities] in Cities;
    minimize
      sum(c in Cities) d[c, next[c]]
    subject to
      circuit(next); # must come back to starting point

The neighborhood for the TSP is a 2-OPT:

* stay feasible, that is always maintain a tour
* select two edges and replace them by other edges
* update the graph to be directed to make a tour

This can be generalized to K-OPT:

* replace the notion of one favorable swap by a search
  of favorable sequences of swaps
* do not search the entire set of sequences, but build one
  incrementally.
* then execute the best subsequence
* the implementation of this is as follows:

  1. choose a vertex `t1` and its edge `x1 = (t1, t2)`
  2. choose an edge `x2 = (t2, t3)` with `d(x2) < d(x1)`
  3. if none exist, restart with another vertex
  4. else we have a solution by removing the edge `(t4, t3)`
     and connecting `(t1, t4)`
  5. compute the cost, but do not connect
  6. instead restart with t1 and its pretended edge `(t1, t4)`
  7. continue extending this sequence until there is no distance
     that is smaller.
  8. Then choose the best sequence.

--------------------------------------------------------------
Graph Coloring
--------------------------------------------------------------

There are two aspects of this problem:

* optimization: reduce the number of colors
* feasibility: two adjacent vertices must be colored differently

How can we combine these two concerns with local search:

* **Sequence of feasibility problems**

  - find an initial solution with k colors (greedy algorithm)
  - remove one color (say `k`)
  - reassign randomlly all k colored vertices with a color in `{1..k-1}`
  - find a feasible solution with `k-1` colors (minimize violations)
  - repeat

* **Staying in the space of solutions**

  - change the color of a vertex (neighborhood)
  - minimize the number of colors
  - changing the color of a vertex doesn't change the number of colors
  - we can use this to guide our search by using color classes
  - `C_i` is the set of vertices colored with `i`
  - use a proxy object as object function; favor large color classes
  - objective: `maximize sum_{i=1..n} (|C_i|^2)`
  - use **Kemp Chains** to exploit the problem structure (richer neighborhoods)
  - uses a bigraph, swap all connected components when you need to swap colors

* **Exploring feasible and infeasible configurations**

  - focus on reducing the number of colors and ensuring feasibility
  - make sure that local optima are feasible
  - use an objective function that balances feasibility and optimality
  - neighborhood: change the color of a vertex
  - a bad edge is an edge whose adjacent vertices have the same color
  - `B_1` is the set of bad edges between vertices colored with `i`
  - the objective functions are:

    * `maximize sum { i=1..n } (|C_i|^2)`  - for the colors
    * `minimize sum { i=1..n } (|B_i|)`    - for the edges
    * `minimize sum { i=1..n } (2*|B_i|*|C_i|) - sum { i=1..n }( |C_i|^2 )`
    * the local minima of the combined objective are legal colorings

--------------------------------------------------------------
Sport Scheduling / Traveling Tournament Problem (TTP)
--------------------------------------------------------------

This problem is defined as follows:

* given `n` teams
* given a matrix `d` of distances between teams
* output a double round robin schedule with:

  - every team meets every other twice: home and away
  - atmost constant: no more than three consecutive games at home or away
  - no repeat constraint: `a @ b` cannot be followed by `b @ a`
  - minimize the total travel distance (huge)
  - hard to solve with constaint programming, local search is better

* the search neighborhood is:

  - swap homes  - swap two teams home / away schedule
  - swap rounds - swap two week schedules
  - swap teams  - swap the team schedule of two teams (except against each other)
    this also requires that you update the opponents (big move)
  - partial swap rounds - swap a piece of two teams rounds   (y-axis)
    this also requires the connected schedules to be udpated (graph)
  - partial swap teams  - swap a piece of two teams schedule (x-axis)
    this also requires that the play twice rule is maintained
    this may also require a propigation of the connected schedules
  - this is represented as a matrix like::

    ..| w1 w2 w3 w4
    ---------------
    t1|  2 @3 @4 @2
    t2| @1 @4  3  1
    t3| @4  1 @2  4
    t4|  3  2  1 @3

    wn = the round week of the schedule
    tn = the team who is being scheduled
     n = tk plays a home game against n
    @n = tk plays an away game against n

Random walks are very useful in choosing which swaps to perform.

--------------------------------------------------------------
Escaping Local Minima
--------------------------------------------------------------

A configuration `c` is a local minima with respect to a
neighborhood `N` if: `\all { n in N(c) } : f(n) >= f(c)`. This
means that any local move away from this configuration cannot
provide a better solution. This value does not gurantee a
globally optimal solution and escaping this local minima is
a critical issue in local search.

A neighborhood `N` is connected if from every configuration `S`,
some optimal solution `O` can be reached by a sequence of moves:

* `S = s0 -> s1 -> s2 -> ... -> sn = O`
* `s_i in N(s_i-1)`
* otherwise depending where we start, we cannot get to the optimal
* we cannot gurantee that we will get there, just that we can
* a greedy search will fail commonly
* if we can represent as a sequence, we have a few ways to escape

  - we can swap entries in the sequence
  - we can reverse subsequnces

--------------------------------------------------------------
Searching Local Neighborhoods
--------------------------------------------------------------

In local search, we have states where are either solutions or
configurations. We search by moving from state `s` to one of
its neighbors using `N(s)` to generate the neighbors of `s`.
We can filter these neighbors with `L(N(s), s)` to only return
legal neighbors. Then we select one of the legal neighbors with
a selection function `S(L(N(s), s), s)`. Usually this search
involves minimizing an objective function `f(s)`.

.. code-block:: python

    def local_search(f, N, L, S):
        '''
        :param f: The optimization function
        :param N: The neighbor generator
        :param L: The legality predicate
        :param S: The selection function
        '''
        possible = initial_solution()  // possibly greedy
        optimal  = possible            // save the best solution
        for k in range(1 to MaxTrials):
            if satisfiable(possible) and f(possible) < f(optimal):
                optimal = possible
            possible = S(L(N(possible), possible), possible)
        return optimal

The following are possible legal neighbor functions:

* selection (greedy)   : `S(L, s) = arg-min(n in L) f(n)`
* local improvement    : `L(N, s) = {n in N | f(n) <  f(s) }`
* no degradation       : `L(N, s) = {n in N | f(n) <= f(s) }`
* possible degradation : `L(N, s) = N` - this selects everything

The following are possible selection functions:

* **best neighbor** - select the "best" neighbor; randomization is useful

.. code-block:: python

    def best_neighbor(N, s):
        ''' Computes the set of best neighbors and chooses
        one of them randomly.
        '''
        optimals = [n for n in N if f(n) < f(s)]
        return random.select(optimals)

    def best_improvement(s):
        return local_search(f, N, local_improvement, best_neighbor)

* **first neighbor** - select the first "legal" neighbor

.. code-block:: python

    def first_neighbor(N, s):
        ''' This avoids scanning the entire neighborhood.
        by just choosing the first neighbor.
        '''
        optimals = sorted(N) # say lexigraphically
        return optimals[0]

    def first_improvement(s):
        return local_search(f, N, local_improvement, first_neighbor)

* **multi-stage** - select one part and then select the remaining part

  - this avoids scanning the entire neighborhood
  - however, it still maintains a greedy flavor
  - one example is  max/min-conflict:

    1. select the variable with the most violations (greedy)
    2. select the value with fewest resulting violations (greedy)

  - another example is min-conflict heuristic:

    1. randomly select a variable with some violations (random)
    2. select the value with the fewest resulting violations (greedy)

* **random walks** - select a neighbor at random and decide if it
  should be accepted or not:

.. code-block:: python

    def random_improvment(N, s):
        ''' Randomly choose a solution and if it is better
        than our current solution, we use it.
        '''
        n = random.select(N)
        return n if f(n) < f(s) else s

    def metropolis_algorithm(N, s):
        pass

**Heuristics** are used to choose the next neighbor. To guide this
selection, it uses only local information (the state `s` and
its neighbors) and works to drive the search towards a local
minimum.

**Metaheuristics** aim at escaping local minima. It works to drive
the search towards a global minima and typically does this using
some memory or learned informatin.

--------------------------------------------------------------
VIDEO 4-8
--------------------------------------------------------------
