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
def show(json: Json): String = json match {
  case JSeq(list)    => "[" + (list map show mkString ", ") + "]"
  case JObj(mapping) =>
    val mappings = mapping map {
      case (key, value) => "\"" + key + "\": " + show(value)
    }
    "{" + (mappings mkString ", ") + "}"
  case JNum(number)  => number.toString
  case JStr(string)  => "\"" + string "\""
  case JBool(bool)   => bool.toString
  case JNull         => "null"
}

/**
 * How the case blocks actually work, in case of the
 * JObj case statement.
 */
type JEntry (String, Json)
trait Function1[-A, +R] {
  def apply(a: A): R
}

new Function1[JEntry, String] {
  def apply(entry: JEntry): String = entry match {
    case (key, value) => "\"" + key + "\": " + show(value)
  }
}

/**
 * You can also subclass functions as map and sequence
 * do. thatis why we can do `map(key)` and `seq(idx)`
 */
trait Map[Key, Value] extends (Key => Value)
trait Seq[Elem] extends (Int => Elem)

/**
 * How can we tell what values are available for
 * a function. We can use partial functions
 */
val fx1: String => String = { case "ping" => "pong" }
fx1("ping") // "pong"
fx1("pong") // exception

val fx2: PartialFunction[String, String] = { case "ping" => "pong" }
fx2.isDefinedAt("ping") // true
fx2.isDefinedAt("pong") // false

trait PartialFunction[-A, +R] extends Function1[-A, +R] {
  def apply(a: A): R
  def isDefinedAt(a: A): Boolean
}

new Function1[String, String] {
  def apply(entry: String): String = entry match {
    case "ping" => "pong"
  }

  def isDefinedAt(key: String): key match {
    case "ping" => true
    case _      => false
  }
}

//------------------------------------------------------------
// Video 2
//------------------------------------------------------------
/**
 * Ideallized combinators that are not tail
 * recursive.
 */
abstract class List[+T] {
  def map[U](fx: T => U): List[U] = this match {
    case x :: xs => fx(x) :: xs.map(fx)
    case Nil => Nil
  }

  def flatMap[U](fx: T => List[U]): List[U] = this match {
    case x :: xs => fx(x) ++ xs.map(fx)
    case Nil => Nil
  }

  def filter(px: T => Boolean): List[T] = this match {
    case x :: xs => if (px(x)) x :: xs.filter(px) else xs.filter(px)
    case Nil => Nil
  }
}

/**
 * Rules for translating `for` statements
 */

// 1. a single for expression is converted to a map
for (x <- e1) yield e2
e1.map(x => e2)

// 2. filter is converted into a lazy filter iterator
for (x <- e1 if f; s) yield e2
for (x <- e1.withFilter(x => f); s) yield e2

// 3. two for expressions converts the first one to flatMap
for (x <- e1; y <- e2; s) yield e3
e1.flatMap(x => for (y <- e2; s) yield e3)

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
(2 to N).flatMap(x =>
    (2 to x).withFilter (y =>
        x % y == 0) map (y => (x, y)))

/**
 * `for` statements can also pattern match.
 * This will print the first and last name of all
 * people with a phone number in area code 212
 */
val data: List[Json] = ...
for {
  JObj(mapping) <- data
  JSeq(phones)   = mapping("phoneNumbers")
  JObj(phone)   <- phones
  JStr(digits)   = phone("number")
  if digists startsWith "212"
} yield (mapping("firstName"), mapping("lastName")

//------------------------------------------------------------
// Video 3
//------------------------------------------------------------
/**
 * You can use any type with for expressions as long as they
 * implement `map`, `flatMap`, and `withFilter`. It should be
 * noted that the concepts should make sense for the type.
 */
trait Generator[+T] {
  def generate: T
}

val integers = new Generator[Int] {
  val rand = new java.util.Random
  def generate = rand.nextInt()
}

val booleans = new Generator[Boolean] {
  def generate = integers.generate > 0
}

val pairs = new Generator[(Int, Int)] {
  def generate = (integers.generate, integers.generate)
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

val booleans = for (x <- integers) yield x > 0
val booleans = integers map { x => x > 0 }
val booleans = new Generator[Boolean] = {
  def generate = (x: Int => x > 0)(integers.generate)
}
// with beta reduction
val booleans = new Generator[Boolean] = {
  def generate = integers.generate > 0
}

val pairs = for (x <- integers; y < integers) yield (x, y)

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

/**
 * And also trees
 */
trait Tree
case class Inner(left: Tree, right: Tree) extends Tree
case class Leaf(value: Int) extends Tree

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

/**
 * We can use this idea to generate random test data
 * for fuzzing or boundary testing. This is a simple example
 * of quick-check or scala-check
 */
def test[T](g: Generator[T], numTimes: Int = 100)(test: T => Boolean): Unit = {
  for (i <- 0 until numTimes) {
    val input = g.generate
    assert(test(value), "test failed for input: " + input)
  }
  println("test passed " + numTimes + " random tests")

}
