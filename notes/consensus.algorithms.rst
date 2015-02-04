================================================================================
Consensus Algorithms
================================================================================

--------------------------------------------------------------------------------
Raft Consensus Algorithm
--------------------------------------------------------------------------------

The main goals and or differences about RAFT is that:

1. Was designed to be easily understood (decomposed
   leader election, log replication, and safety).
2. Has strong leadership where only leaders issue requests
   and other servers are simply passive.
3. Uses a simple join consensus scheme to track membership
   changes.

Consensus algorithms generally work by employing replicated
state machines where by state machines on a collection of
servers compute identical copies of the same state and can
continue operating even if some of the servers are down.
Examples of these are Zookeeper and Chubby.

Replicated state machines are typically implemented using a
replicated log, as shown in. Each server stores a log
containing a series of commands, which its state machine
executes in order. Each log contains the same commands in
the same order, so each state machine processes the same
sequence of commands. Then, because the state machines are
deterministic, each computes the same state and the same
sequence of outputs.

The consensus module of the server is tasked with reading
new commands, adding them to the log, which is then executed
by the deterministic state machine. It communicates with the
consensus modules on every other server to be sure that the
same commands are received and issued in the correct order.

Raft implements consensus by ﬁrst electing a distinguished
leader, then giving the leader complete responsibility for 
managing the replicated log. The leader accepts log entries
from clients, replicates them on other servers, and tells
servers when it is safe to apply log entries to their state
machines.

The Raft safety property is this: if a leader has applied a 
particular log entry to its state machine (in which case the
results of that command could be visible to clients), then
no other server may apply a different command for the same 
log entry.

--------------------------------------------------------------------------------
Paxos Consensus Algorithm
--------------------------------------------------------------------------------

Paxis is constructed using a "Single Decree" that works as follows:

1. One or more severs prose a value
2. Systems must agree on a single value as chosen
3. Only one value is ever chosen

We can combine multiple instances of the Single Decree together to
agree on a series of values forming the log; this is known as
Multi-Paxos (or Multi Decree).

.. todo:: convert notes

--------------------------------------------------------------------------------
Zookeeper Consensus Algorithm
--------------------------------------------------------------------------------

.. todo:: convert notes
