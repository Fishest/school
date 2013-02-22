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
        val file = File.createTempFile("hello", "world)
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
      super.beforeEach() // to be stackable
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
