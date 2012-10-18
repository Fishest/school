============================================================
Chapter 4
============================================================

------------------------------------------------------------
4.1 Polymorphism
------------------------------------------------------------

Cons list is an immutable linked list that is constructed
from two building blocks:

1. Nil - the empty list
2. Cons cell - a cell containing an element and remainder

Example::

    trait List[T] {
      def isEmpty: Boolean
      def head: T
      def tail: List[T]
    }

    class Cons[T](val head: Int, val tail: List[T]) extends List[T] {
      def isEmpty: Boolean = false
    }

    class Nil[T] extends List[T] {
      def isEmpty: Boolean = true
      def head: Nothing = throw NoSuchElementException("Nil.head")
      def tail: Nothing = throw NoSuchElementException("Nil.tail")
    }

    def singleton[T](elem: T): List[T] = new Cons[T](elem, new Nil[T])

    def nth[T](count: int, list: List[T]) : T =
      if (list.isEmpty) throw new IndexOutOfBoundsException()
      else if (count == 0) list.head
      else nth(count - 1, list.tail)

    val conslist = new Cons(1, new Cons(2, new Cons(3, new Nil)))
    val onelist = singleton(1)
    val truelist = singleton(true)
    val third = nth(3, conslist)

------------------------------------------------------------
4.2 Objects Everywhere
------------------------------------------------------------

How can we describe Boolean outside of JVM primitives::

    package idealized.scala

    abstract class Boolean {
      def ifThenElse[T](t: => T, e: => T): T
      def && (x: => Boolean): Boolean = ifThenElse(x, false)
      def || (x: => Boolean): Boolean = ifThenElse(true, x)
      def unary_!:            Boolean = ifThenElse(false, true)
      def == (x: => Boolean): Boolean = ifThenElse(x, x.unary_!)
      def != (x: => Boolean): Boolean = ifThenElse(x.unary_!, x)
      def  < (x: => Boolean): Boolean = ifThenElse(false, x)
      def  > (x: => Boolean): Boolean = ifThenElse(true, x)
    }

    object true extends Boolean {
      def ifThenElse[T](t: => T, e: => T) = t
    }

    object false extends Boolean {
      def ifThenElse[T](t: => T, e: => T) = e
    }

    /**
     * Peano numbers example
     */
    abstract class Natural {
      def isZero: Boolean
      def pred: Natural
      def succ: Natural = new Successor(this)
      def + (that: Nat): Natural
      def - (that: Nat): Natural
    }

    object Zero extends Natural {
      def isZero = true
      def pred = throw new Error()
      def + (that: Nat) = that
      def - (that: Nat) = if (that.isZero) that else throw new Error()
    }

    class Successor(n: Natural) extends Natural {
      def isZero = false
      def pred = n
      def + (that: Nat) = new Successor(n + that)
      def - (that: Nat) = if (that.isZero) this else (n - that.pred)
    }

------------------------------------------------------------
4.3 Functions as Objects
------------------------------------------------------------

How scala treats functions::

  trait Function1[A, B] {
    def apply(x: A) : B
  }

  val fanonymous = (x: Int) => x * x
  fanonymous(7)

  // eta-expansion
  val foject = new Function1[Int, Int] {
    def apply(x: Int) = x * x
  }
  fobject.apply(7)

  // define our own apply methods
  object List {
    def apply[T]() = new Nil
    def apply[T](x: T) = new Cons(x, new Nil)
    def apply[T](x: T, y: T) = new Cons(x, new Cons(7, new Nil))
  }

  List()
  List(1)
  List(1, 2)

------------------------------------------------------------
4.4 Subtyping and Generics
------------------------------------------------------------

Two ways to perform polymorphism:

1. Subtyping (object oriented practice)
2. Generics (functional practice)

Can specify a number of type bounds:

* [S <: T] is an upper bound (S is a subtype of T)
* [S >: T] is an lower bound (S is a supertype of T)
* [S >: T <: V] bound in an interval range

When types are wrapped, we have to consider variance:

* List[S] <: List[T] covariance
* List[S] >: List[T] contravariance

Liskov says that if A <: B, then everything one can do with
a type of B one should be able to do with a type of A (so
IEnumerable <: List):

* in java, arrays are covariant
* in scala, arrays are not covariant

------------------------------------------------------------
4.5 Variance
------------------------------------------------------------

------------------------------------------------------------
4.5 Decomposition
------------------------------------------------------------

------------------------------------------------------------
4.5 Pattern Matching
------------------------------------------------------------

============================================================
Chapter 5
============================================================
