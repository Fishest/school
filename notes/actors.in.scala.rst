================================================================================
Actors in Scala
================================================================================

--------------------------------------------------------------------------------
Chapter 2: Messages All the Way Up
--------------------------------------------------------------------------------

Actosr can only recieve and send messages, so the only way for an actor (who
does not modify its state) to interact with the world is via Continuation
Passing Style (CPS). Usally, the continuation of the message is the original
message sender (which scala includes implicitly), however it can also be a 
child actor that was created. This can be used to create fork/join processing.

Changes in an actor's state are achieved by events which are linearly ordered:

* `initial event`: some startup precursor event
* `arrival event`: represnts a new incoming message (note we never care about
  message sending is because of the asynchrony in the system)
* `activation event`: represents an actor seeing another actor's creation
* `creation event`: represents a newly created actor

The order of events is strict such that an event can only be influenced by
other events that preceded it. This timer ordering is local to each actor
instead of ordered by a global time as in traditional concurrent programming.

Although messages can be lost in the infrastructure (say a receiver crashes),
the actor model assumes that the infrastructure gurantees reliable message
transmission, although the time of delivery may be unknown or unbounded. HA
is genrally achieved with redundancy, replication, and persisted messages.

As an actor can process the messages in its mailbox in any order, it is up
to the developer to ensure the correctness of their program not depending on
any specific message order (however, akka can ensure FIFO delivery and
processing).

.. notes::
   
   * "Laws for Communicating Parallel Processes", Hewitt and Baker
   * Any control structure can be modeled as a sequence of actor events.
   * Generally send messages async, but can be sync with akka

--------------------------------------------------------------------------------
Chapter 3: Scala Actors
--------------------------------------------------------------------------------

page 41: Actors in Scala
