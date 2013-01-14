============================================================
Week 1
============================================================

A game is composed of players, actions, and payoffs. This is
stated more formally as follows::

    G = (N, A, u)       # game definition
    N = {1 .. n}        # players
    A_i = {a_1 .. a_n}  # action set for player i
    A = A_i x .. x A_n  # action profile for users
    u = (u_1 .. u_n)    # profile of utility functions

    payoff for player i: u_i = A => \real


There are two ways to represent games:

* Normal Form (matrix of payoffs wrt actions)
* Extensive Form (causal tree involving timing and info)

------------------------------------------------------------
Section 1.4
------------------------------------------------------------

Prisoners Dilemma is any game such that c > a > d > b::

       C    D
    C  a,a  b,c
    D  c,b  d,d

    d,d: both defect
    a,a: both work together for optimal
    c,b: one defects for best, other loses

Games of pure competetion have players with exactly
opposed interests (two players)::

    a \eta A, u_1(a) + u_2(a) = c
    
    * for some constant c
    * special case for c zero sum

Matching pennies is a simple version of this (can be
generalized into paper rock scissors for example).

There are also games of cooperation where players have
the exact same interests (all players want the same
outcomes)::

    \all a \eta A, \all i, j: u_i(a) = u_j(a)

Which side of the road should you drive on::

       L    R
    L  1,1  0,0
    R  0,0  1,1

It gets interesting when games combines cooperation
and competetion, for example Battle of the Sexes::

       player_1
   ---------------
       B    F
    B  2,1  0,0
    F  0,0  1,2

------------------------------------------------------------
Section 1.5 - Nash Equilibrium
------------------------------------------------------------

Keynes' Beauty Contest game to predict stock value and time
to exit the market. Want to get out of the market right
before other investors. You must decided what the other
players think about the stock:

* Each player names an integer between 1 and 100
* The player who names the integer closest to 2/3 of the
  average integer wins prize; others get nothing.
* Ties are broken uniformly at random

So what will other players do and what should I do in
response. The best response of all the players is the
Nash Equilibrium:

* I believe that the number will be X
* So I will play 2/3 of X
* Given 1..100, X will be no larger than 67
* So the optimal value should not be larger than (2/3) 67
* This continues with (2/3)^n 67 until the NE is 1 (stable point)

Nash equilibria may initially be played until the players learn
the equilibrium of the system (say a few rounds of play), they
will then learn the ideal play.

The best response given all the other players' responses::

    a* = (a_1..a_i-1, a_1+1..a_n)   # other players' responses
    a  =  (a*, a_i)                 # full set of responses
    a_i* \eta BR(a*)
         \iff \all a_i \eta A_i, u_i(a_i*, a*) \gte u_i(a_i, a*)

Since we cannot know all the responses, we have to use a pure
strategy. So we choose the best for everyone overall. In the
prisoners dilemma, both players defect is the best strategy.
There can sometimes be more than one or none at all (the penny
matching game match and not match).

------------------------------------------------------------
Section 1.9 - Strategies
------------------------------------------------------------

Given a strategy s_i, it can can be one of the following:

* Strictly dominant strategy u_i(s_i) > u(s_i*)
* Weakly dominant strategy   u_i(s_i) \gte u(s_i*)

The best strategy that dominates the others is the dominant
one. If all players play the dominant strategy then the
nash equilibrium will be achieved.

We cannot find the optimal solution as an outside observer
as we don't know all the details. However, can we find some
value o and o' such that o is at least as good for every
other agent as another outcome o' and there is an agent
who strictly prefers o to o'.

This is pareto-optimal solution if there is nothing that
is pareto-dominant to it. Basically states that there
cannot be dominant cycles.

In prisoners dilemma, the nash equilibria is the only
state that is not the pareto-optima.
