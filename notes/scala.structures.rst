==================================================
Functional Data Structures in Scala
==================================================

--------------------------------------------------
List
--------------------------------------------------

.. code-block:: scala

    abstract sealed class List[+T] {
      def isEmpty: Boolean
      def head: T
      def tail: List[T]
      def prepend(x: T): List[T] = Cons(x, this)
      def append(x: T):  List[T] =
        if (isEmpty) Cons(x)
        else Cons(head, tail.append(x))

      def apply(n: Int): T = 
        if (isEmpty) fail("index out of bounds")
        else if (n == 0) head
        else tail.apply(n - 1)

      def concat(xs: List[T]): List[T] = 
        if (isEmpty) xs
        else if (xs.isEmpty) this
        else tail.concat(xs).prepend(head)

      def reverse: List[T] =
        @tailrec
        def loop(a: List[T], b: List[T]): List[T] =
          if (a.isEmpty) b
          else loop(a.tail, b.prepend(a.head))
        loop(this, Nil)
    }

    case class Nil extends List[Nothing] {
      override def isEmpty = true
      override def head: Nothing = fail("empty list")
      override def tail: Nothing = fail("empty list")
    }

    case class Cons[T](head: T, tail: List[T] = Nil[T]) extends List[T] {
      override def isEmpty = false
    }

--------------------------------------------------
Queue
--------------------------------------------------

This is implemented in terms of a bankers queue

.. code-block:: scala

    class Queue[T](private in: List[T] = Nil, private out: List[T] = Nil) {
      def enqueue(x: T) : Queue[T] = new Queue(x :: in, out)
      def dequeue: (T, Queue[T]) = out match {
        case (x :: xs) => (x, new Queue(in, xs))
        case Nil => in.reverse match {
          case (x :: xs) => (x, new Queue(Nil, xs))
          case Nil => fail("empty queue")
        }
      }
      def front: T = dequeue match { case (x, _) => x }
      def rear: Queue[T] = dequeue match { case (_, xs) => xs }
      def isEmpty: Boolean = in.isEmpty && out.isEmpty
    }

--------------------------------------------------
Binary Search Tree
--------------------------------------------------

.. code-block:: scala

    abstract sealed class Tree[+T] {
      def value: T
      def left: Tree[T]
      def right: Tree[T]
      def isEmpty: Boolean

      def add(x: T): Tree[T] = 
        if (isEmpty) Branch(x)
        else if (x < value) Branch(value, left.add(x), right)
        else if (x > value) Branch(value, left, right.add(x))
        else this // equal

      def remove(x: T): Tree[T] =
        if (isEmpty) fail("empty tree")
        else if (x < value) Branch(value, left.remove(x), right)
        else if (x > value) Branch(value, left, right.remove(x))
        else {
          if (left.isEmpty && right.isEmpty) Leaf
          else if (left.isEmpty) right
          else if (right.isEmpty) left
          else {
            val succ = right.min
            Branc(succ, left, right.remove(succ))
          }
        }

      def min: T = {
        @tailrec
        def loop(t: Tree[T], m: T) =
          if (t.isEmpty) m else loop(t.left, m)

        if (isEmpty) fail("empty tree")
        else loop(left, value)
      }

      def max: T = {
        @tailrec
        def loop(t: Tree[T], m: T) =
          if (t.isEmpty) m else loop(t.right, m)

        if (isEmpty) fail("empty tree")
        else loop(right, value)
      }

      def size: Int =
        if (isEmpty) 0
        left.size + right.size + 1

      def apply(n: Int): T =
        if (isEmpty) fail("empty tree")
        else if (n < left.size) left.apply(n)
        else if (n > left.size) right.apply(n - size - 1)
        else value

      def valuesByDepth: List[T] =
        def loop(s: List[Tree]): List[T]
          if (s.isEmpty) Nil
          else if (s.head.isEmpty) loop(s.tail)
          else s.head.value :: loop(s.head.left :: s.head.right :: s.tail)
    
        loop(List(this))

      def valuesByBreadth: List[T] =
        def loop(q: Queue[Tree]): List[T]
          if (q.isEmpty) Nil
          else if (q.head.isEmpty) loop(q.tail)
          else q.head.value :: loop(q.tail :+ q.head.left :+ q.head.right)
    
        loop(Queue(this))

      def invert: Tree[T] =
        if (isEmpty) Left else Branch(-value, right.invert, left.invert)
    }

    case class Leaf extends Tree[Nothing] {
      override def value: Nothing = fail("empty tree")
      override def left: Nothing = fail("empty tree")
      override def right: Nothing = fail("empty tree")
      override def isEmpty = true
    }

    case class Branch[T](value: T, left: Tree[T], right: Tree[T]) extends Tree[T] {
      override def isEmpty = false
    }

Example of a Red Black balanced tree:

.. code-block:: scala
    case class RedBranch(value: T, left: Tree[T], right Tree[T]) extends Tree[T] {
      def isBlack: false
    }
    case class BlackBranch(value: T, left: Tree[T], right Tree[T]) extends Tree[T] {
      def isBlack: true
    }


    def balancedAdd(x: T) : Tree[T] =
      if (isEmpty) RedBranch(x)
      else if (x < value) balance(isBlack, value, left.balancedAdd(x), right)
      else if (x > value) balance(isBlack, value, left, right.balancedAdd(x))
      else this

    def balance(b: Boolean, x: T, left: Tree[T], right: Tree[T]): Tree[T] = (b, left, right) match {
      case (true, RedBranch(y, RedBranch(z, a, b), c), d) => BlackBranch(y, RedBranch(z, a, b), RedBranch(x, c, d))
      case (true, a, RedBranch(y, b, RedBranch(z, c, d))) => BlackBranch(y, RedBranch(x, a, b), RedBranch(z, c, d))
      case (true, RedBranch(y, a, RedBranch(z, b, c)), d) => BlackBranch(y, RedBranch(z, a, b), RedBranch(x, c, d))
      case (true, a, RedBranch(y, b, RedBranch(z, c, d))) => BlackBranch(y, RedBranch(x, a, b), RedBranch(z, c, d))
      case (true, _, _)  => BlackBranch(x, left, right)
      case (false, _, _) => RedBranch(x, left, right)
    }


--------------------------------------------------
Trie
--------------------------------------------------

Patricia Trie
Ideal Hash Tree (Phil Bagwell)
http://cstheory.stackexchange.com/questions/1539/whats-new-in-purely-functional-data-structures-since-okasaki

scala.collection.immutable.Vector
scala.collection.immutable.HashMap
scala.collection.immutable.HashSet
