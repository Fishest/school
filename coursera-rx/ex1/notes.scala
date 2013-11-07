import 
//------------------------------------------------------------
// Video 1
//------------------------------------------------------------
/**
 * How could we represent a Json DSL in scala?
 */ 
abstract class Json
case class JSeq(list: List[Json])       extends Json
case class JObj(mapping: Map[String, Json]) extends Json
case class JNum(number: Double)         extends Json
case class JStr(string: String)         extends Json
case class JBool(bool: Boolean)         extends Json
case object JNull                       extends Json

/**
 * How could we convert the DSL structure back to
 * the Json string?
 */
object Json {

  def show(json: Json): String = json match {
    case JSeq(list)    => "[" + (list map show mkString ", ") + "]"
    case JObj(mapping) =>
      val mappings = mapping map {
        case (key, value) => "\"" + key + "\": " + show(value)
      }
      "{" + (mappings mkString ", ") + "}"
    case JNum(number)  => number.toString
    case JStr(string)  => "\"" + string + "\""
    case JBool(bool)   => bool.toString
    case JNull         => "null"
  }
}

/**
 * How the case blocks actually work, in case of the
 * JObj case statement.
 */
trait MyFunction1[-A, +R] {
  def apply(a: A): R
}

object Json2 {
  type JEntry = (String, Json)
  val json_map_func = new Function1[JEntry, String] {
    def apply(entry: JEntry): String = entry match {
      case (key, value) => "\"" + key + "\": " + show(value)
    }
  }
}

/**
 * You can also subclass functions as map and sequence
 * do. thatis why we can do `map(key)` and `seq(idx)`
 */
trait MyMap[Key, Value] extends (Key => Value)
trait MySeq[Elem] extends (Int => Elem)

/**
 * How can we tell what values are available for
 * a function. We can use partial functions
 */
object Json3 {
  try {
    val fx1: String => String = { case "ping" => "pong" }
    fx1("ping") // "pong"
    fx1("pong") // exception
  } catch { case ex: Exception => println(ex); }

  val fx2: PartialFunction[String, String] = { case "ping" => "pong" }
  fx2.isDefinedAt("ping") // true
  fx2.isDefinedAt("pong") // false
}

trait MyPartialFunction[-A, +R] extends Function1[A, R] {
  def apply(a: A): R
  def isDefinedAt(a: A): Boolean
}

object Json4 {
  val my_pong_func = new Function1[String, String] {
    def apply(entry: String): String = entry match {
      case "ping" => "pong"
    }

    def isDefinedAt(key: String): Boolean = key match {
      case "ping" => true
      case _      => false
    }
  }
}

//------------------------------------------------------------
// Video 2
//------------------------------------------------------------
/**
 * Ideallized combinators that are not tail
 * recursive.
 */
abstract class MyList[+T] {
  def map[U](fx: T => U): MyList[U] = this match {
    case x :: xs => fx(x) :: xs.map(fx)
    case Nil => Nil
  }

  def flatMap[U](fx: T => MyList[U]): MyList[U] = this match {
    case x :: xs => fx(x) ++ xs.map(fx)
    case Nil => Nil
  }

  def filter(px: T => Boolean): MyList[T] = this match {
    case x :: xs => if (px(x)) x :: xs.filter(px) else xs.filter(px)
    case Nil => Nil
  }
}

/**
 * Rules for translating `for` statements
 */
object ForStatements {
  val e1 = 1 to 10
  val e2 = 2 to 10
  val e3 = 3 to 10
  val e4 = 4
  val f  = true

  // 1. a single for expression is converted to a map
  for (x <- e1) yield e2
  e1.map(x => e2)

  // 2. filter is converted into a lazy filter iterator
  for (x <- e1 if f; y <- e2) yield e2
  for (x <- e1.withFilter(x => f); y <- e1) yield e2

  // 3. two for expressions converts the first one to flatMap
  for (x <- e1; y <- e2; z <- e3) yield e4
  e1.flatMap(x => for (y <- e2; z <- e3) yield e4)

  /**
   * Using these rules, we can convert for expressions.
   */

  // from the for expression form
  for {
    x <- 2 to N
    y <- 2 to x
    if (x % y == 0)
  } yield (x, y)

  // to its actual implementation
  val result = (2 to N).flatMap(x =>
      (2 to x).withFilter (y =>
          x % y == 0) map (y => (x, y)))
}

/**
 * `for` statements can also pattern match.
 * This will print the first and last name of all
 * people with a phone number in area code 212
 */
object ForStatements2 {
  val data: List[Json] = List(JNull)
  for {
    JObj(mapping) <- data
    JSeq(phones)   = mapping("phoneNumbers")
    JObj(phone)   <- phones
    JStr(digits)   = phone("number")
    if digists startsWith "212"
  } yield (mapping("firstName"), mapping("lastName"))
}

//------------------------------------------------------------
// Video 3
//------------------------------------------------------------

/**
 * You can use any type with for expressions as long as they
 * implement `map`, `flatMap`, and `withFilter`. It should be
 * noted that the concepts should make sense for the type.
 */
trait SimpleGenerator[+T] {
  def generate: T
}

object Generator {
  val integers = new SimpleGenerator[Int] {
    val rand = new java.util.Random
    def generate = rand.nextInt()
  }

  val booleans = new SimpleGenerator[Boolean] {
    def generate = integers.generate > 0
  }

  val pairs = new SimpleGenerator[(Int, Int)] {
    def generate = (integers.generate, integers.generate)
  }
}

/**
 * Can we avoid all the boilerplate of creating new
 * anonymous classes?
 */
trait Generator[+T] { self => // this alias
  def generate: T
  def map[S](f: T => S): Generator[S] = new Generator[S] {
    def generate = f(self.generate)
  }
  def flatMmap[S](f: T => Generator[S]): Generator[S] = new Generator[S] {
    def generate = f(self.generate).generate
  }
}

object Generator2 {

  val integers = new Generator[Int] {
    val rand = new java.util.Random
    def generate = rand.nextInt()
  }
  val booleans  = for (x <- integers) yield x > 0
  val booleans1 = integers map { x => x > 0 }
  val booleans2 = new Generator[Boolean] = {
    def generate = (x => x > 0)(integers.generate)
  }
  // with beta reduction
  val booleans = new Generator[Boolean] = {
    def generate = integers.generate > 0
  }

  val pairs = for (x <- integers; y <- integers) yield (x, y)

  /**
   * Here are some utility generators
   */
  def single[T](x: T): Generator[T] = new Generator[T] {
    def generator = x
  }

  def choose(lo: Int, hi: Int): Generator[Int] =
    for (x <- integers) yield lo + x % (hi - lo)

  def oneOf[T](xs: T*): Generator[T] =
    for (idx <- choose(0, xs.length)) yield xs(idx)
    for (x <- integers) yield lo + x % (hi - lo)

  /**
   * And we can compose these even more to generate
   * random lists.
   */
  def emptyList = single(Nil)
  def nonEmptyList = for {
    head <- integers
    tail <- lists
  } yield head :: tail

  def lists: Generator[List[Int]] = for {
    isEmpty <- booleans
    list    <- if (isEmpty) emptyList else nonEmptyList
  } yield list
}

/**
 * And also trees
 */
trait Tree
case class Inner(left: Tree, right: Tree) extends Tree
case class Leaf(value: Int) extends Tree

object Tree {

  def leafs = for {
    value <- integers
  } yield new Leaf(value)

  def inners = for {
    left  <- trees
    right <- trees
  } yield new Inner(left, right)

  def trees: Generator[Tree] = for {
    isLeaf <- booleans
    tree   <- if (isLeaf) leafs else inners
  } yield tree
}

/**
 * We can use this idea to generate random test data
 * for fuzzing or boundary testing. This is a simple example
 * of quick-check or scala-check
 */
object QuickTest {

  def test[T](g: Generator[T], numTimes: Int = 100)(test: T => Boolean): Unit = {
    for (i <- 0 until numTimes) {
      val input = g.generate
      assert(test(value), "test failed for input: " + input)
    }
    println("test passed " + numTimes + " random tests")
  }
}

//------------------------------------------------------------
// Video 4 - Monads
//------------------------------------------------------------

trait M[T] {
  // usually called bind
  def flatMap[U](f: T => M[U]): M[U]

  /**
   * 1. List is a monad with:      unit(x) = List(x)
   * 2. Set is a monad with:       unit(x) = Set(x)
   * 3. Option is a monad with:    unit(x) = Some(x)
   * 4. Generator is a monad with: unit(x) = single(x)
   */
  def unit[A](x: A): M[A]

  /**
   * Map can be defined for every monad with
   * m map f == m flatMap (x => unit(f(x)))
   *         == m flatMap (f andThen unit)
   */
  def map[A](f: T => A): M[A] 
}

/**
 * Monads must respect three algebraic laws:
 * 1. associativity:
 *    (m flatMap f) flatMap g == m flatMap (x => f(x) flatMap g)
 *
 * 2. left unit:
 *    unit(x) flatMap f == f(x)
 *
 * 3. right unit:
 *    m flatMap unit == m
 *
 * If the monad defines withFilter it is called
 * a monad with zero.
 */

/**
 * Models a value that may exist or not
 */
abstract class Options[+T] {
  def flatMap[U](f: T => Option[U]): Option[U] = this match {
    case Some(x) => f(x)
    case None    => None
  }
}

/**
 * Models an operation that may succed or fail
 * with an exception. Not a monad because left-unit
 * f(x) could throw an exception and the monad will not.
 * We can help this by strengthening the monad rules to 
 * not throw an exception from f.
 */
abstract class Try[+T] {
  def flatMap[U](f: T => Try[U]): Try[U] = this match {
    case Success(x)    => try f(x) catch { case NonFatal(ex) => Failure(ex) }
    case fail: Failure => fail
  }
  
  def map[U](f: T => U): Try[U] = this match {
    case Success(x)    => Try(f(x))
    case fail: Failure => fail
  }
}
case class Success[T](x: T) extends Try[T]
case class Failure(ex: Exception) extends Try[Nothing]

object Try {
  def apply[T](expr: => T): Try[T] =
    try Success(expr)
    catch {
      case NonFatal(ex) => Failure(ex)
    }

  def good_example = Try(1 / 1)
  def fail_example = Try(1 / 0)
}

