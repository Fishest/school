/**
 * Copyright (C) 2009-2013 Typesafe Inc. <http://www.typesafe.com>
 */
package actorbintree

import akka.actor._
import scala.collection.immutable.Queue
import scala.util.Success

object BinaryTreeSet {

  trait Operation {
    def requester: ActorRef
    def id: Int
    def elem: Int
  }

  trait OperationReply {
    def id: Int
  }

  /** Request with identifier `id` to insert an element `elem` into the tree.
    * The actor at reference `requester` should be notified when this operation
    * is completed.
    */
  case class Insert(requester: ActorRef, id: Int, elem: Int) extends Operation

  /** Request with identifier `id` to check whether an element `elem` is present
    * in the tree. The actor at reference `requester` should be notified when
    * this operation is completed.
    */
  case class Contains(requester: ActorRef, id: Int, elem: Int) extends Operation

  /** Request with identifier `id` to remove the element `elem` from the tree.
    * The actor at reference `requester` should be notified when this operation
    * is completed.
    */
  case class Remove(requester: ActorRef, id: Int, elem: Int) extends Operation

  /** Request to perform garbage collection*/
  case object GC

  /** Holds the answer to the Contains request with identifier `id`.
    * `result` is true if and only if the element is present in the tree.
    */
  case class ContainsResult(id: Int, result: Boolean) extends OperationReply
  
  /** Message to signal successful completion of an insert or remove operation. */
  case class OperationFinished(id: Int) extends OperationReply

}

/**
 * The binary tree top level manager actor
 */
class BinaryTreeSet extends Actor with Stash {
  import BinaryTreeSet._
  import BinaryTreeNode._

  def createRoot: ActorRef = context.actorOf(BinaryTreeNode.props(0, initiallyRemoved = true))
  def receive = normal
  
  var root = createRoot

  /**
   * The normal runner of binary tree operations until
   * a garbage collection call is made. It then switches
   * to the GC receiver.
   */
  val normal: Receive = {
    case op: Operation => root ! op
    case GC            => startGarbageCollection
  }

  /**
   * The garbage collection runner queues all messages until
   * the garbage collection is finished. It then converts back
   * to the normal mode.
   */
  def garbageCollecting(newRoot: ActorRef): Receive = {
    case GC            => // already in GC, ignored
    case op: Operation => stash()
    case CopyFinished  => startNormal(newRoot)
  }

  /**
   * Converts to the normal mode of operation
   */
  private def startNormal(newRoot: ActorRef) {
    root ! PoisonPill // recursively shut down all children
    root = newRoot
    context.unbecome()
    unstashAll()
  }
  
  /**
   * Converts to the garbage collection mode of operation
   */
  private def startGarbageCollection() {
    val newRoot = createRoot
    context.become(garbageCollecting(newRoot))
    root ! CopyTo(newRoot)
  }

}

/**
 * The companion object of the individual tree node
 * actors.
 */
object BinaryTreeNode {
  trait Position

  case object Left  extends Position
  case object Right extends Position

  case class CopyTo(treeNode: ActorRef)
  case object CopyFinished

  def props(elem: Int, initiallyRemoved: Boolean) = Props(classOf[BinaryTreeNode],  elem, initiallyRemoved)
}

/**
 * Represents a single node in the binary tree.
 */
class BinaryTreeNode(val elem: Int, initiallyRemoved: Boolean) extends Actor {
  import BinaryTreeNode._
  import BinaryTreeSet._

  var subtrees = Map[Position, ActorRef]()
  var removed  = initiallyRemoved

  def receive = normal


  /**
   * This is the normal mode of operation
   */
  val normal: Receive = {
    case op:Operation =>
      if (op.elem > elem && subtrees.contains(Right))
        subtrees(Right) ! op
      else if (op.elem < elem && subtrees.contains(Left)) 
        subtrees(Left) ! op
      else perform(op)
      
    case CopyTo(actor) => 
      validate(subtrees.values.toSet, removed)
      if (!removed)
        actor ! Insert(self, elem, elem)
      subtrees.values.foreach(_ ! CopyTo(actor))
  }
  
  /**
   * Helper to perform the actual operations on this node
   * @param operation The operation to perform
   */
  def perform(operation: Operation): Unit = operation match {
    case Contains(actor, id, value) =>
      actor ! ContainsResult(id, (value == elem) && !removed)
      
    case Insert(actor, id, value) => 
      if (value == elem) { removed = false }
      else insert(value)
      actor ! OperationFinished(id)
      
    case Remove(actor, id, value) =>
      if (value == elem) { removed = true }
      actor ! OperationFinished(id)
  }
    
  /**
   * This is the copying mode of operation.
   */
  def copying(expected: Set[ActorRef], insertConfirmed: Boolean): Receive = {
    case CopyFinished          => validate(expected - sender, insertConfirmed)
    case op: OperationFinished => validate(expected, true)
  }
  
  /**
   * Given a value, find its position in the tree and insert it
   * @param value The value to insert into the tree
   */
  private def insert(value: Int) {
	val position = if (value > elem) Right else Left
	val node = context.actorOf(BinaryTreeNode.props(value, false))
	subtrees += position -> node
  }

  /**
   * Given an expected set, validate that this node has completed its copying
   * @param expected The expected results to receive
   * @param confirmed A confirmation that this node has been copied
   */
  private def validate(expected: Set[ActorRef], confirmed: Boolean) {
    if (expected.isEmpty && confirmed) {
      context.parent ! CopyFinished 
    } else context.become(copying(expected, confirmed))
  }

}
