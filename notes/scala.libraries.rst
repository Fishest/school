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
                // if test failure, log the directory
                val current = new File(".")
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
