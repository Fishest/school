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

class Replica(val arbiter: ActorRef, persistenceProps: Props) extends Actor {
  import Replica._
  import Replicator._
  import Persistence._
  import context.dispatcher
  
  var seq         = 0L
  var kv          = Map.empty[String, String]
  var secondaries = Map.empty[ActorRef, ActorRef]
  var replicators = Set.empty[ActorRef]
  
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
    case Insert(key, value, id) => handleInsert(key, value, id)
    case Remove(key, id)        => handleRemove(key, id)
    case Get(key, id)           => handleGet(key, id)
    case Replicas(replicas)     => handleReplicas(replicas)
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
      replicators += replicator
      secondaries += replica -> replicator
    }
    
    stopped foreach { replica =>
      val replicator = secondaries(replica)
      context.stop(replicator)
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
	    case Some(v) => kv += key -> v
	    case None    => kv -= key
	  }
	  seq += 1
    }
    if (id <= seq) sender ! SnapshotAck(key, id)   
  }
  
  /**
   * Handler for the replicate operation
   * @param key The key to add the value at
   * @param value The value to start at the given key
   * @param id The client transaction identifier
   */
  private def handleReplicate(key: String, value: Option[String], id: Long) {
    value match {
      case Some(v) => kv += key -> v
      case None    => kv -= key
    }
    sender ! Replicated(key, id)   
  }
  
  /**
   * Handler for the remove operation
   * @param key The key to remove
   * @param id The client transaction identifier
   */
  private def handleRemove(key: String, id: Long) {
    kv -= key
    sender ! OperationAck(id)
  }

  /**
   * Handler for the insert operation
   * @param key The key to add the value at
   * @param value The value to start at the given key
   * @param id The client transaction identifier
   */
  private def handleInsert(key: String, value: String, id: Long) {
    kv += key -> value
    sender ! OperationAck(id)
  }
  
  /**
   * Handler for the get operation
   * @param key The key to get the value of
   * @param id The client transaction identifier
   */
  private def handleGet(key: String, id: Long) {
    sender ! GetResult(key, kv.get(key) ,id)
  }
}
