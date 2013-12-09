import akka.actor.Actor
import akka.actor.Props
import akka.event.LoggingReceive

//------------------------------------------------------------
// Video 1: Introduction, Why Actors
//------------------------------------------------------------

/**
 * This is a simple threading review
 */

//------------------------------------------------------------
// Video 2: The Actor Model
//------------------------------------------------------------

/**
 * The actor model respresents objects and their interactions,
 * resembling human interaction.  An actor (as defiend by
 * Hewitt):
 *
 * 1. is an object with an identity
 * 2. has a defined behavior
 * 3. only interacts using asynchronous message passing
 */

// an actor receives a message and reacts to it, it does not
// return anything, but may emit more messages
type Receive = PartialFunction[Any, Unit]
trait Actor {
  implicit val context: ActorContext
  implicit val self: ActorRef
  def sender: ActorRef
  def receive: Receive
}

trait ActorContext {
  def become(behavior: Receive, discardOld; Boolean = true): Unit
  def unbecome(): Unit

  /**
   * Actors are created by other actors and stop is
   * usually applied to self so actors usually stop
   * themselves.
   */
  def actorOf(p: Props, name: Sring): ActorRef
  def stop(a: ActorRef): Unit
}

abstract class ActorRef {
  def !(msg: Any)(implicit sender: ActorRef = Actor.noSender): Unit
  def tell(msg: Any, sender: ActorRef) = this.!(msg)(sender)
}

/**
 * A simple counter actor. The `!` operater is defined as the
 * `tell` method and it allows one actor to send a message to
 * another actor that it has a reference to.
 */
class Counter extends Actor {
  var count
  def receive = {
    case "incr" => count += 1
    //case ("get", ref: ActorRef) => ref ! count
    case "get" => sender ! count
  }
}

/**
 * We can also remove the variable state of the actor by
 * becoming a new actor.  This functions similar to an asynchronous
 * tail recursion with the following advantages:
 *
 * 1. state change is explicit
 * 2. state is scoped to the current behavior
 */
class Counter extends Actor {
  def counter(count: Int): Receive = {
    case "incr" => context.become(counter(count + 1))
    case "get"  => sender ! count
  }
  def receive = counter(0)
}

/**
 * An example of using actors in a simple program. It should be
 * noted that the actor model permits the following operations:
 *
 * 1. send messages
 * 2. receive message (state only changes from messages)
 * 3. designate the behavior for the next message
 */
class Main extends Actor {
  val counter = context.actorOf(Props[Counter], "counter")
  counter ! "incr"
  counter ! "incr"
  counter ! "incr"
  counter ! "get"

  def receive = {
    case count: Int => println(s"count was $count")
    context.stop(self)
  }
}

//------------------------------------------------------------
// Video 3: Message Processing Semantics
//------------------------------------------------------------

/**
 * Actors Encapsulate Their State:
 * - no direct access is possible to the actor behavior
 * - only messages can be sent to known addresses (ActorRef)
 * - every actor knows its own address (self)
 * - creating an actor returns its address (ActorRef)
 * - addresses can be sent within messages (sender)
 *
 * Actors are completely independent agents of computation:
 * - local execution, no notion of global synchronization
 * - all actors run fully concurrently
 * - message passing primitive is a one-way communication
 *
 * Actors are effectively single threaded:
 * - message are received sequentially
 * - behavior change is effective before processing the next message
 * - processing one message is the atomic unit of execution
 *
 * Blocking is replaced by enqueueing messages.
 */

// it is good practice to define all the possible messages for
// a given actor in its companion object.
object BankAccount {
  case class Deposit(amount: BigInt)  { require(amount > 0) }
  case class Withdraw(amount: BigInt) { require(amount > 0) }
  case class Done
  case class Fail
}

// then implement the primitive operations
// that match the supplied messages
class BankAcount extends Actor {
  import BankAccount._

  var balance = BigInt(0)
  def receive = {
    case Deposit(amount)  =>
      balance += amount;
      sender ! Done
    case Withdraw(amount) if amount <= balance =>
      balance -= amount;
      sender ! Done
    case _ => sender ! Fail
  }
}

// then define the actor collaborations, possible by
// using more actors.
object WireTransfer {
  case class Transfer(to: ActorRef, from: ActorRef, amount: BigInt)
  case class Done
  case class Fail
}

class WireTransfer extends Actor {
  import WireTransfer._

  def receive = {
    case Transfer(to, from, amount) =>
      from ! BankAccount.Withdraw(amount)
      context.become(awaitWithdraw(to, amount, sender))
  }

  def awaitWithdraw(to: ActorRef, amount: BigInt, client: ActorRef): Receive = {
    case BankAccount.Done =>
      to ! BankAccount.Deposit(amount)
      context.become(awaitDeposit(client))
    case BankAccount.Fail =>
      client ! Fail
      context.stop(self)
  }

  def awaitDeposit(client: ActorRef): Receive = {
    case BankAccount.Done =>
      client ! Done
      context.stop(self)
  }
}

// an example of a top level actor managing transactions
// between different accounts. The degugging of akka can
// be enabled by supplying the vm arguments:
// -Dakka.loglevel=DEBUG          <- enables akka debug logging
// -Dakka.actor.debug.receive=on  <- turns on the receive logging
class TransferMain extends Actor {
  val accountA = context.actorOf(Props[BankAccount], "accountA")
  val accountB = context.actorOf(Props[BankAccount], "accountB")

  accountA ! BankAccount.Deposit(100)

  def receive = LoggingReceive {
    case BankAccount.Done => transfer(150)
  }

  def transfer(amount: BigInt): Unit {
    val transaction = context.actorOf(Props[WireTransfer], "transfer")
    transaction ! WireTransfer.Transfer(accountA, accountB, amount)
    context.become(LoggingReceive {
      case WireTransfer.Done =>
        println("sucess")
        context.stop(self)
      case WireTransfer.Fail =>
        println("failed")
        context.stop(self)
    })
  }
}

/**
 * Message Delivery Gurantees
 * - all communication is inherently unreliable (sync calls, network, etc)
 * - delivery of a message requires eventual availability of a
 *   channel and recipient
 *
 * We can classify the amount of delivery effort and gurantees as follows:
 * - at-most-once: sending once delivers [0, 1] times (no state needed)
 * - at-least-once: resending until ack received [1, inf] times (the sender needs state buffer)
 * - exactly-once: processing only first reception delivers 1 time (needs state on both sides)
 *
 * Message reliability support can be achieved with:
 * - all messages being persisted
 * - all message can include correlation ids (unique)
 * - delivery can be retried until successful
 *
 * Reliability can only be achieved by business-level acknowledgement,
 * knowing that a message has been delivered to the receiving actors
 * queue is not enough.
 *
 * To make the previous system reliable:
 * - the activities of WireTransfer should be persisted to storage
 * - each transfer needs a unique identifier
 * - Withdraw and Deposit need identifiers
 * - The ids of the completed actions must be stored in BankAccount
 */
class BankAccountEx {
  val actions = scala.collection.mutable.Set[String]()
}

/**
 * Message Ordering
 * If we send messages to the same destination, they will not arrive
 * out of order. However, if we send messages to different actors and
 * especially if those actors send out messages as well, we cannot
 * gurantee to ordering of the resulting messages (for this a system
 * will need a higher level protocol). Generally message ordering should
 * not be relied upon.
 */

//------------------------------------------------------------
// Video 4: Designing Actor Systems
//------------------------------------------------------------

/**
 * How could we design an actor based system to check the
 * a page and a depth of links.
 */
class Getter(url: String, depth: Int) extends Actor {
  implicit val exec = context.dispatcher.asInstanceOf[Executor with ExecutionContext]

  // This can be reduced using some helper combinators to
  // the following::
  // WebClient.get(url).pipeTo(self)
  // WebClient get url  pipeTo self
  val future = WebClient.get(url)
  futuer onComplete {
    case Success(body)  => self ! body
    case Failure(error) => self ! Status.Failure(error)
  }

  def receive = {
    case body: String =>
      for (link <- findLinks(body))
        context.parent ! Controller.Check(link, depth)
      stop()
    case _: Status.Failure => stop()
    case Abort => stop()
  }

  // since every actor is created by another actor, we
  // have a back reference to the creating parent.
  def stop(): Unit = {
    context.parent ! Done
    context.stop(self)
  }
}

// here we use mutable variables with immutable sets
// so that we do not leak the cache instance to the
// parent.
class Controller extends Actor with ActorLogging {
  var cache = Set.empty[String]
  var children = Set.empty[ActorRef]

  // this will be reset every time we receive a new message
  context.setReceiveTimeout(10 seconds)
  
  def receive = {
    case Check(url, depth) =>
      log.debug("{} checking {}", depth, url)
      if (!cache(url) && depth > 0)
        children += context.actorOf(Props(new Getter(url, depth - 1)))
      cache += url
    case Getter.Done =>
      children -= sender
      if (children.isEmpty) context.parent Result(cache)
    case ReceiveTimeout => children foreach(_ ! Getter.Abort)
  }
}

/**
 * Logging in akka is performed by dedicated actors. Since the
 * logging message will include the source of the message, it is
 * important to correctly name the working actors.
 */
class A extends Actor with ActorLogging {
  def receive {
    case message => log.debug("received message {}", message)
  }
}

/**
 * Akka supports a timer service optimized for high volume,
 * short duration, and frequent cancellation.
 */
trait Scheduler {
  // also overloads for runnable and scala block
  // there are also the same methos for repeatable timers
  def scheduleOne(delay: FiniteDuration, target: ActorRef, message: Any)
      (implicit exec: ExecutionContext): Cancellable
}

/**
 * Using the scheduler we can schedule a task that will run
 * once overall instead of being reset every time a new message
 * arrives.
 */
class B extends Actor {
  import context.dispatcher
  var children = Set.empty[ActorRef]

  // this is not threadsafe
  context.system.scheduler.scheduleOnce(10 seconds) {
    children.foreach(_ ! Getter.Abort)
  }

  // this is the correct way to stay in the actor system
  context.system.scheduler.scheduleOnce(10 seconds, self, Timeout)
  def receive = {
    case Timeout => children.foreach(_ ! Getter.Abort)
  }
}

/**
 * It is also necessary to make sure futures are used
 * correctly when working with actors
 */
class WebCache extends Actor {
  var cache = Map.empty[String, String]
  def receive = {
    case Get(url) =>
      if (cache contains url) sender ! cache(url)
      else {
        val client = sender // close over value, not by name
        WebClient.get(url) map (Result(client, url, _)) pipeTo self
      }
    case Result(client, url, body) =>
      cache += url -> body
      client ! body
  }
}

/**
 * Some general rules for designing actor systems:
 * - a reactive application is non-blocking and event driven from top to bottom
 * - actors are run by a dispatcher (shared) which can also run futures
 * - prefer immutable data structures since they can be shared
 * - prefer context.become for different data states, with data local to the behavior
 * - do not refer to actor state from code that is running asynchronously
 */
class Receptionist extends Actor {

  case class Job(client: ActorRef, url: String) 
  var reqNo = 0

  def receive = waiting

  val waiting: Receive = {
    case Get(url) => context.become(runNext(Vector(Job(sender, url))))
  }

  def running(queue: Vector[Job]): Receive = {
    case Controller.Result(links) =>
      val job = queue.head
      job.client ! Result(job.url, links)
      context.stop(sender) // stop the controller
      context.become(runNext(queue.tail))
    case Get(url) =>
      context.become(enqueueJob(queue, Job(sender, url)))
  }

  def runNext(queue: Vector[Job]): Receive = {
    reqNo += 1
    if (queue isEmpty) waiting
    else {
      val controller = context.actorOf(Props[Controller], s"c$reqNo")
      controller ! Controller.Check(queue.head.url, 2)
      running(queue)
    }
  }

  def enqueueJob(queue: Vector[Job], job: Job): Receive {
    if (queue.size > 3) {
      sender ! Failed(job.url)
      running(queue)
    } else running(queue :+ job)
    }
  }
}

class Main extends Actor {
  import Receptionist._

  val receptionist = context.actorOf(Props[Receptionist], "receptionist")
  receptionist ! Get("www.google.com")

  context.setReceiveTimeout(10 seconds)

  def receieve = {
    case Result(url, links) =>
      println(links.toVector.sorted.mkString(s"results for $url:\n", "\n", "\n"))
    case Failed(url) =>
      println(s"failed to fetch $url")
    case ReceiveTimeout => 
      context.stop(self)
  }

  override def postStop(): Unit = {
    WebClient.shutdown()
  }
}

//------------------------------------------------------------
// Video 5: Testing Actor Systems
//------------------------------------------------------------

/**
 * We can test using the test probe directly
 */
implicit val system = ActorSystem("TestSys")
val toggle = system.actorOf(Props[Toggle]) // the actor to test
val probe = TestPrope()
probe.send(toggle, "how are you")
probe.expectMessage("happy")
probe.send(toggle, "how are you")
probe.expectMessage("sad")
probe.send(toggle, "unknown")
probe.expectNoMsg(1 second)
system.shutdown()

/**
 * We can also do the same thing without having to use
 * the interceptor
 */
new TestKit(ActorSystem("TestSys")) with ImplicitSender {
  val toggle = system.actorOf(Props[Toggle]) // the actor to test
  toggle ! "how are you"
  expectMessage("happy")
}

/**
 * To test with dependency injection, simply use akka
 * say with Spring. Another method is to override methods
 * in test sub-classes to mock results.
 */

/**
 * We can have parent probes by decorating between
 * a child and its parent with a probe.
 */
class StepParent(child: Props, probe: ActorRef) extends Actor {
  context.actorOf(child, "child")
  def receive = {
    case message => probe.tell(message, sender)
  }
}

class FosterParent(child: Props, probe: ActorRef) extends Actor {
  val child = context.actorOf(child, "child")
  def receive = {
    case message if sender = context.parent =>
      probe forward message
      child forward message
    case message =>
      probe forward message
      context.parent forward message
  }
}

/**
 * To allow for these parents to create a new instance,
 * we have to tell it how to create the supplied actor.
 */
class TestSpec extends TestKit(ActorSystem("TestSys"))
  with WordSpecLike with BeforeAndAfterAll with ImplicitSender {

  class FakeController extends Controller { /* with mocks */ }
  def fakeActor: Props = Props(new Receptionist {
    override def controllerProps = Props[FakeController]
  })

  override def afterAll(): Unit = {
    system.shutdown()
  }

  "a receptionist" must {
    "operate correctly" in {
      val receptionist = system.actorOf(fakeActor, "correct")
      recptionist ! Get("example.com")
      expectMsg(Result("example.com", Set("example.com"))
    }
  }
}
