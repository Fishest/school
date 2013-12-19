package kvstore

import akka.actor.{ OneForOneStrategy, Props, ActorRef, Actor }
import kvstore.Arbiter._
import scala.collection.immutable.Queue
import akka.actor.SupervisorStrategy.Restart
import scala.annotation.tailrec
import akka.pattern.{ ask, pipe }
import akka.actor.Terminated
import scala.concurrent.duration._
import akka.actor.PoisonPill
import akka.actor.OneForOneStrategy
import akka.actor.SupervisorStrategy
import akka.util.Timeout
import akka.actor.Cancellable
import akka.actor.ReceiveTimeout

object Replica {
  sealed trait Operation {
    def key: String
    def id: Long
  }
  case class Insert(key: String, value: String, id: Long) extends Operation
  case class Remove(key: String, id: Long) extends Operation
  case class Get(key: String, id: Long) extends Operation

  sealed trait OperationReply
  case class OperationAck(id: Long) extends OperationReply
  case class OperationFailed(id: Long) extends OperationReply
  case class GetResult(key: String, valueOption: Option[String], id: Long) extends OperationReply

  def props(arbiter: ActorRef, persistenceProps: Props): Props = Props(new Replica(arbiter, persistenceProps))
}

/**
 * 
 */
object Monitor {
  import Persistence._
  
  def props(original: ActorRef, persister: ActorRef, replicas: Set[ActorRef],
      persist: Persist, success: AnyRef, failure: AnyRef): Props =
    Props(new Monitor(original, persister, replicas, persist, success, failure))
}

/**
 * 
 */
class Monitor(responder: ActorRef, persister: ActorRef, replicas: Set[ActorRef]=Set.empty[ActorRef],
    persistMsg: Persistence.Persist, successMsg: AnyRef, failureMsg: AnyRef) extends Actor {
  
  import Replica._
  import Persistence._
  import Replicator._
  import context.dispatcher

  var toPersist = 1
  var toReplicate = replicas 
  var cancelPersist = context.system.scheduler.schedule(0.millis, 100.millis) { persister ! persistMsg }
  var cancelReplicate  = context.system.scheduler.schedule(0.millis, 100.millis) {
      toReplicate foreach (_ ! Replicate(persistMsg.key, persistMsg.valueOption, persistMsg.id))
  }
  
  handleResponse(false, false) // in case we didn't have any replicas
  context.setReceiveTimeout(1.seconds)
  
  /**
   * 
   */
  def receive = {
    case Persisted(key, id)  => handleResponse(false, true)
    case Replicated(key, id) => handleResponse(true, false)
    case ReceiveTimeout      => handleTimeout()
    case Replicas(replicas)  => handleReplicaUpdate(replicas)
  }
  
  private def handleReplicaUpdate(replicas: Set[ActorRef]) {
    toReplicate = toReplicate diff replicas
    handleResponse(false, false)
  }
  
  /**
   * 
   */
  private def handleResponse(replicated: Boolean, persisted: Boolean) {
    if (persisted) toPersist  -= 1
    if (replicated) toReplicate -= sender
    
    if (toPersist  == 0 && !cancelPersist.isCancelled) cancelPersist.cancel
    if (toReplicate.size == 0 && !cancelPersist.isCancelled) cancelReplicate.cancel    
    if (toPersist + toReplicate.size == 0) {
      responder ! successMsg
      context.stop(self)
    }
  }
  
  /**
   * 
   */
  private def handleTimeout() {
    responder ! failureMsg
    context.stop(self)
  }
}

/**
 * The actor responsible for storing the current state of the key-value store.
 * There is a primary and secondary version of this.
 */
class Replica(val arbiter: ActorRef, persistenceProps: Props) extends Actor {
  import Replica._
  import Replicator._
  import Persistence._
  import context.dispatcher
  
  var seq         = 0L
  var database    = Map.empty[String, String]
  var secondaries = Map.empty[ActorRef, ActorRef]
  var replicators = Set.empty[ActorRef]
  var persistance = context.actorOf(persistenceProps)
  
  /**
   * This is the supervisor strategy for the persistence actor
   */
  override val supervisorStrategy = OneForOneStrategy(maxNrOfRetries = 5, withinTimeRange = 1.second) {
    case _: PersistenceException  => Restart
  }
  
  /**
   * Arbiter initialization and group membership
   */
  arbiter ! Join
  
  /**
   * This is the initial message handling before our
   * role in the system is decided.
   */
  def receive = {
    case JoinedPrimary   => context.become(leader)
    case JoinedSecondary => context.become(replica)
  }

  /**
   * This is the message handling logic for the leader role.
   */
  val leader: Receive = {
    case Insert(key, value, id)    => handleInsert(key, value, id)
    case Remove(key, id)           => handleRemove(key, id)
    case Get(key, id)              => handleGet(key, id)
    case Replicas(replicas)        => handleReplicas(replicas - self)
  }

  /**
   * This is the message handling logic for the replica role.
   */
  val replica: Receive = {
    case Snapshot(key, value, id)  => handleSnapshot(key, value, id)
    case Get(key, id)              => handleGet(key, id)
  }
  
  /**
   * This is the message handling logic for receiving the
   * current state of the existing replicas.
   */
  private def handleReplicas(replicas: Set[ActorRef]) {
    val current = secondaries.keySet
    val started = replicas diff current
    val stopped = current diff replicas
    
    started foreach { replica =>
      val replicator = context.actorOf(Replicator.props(replica))
      var sequence = 0
      replicators += replicator
      secondaries += replica -> replicator
      
      database foreach { case (k, v) =>
        replicator ! Replicate(k, Some(v), sequence)
        sequence += 1
      }
    }
    
    stopped foreach { replica =>
      val replicator = secondaries(replica)
      context.stop(replicator)
      context.children foreach (_ ! Replicas(Set(replicator)))
      replicators -= replicator
      secondaries -= replica
    }    
  }
  
  /**
   * Handler for the snapshot operation
   * @param key The key to add the value at
   * @param value The value to start at the given key
   * @param id The client transaction identifier
   */
  private def handleSnapshot(key: String, value: Option[String], id: Long) {
    if (id == seq) {
	  value match {
	    case Some(v) => database += key -> v
	    case None    => database -= key
	  }
	  seq += 1
	    
	  val persist = Persist(key, value, id)
	  val success = SnapshotAck(key, id)
	  val failure = SnapshotAck(key, id)
      context.actorOf(Monitor.props(sender, persistance, replicators, persist, success, failure))
    } else if (id < seq) {
      sender ! SnapshotAck(key, id)
    }   
  }
  
  /**
   * Handler for the get operation
   * @param key The key to get the value of
   * @param id The client transaction identifier
   */
  private def handleGet(key: String, id: Long) {
    sender ! GetResult(key, database.get(key) ,id)
  }
  
  /**
   * Handler for the remove operation
   * @param key The key to remove
   * @param id The client transaction identifier
   */
  private def handleRemove(key: String, id: Long) {
    database -= key
    handleBroadcast(key, None, id)
  }

  /**
   * Handler for the insert operation
   * @param key The key to add the value at
   * @param value The value to start at the given key
   * @param id The client transaction identifier
   */
  private def handleInsert(key: String, value: String, id: Long) {
    database += key -> value
    handleBroadcast(key, Some(value), id)
  }
  
  /**
   * Handler for broadcasting new values to replicate and persist
   * @param key The key to add the value at
   * @param value The value to broadcast for the given key
   * @param id The client transaction identifier
   */
  private def handleBroadcast(key:String, value: Option[String], id: Long) {
    val persist = Persist(key, value, id)
    val success = OperationAck(id)
    val failure = OperationFailed(id)
    context.actorOf(Monitor.props(sender, persistance, replicators, persist, success, failure))
  }
}
