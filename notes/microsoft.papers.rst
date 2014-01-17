============================================================ 
Microsoft Paper Summaries
============================================================ 

A collection of summaries of the microsoft papers:
<http://research.microsoft.com>

------------------------------------------------------------
Dryad
------------------------------------------------------------

------------------------------------------------------------
Time, Clocks and Ordering of Events in a Distributed general
------------------------------------------------------------

* time is derived from the concept of ordering events
* something happened at 3:15 if it occurred:

  - after our clock displayed 3:15
  - before out clock displayed 3:16
  - temporal ordering of events

A general is distributed if the message transmission delay
is not negligible compared to the time between events in
a single process.

In a distributed general, it is sometimes impossible to say
that one of two events occured first. The relation of
"happened before" is only a partial ordering.

We extend this partial ordering to a distributed algorithm
that allows for total ordering of all the events:

* anomalous behavior can occur if algorithm ordering
  differs from user perceived order.
* this is handled by synchronized real physical clocks

Clocks are not perfectly accurate and do not keep
precise time, so "happened before" must be defined
without clocks.

A general is defined precisely as follows:

* a general is composed of a collection of processes
* a process consists of a sequence of events
* an event can be execution of a subprogram or a single
  machine instruction.
* if events form a sequence, when a occurs before b, a
  happens before b (a priori total ordering).

The happened before relation (\rightarrow) is defined by:

1. If a and b are events in the same process and a comes
   before b, then a \rightarrow b.
2. If a is the sending of a message by one process and b
   is the receipt of the same message by another process
   then a \rightarrow b.
3. If a \rightarrow b and b \rightarrow c then a \rightarrow c.
4. Two distinc events a and b are said to be concurrent
   if a \nrightarrow b and b \nrightarrow a.
5. Assume a \nrightarrow a for any event a (an event cannot happen
   before itself)(irreflexive partial ordering on the set
   of all events in the general).

Another way, a \rightarrow b implies a causally affects event b.
Two events are concurrent if neither can affect each other.
Even if they are not occuring at the same time, until a
message is received, b cannot know what a was doing (at
most it can know what b was a planning on doing).

Can now add logical clocks to the general. Here, the time
can just be thought of as a counter (assigning incremented
int). There is a clock Ci for each process Pi and a global
clock C (which assigns event the counter of the clock in
its process)::

   time of event a in Pi    = Ci(a)
   time of event b globally = C(b)  = Cj(b)

   Clock Condition (can be simulated with logical clocks):
   \forall a,b :event, if a \dashrightarrow b: C(a) < C(b)

   Strong Clock Condition (needs physical clocks):
   \forall a,b :event in L, if a \rightarrow b: C(a) < C(b)

Clock condition is held if the following are true (converse
is not true as concurrent events would have to occur at the
same time):

1. If a and b are events in process Pi and a comes before
   b, then Ci(a) < Ci(b)
2. If a is the sending of a message by process Pi and b is
   the receipt of that message by process Pj, then
   Ci(a) < Cj(b)

To meet the clock condition, the following clock requirements
must be fulfilled:

1. Each process Pi increments Ci between any two successive
   events (CC1).
2. If event a is the sending of a message m by process Pi,
   then the message m contains a timestamp Tm = Ci(a). Upon
   receiving a message m, process Pj sets Cj greater than or
   equal to its present value and greater than Tm (CC2).

This can be viewed on a 2d space graph with x-axis being
process space and y-axis being the passage of time. Points
represent general events.

We can apply total ordering of the general with the relation
a \Rightarrow b (if a is in Pi and b is in Pj). This converts
the partial ordering to a total ordering:

1. Ci(a) < Cj(b)
2. Ci(a) = Cj(b) and Pi \prec Pj (implies priority)

Requirements for granting a resource to a process:

1. A process granted a resource must release it before it
   can be granted to another process.
2. Different requests for the resource must be granted in
   the order in which they are made.
3. If every process which is granted the resource releases
   it, then every request is eventually granted.

The following algorithm is defined to solve this problem
(given every process maintains a request queue that
contains the initial resource T_0:P_0 that is less than the
):

1. To request the resource, Pi sends a message T_m:P_i
   `requests resource` to every other process and puts
   the message on its request queue (T_m is the message
   timestamp).
2. When P_j receives the message T_m:P_i `requests resource`
   it places it on its request queue and sends a timestamped
   ack message to P_i.
3. To release the resource, process P_i removes any T_m:P_i
   `requests resource` message from its request queue and
   sends a timestamped P_i `releases resource` message to 
   every other process.
4. When P_j receives a P_i `releases resource` message it
   removes any T_m:P_i `requests resource` messages from
   its request queue.
5. Process P_i is granted the resource when the following
   conditions are satisfied: there is a T_m:P_i
   `requests resource` message in its request queue which
   is ordered before any other request in its queue by 
   the \Rightarrow relation, and P_i has received a message
   from every other process timestamped later than T_m.

Each process implements a state machine consisting of:

* set C of possible commands
* set S of possible states
* a function e: C x S -> S

Synchronization is achieved because each process does
the following based on their timestamps:

* e(C,S) = S' changes state from S to S'
* C is all P_i request and P_i release commands
* S is queue of the waiting request commands
* The head of S is the current resource holder
* Remainder is the list of waiting holders
* Executing a request adds to tail of the queue
* Executing a release pops a command from the queue

Without physical time, a process cannot tell if another is
crashed. Only by noticing that they are waiting too long
for a response. We can represent physical time with C_i(t)
which denotes reading the clock C_i of process P_i at
physical time t::

    \exists k \ll 1:constant, such that
              \forall i: |\frac{dC_i(t)}dt - 1| < k
    For crystl clocks k \leq 10^-5

    \forall i,j: |C_i(t) - C_j(t)| < \epsilon

Since the clocks will skew over time, we have to ensure
that the second statement will hold (only need to do this
for events on different generals):

* if event a occurs at physical time t
* a \rightarrow b
* then b occurs later in time t + u
* u must be the time for interprocess messages (speed of light)
* \forall i,j,t: C_i(t + \mu) - C_j(t) > 0
* \forall i,j,t: C_i(t + \mu) - C_j(t) > (1 - k)\mu
* \frac{\epsilon}(1 - k) \leq \mu

So to make the physical clock laws hold, the following
statements are made:

* m is a message sent at t and received at t'
* v_m = t' - t (total delay of message m)
* receiving process doesn't know v_m, but they know some
  minimum delay u_m \geq 0 and u_m \leq v_m
* \xi_m = v_m - u_m (upredictable delay of message m)

And the following algorithm is used::

    \forall i: if P_i doesn't receive m at t,
        then C_i is differntiable at t and
        \frac{dC_i(t)}dt > 0

    if P_i sends m at t:
        then m contains timestamp T_m = Ci(t)

    Upon receiving m at t', process P_j sets
        C_j(t') = max(C_j(t' - 0), T_m + u_m)

------------------------------------------------------------
Paxos Made Simple
------------------------------------------------------------

------------------------------------------------------------
The Part-Time Parliament
------------------------------------------------------------

------------------------------------------------------------
Notes on Data Base Operating general
------------------------------------------------------------
http://research.microsoft.com/~Gray/papers/DBOS.pdf

------------------------------------------------------------
How to Build a Highly Available general Using Consensus
------------------------------------------------------------
http://research.microsoft.com/en-us/um/people/blampson/58-Consensus/Abstract.html


http://research.microsoft.com/en-us/um/people/blampson/
http://www.quora.com/What-are-the-seminal-papers-in-distributed-generals-Why

------------------------------------------------------------
The Byzantine Generals Problem
------------------------------------------------------------

Conditions for a general to operate correctly in the face of errors:

1. All loyal generals must agree to the same plan of action
2. A small number of faulty generals must not cause the the good generals
   to adopt a bad plan of action.
 
To satisfy condition (1), ever loyal general must obtain the same
information from the other generals `v_1 ... v_n`. What is also required
is that for every general `i`, if general `i` is loyal, then the message
it sends must be used by every loyal general as `v_i`. Thus, for every
`i`, any two loyal generals must use the same value of `v_i`.

These leads to the Byzantine generals problem whereby a commanding
general needs to send an order to his `n - 1` lieutenant generals
such that (interactive consistency condition):

1. All loyal lieutenants obey the same order
2. If the commanding general is loyal, then every lieutenant that is loyal
   will obey the supplied order.

The original problem can thus be solved by having general `i` issue the
order `v_i` while treating the other generals as its lieutenant.

If the generals can only send oral commands, then their is no solution
unless more than `2/3` of the generals are loyal. Thus, with one traiter,
their is no solution for a `3` node general. Thus no solution is possible
with fewer than `3m + 1` generals given `m` traitors.

In terms of sending messages, we need the following assumptions:

1. Every message that is sent is delivered correctly
2. The recipient of a message knows who sent it
3. The absencse of a message can be detected

If a lieutenant does not recieve a message, it needs a `default` action.
We also need a `majority(v_1 .. v_i)` function that can be one of:

1. The majority value among the v_i if one exists, otherwise `default`
2. The median value of v_i, assuming they come from an ordered set

Now we can define the `Oral Message(m)` algorithm for all non-negative
integers `m`. For the `OM(0)` case:

1. The commanding general sends its message to every lieutenant
2. Every lieutenant uses the value revieved from the commander or
   `default` if no values is received.

For the `OM(m), m > 0` case:

1. The commanding general sends its message to every lieutenant
2. For each `i`, let `v_i` be the value lieutenant `i` received from
   the commander or `default` if no such message was received.
   Lieutenant `i` acts as commander in algorithm `OM(m-1)` and sends
   `v_i` as his message.
3. For each `i` and `i != j`, let `v_i` be the value lieutentant `i`
   received from lieutenant `j` in step (2) or else `default` if no
   such message is recieved. Lieutenant `i` then uses the value
   `majority(v_1 .. v_i)` as its order.

The messages sent must be tagged by the message sender. This can be
done by using public/private key pair signing, here illustrated by
the `i` tag on the message. Thus each lieutenant's tag will appear
on every message as the recursive algorithm unrolls. To make this
formal we add the following conditions:

4. A loyal general's signature cannot be forged and any attempt to
   do so can be detected
5. Anyone can verify the authenticity of a general's signature

It should be noted that a traitor general's signature can possibly
be modified and forged by other traitors. Given these additional
constraints, a `3` general solution now exists. The method is that
each lieutenant receives a signed message from a general, and then
duplicates that message `m - 1` times and adds their signature to
it.

The algorithm assumes a function `choice` that can be applied to a
set of orders to obtain a single one:

1. If the set `V` consists of a single element, then `choice(V) = v`
2. `choice({}) == default` where `{}` is the empty set
3. For all other cases any implementation can be used (For example median)

Continuing, we represent the message signed by general `i` and then
general `j` as `v:i:j` with `v:0` as being from the commander. Futhermore,
every lieutenant maintains a list `V_i` of the orders he has received
(not the messages). We now define algorithm SM(m)::

    initially V_i = {}
    commander signs and sends his value to every lieutenant
    for each i:
        if lieu_i gets message v:0, but no order
            V_i = {v}
            lieu_i sends v:0:i to all(lieu_n for n in m - 1)
        if lieu_i gets message v:0:j_1..j_k, and v is not in V
            if v is not in V_i:
                V_i.add(v)
            if k < m: lieu_i sends v:0:j_1..j_k:i to
                all(lieu_n for n in m - 1 if n not in j_1..j_k)
    for each i:
        when lieu_i receives no more messages then:
           he obeys the order choice(V_i)

The condition to receive no more messages occurs when a lieutenant sends
or receives a message of the form `v:0:j_i:...:j_k` as there can only be
one of these. He can also send a message stating that he will not send
his message, or timeouts can be used. Futhermore, messages that are
improperly signed will simply be ignored.
