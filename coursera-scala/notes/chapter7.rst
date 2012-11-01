============================================================
Chapter 7
============================================================

------------------------------------------------------------
7.1: Structural Induction on Trees
------------------------------------------------------------

To prove with structural induction that some property P(t)
holds for all trees t of a certain type:

1. show that P(1) holds for all leaves of 1 of a tree
2. for each type of internal node t with subtrees s1..sn
   show that P(s1) && .. && P(sn) implies P(t)

We can show an example of this::

    abstract class IntSet {
      def incl(x: Int): IntSet
      def contains(x: Int): Boolean
    }
    case class Empty extends IntSet
    case class NonEmpty(elem: Int, left: IntSet, right: IntSet)
      extends IntSet

    1. Empty contains x        = false

       a. By definition of the empty contains method

    2. (s incl x) contains x   = true

       a. Base case empty by (1)
       b. Base case NonEmpty by definition of contains method
       c. case where s includes x, reduces to s and true by (b)
       d. case where s does not include x

          i.  x < y: (s.l incl x) contains x => (b)
          ii. x > y: (s.r incl x) contains x => (b)

    3. (s incl x) contains y   = s contains y if x != y

      a. Need to show incl,contains for all cases x < y < z

------------------------------------------------------------
7.2: Streams
------------------------------------------------------------

To find the second prime between a range, however the first
implementation creates an entire list of values just to find
the second prime, can we avoid this::

    ((1000 to 10000) filter isPrime)(1)

    // avoid computing the tail until we need it
    val xs = Stream.cons(1, Stream.cons(2, Stream.empty))
    val xs = Stream(1, 2, 3)
    val ys = (1 to 1000).toStream

    // only evaluate as many values as we need
    ((1000 to 10000).toStream filter isPrime)(1)

    // lazy generator
    // (lo until hi).toStream
    def streamRange(lo: Int, hi: Int): Stream[Int] = 
      if (lo >= hi) Stream.empty
      else Stream.cons(lo, streamRange(lo + 1, hi)

    // strict generator
    def listRange(lo: Int, hi: Int): List[Int] = 
      if (lo >= hi) Nil
      else lo :: listRange(lo + 1, hi)

Streams support almost all method of List, the only exception
is the cons operator `::` which will create a list. The alternative
is the Stream.cons operator `#::` which creates a stream.

How would we implement streams::

    trait Stream[+A] extends Seq[A] {
      def isEmpty: Boolean
      def head: A
      def tail: Stream[A]

      def filter(p: T => Boolean): Stream[T] =
        if (isEmpty) this
        else if (p(head)) cons(head, tail.filter(p))
        else tail.filter(p)
    }

    object Stream {
      def cons[T](hd: T, tl: => Stream[T]) = new Stream[T] {
        def isEmpty = false
        def head = hd
        def tail = tl
      }

      val empty = new Stream[Nothing] {
        def isEmpty = true
        def head = throw new NoSuchElementException("empty.head")
        def tail = throw new NoSuchElementException("empty.tail")
      }
    }

------------------------------------------------------------
7.3: Lazy Evaluation
------------------------------------------------------------

"Do things as lazy as possible and never do them twice." This
is called lazy evaluation and is different to by-name evaluation
since the evaluation is only performed once and then stored for
futher evaluations (haskell does this for everything by default,
scala must be explicit)::

    def x = expression      // by-name evaluation
    val x = expression      // strict evaluation
    lazy val x = expression // lazy evaluation

    def expression = {
      val x = { print("x"); 1 }
      lazy val y = { print("y"); 2 }
      def z = { print("z"); 3 }
      z + y + x +z + y + x
    }
    expression              // prints xzyz

    def cons[T](hd: T, tl: => Stream[T]) = new Stream[T] {
      def isEmpty = false
      def head = hd
      lazy val tail = tl    // won't recompute each time
    }



------------------------------------------------------------
7.4: Computing with Infinite Sequences
------------------------------------------------------------

Here are examples of infinite streams::

    def from(n: Int): Stream[Int] = n #:: from(n + 1)
    val naturals = from(0)
    val multiplesOfFour = naturals map (_ * 4)
    val first100 = (multipleOsFour take 100).toList

Implementation of Sieve of Eratosthenes::

    def sieve(s: Stream[Int]): Stream[Int]a =
      s.head #:: sieve(s.tail filter (_ % s.head != 0))
    val primes = sieve(from(2))
    val first100Primes = (primes take 100).toList

What about square roots::

    def sqrtStream(x: Double): Stream[Double] = {
      def improve(guess: Double) = (guess + x / guess) / 2
      lazy val guesses: Stream[Double] = 1 #:: (guesses map improve)
      guesses
    }
    def isGoodEnough(guess: Double, x: Double) =
      math.abs((guess * guess - x) / x) < 0.0001

    sqrtStream(4) filter(isGoodEnough(_, 4)).take(10)

------------------------------------------------------------
7.5: Case Study: The Water Pouring Problem
------------------------------------------------------------

The framework::

    /**
     * A functional solution to the water pouring problem
     */
    class Pouring(capacity: Vector[Int]) {
      type Glass = Int
      type State = Vector[Int]

      // the initial states of all the glasses
      val initialState = capacity map(x => 0)

      // Classes representing the possible moves from one state to the next
      trait Move {
        /**
         * Generate the next state by performing this move
         * @param state The current state
         * @returns The state achieved by performing this move
         */
        def change(state: State): State
      }

      // a move to empty the specified glass
      case class Empty(glass: Int) extends Move {
        def change(state: State) = state updated (glass, 0)
      }

      // a move to fill the specified glass
      case class Fill(glass: Int) extends Move {
        def change(state: State) = state updated (glass, capacity(glass))
      }

      // a move to pour from one glass into another until filled
      case class Pour(from: Int, to:Int) extends Move {
        def change(state: State) = {
          val amount = state(from) min (capacity(to) - state(to))
          state updated(from, state(from) = amount) updated(to, state(to) - amount)
        }
      }

      // the glasses that are available to pour with
      val glasses = 0 until capacity.length

      // all possible move combinations from one state to the next
      val moves =
       (for (g <- glasses) yield Empty(g)) ++
       (for (g <- glasses) yield Fill(g))  ++
       (for (from <- glasses; to <- glasses if from != to) yield Pour(from, to))

       /**
        * Contains the history graph of glass moves
        * @param history The history of moves in this path
        * @param endState The final state of this path
        */
       class Path(history: List[Move], val endState: State) {
         def extend(move: Move) = new Path(move :: history, move change endState)
         overrid def toString = (history.reverse mkString " ") + "--> " + endState
       }

       // the initial path to start the graph at
       val initialPath = new Path(Nil, initialState)

       /**
        * Generates a stream of unique paths starting at paths
        * @param paths The current start paths
        * @param explored The states we have currently explored
        * @returns A lazy stream of all the unique paths
        */
       def from(paths: Set[Path], explored: Set[State]): Stream[Set[Path]] =
         if (paths.isEmpty) Stream.empty
         else {
           val more = for {
             path <- paths
             next <- moves map path.extend
             if !(explored contains next.endState)
           } yield next
           paths #:: from(more, explored ++ (more map(_.endState)))
         }

       // the path generator seeded with the initial path states
       val pathSets = from(Set(initialPath), Set(InitialState))

       /**
        * Generates a stream of all solutions to the specified target
        * @param target The target pouring value to reach
        * @returns A stream of solutions using the current glasses
        */
       def solution(target: Int): Stream[Path] =
         for {
           pathSet <- pathSets
           path <- PathSet
           if path.endState contains target
         } yield path
    }

    // a simple testing object to validate our solution
    object Tester {
      val problem = new Pouring(Vector(4, 7))
      problem.moves
      problem.pathSets.take(3).toList
      problem.solution(6)
    }

------------------------------------------------------------
7.6: Conclusion
------------------------------------------------------------

Functional programming provides a coherent set of notations
and methods based on:

1. higher order functions
2. case classes and pattern matching
3. immutable collections
4. absence of mutable state
5. flexible evaluation strategies: strict/lazy/by-name

