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

    trait List[+T] {
      def isEmpty: Boolean
      def head: T
      def tail: List[T]
      def prepend [U >: T](elem: U): List[U] = new Cons(elem, this)
    }

    class Cons[T](val head: Int, val tail: List[T]) extends List[T] {
      def isEmpty: Boolean = false
    }

    object Nil extends List[Nothing] {
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
* otherwise is nonvariant

Liskov says that if A <: B, then everything one can do with
a type of B one should be able to do with a type of A (so
IEnumerable <: List):

* in java, arrays are covariant
* in scala, arrays are not covariant

------------------------------------------------------------
4.5 Variance
------------------------------------------------------------

Can specify the variance of types in scala:

* class C[+A] is covariant
* class C[-A] is contravariant
* class C[A]  is nonvariant

Mutable types should not be covariant, immutable can be::

Functions are contravaiant in their agrument types and
covariant in their result type. Invariant types can
appear anywhere::

    package scala;
    trait Function[-T, +U] {
      def apply(x: T): U
    }
  A2 <: A1 and B1 <: B2
  A1 => B1  <: A2 => B2


------------------------------------------------------------
4.6 Decomposition
------------------------------------------------------------

Expression example::

    trait Expression {
      def isNumber: Boolean
      def isSum: Boolean
      def numValue: Int
      def leftOp: Expr
      def rightOp: Expr
    }

    class Number(n: Int) extends Expr {
      def isNumber: true
      def isSum: false
      def numValue: n
      def leftOp: throw new Error()
      def rightOp: throw new Error()
    }

    class Sum(e1: Expr, e2: Expr) extends Expr {
      def isNumber: false
      def isSum: true
      def numValue: throw new Error()
      def leftOp: e1
      def rightOp: e2
    }

    def eval(e: Expr): Int = {
      if (e.isNumber) e.numValue
      else if (e.isSum) eval(e.leftOp) eval(e.rightOp)
      else throw new Error()
    }

    val result = eval(new Sum(new Number(1), new Number(2)))

How can we make eval lighter::

    // java style test and cast
    type.isInstanceOf[T]: Boolean
    type.asInstanceOf[T]: T

    // easier
    trait Expression {
      def eval: Int
      def show: String
    }

    class Number(n: Int) extends Expr {
      def eval: Int = n
    }

    class Sum(a: Expr, b: Expr) extends Expr {
      def eval: Int = a.eval + b.eval
    }

------------------------------------------------------------
4.7 Pattern Matching
------------------------------------------------------------

The sole purpose of test and access methods is to reverse
the construction process. This is a common problem, so fp
languages automate it with pattern matching.

This is facilited with case classes, which are used like::

    val nval = Number(1) // implicit companion factory
    def eval(e: Expr): Int = e match { // expression problem
      case Number(n) => n
      case Sum(e1, e2) => eval(e1) + eval(e2)
    }

    def show(e: Expr): String = e match {
      case Number(n) => n.toString
      case Sum(e1, e2) => show(e1) + " + " + show(e2)
    }

Can pattern match on the following:

* constructors: Number(n)
* variables: a,b,c
* wildcard: _
* constants: (1, true, 'a')
* combined: case Sum(Number(1), Number(n)) => n
