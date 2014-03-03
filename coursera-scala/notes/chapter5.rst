============================================================
Chapter 5
============================================================

------------------------------------------------------------
5.1 Lists
------------------------------------------------------------

Differences between arrays and Lists in Scala:

* Lists are immutable and cannot be changed
* Lists are recursive (arrays are flat)
* Lists are homogenous (all values are the same type)

List examples:

.. code-block:: scala

    val empty = List()
    val numbers = List(1, 2, 3, 4)
    val letters = 'a' :: 'b' :: 'c' :: 'd' :: Nil
    val letters = Nil.::('d').::('c').::('b').::('a')
    // so :: is actuall prepend

    [ 1 | -> ] [ 2 | ->] [ 3 | ->] [ 4 | ->] Nil

Basic List operations:

* `head`: returns the first element of the lilst
* `tail`: returns a list of all elements but the first
* `isEmpty`: returns `true` if the list is empty, otherwise `false`

Can pattern match the list like:

* `x :: xs`       - head, tail
* `Nil`           - empty list
* `x :: Nil`      - list of length 1
* `List(a, b, c)` - list of length 3

Example of pattern matching:

.. code-block:: scala

    def insert(x: T, xs: List[T]): List[T] = xs match {
      case List()  => List(x)
      case y :: ys => if (x <= y) x :: xs else y :: insert(x, ys)
    }

    def isort(xs: List[T]): List[T] = xs match {
      case List()  => List()
      case y :: ys => insert(y, isort(ys))
    }

------------------------------------------------------------
5.2 More on Lists
------------------------------------------------------------

What follows are a few more list functions:

* `list.length`: the number of elements in the list
* `list.last`: the last element in the list
* `list.init`: a new list of all elements but the last
* `list.take(n)`: a list consisting of the first n values
* `list.drop(n)`: a list consisting of all values but first n
* `list(n)`: value at index n in list
* `list.reverse`: reverses a lits
* `list.updated(n, x)`: create a new list with element n change to x
* `xs ++ ys`: combine two lists
* `list.indexOf(x)`: return the index of element x or `None`
* `list.contains(x)`: `true` if the list contains x, else `false`

Examples of how some of these are implemented:

.. code-block:: scala

    def length[T](xs: List[T]): Int = xs match {
      case List()  => 0
      case y :: ys => 1 + length(ys)
    }

    def last[T](xs: List[T]): T = xs match {
      case List() => throw new Error("last")
      case List(x) => x
      case y :: ys => last(ys)
    }

    def init[T](xs: List[T]): T = xs match {
      case List() => throw new Error("last")
      case List(x) => List()
      case y :: ys => y :: init(ys)
    }

    // xs ::: ys
    def concat[T](xs: List[T], ys: List[T]): List[T] = xs match {
      case List() => ys
      case z :: zs => z :: concat(zs, ys)
    }

    def reverse[T](xs: List[T]): List[T] = xs match {
      case List() => xs
      case y :: ys => reverse(ys) ++ List(y)
    }

    // (xs take n) ::: (xs drop n + 1)
    def removeAt[T](xs: List[T], n: Int): List[T] = xs match {
      case List() => xs
      case y :: ys => if (n == 0) ys else y :: removeAt(ys, n - 1)
    }

    def flatten(xs: List[Any]): List[Any] = xs match {
      case (y:List[Any]) :: ys => flatten(y) ::: flatten(ys)
      case y :: ys => y :: flatten(ys)
      case Nil => xs
    }

------------------------------------------------------------
5.3 Pairs and Tuples
------------------------------------------------------------

How to use tuples:

.. code-block:: scala

    val pair = ("answer", 42) 
    val (label, value) = pair

    scala.Tuplen[T1...Tn]
    scala.Tuplen(T1...Tn)

    case class Tuple2[T1, T2](_1: +T1, _2: +T2)

Example merge sort implementation:

.. code-block:: scala

    def merge(xs: List[T], ys: List[T]): List[T] = (xs, ys) match {
      case (Nil, ys) => ys
      case (xs, Nil) => xs
      case (x :: xsl, y :: ysl) =>
        if (x < y) x :: merge(xsl, ys)
        else y :: merge(xs, ysl)
    }

    def msort(xs: List[T]): List[T] = {
      val n = xs.length/2
      if (n == 0) xs
      else {
        val (fst, snd) = xs splitAt n
        merge(msort(fst), msort(snd))
      }
    }
    
------------------------------------------------------------
5.4 Implicit Parameters
------------------------------------------------------------

Parameterize the merge on `T` so can make `msort` generic:

.. code-block:: scala

   def msort[T](xs: List[T])(lt: (T, T) => Boolean): List[T] =
   ...
   if (lt(x, y)) x :: merg(xsl,, ys)
   ...
   msort(nums)((x: Int, y: Int) => x < y)
   msort(fruits)((x: String, y: String) => x.comareTo(y) < 0)

   scala.math.Ordering[T]
   def msort[T](xs: List[T])(ord: Ordering[T]): List[T] =
   ...
   ord.lt(x, y)
   if (ord.lt(x, y)) x :: merg(xsl,, ys)
   ...
   msort(nums)(Ordering.Int)

   def msort[T](xs: List[T])(implicit ord: Ordering[T]): List[T] =
   msort(nums)

A function can take an implicit parameter:

* It must be marked implicit
* must be one non colliding matching type
* implicit must be visible at the point of the function call

------------------------------------------------------------
5.5 Higher Order List Functions
------------------------------------------------------------

There are several recurring patterns while working on lists:

1. `map`: transforming each element in a list
2. `filter`: retrieveing a list of elements satisfying a condition
3. `reduce`: combining elements of a list using an operator

Examples of their usage:

.. code-block:: scala

    // simplified version (not tail recursive)
    abstract class List[T] {
      def map[U](f: T => U): List[U] = this match {
        case Nil     => this
        case x :: xs => f(x) :: xs.map(f)
      }
    }

    val scaled  = xs map(x => x * 5)
    val squared = xs map(x => x * x)

    // simplified version (not tail recursive)
    abstract class List[T] {
      def filter(p: T => Boolean): List[T] = this match {
        case Nil     => this
        case x :: xs => if (p(x)) x :: xs.filter(p) else xs.filter(p)
      }
    }

    val positive = xs filter(x => x > 0)

    def pack[T](xs: List[T]): List[List[T]] = xs match {
      case Nil      => Nil
      case x :: xsl =>
        val (first, rest) = xs span(y => y == x)
        first :: pack(rest)
    }
    pack(List('a', 'a', 'a', 'b', 'c', 'c', 'a'))

    def encode[T](xs: List[T]): List[T, Int)] =
      pack(xs) map (ys => (ys.head, ys.length))
    encode(List('a', 'a', 'a', 'b', 'c', 'c', 'a'))

There are a number of other higher order filter functions:

* `xs filterNot p` - `xs filter(x => !p(x))`
* `xs partition p` - (`xs filter p`, `xs filterNot p`)
* `xs takeWhile p` - takes longest prefix of match
* `xs dropWhile p` - takes the remainder of `takeWhile`
* `xs span p`      - (`xs takeWhile p`, `xs dropWhile p`)

------------------------------------------------------------
5.6 Reduction on Lists
------------------------------------------------------------

Examples using the higher order list fold operations:

.. code-block:: scala

    def sum(xs: List[Int]): Int = xs match {
      case Nil     => 0
      case y :: ys => y + sum(ys)
    }

    def sum(xs: List[Int])  = (0 :: xs) reduceLeft((x, y) => x + y)
    def prod(xs: List[Int]) = (1 :: xs) reduceLeft((x, y) => x * y)

`reduceLeft` does not work on empty lists, `foldLeft` does by taking an
initial accumulator:

.. code-block:: scala

    def sum(xs: List[Int])  = (xs foldLeft 0)(_ + _)
    def prod(xs: List[Int]) = (xs foldLeft 1)(_ * _)

    abstract class List[T] {
      def reduceLeft(op: (T, T) => T): T = this match {
        case Nil     => throw new Error("empty")
        case x :: xs => (xs foldLeft x)(op)
      }

      def foldLeft[U](zero: U)(op: (U, T) => U): U = this match {
        case Nil     => zero
        case x :: xs => (xs foldLeft op(zero, x))(op)
      }
    }

`reduceLeft` and `foldLeft` reduce to the left, there are also `reduceRight`
and `foldRight` that reduces to the right:

.. code-block:: scala

    abstract class List[T] {
      def reduceRight(op: (T, T) => T): T = this match {
        case Nil      => throw new Error("empty")
        case x :: Nil => x
        case x :: xs  => op(x, xs.reduceRight(op))
      }

      def foldRight[U](zero: U)(op: (U, T) => U): U = this match {
        case Nil     => zero
        case x :: xs => op(x, (xs foldRight zero)(op))
      }
    }

If the operator is associative and commutative, left and right will
return the same results. However, some results may only be appropriate
for one version:

.. code-block:: scala

    // here foldLeft would not work correctly as :: isn't on T
    def concat[T](xs: List[T], ys: List[T]): List[T] = 
      (xs foldRight ys) (_ :: _)

    def lengthFun[T](xs: List[T]): Int =
      (xs foldRight 0)((n, t) => t + 1)

    def mapFun[T, U](xs: List[T], f: T => U): List[U] =
      (xs foldRight List[U]())(f(_) :: _)

------------------------------------------------------------
5.7 Reasoning About Concat
------------------------------------------------------------

For list concat, we prove that it is correct by:

* `Nil ++ xs`
* `xs ++ Nil`
* `(xs ++ ys) ++ zs == xs ++ (ys ++ zs)`

Structural induction can be used to prove functions:

* referential transparency can be used to reduce functions as
  pure functional languages are side effect free.
* for lists, show `P(Nil)` holds
* for lists, show if `P(xs)` holds, then `P(x :: xs)` holds
* fold/unfold method to induction

1. Show that we have `P(x)` for the base case
2. For all values >= b, show the induction step (if we have `P(x)`
   then we also have `P(x + 1)`


------------------------------------------------------------
5.8 A Larger Proof on Lists
------------------------------------------------------------
