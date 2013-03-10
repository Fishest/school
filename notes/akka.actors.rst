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
