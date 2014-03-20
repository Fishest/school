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
      foralll r(i in R; j in R; i < j) {
        row[i] != row[j];
        row[i] != row[j] + (j - 1);
        row[i] != row[j] - (j - 1);
      }
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
