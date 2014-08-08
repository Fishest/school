================================================================================
Scala Libraries
================================================================================

--------------------------------------------------------------------------------
ScalaTest
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Features (as of version 2.0):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* HTML result output
* Eclipse plugin test runner
* Great command line runner
* Deep integration with a number of test tools
* A number of convenient assertion matchers

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of traits that can be mixed in:

* **FlatSpec**: in order to use the BDD testing style
* **FunSpec**: in order to use the TDD testing style
* **ShouldMatchers**: in order to use the fluent matchers
* **BeforeAndAfter**: in order to have setup and teardown methods
* **MockitoSugar**: in order to use mockito like `mock[ClassName]`

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FlatSpec Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What follows is a template for a basic ScalaTest unit test using the FlatSpec trait:

.. code-block:: scala

    import org.junit.runner.RunWith
    import collection.mutable.Stack
    import org.scalatest._
    import org.scalatest.runner.JUnitRunner
    
    @RunWith(classOf[JUnitRunner])
    class StackSpec extends FlatSpec with ShouldMatchers {
    
      "A Stack" should "pop values in last-in-first-out order" in {
        val stack = new Stack[Int]
        stack.push(1)
        stack.push(2)
        stack.pop() should equal (2)
        stack.pop() should equal (1)

        // in order to catch exceptions you can surround the call
        val thrown = intercept[NoSuchElementException] {
            stack.pop();
        }
      }
    
      it should "throw NoSuchElementException if an empty stack is popped" in {
        val emptyStack = new Stack[String]
        evaluating { emptyStack.pop() } should produce [NoSuchElementException]
      }
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FunSpec Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What follows is a template for a basic ScalaTest unit test using the FunSpec trait:

.. code-block:: scala
    
    import org.scalatest.{FunSuite, BeforeAndAfter}
    import org.scalatest.mock.MockitoSugar
    import org.junit.runner.RunWith
    import org.scalatest.junit.JUnitRunner
    import org.scalatest.matchers.ShouldMatchers
    
    import org.mockito.Mock;
    import org.mockito.Mockito._;
    import org.mockito.MockitoAnnotations;
    
    import com.amazonaws.services.dynamodb.AmazonDynamoDBClient;
    import com.amazonaws.services.dynamodb.model.QueryRequest;
    import com.amazonaws.services.dynamodb.model.QueryResult;
    
    @RunWith(classOf[JUnitRunner])
    class DynamoScalaTest extends FunSuite with MockitoSugar with ShouldMatchers {
    
        def TestFixture = new {
          val result = mock[QueryResult]
          val client = mock[AmazonDynamoDBClient]
        }
    
        test("testing with mockito works correctly") {
            val F     = new TestFixture
            val query = new QueryRequest
    
            when(F.client.query(query)) thenReturn(F.result)
            F.client.query(query) should equal(F.result)
        }
    }


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Sharing Fixtures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using get-fixture method:

.. code-block:: scala

    def TestFixture = new {
      val result = mock[QueryResult]
      val client = mock[AmazonDynamoDBClient]
    }
    
    test("testing with mockito works correctly") {
        val F = new TestFixture
        when(F.client.call(any())) thenReturn(F.result)

        val request = new Request
        val response = F.client.call(request)
        response should equal F.result
    }

Instantiating fixture-context objects methods:

.. code-block:: scala

    trait Builder {
        val builder = new StringBuilder("scala is ")
    }

    trait Buffer {
        val buffer = ListBuffer("scala", "is")
    }

    test("testing should be productive") in new Builder {
        builder.append("productive");
        assert(builder.toString === "scala is productive")
    }

    test("testing should be productive") in new Builder with Buffer {
        builder.append("clear")
        buffer += ("concise")
        assert(builder.toString === "scala is clear")
        assert(buffer === List("scala", "is", "concise"))
    }


One instance per test method allows the tests to be run in their own
instance of the suite with their own copy of the instance variables,
(it should be noted that there is no cleanup with this method):

.. code-block:: scala

    // if you can set your tests up like this, then you can easily
    // switch to the ParrallelTestExecution trait which extends this
    // and allows all the tests in this suite to be run in parallel.
    class ExampleSuite extends FlatSpec with OneInstancePerTest {
        val builder = new StringBuilder("scala is ")
        val buffer = ListBuffer("scala", "is")

        "testing" should "be productive" in {
            builder.append("productive");
            assert(builder.toString === "scala is productive")
        }

        it should "be clear" in {
            builder.append("clear")
            buffer += ("concise")
            assert(builder.toString === "scala is clear")
            assert(buffer === List("scala", "is", "concise"))
        }
    }

You can also override the lifecycle methods in scalatest to perform
side effect creating actions as well as cleaning up after them:

.. code-block:: scala

    class ExampleSpec extends FlatSpec {
        // NoArgTest contains an apply method to run the test,
        // but it also contains the test name and the configuration map
        // which can be used for your fixture
        override def withFixture(test: NoArgTest) {
            try super.withFixture(test)
            catch {
                val current = new File(".") // if test failure, log the directory
                val files = current.list()
                info("Directory Snapshot: " + files.mkString(", "))
                throw e
            } finall {
                // any post test cleanup, like deleting dirs
            }
        }

        "this test" should "succeed" in { assert(1 + 1 === 2) }
        "this test" should "fail" in { assert(1 + 2 === 2) }
    }

If you need to pass a fixture object into a test and perform cleanup
at the end of the test, you can use the loan-fixture method:

.. code-block:: scala

    import java.util.concurrent.ConcurrentHashMap

    // a simulation of a database server
    object DBServer {
      type DB = StringBuffer
      private val databases = new ConcurrentHashMap[String, DB]
      def createDB(name: String): DB = {
        val db = new StringBuffer
        databases.put(name, db)
        db
      }
      def removeDB(name: String) {
        databases.remove(name)
      }
    }


    import org.scalatest.FlatSpec
    import DBServer._
    import java.util.UUID.randomUUID
    import java.io._

    class ExampleSpec extends FlatSpec {

      def withDatabase(test: DB => Any) {
        val dbname = randomUUID.toString
        val db = createDB(dbname)
        try {
          db.append("scalatest is ") // perform setup
          test(db)
        } finally removeDB(dbname)   // perform cleanup
      }

      def withFile(test: (File, FileWriter) => Any) {
        val file = File.createTempFile("hello", "world")
        val writer = new FileWriter(file)
        try {
          writer.write("scalatest is ") // perform setup
          test(file, writer)
        } finally writer.close()        // perform cleanup
      }

      "testing" should "be productive" in withFile { (file, writer) =>
        writer.write("productive")
        writer.flush()
        assert(file.length === 24)
      }

      "testing" should "be readable" in withDatabase { db =>
        db.append("readable")
        assert(db.toString === "scalatest is readable")
      }

      it should "be concise" in withDatabase { db =>
        withFile { (file, writer) =>
          db.append("clear")
          writer.write("concise")
          writer.flush()
          assert(db.toString === "scalatest is clear")
          assert(file.length === 21)
        }
      }
    }

If all or most tests need the same fixture, then you can override the
`withFixture` method to apply a fixture.Suite:

.. code-block:: scala

    import org.scalatest.fixture
    import java.io._

    class ExampleSpec extends fixture.FlatSpec {
      case class F(file: File, writer: FileWriter)
      type FixtureParam = F // must overload the input to test

      def withFixture(test: OneArgTest) {
        val file = File.createTempFile("hello", "world")
        val writer = new FileWriter(file)
        try {
          writer.write("scalatest is ")                  // setup the fixture
          withFixture(test.toNoArgTest(F(file, writer))) // load the fixture
        } finally writer.close()                         // clean up the fixture
      }

      "testing" should "be easy" in { f =>
        f.writer.write("easy")
        f.writer.flush()
        assert(f.file.length === 17)
      }

      it should "be fun" in { f =>
        f.writer.write("fun")
        f.writer.flush()
        assert(f.file.length === 16)
      }
    }

If you need simple setup and teardown to run before each test, just mixin the
BeforeAndAfter trait. The only way that before and after can interact with the
Suite is through modifying some state (changing vars or modifying vals). As
such, these tests cannot be run in parallel without synchronization:

.. code-block:: scala

    import org.scalatest._
    import collection.mutable.ListBuffer

    class ExampleSpec extends FlatSpec with BeforeAndAfter {
      val builder = new StringBuilder
      val buffer  = new ListBuffer[String]

      before {
        builder.append("scalatest is ")
      }

      after {
        builder.clear()
        buffer.clear()
      }

      "testing" should "be easy" in {
        builder.append("easy")
        assert(builder.toString === "scalatest is easy")
        assert(buffer.isEmpty)
        buffer += "sweet"
      }

      it should "be fun" in {
        builder.append("fun")
        assert(builder.toString === "scalatest is fun")
        assert(buffer.isEmpty)
      }
    }

If you have many fixtures, you can compose them with stackable traits:

.. code-block:: scala

    import org.scalatest._
    import collection.mutable.ListBuffer

    trait Builder extends AbstractSuite { this: Suite =>
      val builder = new StringBuilder

      // to be stackable, the suite must call the super.withFixture
      // of the stacked suite above it.
      abstract override def withFixture(test: NoArgTest) {
        builder.append("scalatest is ")
        try super.withFixture(test)
        finally builder.clear()
      }
    }

    trait Buffer extends AbstractSuite { this: Suite =>
      val buffer = new ListBuffer[String]

      abstract override def withFixture(test: NoArgTest) {
        try super.withFixture(test)
        finally builder.clear()
      }
    }

    // the order in which you mixin the traits determines which
    // is initialized first. So here, Buffer is super to Builder.
    class ExampleSpec extends FlatSpec with Builder with Buffer {
      
      "testing" should "be easy" in {
        builder.append("easy")
        assert(builder.toString === "scalatest is easy")
        assert(buffer.isEmpty)
        buffer += "sweet"
      }

      it should "be fun" in {
        builder.append("fun")
        assert(builder.toString === "scalatest is fun")
        assert(buffer.isEmpty)
      }
    }

This can also be designed by implementing the `BeforeAndAfterEach` trait which
allows one to create setup and teardown methods or by implementing the 
`BeforeAndAfterAll` which allows one to create classSetup and classTeardown
methods:

.. code-block:: scala

  import org.scalatest._

  trait Builder extends BeforeAndAfterEach { this: Suite =>
    val builder = new StringBuilderA

    override def beforeEach() {
      builder.append("scalatest is")
      super.beforeEach()    // to be stackable
    }

    override def afterEach() {
      try super.afterEach() // to be stackable
      finally builder.clear()
    }
  }

  class ExampleSpec extends FlatSpec with Builder {
    "testing" should "be easy" in {
      builder.append("easy")
      assert(builder.toString === "scalatest is easy")
      buffer += "sweet"
    }
  }

--------------------------------------------------------------------------------
ScalaRx
--------------------------------------------------------------------------------

`Project Homepage https://github.com/lihaoyi/scala.rx`_

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Primitives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ScalaRx supplies a number of dataflow primitives (think gpars) that can be used
to construct dataflow graphs. In general, Scala.Rx revolves around constructing
dataflow graphs which automatically keep things in sync, which you can easily
interact with from external, imperative code:

* `Var`
  Is a smart variable which you can get using `a()` and set using `a() = value`.
  Whenever its value changes, it pings any downstream entity which needs to be
  recalculated. Are generally used as inputs into a dataflow graph.

* `Rx`
  Is a reactive definition which automatically captures any `Var` or other `Rx`
  which get called in its body, flagging them as dependencies and re-calculating
  whenever one of them changes. Like a `Var`, you can use the `a()` syntax to
  retrieve its value, and it also pings downstream entities when the value changes.
  Side effects should not be performed here as an `Rx` may run many times for
  each change (make them pure). Are generally used as nodes in a dataflow graph.

* `Obs`
  Is an observer on one or more `Var` or `Rx`, performing some side-effect when
  the observed node changes value and sends it a ping. These are guranteed to
  run only once after all the involved `Rx` have stabilized. Continuing, `Obs`
  will perform an initial run when it is declared to store the first value,
  this can be skipped by supplying `skipInitial=true`. When an `Obs` is
  garbage collected, its callback will stop triggering. Are generally used as
  outputs from the dataflow graph.

.. code-block:: scala

    import rx._

    val a = Var(1)
    val b = Var(2)
    val c = Rx { a() + b() }
    val d = Rx { c() * 4 }

    println(c())  // 3
    println(d())  // 12
    a() = 4
    println(c())  // 6
    println(d())  // 24

    var count = 0;                            // mutable side-effect from o
    val o = Obs(a) { count = a() + 1 }        // re-run on all changes to a
    val x = a.foreach { x => count = x + 1 }  // equivalent to above
    o.kill()                                  // stop all further updates
    x.killAll()                               // stop all further updates from descendents

    val e = Rx { a() / b() }
    e.toTry                                   // Success(0)
    b() = 0
    e.toTry                                   // Failure(java.lang.ArithmeticException)

`Rx` blocks can be nested to form complex associations:

.. code-block:: scala

    import scala.util.Random.{ nextFloat => random }

    trait Webpage {
        val time = Var(random())
        def html: Rx[String]
        def update { time() = random() }
    }
    sealed class Google extends Webpage {
        val html = Rx { "this is google: " + time() }
    }
    sealed class Yahoo extends Webpage {
        val html = Rx { "this is yahoo: " + time() }
    }

    val url  = Var("www.google.com")
    val page = Rx {
        url() match {
            case "www.google.com" => new Google()
            case "www.yahoo.com"  => new Yahoo()
        }
    }

    println(page().html())
    page().update()
    println(page().html())
    page() = "www.yahoo.com"
    println(page().html())

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Primitive Combinators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ScalaRx also defines a number of combinators on the primitives to avoid
having to re-create the common operations: `map`, `filter`, `reduce`. It
should be noted that the counterparts `mapAll`, `filterAll`, and `reduceAll`
exist to operate on `Try[S]` in case failures can occur:

.. code-block:: scala

    val a = Var(2)
    val b = Rx { a() * 2 }  // a.map(_ * 2)
    val c = a.map(_ + 2)    // Rx { a() + 2 }
    val d = c.filter(_ > 3) // d() == 4
    a() = 1                 // d() == 4
    a() = 5                 // d() == 5

    val e = a.reduce(_ + _) // e() == 5
    a() = 6                 // e() == 11

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Asynchronous Combinators
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: scala

    import scala.concurrent.Promise
    import scala.concurrent.ExecutionContext.Implicits.global
    
    val p = Promise[Int]()
    val a = Rx{
      p.future
    }.async(10)
    println(a()) // 10
    
    p.success(5)
    println(a()) // 5


ScalaRx can use the akka scheduler to implement a timer service
that can be used to schedule recurring events:

.. code-block:: scala

    import scala.concurrent.duration._
    implicit val scheduler = new AkkaScheduler(akka.actor.ActorSystem())
    
    val timer = Timer(100 millis)
    var count = 0
    val o = Obs(timer) {
        count = count + 1
    }
    
    println(count) // 3
    println(count) // 8
    println(count) // 13

This same construct is used to implement delays in event propigation:

.. code-block:: scala

    import scala.concurrent.duration._
    implicit val scheduler = new AkkaScheduler(akka.actor.ActorSystem())

    val a = Var(10)
    val b = a.delay(250 millis)

    a() = 5
    println(b()) // 10
    eventually {
        println(b()) // 5
    }

    a() = 4
    println(b()) // 5
    eventually {
        println(b()) // 4
    }

And futhermore debounce logic to allow for a value to settle before
being emitted:

.. code-block:: scala

    import scala.concurrent.duration._
    implicit val scheduler = new AkkaScheduler(akka.actor.ActorSystem())

    val a = Var(10)
    val b = a.delay(250 millis)

    a() = 5
    println(b())     // 5

    a() = 4
    println(b())     // 5
    eventually {
        println(b()) // 4
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Primitive Debugging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ScalaRx maintains the dataflow graph which can be used to inspect why a value is
what it is. Furthermore, it allows one to name the variables so that introspection
can produce readable messages:

.. code-block:: scala

    val a = Var(1, name="a")
    val b = Var(2, name="b")
    val c = Rx(name="c"){ a() + b() }     // 3
    val d = Rx(name="d"){ c() * 5 }       // 15
    val e = Rx(name="e"){ c() + 4 }       // 7
    val f = Rx(name="f"){ d() + e() + 4 } // 26

    println(f.parents)                                 // List(Rx#, Rx#)
    println(f.parents.collect{ case r: Rx[_] => r() }) // List(7, 15)
    println(c.descendants.map(_.name))                 // List(e, d, f, f)

    f.ancestors
     .map{ case r: Rx[_] => r.name + " " + r() }
     .foreach(println)


--------------------------------------------------------------------------------
Scala Blitz
--------------------------------------------------------------------------------

http://scala-blitz.github.io/home/documentation/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Slick
--------------------------------------------------------------------------------

http://slick.typesafe.com/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Breeze
--------------------------------------------------------------------------------

http://www.scalanlp.org/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Monocle
--------------------------------------------------------------------------------

https://github.com/julien-truffaut/Monocle

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Shapeless
--------------------------------------------------------------------------------

https://github.com/milessabin/shapeless

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Spire
--------------------------------------------------------------------------------

https://github.com/non/spire

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this


--------------------------------------------------------------------------------
Scala Algebird
--------------------------------------------------------------------------------

https://github.com/twitter/algebird

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this

--------------------------------------------------------------------------------
Twitter Scala
--------------------------------------------------------------------------------

http://twitter.github.io/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: look at this
