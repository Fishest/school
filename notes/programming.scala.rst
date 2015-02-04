================================================================================
Programming in Scala 2e
================================================================================

David Pollak - Lift
Alex Payne - Twitter
Steven Jenson - Twitter

--------------------------------------------------------------------------------
Introduction
--------------------------------------------------------------------------------

What follows is a listing of the basic operations in Scala:

.. code-block:: scala

    def say(x: String) = "saying " + x
    def say(x: String): String = "saying " + x
    def say(x: String): String {
      return "saying " + x
    }

    var i = 0
    while (i < args.length) {
      if (i != 0) print(" ")
      print(args(i))
      i += 1
    }

    args.foreach(println)
    args.foreach(println(_))
    args.foreach(arg => println(arg))
    args.foreach(arg: String => println(arg))

    for (arg <- args)
      println(arg)

    val strings: Array[String] = new Array[String](2)
    strings(0) = "hello"    // strings.update(0, "hello")
    strings(1) = "world"    // strings.update(0, "world")
    for (i <- 0 to 1)       // 1 <- 0.to(0)
      println(strings(i))   // strings.apply(0)

    val strings = Array("hello", "world) // this is mutable
    val strings = List("hello", "world)  // this is immutable

    val heredoc = """This is printed funny
                     because of the indenting"""

    val heredoc = """\|This is printed correctly
                     \|with expected indenting""".stripMargin

    // symbols are interned so there is one instance
    val symbol = 'someSymbolName
    symbol.name

Notes:

* Recursive functions must specify the return type
* If a method takes only one parameter, you can call it without
  a dot or parentesis
* This also requires that the receiver is specified
  (`Console print 10` works but `print 10` does not)
* Scala doesn't actually have operators (they are just methods)
  so you simply perform method overloads instead of operator
  overloading.
* If a method name ends in a `:`, the method is invoked on the
  right operand: `x :: xs` => `xs.::(x)`
* scala compiler is slow because it has to load and parse jars.
  fsc runs as a daemon and eliminates this startup delay.

--------------------------------------------------------------------------------
Collections
--------------------------------------------------------------------------------

.. code-block:: scala

    val mapping = Map[Int, String]()
    mapping += (1 -> "value")

    // every object has a `->` method defined in an implicit
    val tuple = 1 -> "value" 
    val numerals = Map(1 -> "I", 2 -> "II")

    // quick way to read a file
    import Scala.io.Source.fromFile
    for (line <- fromFile("path").getLines())
        println(line)

    val maximum = 10.max(20)
    val minimum = 10.min(20)

Notes:

* There are mutable and immutable collections (import into scope to redefine
  which variant is being used).
* A function returning `Unit` has side effects
* A program using vars is not functional
* scala fields are public by default
* method parameters are vals

--------------------------------------------------------------------------------
Language Semantics
--------------------------------------------------------------------------------

.. code-block:: scala

   // the following two are the same
   def add(a: Int) : Unit = sum += a
   def add(a: Int) { sum += a }

   // this is an inferred return value of Int
   def add(a: Int) = { sum + a }

   // the standard scala way is to put infix operators at
   // the end of the statement
   x    // x
   + y  // abs(y)

   (x   // x + y
   + y)

   x +  // x + y
   y

There are only three semicolon rules (the end of the line is treated as a `;`
except for the following cases):

1. line ends in a word that is not legal (`.`, infix operator)
2. Next line begins with a word that cannot start a statement
3. The line ends while in a `()` `[]`

--------------------------------------------------------------------------------
Classes
--------------------------------------------------------------------------------

Scala classes cannot have static members, for this one would use singleton
objects. If a class and and object share a name, it makes the object a companion
object (must be in same source file). Each of these can access each others
private members. Without a common class, it becomes a standalone object.

`object` can extend classes and traits:

.. code-block:: scala

   // the following are imported by default
   import java.lang
   import scala
   import Predef

   // How to define a scala main method
   object MainArgument {
      def main(args: Array[String]) {
      }
   }


--------------------------------------------------------------------------------
Stackable Trait Pattern
--------------------------------------------------------------------------------

The stackable trait pattern basically allows you to define mixin decorators
that can will defer to a concrete implementation of an interface. Here is an
example to add new functionality to a `IntQueue`:

.. code-block:: scala

    abstract class IntQueue {
      def put(x: Int): Unit
      def get(): Int
    }

We start with the core functionality defined as follows:

.. code-block:: scala

    import scala.collection.mutable.ArrayBuffer

    class CoreIntQueue extends IntQueue {
      val buffer = new ArrayBuffer[Int]

      def put(x: Int) { buffer += x }
      def get() = buffer.remove(0)
    }

Now we want to define some advanced behavior that we would like to add
to our `IntQueue`:

.. code-block:: scala

    trait Doubling extends IntQueue {
      abstract override def put(x: Int) { super.put(x * 2) }
    }

    trait Incrementing extends IntQueue {
      abstract override def put(x: Int) { super.put(x + 1) }
    }

    trait Filtering extends IntQueue {
      abstract override def put(x: Int) {
        if (x >= 0) super.put(x)
      }
    }

Now we can mix in the features that we like into the instance of our
queue:

.. code-block:: scala

    class DoublingIntQueue extends BasicIntQueue with Doubling
    val queue = new DoublingIntQueue
    queue.put(10)
    queue.get()  // 10: Int

    val queue = new BasicIntQueue with Filtering
    queue.put(-10)
    queue.put(10)
    queue.get()  // 10: Int

    val queue = new BasicIntQueue with Filtering with Incrementing
    queue.put(-1)
    queue.put(0)
    queue.put(1)
    queue.get()   // 0: Int
    queue.get()   // 1: Int
    queue.get()   // 2: Int

Here is a helpful trait that can be used with stackable to create
virtual inheritence:

.. code-block:: scala

    trait Lifecycle {
      def startup(): Unit
      def shutdown(): Unit
    }

.. todo:: finish notes
