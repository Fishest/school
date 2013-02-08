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

What follows is a template for a basic ScalaTest unit test using the FlatSpec trait::

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

What follows is a template for a basic ScalaTest unit test using the FunSpec trait::
    
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

The get-fixture method::

  def TestFixture = new {
    val result = mock[QueryResult]
    val client = mock[AmazonDynamoDBClient]
  }
    
        test("testing with mockito works correctly") {
            val F     = new TestFixture
