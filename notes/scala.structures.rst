==================================================
Functional Data Structures in Scala
==================================================

--------------------------------------------------
Totally Ordered Type
--------------------------------------------------

Given a compare function, we can provide all the primitives
needed for a totally ordered type, (note, we can also define
these operations in terms of `lteq` or `gteq`):

https://github.com/scala/scala/blob/master/src/library/scala/math/Ordering.scala

.. code-block:: scala

    trait Ordering[T] { 
      def compare(x: T, y: T): Int
      def eq(x: T, y: T): Boolean   = compare(x, y) == 0
      def lt(x: T, y: T): Boolean   = compare(x, y)  < 0
      def gt(x: T, y: T): Boolean   = compare(x, y)  > 0
      def lteq(x: T, y: T): Boolean = compare(x, y) <= 0
      def gteq(x: T, y: T): Boolean = compare(x, y) >= 0
      def max(x: T, y: T): T = if (gteq(x, y)) x else y
      def min(x: T, y: T): T = if (lteq(x, y)) x else y
    }

--------------------------------------------------
List
--------------------------------------------------

https://github.com/scala/scala/blob/master/src/library/scala/collection/immutable/List.scala

.. code-block:: scala

    abstract sealed class List[+T] {
      def isEmpty: Boolean
      def head: T
      def tail: List[T]
      def prepend(x: T): List[T] = Cons(x, this)
      def append(x: T):  List[T] =
        if (isEmpty) Cons(x)
        else Cons(head, tail.append(x))

      def update(n: Int, x: T): List[T] =
        if (isEmpty) fail("index out of bounds")
        else if (n == 0) Cons(x, tail)
        else Cons(head, update(n - 1, x))

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

      // List(1,2,3,4).suffixes =
      //   [[1,2,3,4], [2,3,4], [3,4], [4], []]
      def suffixes: List[List[T]] =
        if (isEmpty) this
        else Cons(this, tail.suffixes)
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
Stack
--------------------------------------------------

https://github.com/scala/scala/blob/master/src/library/scala/collection/immutable/Stack.scala

.. code-block:: scala

    class Stack[+T](xs: List[T]) {
      def reverse: Stack[T] = new Stack(xs.reverse)
      def push(x: T): Stack[T] = new Stack(x :: xs)
      def pop: (T, Stack[T]) =
        if (isEmpty) fail("empty stack")
        else (xs.head, new Stack(xs.tail)
      def isEmpty: xs.isEmpty
    }

--------------------------------------------------
Queue
--------------------------------------------------

https://github.com/scala/scala/blob/master/src/library/scala/collection/immutable/Queue.scala

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

      def contains(x: T) : Boolean =
        if (isEmpty) false
        else if (x == value) true
        else if (x > value) right.contains(x)
        else if (x < value) left.contains(x)

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

    object Tree {
      // Generate a complete binary tree with x stored
      // at every node and copy as many paths as possible.
      def complete[T](x: T, d: Int): Tree[T] =
        lazy val child = complete(x, d - 1)
        if (d == 0) Leaf else Branch(x, child, child)
    }

Example of a Red Black balanced tree:

https://github.com/scala/scala/blob/master/src/library/scala/collection/immutable/RedBlackTree.scala

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
Map Using A Tree
--------------------------------------------------

.. code-block:: scala

    // Scala imports an implicit Ordering[K] into
    // the Map[K, V] extends Tree[(K, V)] to redefine
    // the ordering operations.
    type Entry[K, V] = Tuple[K, V]
    class EntryOrdering extends Ordering[Entry[K, V]] {
      def compare(x: Entry[K, V], y: Entry[K, V]) =
        if (x._1 == y._1) 0
        else if (x._1 < y._1) -1
        else 1
    }

    class Map[K,V] Tree[Entry[K,V]] {
      def put(k: K, v: V): Map[K, V] =
        if (isEmpty) Branch((k, v))
        else if (x < value) Branch(value, left.add(x), right)
        else if (x > value) Branch(value, left, right.add(x))
        else Branch((k, v), left, right)
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

--------------------------------------------------
Priority Queue (Heap)
--------------------------------------------------

.. code-block:: scala

    //
    // Base trait for a heap using ML style
    // type declarations for heap, element, and ordering
    //
    trait Heap {
      type H // type of a heap
      type A // type of an element
      def order: Ordering[A] // ordering on elements

      def empty: H // the empty heap
      def isEmpty(h: H): Boolean // whether the given heap h is empty

      def insert(x: A, h: H): H // the heap resulting from inserting x into h
      def meld(h1: H, h2: H): H // the heap resulting from merging h1 and h2

      def findMin(h: H): A // a minimum of the heap h
      def deleteMin(h: H): H // a heap resulting from deleting a minimum of h
    }

A binomial tree is one that satisfies the following properties:

* a binomial tree of rank 0 is a singleton.
* a binomial tree of rank r + 1 if formed by linking two trees of
  rank r with one being the left most child of the other.
* binomial tree of rank r has 2^r nodes
 
A binomial queue is therefore a forest of heap ordered binomial
trees where no two trees have the same rank. Since there are 2^r
nodes, the ranks can be thought of a binary number. So a tree with
21 nodes has trees of rank 10101 (16, 4, 1). Adding a new entry in
the queue is equivalent to adding a singleton node and merging the
matching tree ranks from right to left. This can also be seen as
adding 1 to the binary rank representation (with carry).

Deleting the miminum node in the queue just removes the root from
the min ranked tree. This resuling tree is thus itself a binomial
queue that can be melded into the existing queue. It should be noted
that the queue stores trees in increasing rank for good insert
performance and the tree's children are in decreasing rank for good
link perforamance. This is why we reverse the children in the deleteMin.

Also, the rank is usually defined by the parent and children aquire their 
rank based on their position in the tree, not labeled individually.

.. code-block:: scala

    //
    // Binomial hepa implementation based on Brodal heaps
    // - fibonacci heap
    // - Vuillemin binomial queue
    //
    trait BinomialHeap extends Heap {

      type Rank = Int
      case class Node(x: A, r: Rank=0, c: List[Node]=Nil)
      override type H = List[Node]

      protected def root(t: Node) = t.x
      protected def rank(t: Node) = t.r
      protected def link(t1: Node, t2: Node): Node = // t1.r==t2.r
        if (order.lteq(t1.x, t2.x)) Node(t1.x, t1.r + 1, t2::t1.c) else Node(t2.x, t2.r + 1, t1::t2.c)
      protected def ins(t: Node, ts: H): H = ts match {
        case Nil    => List(t)
        case tp::ts => // t.r <= tp.r
          if (t.r < tp.r) t::tp::ts else ins(link(t, tp), ts)
      }

      override def empty = Nil
      override def isEmpty(ts: H) = ts.isEmpty

      override def insert(x: A, ts: H)  = ins(Node(x), ts)
      override def meld(ts1: H, ts2: H) = (ts1, ts2) match {
        case (Nil, ts)          => ts
        case (ts, Nil)          => ts
        case (t1::ts1, t2::ts2) =>
          if (t1.r < t2.r) t1::meld(ts1, t2::ts2)
          else if (t2.r < t1.r) t2::meld(t1::ts1, ts2)
          else ins(link(t1, t2), meld(ts1, ts2))
      }

      override def findMin(ts: H) = ts match {
        case Nil    => throw new NoSuchElementException("min of empty heap")
        case t::Nil => root(t)
        case t::ts  =>
          val x = findMin(ts)
          if (order.lteq(root(t), x)) root(t) else x
      }

      override def deleteMin(ts: H) = ts match {
        case Nil   => throw new NoSuchElementException("delete min of empty heap")
        case t::ts =>
          def getMin(t: Node, ts: H): (Node, H) = ts match {
            case Nil     => (t, Nil)
            case tp::tsp =>
              val (tq, tsq) = getMin(tp, tsp)
              if (order.lteq(root(t), root(tq))) (t, ts) else (tq, t::tsq)
          }
          val (Node(_, _, c), tsq) = getMin(t, ts)
          meld(c.reverse, tsq)
      }
    }

Another queue is the skew binomial queue which makes use of the
skew binary numbers idea to reduce carries on insert to at most
one node.

A skew binomial tree is one that satisfies the following properties:

* a skew binomial tree of rank 0 is a singleton.
* a skew binomial tree of rank r + 1 if formed in one of three ways:

  - a simple link making one tree of rank r the child of another tree
    of rank r
  - a type A skew link, making two trees of rank r children of a tree
    of rank 0
  - a type B skew link, making a tree of rank 0 and a tree of rank r
    the leftmost children of a tree of rank r.

A perfrectly balanced tree only allows simple and typeA links. Otherwise
a tree allowing all three will have 2^r <= [t] <= 2^(r + 1) - 1 nodes.
The height of the tree is equal to the rank.

.. code-block:: scala

    trait SkewBinomialHeap extends BinomialHeap {
      protected def skewLink(t1: Node, t2: Node, t3: Node): Node =
        if (order.lteq(t2.x, t1.x) and order.lteq(t2.x, t3.x)) Node(t2.x, t2.r + 1, t1::t3::t2.c)
        else if (order.lteq(t3.x, t1.x) and order.lteq(t3.x and t2.x) Node(t3, t3.r + 1, t1 :: t2 :: t3.c)
        else Node(t1, t2.r + 1, t2 :: t3)

      protected def uniqify(t: Node): Node = t match {
        case Nil  => Nil
        case t:ts => ins(t, ts) // eliminate initial duplicate
      }
      protected def meldUnique(ts1: H, ts2: H) = (ts1, ts2) match {
        case (Nil, ts)          => ts
        case (ts, Nil)          => ts
        case (t1::ts1, t2::ts2) =>
          if (t1.r < t2.r) t1 :: meldUnique(ts1, t2::ts2)
          else if (t2.r < t1.r) t2 :: meldUnique(t1::ts1, ts2)
          else ins (link (t1, t2), meldUniq (ts1, ts2))
      
      override def insert(x: A, ts: H)  = ts match {
        case t1::t2::ts  => 
          if (t1.r == t2.r) skewLink(Node(x), t1, t2) :: ts else Node(x) :: ts
        case _ => Node(x) :: ts

      override def meld(ts1: H, ts2: H) = meldUnique(uniqify ts1, uniqify ts2)
      override def deleteMin(ts: H) = ts match {
        case Nil   => throw new NoSuchElementException("delete min of empty heap")
        case t::ts =>
          def getMin(t: Node, ts: H): (Node, H) = ts match {
            case Nil     => (t, Nil)
            case tp::tsp =>
              val (tq, tsq) = getMin(tp, tsp)
              if (order.lteq(root(t), root(tq))) (t, ts) else (tq, t::tsq)
          }
          def split(ts, xs, cs): (H, H) = cs match {
            case Nil  => (ts, xs)
            case t::c =>
              if (c.r == 0) split(ts, root(t) :: xs, c) else split(t::ts, xs, c)
          }
          val (Node(_, _, c), tsq) = getMin(t, ts)
          val (tsq2, xsq) = split([], [], c)
          xsq.fold(meld(tsq, tsq2))(insert)
    }

We can add an O(1) `findMin` operator by wrapping a queue implementation
in a decotrator and maintaining the current min:

.. code-block:: scala

    trait FindMinHeap(heap: H) extends Heap {
      type H = heap.H
      type A = heap.A

      def empty: heap.empty
      def isEmpty(h: H): Boolean // whether the given heap h is empty

      def insert(x: A, h: H): H // the heap resulting from inserting x into h
      def meld(h1: H, h2: H): H // the heap resulting from merging h1 and h2

      def findMin(h: H): A // a minimum of the heap h
      def deleteMin(h: H): H // a heap resulting from deleting a minimum of h
    }

    case class MinEmpty(heap: H) extends FindMinHeap
    case class MinRoot(x: A, heap: H) extends FindMinHeap

Here is an example of mixing in the various traits to create a
queue of type int with the binomial heap implementation:

.. code-block:: scala

    //
    // To instantiate an instance of the heap
    //
    trait IntHeap extends Heap {
      override type A  = Int
      override def order = scala.math.Ordering.Int
    }
    val heap = new IntHeap with BinonmailHeap
