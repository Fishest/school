import akka.actor.Actor
import akka.actor.Props
import akka.event.LoggingReceive

//------------------------------------------------------------
// Video 1: Actors are Distributed (Ronal Kuhn)
//------------------------------------------------------------

/**
 * When doing distributed actors (involving network) there are
 * a number of things that are impacted:
 * - data can only be shared by value (ipc can use reference)
 * - lower bandwidth (memory vs network)
 * - higher latency
 * - partial failure (syn/ack failure)
 * - possible data corruption
 *
 * Distributed computing breaks assumptions made by a synchronous
 * programming model. Actor programming is asynchronous and one
 * way. Encapsulation makes them look the same weither they are
 * remote or local (designed for the remote case first).
 */

/**
 * The actor hierarchy forms a tree just like a filesystem. All
 * actors are created under the parent system actor. Every actor
 * has a unique path based on a URI:
 * - akka://authority/path        // actorpath
 * - akka://authority/path#123345 // actorref
 * - akka.tcp://authority@1.1.1.1:1234/path
 *
 * An actor name is unique for the given parent.
 * ActorRef points to a single actor (must exist)
 * ActorPath is a full name (may not exist)
 */
import akka.actor.{Identify, ActorIdentity}
case class Resolve(path: ActorPath)
case class Resolved(path: ActorPath, actor: ActorRef)
case class NotResolved(path: ActorPath)

class Resolver extends Actor {
  def receive = {
    case Resolve(path) => context.actorSelection(path) ! Identify((path, sender))
    case ActorIdentity((path, cilent), Some(ref)) => client ! Resolved(path, ref)
    case ActorIdentity((path, cilent), None) => client ! NotResolved(path)
  }

  context.actorSelection("child/grandChild") // lookup a grandchild
  context.actorSelection("../sibling")       // lookup a sibling
  context.actorSelection("/user/app")        // lookup local root
  context.actorSelection("/user/controls/*") // broadcast using wildcards
}

/**
 * A cluster is a set of nodes where all nodes are
 * in agreement about who is in the group, all working
 * on some common task.
 *
 * A single node can declare itself a cluster (join itself).
 * Other nodes cam then join the cluster by sending a join
 * message to any cluster member. Once all the members of
 * the cluster know about the joining node, it becomes a member
 * of the cluster. Communication is done via an epedemic gossip
 * protocol (gossip to N nodes every second).
 *
 * To enable clustering, add the following package:
 * "com.typesafe.akka" %% "akka-cluster" % "2.2.1"
 *
 * Then configure (these can also be set as VM arguments):
 * akka {
 *   actor {
 *     provider = akka.cluster.ClusterActorRefProvider
 *   }
 * }
 */
class ClusterMain extends Actor {
  // this will start a single cluster node on port 2552
  // to have a number of entities using different ports,
  // the following configuration is needed:
  // akka.remove.netty.tcp.port = 0
  val cluster = Cluster(contet.system)
  cluster.subscribe(self, classOf[ClusterEvent.MemberUp])
  cluster.join(cluster.selfAddress)

  def receive = {
    case ClusterEvent.MemberUp(member) =>
      if (member.address != cluster.selfAddress) {
        // a new member joined the cluster
      }
  }
}

class ClusterWorker extends Actor {
  val cluster = Cluster(contet.system)
  val main = cluster.selfAddress.copy(port = Some(2552))
  cluster.subscribe(self, classOf[ClusterEvent.MemberRemoved])
  cluster.join(main)

  def receive = {
    case ClusterEvent.MemberRemoved(member, _) =>
      // the cluster is being shutdown as the main has stopped
      if (member.address == main) context.stop(self)
  }
}

class ClusterReceptionist extends Actor {
  val cluster = Cluster(contet.system)
  cluster.subscribe(self, classOf[ClusterEvent.MemberUp])
  cluster.subscribe(self, classOf[ClusterEvent.MemberRemoved])

  override def postStop(): Unit {
    cluster.unsubscribe(self)
  }

  def receive = awaitingMembers
  def awaitingMembers: Receive = {
    case current: ClusterEvent.CurrentClusterState =>
      val addresses = current.members.toVector map (_.address)
      val notMe = address filter (_ != cluster.selfAddress)
      if (notme.nonEmpty) context.become(active(notMe))
    case MemberUp(member) if (member.address != cluster.selfAddress) =>
      context.become(active(Vector(member.address)))
    case Get(url) => sender ! Failed(url, "no nodes avilable")
  }

  def active(addresses: Vector[Address]): Recieve = {
    case MemberUp(member) if (member.address != cluster.selfAddress) =>
      context.become(active(addresses :+ member.address)))
    case MemberRemoved(member, _) =>
      val next = addresses filterNot(_ == member.address)
      if (next.isEmpty) context.become(awaitingMembers)
      else context.become(active(next))
    case Get(url) if context.children.size < addresses.size =>
      val client = sender
      val address = pick(addresses)
      context.actorOf(Props(new Customer(client, url, address)))
    case Get(url) => sender ! Failed(url, "too many parallel queries")
  }
}

class Customer(client: ActorRef, url: String, node: Address) extends Actor {
  // this changes who the sender of the messages will be set to
  // this is because this is an ephemeral node that should not be accessed
  // from the outside world.
  implicit val s = context.parent
  
  override val supervisionStrategy = SupervisorStrategy.stoppingStrategy
  val props = Props[Controller].withDeploy(Deploy(scope = RemoveScope(node)))
  val controller = context.actorOf(props, "controller")
  context.watch(controller)
  context.setReceiveTimeout(5.seconds)

  controller ! Controller.Check(url, 2)

  def receive = ({ // partial function literal
    case ReceiveTimeout => 
      contet.unwatch(controller)
      client ! Receptionist.Failed(url, "controller timed out")
    case Terminated(_) =>
      client ! ReceptionistFailed(url, "controller died")
    case Controller.Result(links) =>
      contet.unwatch(controller)
      client ! Receptionish.Result(url, links)
  // this applies a single message to the partial literal and then
  // uses the andThen combinator to run the anonymous function
  }: Receive) andThen (_ => context.stop(self))
}

/**
 * Leader election is performed by sorting the list of
 * nodes in the member list and the first entry in the list
 * is the leader (bully)
 */

//------------------------------------------------------------
// Video 2: Actors are Distributed (2)
//------------------------------------------------------------

/**
 * The akka cluster node life-cyle:
 * 1. joining - When a node is created and wants to join the cluster
 * 2. Up      - When a node has joined the cluster
 * 3. Leaving - When a node wants to leave the cluster
 * 4. Exiting - When leader sets leaving node to this
 * 5. Removed - When all nodes know about the exit, node is removed
 *            - When a node becomes unreachable, it transitions to Down
 * 6. Down    - When a node has failed (is a system decision, not a transition)
 *            - When consensus is reached, this transitions to Removed
 *
 * Unreachable is not a state, but more of a flag as it can be restored
 * when the node is reachable again (can become unreachable from any
 * state).
 *
 * Consensus is unabtainable if some members are unreachable. Every
 * node is monitored using heartbeats from several neighbors. If a
 * node is unreachable for one, it is unreachable for all. Nodes can
 * be removed to restore cluster consensus. Node monitoring is done
 * via chord with M connections where M is less than the number of
 * nodes. Heartbeats can be configured, defaults to 5 seconds. Broken
 * links can be restored if message routing is allowed.
 *
 * MemberUp      - Event emitted with transition from (1) to (2)
 * MemberRemoved - Event emitted with transition from (6) to (5) and (4) to (5)
 * There are also other events that can be monitored like MemberUnreachable
 */

/**
 * Actors on nodes which are removed from the cluster must be dead:
 * - allows clean up of remote deployed child actors
 * - decision must be taken consistently within the cluster
 * - once Terminated has been delivered, the actor cannot come back (it must be restarted)
 *
 * Lifecycle monitoring is important for distributed failover:
 * - delivery of Terminated is guranteed (event if sending actor is dead)
 * - This is because the message can be synthesized if needed (created locally)
 * - message must be delivered for cluster health, so is treated specially
 */
class ClusterWorker extends Actor {
  val cluster = Cluster(contet.system)
  val main = cluster.selfAddress.copy(port = Some(2552))
  cluster.subscribe(self, classOf[ClusterEvent.MemberUp])
  cluster.join(main)

  def receive = {
    case ClusterEvent.MemberUp(member) =>
      if (member.address == main) {
        val path = RootActorPath(main) / "user" / "app" / "receptionist"
        context.actorSelection(path) ! Identify("42")
      }
    case ActorIdentity("42", Some(ref)) => context.watch(ref)
    case ActorIdentity("42", None) => context.stop(self)
    case Terminated(_) => context.stop(self)
  }
}

//------------------------------------------------------------
// Video 3: Eventual Consistency
//------------------------------------------------------------

// Strong consistency: after an update succeeds all reads will
// return the updated value
object StrongLockedValue {
  private var field = 0;
  def update(f: Int => Int): Int = synchronized {
    field = f(field)
    field
  }
  def read(): Int = synchronized { field }
}

// Weak consistency: after an update, conditions must be met
// before all reads return the new value (inconsistency window).
object WeakLockedValue {
  private @volatile var field = 0;
  def update(f: Int => Int): Future[Int] = Future {
    synchronized {
      field = f(field)
      field
    }
  }
  def read(): Int = field
}

// Eventual consistency: once no more updates are made to an object,
// there is a time after which all reads return the last written value.
case class Update(x: Int)
case object Get
case class Result(x: Int)
case class Sync(x: Int, timestamp: Long)
case object Hello

/**
 *
 */
case DistributdStore extends Actor {
  var peers = List[ActorRef] = Nil
  var field = 0
  var lastUpdated = System.currentTimeMillis()

  def receive = {
    case Update(x) =>
      field = x
      lastUpdated = System.currentTimeMillis()
      peers foreach(_ ! Sync(field, lastUpdated))
    case Get => sender ! Result(field)
    case Sync(x, timestamp) if timestamp > lastUpdated =>
      field = x
      lastUpdated = timestamp
    case Hello =>
      peers ::= sender
      sender ! Sync(field, lastUpdated)
  }
}

// To play with actors in the REPL
import akka.actor._
implicit val system = ActorSystem("distributed")
import Actor.DSL._
implicit val sender = actor(new Act { become { case msg => println(msg) } })

val a = system.actorOf(Props[DistributedStore])
val b = system.actorOf(Props[DistributedStore])
a ! Get
b ! Get
a.tell(Hello, b)
b.tell(Hello, a)
b ! Update(42)
a ! Get
system.shutdown()

/**
 * In order to maintain state in a distributed system, one method
 * is using convergent data structures known as (CRDT). The state
 * diagram for an actor is such a strucure (directed acyclic graph
 * of states):
 * - conflicts can always be resolvd locally
 * - conflict resolution is commutative
 * - heuristic is follow presidence (if one is down, must be the case)
 */

//------------------------------------------------------------
// Video 4: Actor Composition
//------------------------------------------------------------

/**
 * The interface of an actor is defined by what messages it 
 * accepts, the type of an actor is structural. The structure
 * may change at any time defined by a protocol. Superficially
 * current Actor implementations are untyped:
 * - sending a message is (Any => Unit)
 * - behavior is PartialFunction[Any, Unit]
 *
 * Actors are composed like human organistions; they are composed
 * on a protocol level, so they can:
 * - translate and forward requests (bridge, decorator)
 * - translate and forward replies (bridge)
 * - split up requests and aggregate replies (facade)
 * - can alter frequency, ordering, and timing of messages
 */

/**
 * The Customer Pattern (request-reply)
 * Customer address is included in the original request.
 * This allows for dynamic composition of actor systems.
 */

/**
 * Interceptors
 * Simply wrap an existing actor and forward the message.
 * If this is a one way message, the intercepter does not
 * even need to keep state.
 */
class AuditTrail(actor: ActorRef) extends Actor with ActorLogging {

  def receive = {
    case message =>
      log.info("sent {} to {}", message, actor)
      target forward message
  }
}

/**
 * The ask pattern
 * Using the ask operator (?), akka can create a simple
 * light weight pseudo actor that will wait for a response
 * to a given message. The ask operater returns a Future[Any].
 *
 * The alternate implementation is to spawn an actor to do this
 * work for us. This will take a bit more resources and require
 * a bit more code.
 */
import akka.pattern.ask

class PostsByEmail(service: ActorRef) extends Actor {
  implicit val timeout = Timeout(3.seconds)

  def receive = {
    case Get(email) =>
      (service ? FindByEmail(email))                              // Future[Any]
        .mapTo[UserInfo]                                          // Future[UserInfo]
        .map(info => Result(info.posts.filter(_.email == email))) // Future[Result]
        .recover { case ex => Failure(ex) }                       // [Failure]
        .pipeTo(sender)
  }
}

/**
 * Result Aggregation
 */
class PostSummary(...) extends Actor {
  implicit val timeout = Timeout(500.millis)

  def receive = {
    case Get(post, user, pass) =>
      val response = for {
        status <- (publisher ? GetStatus(post)).mapTo[PostStatus]
        text   <- (database ? Get(post)).mapTo[Post]
        auth   <- (authenticator ? Login(user, pass)).mapTo[AuthStatus]
      } yield
        if (auth.isSuccessful) Result(status, text)
        else Failure("not authorized")
      response pipeTo sender
  }
}

/**
 * Risk Delegation:
 * - create a child actor to perform a dangerous task
 * - apply lifecycle monitoring
 * - report success/failure back to requestor
 * - ephemeral actor shuts down after each task
 */
class FileWriter extends Actor {
  var workerToCustomer = Map.empty[ActorRef, ActorRef]
  override val supervisorStrategy = SupervisorStrategy.stoppingStrategy

  def receive = {
    case Write(contents, file) =>
      val worker = context.actorOf(Props(new FileWorker(contents, file, self)))
      context.watch(worker)
      workerToCustomer += worker -> sender
    case Done =>
      workerToCustomer.get(sender).foreach(_ ! Done)
      workerToCustomer -= sender
    case Terminated(worker) =>
      workerToCustomer.get(worker).foreach(_ ! Done)
      workerToCustomer -= worker
  }
}

/**
 * Facade Actors:
 * - translation
 * - validation
 * - rate limiting
 * - access control
 *
 * Lax typing makes these patterns super easy (think python)
 */

//------------------------------------------------------------
// Video 5: Scalability
//------------------------------------------------------------

/**
 * Low perfomance means the system is slow for a single client
 * Low scalability means the system is fast for a single client
 * but slow when used by many clients.
 *
 * One actor can only handle a single message at a time. Stateless
 * replicas can run concurrently. For this we need to route messages
 * to worker pools:
 * - stateful: round robin, smallest queue, adaptive, ...
 * - stateless: random, consistent hashing, ...
 */

/**
 * Round Robin
 * - equal distribution of messages to routees
 * - hiccups or unequal message processing time leads to imbalance
 * - imbalances lead to larger spread in latency spectrum
 */

/**
 * Smallest Mailbox Routing
 * - requires routees to be local to inspect mailbox
 * - evens out imbalances, less persistant latency spread
 * - high routing cost, only worth it for high processing cost
 * - reading mailbox size is costly (concurrent queue)
 */

/**
 * Share Work Queue
 * - requires routees to be local
 * - most homogenous latency
 * - effectively a pull model
 */

/**
 * Adaptive Routing
 * - requires feedback about processing times, queue size, and latencies
 * - feedback can be sampled coursely (statistical models)
 * - steering the routing weight subject to feedback control theory
 *   - oscillations, over damping, etc
 */

/**
 * Random Distribution
 * - asymptotically equal distribution of messages
 * - no shared state needed, low routing overhead
 * - works with serveral distributed routers to several routees
 * - can stochastically lead to imbalances
 */

/**
 * Consistent Hashing
 * - splitting incoming message stream according to some criterion
 * - bundle substreams and send them to same routees consistently
 * - can exhibit systematic imbalances based on hash function
 * - different latencies for parts of the input spectrum (harder messages)
 * - no shared state needed for distributed routers
 *
 * Multiple writers to the same state require appropriate data structures
 * and are eventually consistent.
 */

/**
 * Replication of Stateful Actors
 * - based on persistant state
 * - only one instance available at any time
 * - consistent routing to active instances
 * - failure means just replaying state to new instance (event stream)
 * - possible buffering during recovery
 * - migration means recovery at a different location
 *
 * Asynchronous message passing enables vertical scalability
 * Location transparency enables horizontal scalability
 */

//------------------------------------------------------------
// Video 6: Responsiveness
//------------------------------------------------------------

/**
 * Responsiveness is the ability of a system to respond to
 * input in time. If it does not respond in time, it is not
 * available. The goal of resillience is to be available.
 * Responsiveness implies resillience to overload scenarios.
 */

/**
 * To lower call latencies, it is neccessary to exploit
 * parallelism.
 */
class PostSummary(...) extends Actor {
  implicit val timeout = Timeout(500.millis)

  def receive = {
    case Get(post, user, pass) =>
      // this generates three futures, so the slowest is the bounding call
      val status = (publisher ? GetStatus(post)).mapTo[PostStatus]
      val text   = (database ? Get(post)).mapTo[Post]
      val auth   = (authenticator ? Login(user, pass)).mapTo[AuthStatus]
      val response = for (s <- status, t <- text, a <- auth) yield {
        if (auth.isSuccessful) Result(status, text) else Failure("not authorized")
      }
      response pipeTo sender
  }
}

/**
 * When incoming request rate rises, latency typically rises
 * - avoid dependency of processing cost on load
 * - add parallelism elastially (resizing routers)
 *
 * When the rate exceeds the systems capacity requests will pile up
 * - processing gets backlogged
 * - clients timeout, leading to unnecessary work being performed.
 *
 * Can solve this problem with the Circuit Breaker pattern
 */
class Retriever(service: ActorRef) extends Actor {
  implicit val timeout = Timeout(2.seconds)

  val breaker = CircuitBreaker(context.system.scheduler,
    maxFailure  = 3,
    callTimeout = 1.second,
    maxTimeout  = 30.seconds)

  def receive = {
    case Get(user) =>
      val result = breaker.withCircuitBreaker(service ? user).mapTo[String]
      ...
  }
}

/**
 * Bulk Heading
 * Seperate computing intensive parts from client facing parts.
 * Actor isolation is not enough: execution mechanism is still shared.
 * Dedicate disjoint resources to different parts of the system.
 */
Props[MyActor].withDispatcher("compute-jobs")

// default configuration
akka.actor.default-dispatcher {
  executor = "fork-join-executor"
  fork-join-executor {
    parallelism-min = 8
    parallelism-max = 64
    parallelism-factor = 3.0
  }
}

// customer configuration
compute-jobs.fork-join-executor {
    parallelism-min = 4
    parallelism-max = 4
}

/**
 * Failures vs Responsiveness
 * Detecting failures takes time, usually a timeout. Immediate
 * failover requires that the backup be readily available. Instant
 * failover is possible in active-active systems:
 * - sends updates to all systems
 * - respond to client when a quorom responds
 *
 * reactivemanifesto.com
 */
