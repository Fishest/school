============================================================
Chapter 6
============================================================

------------------------------------------------------------
6.1 Other Collections
------------------------------------------------------------

Lists are linear in access time (the start is quicker to
access than the middle or end). Vectors are trees of
32 element bucket chains:

- vectors great cache locality, lists may not
- vectors are O(logN) for search, lists are O(n)
- `x +: xs` creates a new Vector with x followed by xs
- `xs :+ x` creates a new Vector with xs followed by x
- cons for list is O(1), O(logN) for vector
- have to clone parents to root to keep Vector immutable

List and Vector are subclasses of Seq which is a subset of
Iterable. Arrays and Strings are implicitly converted to Seq::

    val a = Array(1, 2, 3, 4)
    val m = a map (x => x * 2)
    val s = "Hello World"
    val u = s filter (c => c.isUpper)

Ranges allow us to specify evenly spaced range values, they
are represented as a class with fields(start, stop, step)::

    val r: Range = 1 until 5
    val s: Range = 1 to 5
    val t: Range = 1 to 10 by 3
    val u: Range = 6 to 1 by -2

There are a number of operations on Seq:

- xs exists p  = checks if the predicate exists once in xs
- xs forall p  = checks if the predicate exists for all xs
- xs zip ys    = List[(T, U)]
- pair unzip   = (List[T], List[U])
- xs flatMap f = applies all elements to f and concats result
- xs sum       = the aggregate sum of the elements
- xs product   = the aggregate product of the elements
- xs max       = the largest value in xs
- xs min       = the smallest value in xs

Examples::

    // to list all the combinations of 1..M and 1..N
    (1 to M) flatMap (x => (1 to N) map (y => (x, y)))

    // scalar product of two vectors
    (xs zip ys) map(xy => xy._1 * xy._2) sum
    (xs zip ys) map { case (x,y) => x * y } sum

    def isPrime(n: Int): Boolean =
      (2 until n) forall(d => n % d != 0)

------------------------------------------------------------
6.2 Combinatorial Search
------------------------------------------------------------

Can replace nested loops with higher order functions on
sequences::

    val n = 7
    (1 until n) map (i =>
      (1 until i) map (j => (i, j)).flatten

    //xs flatMap f = (xs map f).flatten
    val pairs = (1 until n) flatMap (i =>
      (1 until i) map (j => (i, j))
    val primes = pairs filter(pair => isPrime(pair._1 + pair._2))

    // example of for expressions
    case class Person(name: String, age: Int)
    // equal expression
    // persons filter(p => p.age > 20) map (p => p.name)
    for (p <- persons if p.age > 20) yield p.name

`for ( s ) yeild e`:

- s is a sequence of generators and filters
- e is an expression whose value is returned by iteration
- generator is of the form p <- e (p is a pattern and e is
  an expression whose value is a collection)
- A filter is of the form `if f` where f is a predicate
- The sequence must start with a generator
- If there are several, the last should vary faster than the
  first.

Can use {} instead of () so you don't have to put ; between::

    // prime tuples
    for {
      i <- 1 until n
      j <- 1 until i
      if isPrime(i + j)
    } yield (i, j)

    // scalar product
    (for {
      (x,y) <- xs zip ys
    } yield x * y).sum


------------------------------------------------------------
6.3 Combinatorial Search Examples
------------------------------------------------------------

Sets have most of the operations on sequences. They can be
created in a few ways::

    val fruit = Set("apple", "banana", "pear")
    val s = (1 to 6).toSet

Principals of sets:

1. Sets are unordered
2. Sets do not have duplicate values
3. The fundamental operation is contains: `s contains 5`

------------------------------------------------------------
6.4 Queries with For
------------------------------------------------------------

The for notation is essentially equivalent to the common
operations for querying a database::

    case class Book(title: String, authors: List[String])
    ...
    for (b <- books; a <- b.authors if a startsWith "Bird,")
    yield b.title

    // select title from books if title contains "Program"
    for (b <- books; if b.title indexOf "Program" >= 0)
    yield b.title

    val authors = for {
      b1 <- books
      b2 <- books
      // if != b2 would cause repeats
      if b1.title < b2.title
      a1 <- b1.authors
      a2 <- b2.authors
      if a1 == a2
    } yield a1
    authors.distinct // to remove duplicates for 3 authors

------------------------------------------------------------
6.5 Translation of For
------------------------------------------------------------

The syntax of for is closely related to the higher order
functions map, flatMap, and filter::

    def mapFun[T, U](xs: List[T], f: T => U): List[U] =
      for (x <- xs) yield f(x)

    def flatMapFun[T, U](xs: List[T], f: T => Iterable[U]): List[U] =
      for (x <- xs; y <- f(x)) yield y

    def filterFun[T](xs: List[T], f: T => Boolean): List[T] =
      for (x <- xs if p(x)) yield x

However, scala converts these the other way during compilation::

    // for (x <- e1) yield e2
    e1.map(x => e2)

    // for (x <- e1 if f; s) yield e2
    // withFilter is a lazy filter operation
    for (x <- e1.withFilter(x => f); s) yield e2

    // for (x <- e1; y <- e2; s) yield e3
    e1.flatMap(x => for (y <- e2; s) yield e3)

    //
    // for {
    //   i <- 1 until n
    //   j <- 1 until j
    //   if isPrime(i + j)
    // } yield (i, j)
    //
    (1 until n).flatMap(i =>
      (1 until i).withFilter(j => isPrime(i + j))
        .map(j => (i, j)))

    //
    // for (b <- books; a <- b.authors if a startsWith "Bird")
    // yield b.title
    //
    books.flatMap(b =>
      b.authors.withFilter(a => a startsWith "Bird")
        .map(c => c.title)

If you want to use for expressions on your own types, just implement
map, flatMap, and withFilter for these types:

* ScalaQuery
* Slick
* Microsoft LINQ

------------------------------------------------------------
6.6 Maps
------------------------------------------------------------

------------------------------------------------------------
6.6 Putting the Pieces Together
------------------------------------------------------------
