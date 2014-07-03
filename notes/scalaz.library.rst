================================================================================
Scalaz
================================================================================

.. todo:: http://vimeo.com/10482466
.. todo:: http://eed3si9n.com/learning-scalaz/Combined+Pages.html

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Scalaz provides purely functional data structures to complement those from the
Scala standard library. It defines a set of foundational type classes
(e.g.  Functor, Monad) and corresponding instances for a large number of data
structures.

.. code-block:: scala

    //
    // Simply save this to build.sbt and then run sbt console
    //
    scalaVersion := "2.11.0"

    val scalazVersion = "7.0.6"

    libraryDependencies ++= Seq(
      "org.scalaz" %% "scalaz-core" % scalazVersion,
      "org.scalaz" %% "scalaz-effect" % scalazVersion,
      "org.scalaz" %% "scalaz-typelevel" % scalazVersion,
      "org.scalaz" %% "scalaz-scalacheck-binding" % scalazVersion % "test"
    )

    scalacOptions += "-feature"

    initialCommands in console := "import scalaz._, Scalaz._"

--------------------------------------------------------------------------------
Polymorphism Overview
--------------------------------------------------------------------------------

* **Parametric Polymorphism**

  Parametric polymorphism refers to when the type of a value contains one or
  more (unconstrained) type variables that may be adopted to any type:

.. code-block:: scala

    def head[A](list: List[A]): A = list(0)

* **Subtype Polymorphism**

  We can add extra functionality to a type by creating a subtype trait for
  it, however, we have to pull it in everytime we want to use it:

.. code-block:: scala

    trait Plus[A] {
        def plus(a2: A): A
    }

    def plus[A <: Plus[A]](a1: A, a2: A): A = a1.plus(a2)

* **Adhoc Polymorphism**

  Scala implicits allow for adhoc polymorphism that can allow different
  functions for different types of `A`, types can be extended without
  their source, the functions can be enabled or disabled in different
  scopes:

.. code-block:: scala

    trait Plus[A] {
        def plus(a2: A): A
    }

    def plus[A : Plus[A]](a1: A, a2: A): A = implicitly[Plus[A]].plus(a1, a2)


--------------------------------------------------------------------------------
Monoid Overview
--------------------------------------------------------------------------------

Monoid is a type for which there exists a function `mappend`, which produces
another type in the same set; and also a function that produces a zero:

.. code-block:: scala

    //
    // The base trait for a monoid which abstracts adding two instances of
    // the same type and supplying a zero of that type.
    //
    trait Monoid[A] {
        def mappend(a: A, b: A): A
        def mzero: A
    }

    //
    // Package all the monoid instances into an object to use scala's implicit
    // resolution rules (when it needs an implicit parameter of some type it will
    // look for anything in scope as well as including the companion object of the
    // type being searched for).
    //
    object Monoid {
        implicit val IntMonoid =  new Monoid[Int] {
            def mappend(a: Int, b: Int):Int = a + b
            def mzero:Int  = 0
        }

        implicit val StringMonoid =  new Monoid[String] {
            def mappend(a: String, b: String):String = a + b
            def mzero:String  = ""
        }
    }

    // specifying a monoid to abstract the algebra
    def sum[A](xs: List[A], m: Monoid[A]): A =
        xs.foldLeft(m.mzero)(m.mappend)

    // using implicits so the type doesn't have to be specified
    def sum[A: Monoid](xs: List[A])(implicit m: Monoid[A]): A =
        xs.foldLeft(m.mzero)(m.mappend)

    // re-written using context bounds instead of implicity partials
    def sum[A: Monoid](xs: List[A]): A = {
        val m = implicitly[Monoid[A]]
        xs.foldLeft(m.mzero)(m.mappend)
    }

--------------------------------------------------------------------------------
Fold Overview
--------------------------------------------------------------------------------

The idea of reducing a list to a single element is abstracted with the idea
of folding:

.. code-block:: scala

    // we can extract the idea of folding out to a trait
    trait FoldLeft[F[_]] {
        def foldLeft[A, B](xs: F[A], zero: B, func: (B, A) => B): B
    }

    // then create a few implementations of it, say for list
    object FoldLeft {
        implicit val FoldLeftList = new FoldLeft[List] {
            def foldLeft[A, B](xs: List[A], zero: B, func: (B, A) => B) =
                xs.foldLeft(zero)(func)
        }
    }

    // now our sum function can work with anything that is foldable
    def sum[M[_]: FoldLeft, A: Monoid](xs: M[A]): A = {
        val m = implicitly[Monoid[A]]
        val f = implicitly[FoldLeft[M]]
        f.foldLeft(xs, m.mzero, m.mappend)
    }

The two types `Monoid` and `FoldLeft` are typeclasses which come from
haskell. Scalaz defines many of these typeclasses which can be used to
define functions in terms of capabilities that are needed and nothing
more.

--------------------------------------------------------------------------------
Scalaz Method Enrichment Summary
--------------------------------------------------------------------------------

Say we would like to provide an operator to perform the plus operation instead
of creating a method:

.. code-block:: scala

    trait MonoidOp[A] {
        val monoid: Monoid[A]
        val value: A
        def \|+|(a2: A) = monoid.mappend(value, a2)
    }

    implicit def toMonoidOp[A: Monoid[A]](a: A) = new MonoidOp[A] {
        val monoid = implicitly[Monoid[A]]
        val value  = a
    }

    3 |+| 4
    "a" |+| "b"

Scalaz offers a number of shortcut syntax for scala if you want to use it:

.. code-block:: scala

    1.some | 2       == Some(1).getOrElse(2)
    (1 > 10) ? 1 | 2 == if (1 > 10) 1 else 2

--------------------------------------------------------------------------------
Scalaz Typeclasses
--------------------------------------------------------------------------------

* **Equal**

  Instead of the standard `==`, `Equal` enables `===`, `=/=`, and `assert_===`
  syntax by declaring equal method. The main difference is that `===` will fail
  compilation if you tried to compare Int and String.

Note: I originally had /== instead of =/=, but Eiríkr Åsheim pointed out to me:

.. code-block:: scala

    1 == 1                 // true
    1 == 2                 // false
    1 != "two"             // true
    1.some /= 2.some       // true
    1.some == "two".some   // false

    1 === 1                // true
    1 === 2                // false
    1 =/= "two"            // compile error
    1.some =/= 2.some      // true
    1.some === "two".some  // compile error

    1 =/= 2 && true        // true

* **Order**

  This enables rich order comparision using the `Order` typeclass.
  It provides new methods `gt`, `lt`, `lte`, `gte`, `min`, `max`,
  and `?|?` which returns `Ordering { LT, GT, EG }`:

.. code-block:: scala

    2 gt 1                 // true
    1 lt 5                 // true
    1.0 gte 1              // compile error
    "a" ?|? "b"            // Ordering.LT

* **Show**

  This enables the `show` method on all implemented types which
  converts the type to its string representation as a `scalaz.Chord`.
  It also includes the alternative `shows` which converts to a
  standard `String`:

.. code-block:: scala

    2.show
    5.0.shows
    "a".show

* **Enum**

  Instead of the standard `to`, `Enum` enables `|->` that returns a
  List by declaring `pred` and `succ` methods on top of the `Order`
  typeclass. There are a number of operations it enables:
  `-+-`, `---`, `from`, `fromStep`, `pred`, `predx`, `succ`, `succx`,
  `|-->`, `|->`, `|==>`, `|=>`.

.. code-block:: scala

    1 to 5      // Range(1, 2, 3, 4, 5), starndard scala

    'c'.pred  === 'a'.succ
    'c'.predx === 'b'.some
    'a'.succx === 'b'.some

    5 --- 6   === -1
    5 -+- 6   === 11

    'a'.from.take(10)            === 'a' \|=> 'i'     // return EphemeralStream
    2.fromStep(2).take(5)        === 2 \|==>(2, 10)   // return EphemeralStream
    'a'.from.take(10).toList     === 'a' \|-> 'i'     // return List
    2.fromStep(2).take(5).toList === 2 \|-->(2, 10)   // return List

    implicitly[Enum[Char]].min                        // return Option[minimum bound]
    implicitly[Enum[Int]].max                         // return Option[maximum bound]

One can make their own types work with the scalaz typeclasses,
however it should be noted that some of the scalaz typeclasses
are non-variant making inheritence an issue:

.. code-block:: scala

    case class TrafficLight(name: String)
    val red    = TrafficLight("red")
    val yellow = TrafficLight("yellow")
    val green  = TrafficLight("green")
    implicit val TrafficLightEqual: Equal[TrafficLight] = Equal.equal(_ == _)

    red === yellow     // false
    red === red        // true
    red === "red"      // compile error

--------------------------------------------------------------------------------
Custom Typeclass
--------------------------------------------------------------------------------

.. code-block:: scala

    trait CanTruthy[A] { self =>
        def truths(a: A): Boolean
    }

    object CanTruthy {
        def apply[A](implicit ev: CanTruthy[A]): CanTruthy[A] = ev
        def truthys[A](f: A => Boolean): CanTruthy[A] = new CanTruthy[A] {
            def truths(a: A): Boolean = f(a)
        }
    }

    trait CanTruthyOps[A] {
        def self: A
        implicit def F: CanTruthy[A]
        final def truthy: Boolean = F.truthys(self)
    }

    // import CanIsTruthyOpts._
    object CanIsTruthyOps {
        implicit def toCanIsTruthyOps[A](v: A)(implicit ev: CanTruthy[A]) {
            new CanTruthyOps[A] {
                def self: A = v
                implicit def F: CanTruthy[A] = ev
            }
        }
    }

We can now define the typeclass for the various types that we
plan to use it with:

.. code-block:: scala

    //
    // Define truthiness for integers
    //
    implicit val intCanTruthy: CanTruthy[Int] = CanTruthy.truthys({
        case 0 => false
        case _ => true
    })

    0.truthy
    1.truthy

    //
    // Define truthiness for Lists
    // we actually need to create a special implicit for Nil because
    // of the variance issue.
    //
    implicit val nilCanTruthy: CanTruthy[scala.collection.immutable.Nil.type] = CanTruthy.truthys(_ => false)
    implicit def listCanTruthy[A]: CanTruthy[List[A]] = CanTruthy.truthys({
        case Nil => false
        case _   => true
    })

    Nil.truthy
    List(1).truthy

    //
    // Boolean is simply the identity function
    //
    implicit val boolCanTruthy: CanTruthy[Boolean] = CanTruthy.truthys(identity)

    false.truthy
    true.truthy

Finally, we can make a new method that simulates `if then else`:

.. code-block:: scala

    def truthyIf[A: CanTruthy, B, C](cond: A, ifyes: => B, ifnot: => C) =
        if (cond.truthy) ifyes else ifnot

    truthyIf(Nil) { "this is true" } { "this is false" }
    truthyIf(1)   { "this is true" } { "this is false" }

--------------------------------------------------------------------------------
Functor
--------------------------------------------------------------------------------

`Functor` describes a typeclass that can be mapped over:

*We can think of fmap as] a function that takes a function and returns a new
function that’s just like the old one, only it takes a functor as a parameter
and returns a functor as the result. It takes an a -> b function and returns
a function f a -> f b. This is called lifting a function.*

.. code-block:: scala

    trait Functor[F[_]] { self =>
        def map[A, B](fa: F[A])(f: A => B): F[B] // lift f into F and apply to F[A]
    }

    trait FunctorOps[F[_], A] extends Ops[F[A]] {
      implicit def F: Functor[F]
      import Leibniz.===

      final def map[B](f: A => B): F[B] = F.map(self)(f)
    }

    List(1, 2, 3) map { _ + 2 }              // mapping over a list
    (1, 2, 3) map { _ + 2 }                  // mapping over a tuple
    (((x: Int) => x + 1) map { _ * 7 })(3)   // mapping over a function (composition)

    //
    // Note that the functor composition is reversed from
    // f compose g
    //
    val multBy2 = Functor[List].lift {(_: Int) * 2}
    multBy2(List(1, 2, 4))       // List(2, 4, 8)
    List(1, 2, 3) >| "x"         // List[String] = List(x, x, x)
    List(1, 2, 3) as "x"         // List[String] = List(x, x, x)
    List(1, 2, 3).fpair          // List[(Int, Int)] = List((1,1), (2,2), (3,3))
    List(1, 2, 3).strengthL("x") // List[(String, Int)] = List((x,1), (x,2), (x,3))
    List(1, 2, 3).strengthR("x") // List[(Int, String)] = List((1,x), (2,x), (3,x))
    List(1, 2, 3).void           // List[Unit] = List((), (), ())

--------------------------------------------------------------------------------
Applicative
--------------------------------------------------------------------------------

`pure` should take a value of any type and return an applicative value with that
value inside it. Better said is that it takes a value and puts it in some sort
of default (or pure) context:

.. code-block:: scala

    List(1, 2, 3, 4) map {(_: Int) * (_:Int)}  // type mismatch, needs two arguments
    val apply = List(1, 2, 3, 4) map {(_: Int) * (_:Int)}.curried // can curry to fix this
    apply map { _(9) }

    trait Applicative[F[_]] extends Apply[F] { self =>
      // basically an abstract constructor for a context
      def point[A](a: => A): F[A]

      // alias for `point`
      def pure[A](a: => A): F[A] = point(a)
    }

    1.point[List]
    1.point[Option] map { _ + 2 }

Including the `Apply` typeclass enables the `<*>`, `<*`, `*>` operators which can be
thought of as a beefed-up `fmap`. Whereas `fmap` takes a function and a functor and
applies the function inside the functor value, `<*>` takes a functor that has a
function in it and another functor and extracts that function from the first functor
and then maps it over the second one:

.. code-block:: scala

    trait Apply[F[_]] extends Functor[F] { self =>
      def ap[A,B](fa: => F[A])(f: => F[A => B]): F[B]
    }

    9.some <*> {(_: Int) + 3}.some
    3.some <*> { 9.some <*> {(_: Int) + (_: Int)}.curried.some }
    // the other two operators return the lhs or rhs respectively
    List(9) <* List({ (_:Int) + 2 })

    ^(9.some, 5.some) { _ + _ }    // there is also an applicative helper
    (9.some |@| 5.some) { _ + _ }  // using the applicative builder

    List(1, 2, 3) <*> List((_: Int) * 0, (_: Int) + 2, (_: Int) * 5)
    (List("a", "b", "c") |@| List("!", "?", ".")) { _ + _ }

We can take this further and make more powerful utility applicative
methods:

.. code-block:: scala

    val lifted = Apply[Option].lift2((_: Int) :: (_: List[Int]))
    lifted(3.some, List(4).some) // Some(List(3, 4))

    def sequenceA[F[_]: Applicative, A](list: List[F[A]]): F[List[A]] = list match {
        case Nil     => (Nil: List[A]).point[F]
        case x :: xs => (x |@| sequenceA(xs)) {_ :: _} 
    }

    sequenceA(List(1.some, 2.some))   // Some(List(1, 2))
    sequenceA(1.some :: None :: Nil)) // None

--------------------------------------------------------------------------------
Kinds
--------------------------------------------------------------------------------

In order to reason about values, we have types. However, we can also reason
about types by using the type's type, known as a kind.

Int and every other types that you can make a value out of is called a proper
type and denoted with a symbol `*` (read “type”). This is analogous to value 1
at value-level.

A first-order value, or a value constructor like `(_: Int) + 3`, is normally
called a function. Similarly, a first-order-kinded type is a type that accepts
other types to create a proper type. This is normally called a type constructor.
`Option`, `Either`, and `Equal` are all first-order-kinded. To denote that these
accept other types, we use curried notation like `* -> *` and `* -> * -> *`.
Note, `Option[Int]` is `*` while `Option` is `* -> *`.

A higher-order value like `(f: Int => Int, list: List[Int]) => list map {f}`, is
a function that accepts other functions and is normally called higher-order
function. Similarly, a higher-kinded type is a type constructor that accepts
other type constructors. These are denoted as `(* -> *) -> *`. All of the types in
scala can be investigated using the `:kind <-v> <type>` operation in the repl.

The newtype keyword in Haskell is made for the cases when we want to just take
one type and wrap it in something to present it as another type. In scala, we 
do this using the newly added tagged types:

.. code-block:: scala

    type Tagged[U] = { type Tag = U }
    type @@[T, U] = T with Tagged[U]  // essentially case class Tag(v: T)

    sealed trait KiloGram
    def KiloGram[A](a: A): A @@ KiloGram = Tag[A, KiloGram](a)

    sealed trait JoulePerKiloGram
    def JoulePerKiloGram[A](a: A): A @@ JoulePerKiloGram = Tag[A, JoulePerKiloGram](a)
    def energyR(m: Double @@ KiloGram): Double @@ JoulePerKiloGram
        = JoulePerKiloGram(299792458.0 * 299792458.0 * m)


    val mass = KiloGram(20.0)   // 20.0: scalaz.@@[Double,KiloGram]
    val result = 2 * mass       // 40.0: Double
    val energy = energyR(mass)  // 1.79751035747363533E18: scalaz.@@[Double,JoulePerKiloGram]
    energyR(10.0)               // compile error, type mismatch

--------------------------------------------------------------------------------
Monoids
--------------------------------------------------------------------------------

A monoid is when you have an associative binary function and a value which acts
as an identity with respect to that function:

.. code-block:: scala

    // extends semigroup with identity
    trait Monoid[A] extends SemiGroup[A] { self =>
      def zero: A
    }

    // defines the associative binary operation
    trait Semigroup[A] { self =>
      def append(a1: A, a2: => A): A
    }

    // adds aliases for append
    trait SemigroupOps[A] extends Ops[A] {
      final def \|+|(other: => A): A = A.append(self, other)
      final def mappend(other: => A): A = A.append(self, other)
      final def ⊹(other: => A): A = A.append(self, other)
    }

    "one" |+| "two"
    List(1, 2, 3) |+| List(4, 5, 6)

    Monoid[List[Int]].zero  // List()
    Monoid[String].zero     // ""

To choose which monoid operation to use (multiple, addition, etc),
we use scala tags. There are 8 possible tags defined for monoids:

.. code-block:: scala

    10 |+| Monoid[Int].zero // addition is the default
    Tags.Multiplication(10) |+| Monoid[Int @@ Tags.Multiplication].zero
    Tags.Disjunction(true)  |+| Tags.Disjunction(false)  // true, || operation
    Tags.Conjunction(true)  |+| Tags.Conjunction(false)  // false, && operation
    Monoid[Ordering].zero   |+| (Ordering.LT: Ordering)  // ordering monoid

    // the ordering monoid can be used to chain comparisons
    def lengthCompare(lhs: String, rhs: String): Ordering =
        (lhs.length ?|? rhs.length) |+| (lhs ?|? rhs)

    lengthCompare("zen", "ants")  // Ordering.LT
    lengthCompare("zen", "ant")   // Ordering.GT

--------------------------------------------------------------------------------
Functor Laws
--------------------------------------------------------------------------------

All functors respect a few laws which. The first functor law states that if we
`map` the `id` function over a functor, the functor that we get back should
be the same as the original functor:

.. code-block:: scala

    List(1, 2, 3) map {identity} assert_=== List(1, 2, 3)

The second functor law state that composing two functions and then mapping the
resulting function over a functor should be the same as first mapping one
function over the functor and then mapping the other one:

.. code-block:: scala

    (List(1, 2, 3) map {{(_: Int) * 3} map {(_: Int) + 1}}) assert_===
    (List(1, 2, 3) map {(_: Int) * 3} map {(_: Int) + 1})

Scalaz verifies this with the `FunctorLaw` trait:

.. code-block:: scala

    trait FunctorLaw {
      // The identity function, lifted, is a no-op
      def identity[A](fa: F[A])(implicit FA: Equal[F[A]]): Boolean =
        FA.equal(map(fa)(x => x), fa)

      // a series of maps can be rewritten as a single map on a composed function
      def associative[A, B, C](fa: F[A], f1: A => B, f2: B => C)(implicit FC: Equal[F[C]]): Boolean =
        FC.equal(map(map(fa)(f1))(f2), map(fa)(f2 compose f1))
    }

    functor.laws[List].check

--------------------------------------------------------------------------------
Applicative Laws
--------------------------------------------------------------------------------

.. code-block:: scala

    trait ApplicativeLaw extends FunctorLaw {
      def identityAp[A](fa: F[A])(implicit FA: Equal[F[A]]): Boolean =
        FA.equal(ap(fa)(point((a: A) => a)), fa)

      def composition[A, B, C](fbc: F[B => C], fab: F[A => B], fa: F[A])(implicit FC: Equal[F[C]]) =
        FC.equal(ap(ap(fa)(fab))(fbc), ap(fa)(ap(fab)(ap(fbc)(point((bc: B => C) => (ab: A => B) => bc compose ab)))))

      def homomorphism[A, B](ab: A => B, a: A)(implicit FB: Equal[F[B]]): Boolean =
        FB.equal(ap(point(a))(point(ab)), point(ab(a)))

      def interchange[A, B](f: F[A => B], a: A)(implicit FB: Equal[F[B]]): Boolean =
        FB.equal(ap(point(a))(f), ap(f)(point((f: A => B) => f(a))))
    }

--------------------------------------------------------------------------------
Semigroup Laws
--------------------------------------------------------------------------------

.. code-block:: scala

    //
    // A semigroup in type F must satisfy two laws:
    // *  closure       - `∀ a, b in F, append(a, b)` is also in `F`. This is enforced by the type system.
    // *  associativity - `∀ a, b, c` in `F`, the equation `append(append(a, b), c) = append(a, append(b , c))` holds.
    //
    trait SemigroupLaw {
      def associative(f1: F, f2: F, f3: F)(implicit F: Equal[F]): Boolean =
        F.equal(append(f1, append(f2, f3)), append(append(f1, f2), f3))
    }

    semigroup.laws[Int].check
    semigroup.laws[Int @@ Tags.Multiplication].check

--------------------------------------------------------------------------------
Monoid Laws
--------------------------------------------------------------------------------

.. code-block:: scala

    // 
    // Monoid instances must satisfy the semigroup laws and 2 additional laws:
    // * left identity  - `forall a. append(zero, a) == a`
    // * right identity - `forall a. append(a, zero) == a`
    // 
    trait MonoidLaw extends SemigroupLaw {
      def leftIdentity(a: F)(implicit F: Equal[F]) = F.equal(a, append(zero, a))
      def rightIdentity(a: F)(implicit F: Equal[F]) = F.equal(a, append(a, zero))
    }

    monoid.laws[Int].check
    monoid.laws[Int @@ Tags.Multiplication].check

We can make `Option` a monoid by simply applying the append of its internal values
as monoids if they exist and zero otherwise:

.. code-block:: scala

    implicit def optionMonoid[A: Semigroup]: Monoid[Option[A]] = new Monoid[Option[A]] {
      def append(f1: Option[A], f2: => Option[A]) = (f1, f2) match {
        case (Some(a1), Some(a2)) => Some(Semigroup[A].append(a1, a2))
        case (Some(a1), None)     => f1
        case (None, Some(a2))     => f2
        case (None, None)         => None
      }

      def zero: Option[A] = None
    }

    "hello".some |+| "world".some
    (none: Option[String]) |+| "world".some
    "hello".some |+| (none: Option[String])

If we would like the `Option` monoid to simply choose the first or last
value that exists, we can use the tagged types:

.. code-block:: scala

    Tags.First('a'.some) |+| Tags.First('b'.some)            // a.some
    Tags.First(none: Option[Char]) |+| Tags.First('b'.some)  // b.some
    Tags.Last('a'.some) |+| Tags.Last('b'.some)              // b.some
    Tags.Last("a".some) |+| Tags.Last(none: Option[Char])    // a.some

--------------------------------------------------------------------------------
Foldable
--------------------------------------------------------------------------------

Once we have monoids, we can make a typeclass for types that can be folded over
(all monoids are included in this set). The trait for this is `Foldable`:

.. code-block:: scala

    trait Foldable[F[_]] { self =>
      // map each element of the structure to a [[scalaz.Monoid]], and combine the results
      def foldMap[A,B](fa: F[A])(f: A => B)(implicit F: Monoid[B]): B
    
      // right-associative fold of a structure
      def foldRight[A, B](fa: F[A], z: => B)(f: (A, => B) => B): B
    }

Using this, scalaz goes absolutely apeshit in defining a number of fold
operations:

.. code-block:: scala

    // wraps a value `self` and provides methods related to `Foldable`
    trait FoldableOps[F[_],A] extends Ops[F[A]] {
      implicit def F: Foldable[F]

      final def foldMap[B: Monoid](f: A => B = (a: A) => a): B = F.foldMap(self)(f)
      final def foldRight[B](z: => B)(f: (A, => B) => B): B = F.foldRight(self, z)(f)
      final def foldLeft[B](z: B)(f: (B, A) => B): B = F.foldLeft(self, z)(f)
      final def foldRightM[G[_], B](z: => B)(f: (A, => B) => G[B])(implicit M: Monad[G]): G[B] = F.foldRightM(self, z)(f)
      final def foldLeftM[G[_], B](z: B)(f: (B, A) => G[B])(implicit M: Monad[G]): G[B] = F.foldLeftM(self, z)(f)
      final def foldr[B](z: => B)(f: A => (=> B) => B): B = F.foldr(self, z)(f)
      final def foldl[B](z: B)(f: B => A => B): B = F.foldl(self, z)(f)
      final def foldrM[G[_], B](z: => B)(f: A => ( => B) => G[B])(implicit M: Monad[G]): G[B] = F.foldrM(self, z)(f)
      final def foldlM[G[_], B](z: B)(f: B => A => G[B])(implicit M: Monad[G]): G[B] = F.foldlM(self, z)(f)
      final def foldr1(f: (A, => A) => A): Option[A] = F.foldr1(self)(f)
      final def foldl1(f: (A, A) => A): Option[A] = F.foldl1(self)(f)
      final def sumr(implicit A: Monoid[A]): A = F.foldRight(self, A.zero)(A.append)
      final def suml(implicit A: Monoid[A]): A = F.foldLeft(self, A.zero)(A.append(_, _))
      final def toList: List[A] = F.toList(self)
      final def toIndexedSeq: IndexedSeq[A] = F.toIndexedSeq(self)
      final def toSet: Set[A] = F.toSet(self)
      final def toStream: Stream[A] = F.toStream(self)
      final def all(p: A => Boolean): Boolean = F.all(self)(p)
      final def ∀(p: A => Boolean): Boolean = F.all(self)(p)
      final def allM[G[_]: Monad](p: A => G[Boolean]): G[Boolean] = F.allM(self)(p)
      final def anyM[G[_]: Monad](p: A => G[Boolean]): G[Boolean] = F.anyM(self)(p)
      final def any(p: A => Boolean): Boolean = F.any(self)(p)
      final def ∃(p: A => Boolean): Boolean = F.any(self)(p)
      final def count: Int = F.count(self)
      final def maximum(implicit A: Order[A]): Option[A] = F.maximum(self)
      final def minimum(implicit A: Order[A]): Option[A] = F.minimum(self)
      final def longDigits(implicit d: A <:< Digit): Long = F.longDigits(self)
      final def empty: Boolean = F.empty(self)
      final def element(a: A)(implicit A: Equal[A]): Boolean = F.element(self, a)
      final def splitWith(p: A => Boolean): List[List[A]] = F.splitWith(self)(p)
      final def selectSplit(p: A => Boolean): List[List[A]] = F.selectSplit(self)(p)
      final def collapse[X[_]](implicit A: ApplicativePlus[X]): X[A] = F.collapse(self)
      final def concatenate(implicit A: Monoid[A]): A = F.fold(self)
      final def traverse_[M[_]:Applicative](f: A => M[Unit]): M[Unit] = F.traverse_(self)(f)
    }

--------------------------------------------------------------------------------
Monads
--------------------------------------------------------------------------------

*Monads are a natural extension applicative functors, and they provide a
solution to the following problem: If we have a value with context, `m a`, how
do we apply it to a function that takes a normal a and returns a value with a
context.*

.. code-block:: scala

    trait Bind[F[_]] extends Apply[F] { self =>
      // Equivalent to `join(map(fa)(f))`
      def bind[A, B](fa: F[A])(f: A => F[B]): F[B]
    }

    // since this extends applicative, there is no confusion between
    // return vs pure; they both use point
    trait Monad[F[_]] extends Applicative[F] with Bind[F] { self =>
    }

    // wraps a value `self` and provides methods related to `Bind`
    trait BindOps[F[_],A] extends Ops[F[A]] {
      implicit def F: Bind[F]

      import Liskov.<~<
    
      def flatMap[B](f: A => F[B]) = F.bind(self)(f)
      def >>=[B](f: A => F[B]) = F.bind(self)(f)
      def ∗[B](f: A => F[B]) = F.bind(self)(f)
      def join[B](implicit ev: A <~< F[B]): F[B] = F.bind(self)(ev(_))
      def μ[B](implicit ev: A <~< F[B]): F[B] = F.bind(self)(ev(_))
      def >>[B](b: F[B]): F[B] = F.bind(self)(_ => b)
      def ifM[B](ifTrue: => F[B], ifFalse: => F[B])(implicit ev: A <~< Boolean): F[B] = {
        val value: F[Boolean] = Liskov.co[F, A, Boolean](ev)(self)
        F.ifM(value, ifTrue, ifFalse)
      }
    }

    3.some flatMap { x => (x + 1).some }              // 4.some
    (none: Option[Int]) flatMap { x => (x + 1).some } // none

--------------------------------------------------------------------------------
Tips and Tricks
--------------------------------------------------------------------------------

If you need to paste a large amount of code into a `sbt console`, simply type
`:paste` and then you are in a paste session. When you are done pasting your
blob, just type `<ctrl> + d` and the whole chunk will be evaluated at once.

Case classes have a default copy constructor that uses the current values
as named default arguments:

.. code-block:: scala

    case class Point(x: Int, y: Int) {
      def moveLeft(d: Int)  = copy(x = x - d)
      def moveRight(d: Int) = copy(x = x + d)
      def moveUp(d: Int)    = copy(y = y + d)
      def moveDown(d: Int)  = copy(y = y - d)
    }
    val point = Point(2, 4)
    val moved = point.moveLeft(4)

Long story short, bind works, `>>=` is an alias for it, `>>` is the
s-combinator, and scala has the `for-expression` instead of the haskel
`do-expression`. A cool thing, pattern matching works in for expressions:

.. code-block:: scala

    val first = for {
        (x :: xs) <- "hello".toList.some
    } yield x

    first assert_=== 'h'.some

    val what = for {
        (x :: xs) <- "".toList.some
    } yield x

    what assert_=== (none: Option[Char])
