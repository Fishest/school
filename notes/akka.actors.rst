================================================================================
Akka Actors
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Akka is an implementation of the actor model on the JVM. It can be used from
scala or with regular java (and by extension other languages on the JVM). As
of scala 2.10, akka is the default implementation of the actor model in scala.
An actor is a container for state, behavior, a mailbox, children, and a
supervision strategy; all of which is contained in an `ActorReference`.

The actor model specifies the following:

1. Actors are independent units that receive work from their mailbox
2. Actors can only communicate with each other via sending messages to each
   other's mailbox
3. Messages are received one at a time in some order (time dependent FIFO by
   default, but can be switched to say priority)
4. Actors can start, stop, restart, and become new actors

When designing an actor system, the actors should be organized into a natural
hierarchy. This can be easily be seen by a task that needs to be split into
smaller more manageable pieces. The top level task will create N child actors
to handle each smaller piece of work. The parent is now the supervisor of the
children it created and has the responsibility of managing their state. When the
child receives an error or a message it cannot handle, it can send it up the
chain to the parent who can make a better decision.

Don't worry about the number of actors (millions) as each actor is only 300
bytes. Just worry about the system and the messages.

.. notes::

   Unbounded indeterminism are key attributes of concurrent programming.
   In a pure actor system (erlang) every object is an actor.
   Original OO was objects communicating via messaging.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Few Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. If an actor is managing another (by passing sub-tasks), then it should manage
   that child as it knows the probable errors and how to handle them.
2. If a message is deemed important, then an actor may need to create an actor
   for each message and handle errors for that message so it is not lost (this
   is the error kernel pattern).
3. If one actor has another as a dependency, it should watch the liveness of
   the dependency (this is not supervision).

Actors can also be used as configuration containers: logging, configuration,
scheduling, etc. This removes shared state and can make the communication
transparent (locally or distributed).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Best Practices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Actors should behave nicely, process events and generate response in an
   event driven manner, not passively block (thread, socket, resource). In
   this case, a special thread should perform this action and send messages to
   the actor in question.
2. Message should always be immutable
3. Actors are containers for behavior and state. Do not send closures or mutable
   state in messages.
4. Create top-level actors sparingly and prefer truely hierarchical systems.

--------------------------------------------------------------------------------
Modules
--------------------------------------------------------------------------------

There are a modules that integrate new features and libraries with akka. What
follows are a few of the important ones:

* `akka-actor`

  This is the base library for using local actors on the JVM.

* `akka-remote`

  Allows actors to communicate across remote machines as if they were local
  actors.

* `akka-slf4j`

  Integrates the logging mechanism slf4j into the actor framework and provides
  logging points to easily enable logging of: received messages, kill actions,
  errors, etc.

* `akka-testkit`

  Provides a toolkit for testing actors in unit tests.

* `akka-kernel`

  Provides a simple microkernel for using akka as a mini application server.

* `akka-<storage system>-mailbox`

  Provides a means of making durable messages. The currently available data
  stores are:

page 11: Akka


================================================================================
Akka Documentation
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

The quintessential feature of actor systems is that tasks are split up and
delegated until they become small enough to be handled in one piece. In doing so,
not only is the task itself clearly structured, but the resulting actors can
be reasoned about in terms of which messages they should process, how they should
react normally and how failure should be handled. If one actor does not have
the means for dealing with a certain situation, it sends a corresponding failure
message to its supervisor. General guidelines to this hierarchy are as follows:

* if one actor manages another (by sending sub tasks), it should supervise it,
  this is because it knows what errors may occur and how to handle them.
* if one actor carries very important information that it cannot lose, it should
  let child actors perform dangerous tasks (error kernel pattern).
* if one actor depends on another actor for carrying out its duty, it should watch
  that actors liveness and act upon its termination.

Some best practices for designing correct actor systems:

* Actors should not block on some external entity—which might be a lock, a network
  socket, etc.—unless it is unavoidable.
* Do not pass mutable objects between actors. In order to ensure
* Do not send behaviour with messages (closures)
* Create few top level actors and focus on a correct hierarchy

The following are a collection of solutions to blocking within an actor:

* Do the blocking call in an actor with a dedicated thread pool for this purpose
* Do the blocking call within a future with an upper bound on these calls (memory)
* Do the blocking call within a future on a bounded threadpool
* Dedicate a single thread as a event reactor which then dispatches resulting messages

--------------------------------------------------------------------------------
Actor Supervision
--------------------------------------------------------------------------------

When a subordinate actor detects an error, it suspends itself and its subordinates
and sends a messages to its supervisor signaling a failure. The supervisor then has
four options for how to handle this error:

1. resume the subordinate while keeping the current accumulated state
2. restart the subordinate clearing out its current accumulated state
3. stop the subordinate actor permanently
4. escalate the failure, thus failing itself

The actor system will start at least three default actors:

* `/`
  This is known as the **Root Actor** and is basically the top level catch
  statement for the actor system. At the first sign of a bubbled exception it
  will shutdown the actor system.

* `/user`
  This is known as the **Guardian Actor** and is the parent of all user created
  actors. As such, it is the most interacted with actor. All actors created with
  `system.actorOf` are children of this actor.

* `/system`
  This is known as the **System Guardian** and is used to maintain orderly shutdown
  of system internals like actor logging.

* `/deadLetters`
  This is where all messages sent to stopped or non-existing actors are routed to.

* `/remote`
  This is an artificial path where all remote actor references are kept.

Generally failures for actors fall into three categories:

1. **Systematic** - programming errors for the message(s) being received
2. **Transient**  - failure of some external resource during processing
3. **Corruption** - when the actors internal state has been corrupted

Because of case (3), it is generally better to simply restart the failed
actor with fresh state. Since `ActorRef` allow for a level of indirection,
the rest of the system will continue to function correctly even after a 
newly restarted actor. The actor restart process is as follows:

1. suspend the actor and recursively suspend all its children
2. call the old instance's `preRestart` hook
2a. The default is to send all children `Termination` messages and calling `postStop`
3. wait for all the children to stop (`context.stop(child)`)
4. create a new actor using the original provided factory again
5. invoke `postRestart` on the new instance
5a. The default is to call `preStart`
6. send restart requests to all the children which were not killed
6a. The children will recursively follow the same process from step (2)
7. resume the actor

Any actor may also monitor another actor. Unlike supervision which is allowed
from a parent and child relationship, a managing actor can only see if another
actor is alive or dead by listening for a `Terminated` message (the default
behavior if it is not called is to throw a `DeathPactException`):

.. code-block:: scala

    context.watch(actorRef)   // to start monitoring
    context.unwatch(actorRef) // to stop monitoring

There are two supervision strategies that can be used by a parent:

1. `OneForOneStrategy` - only terminate the failing child on a failure
1. `AllForOneStrategy` - terminate all the children on a failure from any child


--------------------------------------------------------------------------------
Actor References
--------------------------------------------------------------------------------

An `ActorReference` is a subtype of an `ActorRef` whose purpose is to send
messages to the actor it represents. Each actor has a reference to itself through
the `self` field and the sender of the current message throught the `sender` fields.
There are a number of references for local, in process, remote, promise, etc actors.

.. image:: images/actor-path.png
   :target: http://doc.akka.io/docs/akka/2.3.3/general/addressing.html
   :align: center

Actors are represented using a hierarchical filesystem like path where deeper paths
represent childern of the previous parents. The difference between an actor path
and an actor reference is that the reference points to an existing actor while a path
may not point to an existing actor. An old actor reference to the same path as a new
actor will not be valid to the new actor. What follows are some akka path examples:

.. code-block:: scala

    "akka://my-sys/user/service-a/worker1"                   // purely local
    "akka.tcp://my-sys@host.example.com:5678/user/service-b" // remote tcp
    "akka.udp://my-sys@host.example.com:5678/user/service-b" // remote udp

There are two ways to get references to actors: creating them or looking them up.
Actors have a logical path that points directly to them and a physical path which
can be used to send to remote actors without having to query ahead of time. 

.. code-block:: scala

    ActorSystem.actorOf  // to create an initial actor
    ActorContext.actorOf // to create an child actor from the existing actor
    ActorSystem.actorSelection // to lookup an actor in the registry
    ActorContext.actorSelection // to lookup an actor starting at the current hierarchy

    context.actorSelection("..")           ! parentMessage
    context.actorSelection("../brother")   ! siblingMessage
    context.actorSelection("../\*")        ! allSiblingsMessage
    context.actorSelection("/user/cousin") ! cousinMessage

.. note:: To get all the siblings in a wild card lookup, one will need to send
   a message to all discovered actors, listen to response messages, and then
   store the resulting sender values in a collection.

.. image:: images/actor-remote-deployment.png
   :target: http://doc.akka.io/docs/akka/2.3.3/general/addressing.html
   :align: center

--------------------------------------------------------------------------------
Location Transparency
--------------------------------------------------------------------------------

page 24
