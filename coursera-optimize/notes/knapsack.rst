==============================================================
Knapsack Problem
==============================================================

--------------------------------------------------------------
Greedy Algorithm
--------------------------------------------------------------

Greedy algorithms are used as a very simple heuristic, but may
not create the optimal solution. Using the heuristic, we will
pick one item at a time. Example greedy algorithms for the
knapsack problem are:

* take the items in order of valuation (ignoring weight)
* take as many items as possible (using lowest weights)
* take items based on value density (value / weight)

There are many greedy algorithms and they will differ depending
on the problem and its parameters. The good thing about these
are that they are quick to implement and are quite fast. This
makes them useful as a baseline for the problem to import upon.

The big problem with these are not guranteed to be quality
solutions and the quality can vary wildly with the input. Also,
the problem feasability must be "easy" to compute.

Going further, we need more advanced solutions that allow us to
prove that they are optimal, provide quality solutions across a
wide range of inputs, and are feasible problems to solve. Examples
of more advanced algorithms are:

* Constraint Programming
* Local Search
* Mixed Integer Programming
* Dynamic Programming

--------------------------------------------------------------
Modeling
--------------------------------------------------------------

The formal model for the knapasck problem is::

  the capcity of the knapsack is K

  for each item i in I:
      weight of i is w_i
      value of i  is v_i

  Find a subset of the items I such that
      the total value is maximized
      the total weight does not exceed K

  x_i represents the selection status of an item
      1 if the item was selected
      0 if the item was not selected

  constraint: sum(x_i * w_i for i in I) <= K
  objective:  sum(x_i * v_i for i in I)
  maximize the objective subject to the constraint

In order to model an optimization problem, we need the following
which describe what should be done not how (note, there may be
many ways to model a given problem):

* decide on the decision variables
* decide on some encoding of these variables
* express the problem constraint in terms of these variables
* they should capture the solution of the problem
* express an objective function that specifies the solution quality

We can now simply enumerate all the solutions using `X_i` giving us
an n-tuple where n = `|X|`. It should be noted that not all of these
solutions are feasible, but the total number of generated entries is
`2^|X|` which is exponential. If `|X| = 50` and it takes 1 millisecond
to check a solution, it will take 1,285,273,866 centuries to compute.

--------------------------------------------------------------
Dynamic Programming
--------------------------------------------------------------

Dynamic programming can be used to find the optimal solution to
the knapsack problem. This is a divide and conquer algorithm
that uses a bottom up approach. Formally::

    O(k, j) = the optimal solution given
      - the knapsack size k 
      - items in the range I[1..j]

The final solution is `O(K, N)` where `N = |I|`:

* assume we know how to solve `O(k, j - 1) for all k in 0..K`
* then using those solutions, add one more item `j`
* if `w_j > k` we simply use the previous max value `O(k, j - 1)`
* if `w_j <= k` This presents two cases:

  1. do not select j, then `O(k, j) = O(k, j - 1)`
  2. do select j, then `O(k, j) = v_j + O(k - w_j, j - 1)`
 
     
The recurrance relation can be defined formally as::

    O(k, j) = max(O(k, j - 1), v_j + O(k - w_j, j - 1)) if w_j <= k
    O(k, j) = O(k, j - 1) otherwise
    O(k, 0) = 0 for all k

We then use this to build up a table of the possible values.
In order to find which items to use, simply start at the bottom
right of the table and do the following:

1. if the value to the left `j-1` is the same value as the current `j`
   this means we did not select this item. Continue with `j-1`
2. if the value is different, this means that we selected this item.
   Include `j` in the result and continue looking up the table
   at `k - (w_j - w_j_1)`

The total complexity is `O(k*n)`. This is exponential with `k` as
we are essentially encoding `k` with `log2(k)` bits. So this is a
psedo-polynomial algorithm that works great for small values of `k`.

--------------------------------------------------------------
Relaxation, Branch, and Bound
--------------------------------------------------------------

Branch and bound does an exaustive search, but tries to restrict
the number of subtrees that are explored. There are two steps:

1. `branching` - split the problem into a number of sub-problems
2. `bounding` - find an optimistic estimation of the solution (max/min)

We find the optimistic estimate by relaxing the problem or some
of its constraints. Then we maintain the current min / max and use
that to decide if we should continue to branch on a given decision.
If we reach a state where we are currently worse than our best
solution, we can simply stop evaluating that branch of the tree.
The relaxations we can make are:

* relax the total weight of the knapsack
* `linear` - we can take a fraction of an item (not just 1/0)

  - order the items by descending `v_i / w_i`
  - select items until the capacity is not exhausted
  - select a fraction of the last item
  - this is close to the greedy solution

We can use this estimate as the best possible value we could
get (an upper bound). And then use this to prune our tree::

    items = [ (45, 5), (48, 8), (35, 3) ]
    root  = { value: 0, weight: 10, estimate: 92 }

                     take(item[0])             # we walk a decision tree of what items to take
                        /   \
            { 45, 5, 92 } : { 0, 10, 77 }      # not taking item0 is less than dominating
            take(item[1])                      # so we only explore the left branch
               /   \
    { _, -3, _ } : { 45, 5, 80 }               # taking item1 exceeds capacity
                   take(item[2])               # so we only take right branch
                       /   \
           { 80, 2, 80 } : { 45, 5, 45 }       # the dominating solution is 80
    

--------------------------------------------------------------
Search Strategies
--------------------------------------------------------------

There are several search strategies that can be used when doing
a branch and bound algorithm.

`Depth first search` prunes when a node estimation is worse
than the best estimate found so far.

`Best First` selects the node with the best estimation (given
a choice of which to expand next). It prunes when all the
remaining nodes are less than the current best estimate.

`Least discrepancy` trusts a greedy heuristic. Assume you have
a very good heuristic; we then explore attempting to avoid
mistakes. Then explore the tree with an increasing numbr of
mistakes; trusting the heuristic less and less (right is
a mistake, left is correct). This then prunes just like
best first search (don't explore branches less than the
current best estimate).

The best way to make a search strategy more efficient is to
find a well formed relaxation. These can be hard to find
and may be problem specific.
