==============================================================
Constraint Programming
==============================================================

This works by using constraints to reduce the set of values
that each variable can take and then remove those values from
any solution. It can be thought of as a branch and prune
algorithm. It is a method, not a heuristic meaning that if
it is given enough time it will not only find a solution, but
the optimal one.

Then try to convey the structure of the problem as explicitly
as possible (express the substructures of the problem). This
gives the solver as much information as possible. This works
by propigating the constraints forward to reduce the set of
values that can be applied without having to do any searching
or branching (for example, if one variable has only a single
value that it can take). The algorithm then switches between
making a choice, propigating the constraints, and making the
next forced moves. If we arrive at a state with no further
available moves and we are not at a solution, we have to
backtrack and modify an existing choice.

The two key pieces to these algorithms are:

**Pruning**
  Reducing the search space as much as possible. This is done by
  using constraints to remove from the variable domain values that
  cannot belong to a solution.

**Branching**
  Decomposing the problem into subproblems and explore them. We
  then try all possible values for a variable until a solution
  is found or no possible solution exists.

--------------------------------------------------------------
Propigation Engine
--------------------------------------------------------------

The core of the constraint programming solver is the propigation
engine which is a simple fixed point algorithm::

    propagate() {
      repeat {
        select a constraint c;
        if c is not feasable given its domain store:
          return failure;
        else: apply the pruning algorithm associated with c;
      } until no constraint can remove a value from its domain;
      return success;
    }

For feasability checking, simply do the following::

  D(x) = { 0, 1, 2 } # given the domain set for x
  D(y) = { 1, 2, 3 } # given the domain set for y
  |D(x) u D(y)| >= 2 # does their union contain at least 2 unique values

To prune a search space::
  D(x) = { 1 }       # given x can only be one value
  D(y) = { 1, 2, 3 } # and that value exists in the domain of y
  D(y) = D(y) - D(x) # prune by taking the set difference

To start searching, first initialize the domain for the variables
to the range of values between their minimum possible value and
maximum possible value (in case of equations).

--------------------------------------------------------------
Linear Constraints Over Integers
--------------------------------------------------------------

Consider the constraint::

    a_1*x_1 + ... + a_n*x_n >= b_1*y_1 + ... + b_m*y_m
    a_i, b_j >= 0 and are constants
    x_i, y_j are varibles with domain of D(x_i), D(y_j)
 
We can define the feasibility test of the current domain as::

    l = a_1 * max(D(x_1)) + ... + a_n * max(D(x_n))
    r = b_1 * min(D(y_1)) + ... + b_m * min(D(y_m))

    if l >= r: there is still a feasible solution
    else: there is no longer a feasible solution

To prune the search space for a given variable (note we need
to stay with integers, hence the ceil and floor)::

    x_i >=  ceil[(r - (l - a_i * max(D(x_i)))) / a_i]
    y_j <= floor[(l - (r - b_j * min(D(y_j)))) / b_j]

--------------------------------------------------------------
Constraints Propigation Modeling Language
--------------------------------------------------------------


--------------------------------------------------------------
Magic Series Problem
--------------------------------------------------------------

Find a number series so that it specifies the number of
occurrences of each digit in the series::

    int n = 5;
    range D = 0..n-1;
    var {int} series[D] in D;

    solve {
      forall (k in D) {
        series[k] = sum(i in D) (series[i] = k);
      }
    }


This is an example of reification which converts a series
into a `0/1` decision variable. Without reification, this
converts roughly into::

    int n = 5;
    range D = 0..n-1;
    var {int} series[D] in D;

    solve {
      forall (k in D) {
        var {int} b[D] in 0..1;
        forall (i in D) {
          booleq(b[i], series[i], k);
        }
        series[k] = sum(i in D) b[i];
      }
    }

    booleq(b, x, v) = (b == 1 and x == v) or (b == 0 and x != v)

--------------------------------------------------------------
Stable Marriage Problem
--------------------------------------------------------------

The rules for the stable marriage problem is defined as:

1. every women provides a ranking of every man
2. every man provides a ranking of every women
3. if wife a prefers another husband over her own, that husband must
   prefer his existing wife b over wife a.
4. if husband a prefers another wife over her own, that wife must
   prefer her existing husband b over husband a.

This can be modeled as follows::

    enum Men { A, B, C, D };
    enum Women { E, F, G, H };

    int wrank[Men, Women]; # wrank[A][E] is man 'A's rank of woman 'E'
    int mrank[Women, Men]; # mrank[E][A] is woman 'E's rank of man 'A'

    var {Women} wife[Men];
    var {Men} husband[Women];

    solve {
      forall (m in Men)
        husband[wife[m]] = m; # a mans wife must be married to him
      forall (w in Women)
        wife[husband[w]] = w; # a women's husband must be married to her
      forall (m in Men, w in Women)
        #  => w prefers her husband to any other man
        wrank[m, w] < wrank[m, wife[m]] => mrank[w, husband[w]] < mrank[w, m]
      forall (w in Women, m in Men)
        #  => m prefers his wife to any other woman
        mrank[w, m] < mrank[w, husband[w]] => wrank[m, wife[m]] < mrank[m, w]
    }

--------------------------------------------------------------
8-Queens Problem
--------------------------------------------------------------

The hard part of solving a constraint problem is figuring out
how to model the problem. Here is one possible model for the
8-queens problem::

    range R = 1..8;
    var {int} for row[R] in R;

    solve {
      forall(i in R; j in R; i < j) {
        row[i] != row[j];
        row[i] != row[j] + (j - 1);
        row[i] != row[j] - (j - 1);
      }
    }

We can make this model stronger using a dual model which will
constrain the rows and the columns::

    range R = 1..8;
    range C = 1..8;

    var {int} for row[R] in R;
    var {int} for col[C] in C;

    solve {
      // this is the row model
      forall(i in R; j in R; i < j) {
        row[i] != row[j];
        row[i] != row[j] + (j - 1);
        row[i] != row[j] - (j - 1);
      }
      // this is the column model
      forall(i in C; j in C; i < j) {
        col[i] != col[j];
        col[i] != col[j] + (j - 1);
        col[i] != col[j] - (j - 1);
      }
      // this binds the two models together
      forall(r in R, c in C)
        (row[c] = r) <=> (col[r] = c);
    }

--------------------------------------------------------------
Map Coloring Problem
--------------------------------------------------------------

It has been proven that any map can be colored with only four
colors. In order to do this with constraint programming, we
have to do the following:

1. choose the decision variables
2. express the constraints in terms of the decision variables 

The decision variables are going to be:

* the color assigned to each country
* the domain of variables is the set of colors that can be assigned
* the constraints are that no adjacent country can have the same color

This can be modeled as follows::

    enum Countries = { Belgium, Denmark, France Germany, Netherlands, Luxemberg };
    enum Colors = { black, yellow, red, blue };
    var {Colors} color[Countries];

    solve {
        color[Belgium] != color[France];
        color[Belgium] != color[Germany];
        color[Belgium] != color[Netherlands];
        color[Belgium] != color[Luxemburg];
        color[Denmark] != color[Germany];
        color[France]  != color[Germany];
        color[France]  != color[Luxemburg];
        color[Germany] != color[Netherlands];
        color[Germany] != color[Luxemburg];
    }
Using global constraints, we can reformulate this as::

    enum Countries = { Belgium, Denmark, France Germany, Netherlands, Luxemberg };
    var {int} color[Countries] in 1..4;
    minimize
      max(c in Countries) color[c]
    subject to {
        color[Belgium] != color[France];
        color[Belgium] != color[Germany];
        color[Belgium] != color[Netherlands];
        color[Belgium] != color[Luxemburg];
        color[Denmark] != color[Germany];
        color[France]  != color[Germany];
        color[France]  != color[Luxemburg];
        color[Germany] != color[Netherlands];
        color[Germany] != color[Luxemburg];
    }

--------------------------------------------------------------
Sudoku Problem
--------------------------------------------------------------

This can be modeled as follows::

    range R = 1..9;
    var{int} s[R,R] in R;
    solve {
      // add constraints on fixed initial values
      forall(i in R)
        alldifferent(all(j in R) s[i,j]);
      forall(j in R)
        alldifferent(all(i in R) s[i,j]);
      forall(i in 0..2,j in 0..2)
        alldifferent(all(r in i*3+1..i*3+3,
                         c in j*3+1..j*3+3) s[i,j]);
    }

--------------------------------------------------------------
Global Constraints
--------------------------------------------------------------

These capture combinatorial substructures that arise in many
applications. They also make modeling easier and more natural.
If we know these, we can give them directly to the solver so
that it doesn't have to discover the constraints on its own.
Once it knows these global constraints, it can use dedicated
algorithms to solve them which can test for feasibility much
quicker. For example::

    // the following constraint (without global constraints)
    range R = 1..R;
    var{int} row[R] in R;
    solve { 
      forall(i in R,j in R: i < j) {
        row[i] != row[j];
        row[i] + i != row[j] + j;
        row[i] - i != row[j] - j;
      }
    }

    // can be defined as (with global constraints)
    range R = 1..R;
    var{int} row[R] in R;
    solve { 
      forall(i in R,j in R: i < j) {
        alldifferent(row);
        alldifferent(all(i in R) row[i] + i);
        alldifferent(all(i in R) row[i] - i);
      }
    }

Table constraints are the simplest global constraint.
It basically makes a table of all legal combinations
of variable assignments. When new constraints are
added, the table can be easily reduced.

--------------------------------------------------------------
Symmetries
--------------------------------------------------------------

Many problems naturally exhibit symmetry in their solutions.
Exploring symmetrical parts of the search space is a waste of
time, so if we can recognize where this is happening, we can
prune half of the search space immediately. There are many kinds
of symmetries, but we will be concerned with the following two:

* **variable symmetry**
* **value symmetry**

--------------------------------------------------------------
Balanced Incomplete Block Designs (BIBD)
--------------------------------------------------------------

This problem is defined as follows:

* Input:  `(v, b, r, k, l)`
* Output: `v` by `b` 0/1 matrix with exactly:

  - `r` ones per row
  - `k` ones per column
  - `l` scalar product value

This can be modeled as follows::

    range Rows = 1..v;
    range Cols = 1..b;
    var{int} m[Rows,Cols] in 0..1;
    solve {
      forall (i in Rows)
        sum(y in Cols) m[i, y] = r;
      forall (j in Cols)
        sum(x in Rows) m[x, j] = k;
      forall (i in Rows, j in Rows: j > 1)
        sum(x in Cols) (m[i,x] & m[j,x]) == 1;
    }

The problem with this solution is that there are a
large number of symmetrical solutions (swap any two
columns or swap any two rows). Therefore, we would like
to break this symmetry. We can do this by imposing an
ordering on the variables by imposing a lexicographic
constraint on the rows (in terms of the base 2 value).
This can be modeled with the addition of the following
two constraints::

    forall (i in 1..v-1)
      lexleq(all(j in Cols) m[i,j], all(j in Cols) m[i+1, j]);
    forall (j in 1..b-1)
      lexleq(all(i in Rows) m[i,j], all(i in Rows) m[i, j+1]);

--------------------------------------------------------------
Scene Allocation Problem
--------------------------------------------------------------

The problem is shooting scenes in a movie and can be defined
as follows:

* an actor plays in some of the scenes
* at most `k` scenes can be shot per day
* each actor is paid by the day
* minimize the total cost

This can be modeled as follows::

    range Scenes = 1..n;
    range Days = 1..m;
    range Actor = ...;
    int fee[Actor] = ...;

    set{Actor} appears[Scene];
    set{int} which[a in Actor] = setof(i in Scenes) member(a, appears[i]);
    var{int} shoot[Scenes] in Days;

    minimize
      sum(a in Actor) sum(d in Days)
        fee[a] * or(s in which[a]) (shoot[s]=d)
    subject to
      atmost(all(i in Days) 5, Days, shoot);

The symmetry in this problem is that the days are interchangeable.
If you swap all the scenes in day 1 with all the scenes in day 2,
you still have a solution. We can break this symmetry by only adding
a new day if no other day can be a solution::

    subject to
      atmost(all(i in Days) 5, Days, shoot);
      scene[1] = 1; // scene 1 is scheduled on day 1
      forall(s in Scenes: s > 1)
        scene[s] <= max(k in 1..s-1) scene[k] + 1

We can also employ this symmetry breaking during the search
phase as follows::

    using {
      while (!bound(shoot)) {
        int eday = max(-1, maxBound(shoot));                 # the current max day
        selectMin(s in Scenes : !shoot[s].bound())
          (shoot[s].getSize(), -sum(a in appears[s]) fee[a]) # dynamic ordering
        tryall(d in 0..eday + 1)                             # existing days, and then a new day
          shoot[s] = d;
      }
    }

--------------------------------------------------------------
Market Split Problem
--------------------------------------------------------------

This problem can be expressed as follows::

    range C = ...;
    range V = ...;
    int w[C,V] = ...;
    int rhs[C];
    var{int} x[V] in 0..1;
    solve {
      forall(c in C)
        sum(v in V) w[c,v] * x[v] = rhs[c]

      // the following unifies all the variables into another constraint
      sum(v in V) (sum(c in C) alpha * w[c,v]) * x[v] = sum(c in C) alpha^2 * rhs[c];
    }

--------------------------------------------------------------
Redundant Constraints
--------------------------------------------------------------

There are a few reasons to add redundant constraints:

1. They are semantically redundant
2. They reduce the search space (computationally significant)
3. They express properties of the solutions not captured by the model
4. They boost the propagation of other constraints
5. They provide a more global view
6. They combine existing constraints
7. They improve communication

We can use this idea to add extra information to the magic series
problem::

    int n = 5;
    range D = 0..n-1;
    var {int} series[D] in D;

    solve {
      forall (k in D)
        series[k] = sum(i in D) (series[i] = k);
      sum(i in D) series[i] = n
    }

A few ways to add redundant constraints are:

1. add a global constraint (say `alldiff`)
2. add a surrogate constraint (merge two constraints)
3. add an implied constraint (extract properties from constraints) 
4. dual modeling (use two different models at once)
 
--------------------------------------------------------------
Car Sequencing Problem
--------------------------------------------------------------

This problem can be expressed as follows::

    range Slots = ...;
    range Configs = ...;
    range Options = ...;
    int demain[Configs] = ...;
    int nbCars = sum(c in Configs) demand[c];
    int lb[Options] - ...;
    int ub[Options] = ...;
    int requires[Options,Config] = ...;
    var{int} line[Slots] in Configs;
    var{int} setup[Options,Slots] in 0..1;

    solve {
      // make sure that the configurations scheduled for
      // the given slots meets the requested demand for
      // each configuration
      forall(c in Configs)
        sum(s in Slots) (line[s] = c) = demand[c];
      // makes sure that the scheduling is correct
      forall(s in Slots, o in Options)
        setup[o, s] = requires[o, line[s]];
      // makes sure the lower bound is produced
      forall(o in Options, s in 1..nbCars-ub[o] + 1)
        sum(j in s..s + ub[o] - 1) setup[o, s] <= lb[o];
      // recursive window constraint of production size
      forall(o in Options, i in 1..demand[o])
        sum(s in 1..nbCars-i*ub[o]) setup[o, s] >= demand[o] - i * lb[o];
    }

--------------------------------------------------------------
Global Constraints
--------------------------------------------------------------

These are examples of pruning with specific algorithms for
various global constraints.

The gold standard for pruning is if value `v` is  in the domain
of variable `x`, then there exists a solution to the constraint
with value `v` assigned to variable `x`. This is referred to as
arc consistency or domain consistency.

For the binary knapsack, we can compute a DP graph using a foward
and backward phase to see what results are feasible.

`all_different` can be solved using a Bipartie graph with the variables
on the left and the values on the right. Edges are then drawn
between values that each variable can possibly be. The solution is
to then find a `matching` for the graph `G=(V,E)` which is a set
of edges in `E` such that no two edges in `E` share a vertex.
A `maximum matching` `M` for a graph `G` is a matching with the
largest number of edges. If `M` doesn't equal the number of
variables, then the solution is not feasible.

To solve this, first find a matching, then improve it until a
solution is found (using alternating paths):

1. start from a free vertex `x`
2. if there is an edge `(x,v)` where `v` is not matched, then
   insert `(x,v)` in the matching.
3. otherwise, take a vertex `v` matched to `y` and remove `(y,v)`
   and add `(x,v)` from the matching and restart at step `2` with
   `y` instead of `x`.

To create an alternating path for the matching, create a directed
graph such that the edges in the matching are from left to right
and edges not in the matching are directed right to left. Once
you land in a free vertex on the right, you are done. So it starts
at a free vertex on the left and ends in another free vertex on
the right. When you find a path, simply reverse the edges and
you have a new matching. To follow the path, simply use DFS.

To see if an assignment is feasible, simply remove an edge and
try to see if you can form a maximum matching. The problem with
this is that you have to do this over and over for each edge. We
can exploit a property by `Berge (1970)` to make this check
easier:

1. Given a matching `M`, create a directed graph with the edge
   direction reversed
2. Search for even alternating paths starting from free vertex `P`
3. Search for all strongly connected components and collect all
   edges belonging to them in `C`
4. Remove all edges not in `M, P, C`
5. These are the pruned infeasible edges

--------------------------------------------------------------
Search in Constraint Programming
--------------------------------------------------------------

The system should use feasibility information for branching.
There are a few heuristics which are used to exploit this:

* **First Fail Priniciple**
  We should try first where we are most likely to fail. Do the
  hard stuff first to create a smaller search tree.

* **Variable / Value Labeling**
  Choose a variable to assign next and choose the value to
  assign. Choose the variable with the smallest domain. The
  variable ordering is dynamic. Next, choose the most
  constrained variable (say order by middle of board).
  For choosing values, choose the value that leaves as many
  options as possible for the other variables.

.. code-block:: text

    using {
      forall(r in R)
        // order iteration first by remaining slots
        // then by the row distance from the board center
        by row[r].getSize(), abs(r-n/2)
        ...
    }

* **Value / Variable Labeling**
  Choose the value to assign next and then choose the variable
  to assign this value. This is useful when you know that value
  must be assigned such as in scheduling and resource allocation
  problems.

* **Domain Splitting**
  Choose a variable and split its domain in two or more sets.
  Then assign either the top or bottom set to the variable.
  This produces a much weaker commitment to the label.

* **Symmetry Breaking During Search**
  These are the same constraints that are specified in the model,
  but during the search phase.

* **Randomization and Restarts**
  Sometimes there is no obvious search ordering, but there is one
  that is just hard to find. We can brute force to find this
  ordering and if we cannot find a solution in a given time,
  randomize and then restart.

* **Focusing on the Objective**

We search by pruning until we have to make a choice. We then
make a choice and continue until a constraint fails. The solver
then goes back to the last `tryall` and assigns a value that
has not been tried before. If no such value is left, the system
backtracks to an earlier non-deterministic instruction.

To search in a CP program, we can again model the 8-queens
problem::

    range R = 1..8;
    var {int} for row[R] in R;

    solve {
      forall(i in R; j in R; i < j) {
        row[i] != row[j];
        row[i] != row[j] + (j - 1);
        row[i] != row[j] - (j - 1);
      }
    }
    using {
      forall(r in R)   // unrolls to |R| tryall statements
        tryall(v in R) // unrolls to trying each value for r
          row[r] = v;  // add a new constraint to the store
    }

--------------------------------------------------------------
Euler Knight Problem
--------------------------------------------------------------

This problem can be expressed as follows::

    range Board = 1..64;
    var{int} jump[i in Board] in Knightmoves(i);
    solve {
      circuit(jump);
    }

Start in the corners first (they have the least number of
moves).

--------------------------------------------------------------
Generalized Quadratic Assignment Problem
--------------------------------------------------------------

This problem can be expressed as follows:

* `f` - the communication frequency matrix
* `h` - the distance matrix (hops)
* `x` - the assignment vector (decision variables)
* `C` - the sets of components
* `Sep` - separation constraints
* `Col` - colocation constraints

This can be modeled as follows::

    minimize // the objective function
      sum(a in C,b in C: a != b) f[a,v]*h[x[a],x[b]]
    subject to {
      forall(S in Col, c1 in S, c2 in S: c1 < c2)
        x[c1] = x[c2];
      forall(S in Sep)
        alldifferent(all(c in S) x[c]);
    }
    using {
      while (!bound(x))
        selectMax(i in C: !x[i].bound(), j in C) (f[i,j])
          tryall(n in N) by (min(l in x[j].memberOf(l)) h[n, l])
            x[i] = n;
    }

--------------------------------------------------------------
The Perfect Square Problem (value / variable)
--------------------------------------------------------------

This involves taking a number of smaller squares and fitting
them together to form a much larger perfect square without any
gaps. The decision variables are the x,y coordinates of the
bottom left corner of every sub-square. The constraints are
that the squares fit in the larger square and they do not
overlap.

This can be modeled as follows::

    range R = 1..8;
    int s = 122; range Side = 1; range Square 1..21;
    int side[Square] = [
        50, 42, 37, 35, 33, 29, 27, 25, 24,
        19, 18, 17, 16, 15, 11, 9, 8, 7, 6, 4, 2];

    var{int} x{Square} in Side;
    var{int} y{Square} in Side;

    solveall {
      # squares can fit in the bigger square
      forall (i in Square) {      #
        x[i] <= s - side[i] + 1;
        y[i] <= s - side[i] + 1;
      }
      # overlapping constraint
      forall (i in Square, j in Square: i < j) {
             x[i] + side[i] <= x[j]
          || x[j] + side[j] <= x[i]
          || y[i] + side[i] <= y[j]
          || y[j] + side[j] <= y[i];
      }
      # that each line of edges combibines to less than the size
      forall (p in Square) {
        sum(i in Square) side[i] * (x[i] <= p) && (x[i] >= p - side[i] + 1)) = s;
        sum(i in Square) side[i] * (y[i] <= p) && (y[i] >= p - side[i] + 1)) = s;
      }
    } using {
      forall (p in Side)     # choose an x-coordinate
        forall (i in Square) # consider a square i
          try                # decide whether to place i at p
            x[i]  = p;
          | x[i] != p;

      forall (p in Side)
        forall (i in Square)
          try
            y[i]  = p;
          | y[i] != p;
    }

--------------------------------------------------------------
The Magic Square Problem (domain splitting)
--------------------------------------------------------------

The rules for this problem are:

1. all numbers are different
2. all rows, cols, and diagonals sum to the same number

This can be modeled as follows::

    range R = 1..n;
    range D = 1..n^2;
    int T = n*(n^2 + 1) / 2;
    var{int} s[R, R] in D;
    solve {
      forall (i in R) {
        sum(j in R) s[i, j] = T;
        sum(j in R) s[j, i] = T;
      }
      sum (i in R) s[i,i] = T;
      sum (i in R) s[i,n - i + 1] = T;
      alldifferent(all(i in R, j in R) s[i,j]);
    } using {
      timeLimit = 10;
      repeat {
        limitTime(timeLimit) {
          var{int}[] x = all(i in R, j in R) s[i, j];
          range V = x.getRange();
          while (!bound(x)) {
            selectMin[3](i in V:!x[i].bound())(x[i].getSize()) {
              int mid = (x[i].getMin() + x[i].getMax()) / 2;
              try x[i] <= mid | x[i]  > mid;
            }
          }
        } onFailure {
          timeLimit = 1.1 * timeLimit;
        }
      }
    }

Randomization and restarts proves to be helpful here:

1. apply a heuristic, but with randomization
2. run the search for a certain amount of time
3. if the limit is reached, restart and increase the limit
