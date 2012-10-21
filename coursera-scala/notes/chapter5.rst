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

List examples::

    val empty = List()
    val numbers = List(1, 2, 3, 4)
    val letters = 'a' :: 'b' :: 'c' :: 'd' :: Nil
    val letters = Nil.::('d').::('c').::('b').::('a')
    // so :: is actuall prepend

    [ 1 | -> ] [ 2 | ->] [ 3 | ->] [ 4 | ->] Nil

Basic List operations:

* head: returns the first element of the lilst
* tail: returns a list of all elements but the first
* isEmpty: returns 'true' if the list is empty, otherwise 'false'

Can pattern match the list like:

* x :: xs (head, tail)
* Nil (empty list)
* x :: Nil (list of length 1)
* List(a, b, c) (list of length 3)

Example of pattern matching::

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

* list.length: the number of elements in the list
* list.last: the last element in the list
* list.init: a new list of all elements but the last
* list.take(n): a list consisting of the first n values
* list.drop(n): a list consisting of all values but first n
* list(n): value at index n in list
* list.reverse: reverses a lits
* list.updated(n, x): create a new list with element n change to x
* xs ++ ys: combine two lists
* list.indexOf(x): return the index of element x or None
* list.contains(x): true if the list contains x, else false

Examples of how some of these are implemented::

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

How to use tuples::

    val pair = ("answer", 42) 
    val (label, value) = pair

    scala.Tuplen[T1...Tn]
    scala.Tuplen(T1...Tn)

    case class Tuple2[T1, T2](_1: +T1, _2: +T2)

Example merge sort implementation::

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
    
