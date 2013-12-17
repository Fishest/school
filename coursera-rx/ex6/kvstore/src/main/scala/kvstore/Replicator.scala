package kvstore

import akka.actor.Props
import akka.actor.Actor
import akka.actor.ActorRef
import scala.concurrent.duration._
import akka.actor.Cancellable

object Replicator {
  case class Replicate(key: String, valueOption: Option[String], id: Long)
  case class Replicated(key: String, id: Long)
  
  case class Snapshot(key: String, valueOption: Option[String], seq: Long)
  case class SnapshotAck(key: String, seq: Long)

  def props(replica: ActorRef): Props = Props(new Replicator(replica))
}

class Replicator(val replica: ActorRef) extends Actor {
  import Replicator._
  import Replica._
  import context.dispatcher
  
  // secondary-id -> (primary reference, original message, schedule-cancellation)
  var acks = Map.empty[Long, (ActorRef, Replicate, Cancellable)]
  var _counter = 0L
  def nextSequence = {
    val result = _counter
    _counter += 1
    result
  }
  
  /**
   * This is the handling logic for the replica manager
   */
  def receive: Receive = {
    case Replicate(key, value, id) => handleReplicate(key, value, id)
    case SnapshotAck(key, id)      => handleSnapshotAck(key, id)
  }

  /**
   * This is the handler for the snapshot acknowledge message.
   * @param key The key that was correctly replicated
   * @param id The identifier from the secondary replica
   */
  private def handleSnapshotAck(key: String, id: Long) {
    if (acks.contains(id)) {
      val (actor, message, cancel) = acks(id)
      cancel.cancel
      actor ! Replicated(message.key, message.id)
      acks -= id
      
    }
  }
  
  /**
   * This is the handler for the replicate message.
   * @param key The key to replicate to the secondary
   * @param value The value (insert or remove) to replicate
   * @param id The identifier from the primary replica 
   */
  private def handleReplicate(key: String, value: Option[String], id: Long) {
    val seq = nextSequence
    val msg = Snapshot(key, value, seq)
    val cancel = context.system.scheduler.schedule(0.millis, 100.millis) { replica ! msg }
    acks += seq -> (sender, Replicate(key, value, id), cancel)
  }
}
