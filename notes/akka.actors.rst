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

Akka succeeds where other remoting protocols before have failed as it was
designed from the start to work remotely and deal with the consequences of this
up front:

* all message must be serializable (including closure actor factories)
* all communication must be asynchronous as message can be quick or slow
* all transports are controlled by configuration, the api does not change
* all actor communication is symmetric (a -> b and b -> a)
* there are no actors that just accepts and no actors that only connect
* parallel actors can be created just by specifying `withRouter`

--------------------------------------------------------------------------------
Akka and the Java Memory Model
--------------------------------------------------------------------------------

Akka guarantees the two following rules:

* **The Actor Send Rule**
  The send of the message to an actor happens before the receive of that message
  by the same actor.

* **The Actor Subsequent Processing Rule**
  Processing of one message happens before processing of the next message by the
  same actor. In short this means that changes to internal fields are visible
  when the next message is processed even without `volatile`.

In terms of futures, the general rules to follow are:

* only close over final variables or fields
* otherwise mark the fields as volatile to observe changes
* if you close over a reference, make sure it is thread safe
* avoid locking as it will affect the actor system performance
* do not close over local actor state (like sender) and expose it to other threads

Akka also offers a software transactional memory (STM) implementation that
offers the following rule:

* **The Transactional Reference Rule**
  A successful write during commit, on an transactional reference, happens
  before every subsequent read of the same transactional reference

In short, make as much as possible immutable (messages and state) and you will
simply avoid a number of issues.

--------------------------------------------------------------------------------
Message Delivery Reliability
--------------------------------------------------------------------------------

The rules for message sends are as follows:

* at-most-once delivery, i.e. no guaranteed delivery
* message ordering per sender–receiver pair

It should be noted that there are three general categories of message delivery
that are supported by messaging systems:

* **At Most Once Delivery**
  This means that for each message handed to the mechanism, that message is
  delivered zero or one times; in more casual terms it means that messages may
  be lost.

* **At Least Once Delivery**
  This means that for each message handed to the mechanism potentially multiple
  attempts are made at delivering it, such that at least one succeeds; again,
  in more casual terms this means that messages may be duplicated but not lost.

* **Exactly Once Delivery**
  This means that for each message handed to the mechanism exactly one delivery
  is made to the recipient so the message can neither be lost nor duplicated.

Akka can enable `Ack / Retry` messaging protocols by using channels along with
message persistance. By including a unique identifier (guid) with each message
and tracking it in the business layer. An alternative to this would be to make
the business layer idempotent based on the operation or the tracking number.
Another method of enabling this is by using event sourcing along with akka
persistance. Finally, one can implement a custom mailbox to enable acking at
that level.

--------------------------------------------------------------------------------
Dead Letter Queues
--------------------------------------------------------------------------------

Messages that cannot be delivered will be sent to the synthetic actor at the
`/deadLetters` path. It should be noted that this is a best effort delivery and
mail even fail within a local JVM. The dead letter actor can be used to log
messages that fail to arrive to actors. To receive the dead letters, simply
subscribe to `akka.actor.DeadLetter` on the event stream. The actor will then
receive all local messages sent to the dead letter queue (not over the network).
To receive all the messages from remote systems, an actor must receive from
each machine and then route to a single endpoint.

--------------------------------------------------------------------------------
Akka Configuration
--------------------------------------------------------------------------------

Akka is configured using the TypeSafe config library which is implemented in
java with no dependencies. The configuration allows one to tune all portions
of the actor system including:

* logging level and logging backend
* enabling message remoting
* customer message serializers
* definition of routers
* tuning of various dispatchers

All the configuration is stored in instances of the `ActorSystem`. it can be
configured as follows:

.. code-block:: scala

    val config = ConfigFactory.load()
    val system = ActorSystem("application", config)

    // is equivalent to the following
    val system = ActorSystem.create()

    // to print out the current settings
    System.out.prinln(system.settings());

    // to configure multiple actor systems
    val config  = ConfigFactory.load()
    val system1 = ActorSystem("app1", config.getConfig("app1").withFalback(config))
    val system2 = ActorSystem("app2", config.getConfig("app2").withFalback(config))

By default the configuration is read from the root of the classpath at the
following files in order:

1. `application.conf`
2. `application.json`
3. `application.properties`
4. `reference.conf` - if you are writing an akka library

The default configuration file can be changed using the property
`-Dconfig.resource=/<new-name.conf>`. What follows is an example
akka configuration file:

.. code-block:: text

    # to include another file, like development.conf
    include "development"

    akka {
      # Loggers to register (akka.event.Logging$DefaultLogger logs to STDOUT)
      loggers = ["akka.event.slf4j.Slf4jLogger"]

      # Log levelOptions: OFF, ERROR, WARNING, INFO, DEBUG
      loglevel = "DEBUG"

      # Log level for the very basic logger activated during ActorSystem startup.
      # This logger prints the log messages to stdout (System.out).
      # Options: OFF, ERROR, WARNING, INFO, DEBUG
      stdout-loglevel = "DEBUG"

      actor {
        provider = "akka.cluster.ClusterActorRefProvider"
        default-dispatcher {
          # Throughput for default Dispatcher, set to 1 for as fair as possible
          throughput = 10
        }
      }
      remote {
        # The port clients should connect to. Default is 2552.
        netty.tcp.port = 4711
      }
    }

To debug your configuration, simply use the following:

.. code-block:: scala

    import com.typesafe.config._
    val config = ConfigFactor.parseString("a.b=12")
    val string = config.root.render

--------------------------------------------------------------------------------
Actors
--------------------------------------------------------------------------------

To create an actor, simply extend the `Actor` class and implement the `receive`
method which is `PartialFunction[Any, Unit]`:

.. code-block:: scala

    import akka.actor.Actor
    import akka.actor.Props
    import akka.event.Logging

    class SimpleActor(argument: String) extends Actor {
        val log = Logging(context.system, this)

        //
        // If a default handler is not supplied, a message for which
        // there is no partial function will result in a
        // akka.actor.UnhandledMessage(message, sender, recipiient)
        // being published to the event stream.
        //
        def receive = {
          case "test" => log.info("received test")
          case other  => log.info("received unknown message ${other}")
        }
    }

    //
    // Best practice for creating an actor is to provide a factory
    // method in a companion object.
    //
    object SimpleActor {
        def props(argument: String): Props = Props(new SimpleActor(argument0))
    }

In order to create and configure an actor, `Props` are used which are immutable
recipies for creating said actors:

.. code-block:: scala

    val props1 = Props[SimpleActor]                       // cannot supply arguments
    val props2 = Props(new SimpleActor("arguments"))      // only use outside of an actor
    val props3 = Props(classOf[SimpleActor], "arguments") // validates constructor

Using those recipies, we can use the actor system or context to create an actual
actor reference:

.. code-block:: scala

    import akka.actor.ActorSystem

    //
    // Names should be given to actors to help debugging. They must
    // not start with $ and they must be unique (in the full path).
    // So two different parents can have children with the same name.
    //
    val system = ActorSystem("simple-system")
    val parent = system.actorOf(Props[ParentActor], name="parent")

    //
    // The actorOf creates an immutable actorRef that points directly
    // to the given actor. This type is serializable and can be sent
    // over the network to another system.
    //
    class ParentActor extends Actor {
      //
      // The created actor is automatically started asynchronously
      //
      val child = context.actorOf(Props[ChildActor], "argument")
      def receive {}
    }


.. todo
.. image:: images/actor-lifecycle.png
   :target: http://doc.akka.io/docs/akka/2.3.3/general/addressing.html
   :align: center

There are two methods of communicating with actors:

* `!` or `tell` - is a fire and forget message
* `?` or `ask`  - returns a `Future` for a possible reply

The ask pattern leads to examples like the following:

.. code-block:: scala

    import akka.pattern.{ ask, pipe }
    import system.dispatcher // The ExecutionContext that will be used

    case class Result(x: Int, s: String, d: Double)
    case object Request

    //
    // The ask works by creating an internal actor to track the state of
    // the message. The implicit timeout is used to fail the future.
    //
    implicit val timeout = Timeout(5 seconds)   // needed for ‘?‘ below
    val future: Future[Result] = for {
        x <- ask(actorA, Request).mapTo[Int]    // call pattern directly
        s <- (actorB ask Request).mapTo[String] // call by implicit conversion
        d <- (actorC ? Request).mapTo[Double]   // call by symbolic name
    } yield Result(x, s, d)                     // async composition of three futures

    //
    // Using the pipe operation instead of manually installing
    // onComplete handlers prevents closing over local state which
    // will can a failure.
    //
    future pipeTo actorD                        // install an onComplete send to actorD
    pipe(future) to actorD                      // equivalent to above

    //
    // To send a failure response back from the asked actor
    // one must send a akka.actor.Status.Failure(ex)
    // 
    try {
        val result = operation()
        sender() ! result
    } catch {
        case ex: Exception =>
            sender() ! akka.actor.Status.Failure(ex)
            throw ex
    }

The following is an example of the remaining parts of the akka api:

.. code-block:: scala

    //
    // To install a default response actor as the dead letter queue
    //
    var actor = system.deadLetters

    //
    // To send a message to another actor while keeping the original
    // sender, use foward. This is useful for message routers, load
    // balances, and repliators.
    //
    target forward message

    //
    // To get a handle to the original sender of a message, use the
    // sender() method. This can be stored to maintain a reference
    // for later usage.
    //
    case request =>
        sender ! process(request) // by default sender is the deadLetter

    //
    // To get an alert if the actor has not received a message in a
    // defined time period, use the receive timeout. Note, the timeout
    // may trigger and get enqueued behind the next message that
    // arrives to the actor.
    //
    context.setReceiveTimeout(30 milliseconds)

    def receive = {
        case ReceiveTimeout =>
          context.setRecieveTimeout(Duration.Undefined)  // to turn it off
          throw new RuntimeException("receive timed out")
    }

    //
    // An actor can be stopped by calling stop on its context or
    // actorRef. This is asynchronous so the command may return before
    // the actor is actually stopped.
    //
    context.stop()
    actor ! akka.actor.PoisonPill // another way to stop an actor
    actor ! Kill                  // yet another way

Actors can change their recieve loop implemenation on the fly with
`become` and `unbecome`:

.. code-block:: scala

    class HotSwapActor extends Actor {
        import context._

        def angry: Receive = {
            case "foo" => sender() ! "I am already angry?"
            case "bar" => become(happy)
        }

        def happy: Receive = {
            case "bar" => sender() ! "I am already happy :-)"
            case "foo" => become(angry)
        }

        def receive = {
            case "foo" => become(angry)
            case "bar" => become(happy)
        }
    }

Actors can also queue up messages that should be processed later
by using a stash:

.. code-block:: scala

    import akka.actor.Stash

    //
    // The stash is backed by an immutable vector, however
    // it is ephemeral just like the actors mailbox so if 
    // it goes down, so does the stash.
    //
    class ActorWithProtocol extends Actor with Stash {
        def receive = {
            case "open" =>
                unstashAll()
                context.become({
                    case "write" => // do writing...
                    case "close" =>
                        unstashAll()
                        context.unbecome()
                    case message => stash()
                }, discardOld = false) // stack on top instead of replacing
            case message => stash()
        }
    }

Actor implementation can also be chained like mixins to reuse
common receive loops:

.. code-block:: scala

    trait ProducerBehavior { this: Actor =>
        val producerBehavior: Receive = {
            case Produce =>
                sender() ! Give("thing")
        }
    }

    trait ConsumerBehavior { this: Actor with ActorLogging =>
        val consumerBehavior: Receive = {
            case actor: ActorRef =>
                actor ! Produce
            case Give(thing) =>
                log.info("Got a thing! It’s {}", thing)
        }
    }

    class Producer extends Actor with ProducerBehavior {
        def receive = producerBehavior
    }

    class Consumer extends Actor with ActorLogging with ConsumerBehavior {
        def receive = consumerBehavior
    }

    class ProducerConsumer extends Actor
        with ActorLogging
        with ProducerBehavior
        with ConsumerBehavior {

        def receive = producerBehavior orElse consumerBehavior
    }

    // the producer consumer protocol
    case object Produce
    final case class Give(thing: Any)

--------------------------------------------------------------------------------
Initialization Patterns
--------------------------------------------------------------------------------

.. todo:: page 85
