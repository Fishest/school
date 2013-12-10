import akka.actor.Actor
import akka.actor.Props
import akka.event.LoggingReceive

//------------------------------------------------------------
// Video 1: Failure Handling with Actors
//------------------------------------------------------------

/**
 * How are errors handled in an actor system:
 * - reify as a message
 * - send the message back to the sending actor or a known address
 *
 * The actor model is anthropomorphic
 * - Actors work in teams (systems)
 * - individual failure is handled by the team leader
 */

/**
 * Resiliance demands containment and delegation of failure:
 * - failed actor is terminated or restarted
 * - decision must be taken by one other actor
 * - supervised actors form a tree structure
 * - the supervisor needs to create its subordinate
 */
class Manager extends Actor {

  override val supervisorStrategy = OneForOneStrategy() {
    case _: DbException          => Restart // reconnect to the database
    case _: ActorKilledException => Stop    // actor ! kill
    case _: ServiceDownException => Escalate
  }

  context.actorOf(Props[DbActor], "database")
  context.actorOf(Props[ServiceActor], "service")
}

/**
 * We can also do any kind of processing we would like in the supervisor
 * handling strategy, like a restart count.
 */
class RestartManager extends Actor {

  var restarts = Map.empty[ActorRef, Int].withDefaultValue(0)
  override val supervisorStrategy = OneForOneStrategy() {
    case _: DbException          => restarts(sender) match {
      case toomany if toomany > 10 => restarts -= sender; Stop
      case n => restarts = restarts.updated(sender, n + 1); Restart
    }
  }

  context.actorOf(Props[DbActor], "database")
  context.actorOf(Props[ServiceActor], "service")
}

/**
 * The OneForOneStrategy operates on each actor independently.
 * If the manager is supervising a collection of actors that have
 * to live and die together, then you can use AllForOneStrategy:
 * - all actors restart / stop together, not individually
 * - allows a finite number of restarts
 * - allows a finite number of restarts in a time window
 * - if restriction is violated, stop instead of restart
 */
AllForOneStrategy(maxNrOfRestarts = 10, withinTimeRange = 1 minute) {
  case _: DBException => Restart // will become stop after violated restriction
}

/**
 * The actor identity must be stable so that an actor can be restarted.
 * In Akka the ActorRef stays valid after a restart. In Erlang, the name
 * is registered for a current PID (name registry).
 *
 * In the actor model, restarting means:
 * - unexpected error conditions are handled explicity
 * - unexpected error indicates invalidated error state
 * - restarting restores the initial behavior / state
 */

/**
 * The actor lifecycle is as follows:
 * - start, (restart)*, stop
 * - preStart is called after the actor is intially created
 * - preRestart, postRestart are called after an actor is restarted
 * - postStop hook is called after actor is stopped.
 *
 * These hooks can be overriden in the actor implementation to perform
 * tasks like:
 * - disconnect from database, close socket handles, etc
 * - send messages for lifecycle events
 *
 * It should be noted that actor local state cannot be kept across restarts,
 * only external state can be managed like this. Also, child actors that were
 * not stopped during restart will be restarted recursively.
 */
trait Actor {
  def preStart(): Unit = {}
  def preRestart(reason: Throwable, message: Option[Any]): Unit = {
    context.children foreach (context.stop(_))
    postStop()
  }
  def postRestart(reason: Throwable): Unit = {
    preStart()
  }
  def postStop(): Unit = {}
}

// We can register an event listener by using the lifecycle events
class Listener(source: ActorRef) extends Actor {
  override def preStart() { source ! RegisterListener(self) }
  override def preRestart(reason: Throwable, message: Option[Any]) { }
  override def postRestart(reason: Throwable) {}
  override def postStop() { source ! UnregisterListener(self) }
}

//------------------------------------------------------------
// Video 2: Lifecycle Monitoring and the Error Cycle
//------------------------------------------------------------

/**
 * The only observable transistion occurs when stopping an actor:
 * - having an ActorRef implies liveness (at some point)
 * - restarts are not externally visible
 * - after stop, there will be no more responses
 *
 * No responses can also be a case of communication failure, so
 * Akka supports Lifecycle Monitoring (DeathWatch):
 * - an actor registers its interest with `context.watch(target)`
 * - it will receieve a Terminated(target) message when the target stops
 * - it will receive no more directy messages from target after that message
 * - indirect messages may still arrive
 */
trait ActorContext {
  def watch(target: ActorRef): ActorRef
  def unwatch(target: ActorRef): ActorRef
}

case class Terminated private[akka] (actor: ActorRef)
  (val existenceConfirmed: Boolean, val addressTerminatd: Boolean)
  extends AutoReceiveMessage with PossiblyHarmful

/**
 * Each actor maintains a list of the actors it created:
 * - the child has been entered when context.actorOf returns
 * - the child has been removed when Terminated is received
 * - an actor name is available iff there is no such child
 *   otherwise trying to create a child with the same name will
 *   throw an exception.
 */
trait ActorContext {
  def children: Iterable[ActorRef]
  def child(name: String): Option[ActorRef]
}

// we can use this list to reformulate our previous controller
class Controller extends Actor with ActorLogging {
  override val supervisorStrategy = OneForOneStrategy(maxNrOfRetries = 5) {
    case _: Exception => SupervisorStrategy.Restart
  }

  def receive = {
    case Check(url, depth) =>
      if (!cache(url) && depth > 0)
        context.watch(contxt.actorOf(getterProps(url, depth - 1)))
      cache += url
    case Terminate(_) =>
      if (context.children.isEmpty) context.parent ! Result(cache)
    case ReceiveTimeout => context.children foreach context.stop
  }
}

// we can also use failure to switch to a backup, say database
class Manager extends Actor {
  def receive = prime()
  def prime(): Receive = {
    val db = context.actorOf(Props[DBActor], "db")
    context.watch(db)
    {
      case Terminated("db") => context.become(backup())
    }
  }
  def backup(): Receive = {}
}

/**
 * Keep important data near the root and delegate risk to the leaves:
 * - restarts are recursive (supervised actors are part of the state)
 * - restarts are more frequent at the leaves
 * - avoid restarting actors with important state
 */

/**
 * One can use the EventStream to implement topic based messaging. Actors
 * can send messages to unknown recipients and actors can subscribe to
 * any parts of the EventStream.
 */
trait EventStream {
  def subscribe(subscriber: ActorRef, topic: Class[_]): Boolean
  def unsubscribe(subscriber: ActorRef, topic: Class[_]): Boolean
  def unsubscribe(subsriber: ActorRef): Unit
  def publish(event: AnyRef): Unit
}

// And to implement a log message listener
class Listener extends Actor {
  context.system.eventStream.subscribe(self, classOf[LogEvent])
  def receive = {
    case e: LogEvent => ...
  }
  override def postStop(): Unit = {
    context.system.eventStream.unsubscribe(self)
  }
}

/**
 * Since Actor.Receive is a partial function, not all messages may
 * apply. As such, unhandled messages are sent to the unhandled method.
 * All watchers will sign the death pact so that they will all die together.
 */
trait Actor {
  def unhandled(message: Any): Unit = message match {
    case Terminated(target) => throw new DeathPatchException(target)
    case msg => context.system.eventStream.publish(UnhanldedMessage(msg, sender, self))


  }
}

//------------------------------------------------------------
// Video 3: Persistant Actor State
//------------------------------------------------------------

/**
 * Actors representing a stateful resource:
 * - shall not lose important state due to system failure
 * - must persiste important state as needed
 * - must recover state at (re)start
 *
 * There are two possibilities for persisting state:
 * - in-place updates (database, file replace, etc)
 * - persist changes in append-only fashion (journal)
 *
 * The benefits of persisting the current state is:
 * - the state can be loaded in constant time
 * - data volume depends on the number of records, not their change rate
 *
 * The benefits of persisting changes:
 * - history can be replayed, audited, or restored
 * - some processing errors can be corrected retroactively
 * - additional insight can be gained on a business process
 * - writing an IO stream optimizes bandwidth
 * - changes are immutable and can be freely replicated
 * - immutable snapshots can be used to bound recovery time
 */

/**
 * Command Sourcing (with Channels):
 * - persist the command before procesing
 * - persiste the acknowledgement when processed
 *
 * During Recovery:
 * - all command are replayed to recover state (rebuild state from start)
 * - a persistent channel discards messages already seen by other actors
 */

/**
 * Event Sourcing:
 * - generate change request (events) instead of modify local state
 * - persist and apply them
 * 
 * A command describes something that will happen, an event describes
 * something that happend sometime in the past.
 *
 * During Recovery:
 * - simply replay the event log to the actor
 *
 * When to apply events:
 * - applying after persisting leaves the actor in a stale state
 * - applying before persisting relies on regenerating during replay
 * - can degrade performance by blocking messages until the event is persisted
 */
sealed trait Event
case class PostCreated(text: String) extends Event
case object QuotaReached extends Event

case class State(posts: Vector[String], disabled: Boolean) {
  def updated(e: event): State = e match {
    case PostCreated(text) => copy(posts = posts :+ text)
    case QuotaReached      => copy(disabled = true)
  }
}

class UserProcessor extends Actor {
  var state = State(Vector.empty, false)
  def receive = {
    case NewPost(text) =>
      if (!state.disabled) emit(PostCreated(text), QuotaReached)
    case e: Event => state = state.updated(e)
  }
  def emit(events: Event*) = ... // send to the event log
}

/**
 * We can buffer messages while the state is in flux using the
 * stash trait.
 *
 * Persisting the event and persisting that it was done cannot be
 * atomic:
 * - perform it before persisting for at-least-once semantics (may happen many times)
 * - perform it after persisting for at-most-once semantics (may not happen)
 */
class UserProcessor extends Actor with Stash {
  var state: State = ...
  def receive = {
    case NewPost(text) if !state.disabled =>
      emit(PostCreated(text), QuotaReached)
      context.become(waiting(2), discardOld = false)
  }

  def waiting(n: Int): Receive = {
    case e: Event => 
      state = state.updated(e)
      if (n == 1) { context.unbecome(); unstashAll() }
      else context.become(waiting(n - 1))
    case _ => stash()
  }
}
