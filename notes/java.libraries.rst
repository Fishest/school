================================================================================
Java Libraries
================================================================================

--------------------------------------------------------------------------------
JUnit
--------------------------------------------------------------------------------

http://junit.sourceforce.com

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Basic template of a JUnit test:

.. code-block:: java

    import org.juni.*;
    import static org.junit.Assert.*;
    import java.util.*;

    private class SampleTest {
        private List emptyList;

        // code that is run once on test startup
        @BeforeClass
        public static void setupClass() { }

        // code that is run once on test shutdown
        @AfterClass
        public static void teardownClass() { }

        // code that is run before each test
        @Before
        public void setup() {
            emptyList = new ArrayList();
        }

        // code that is run after each test
        @After
        public void teardown() {
            emptyList = null;
        }

        // code that tests a single expectation
        @Test
        public void testSomeBehavior() {
            assertEquals("emptylist should have 0 elements", 0,
                emptyList.size());
        }

        @Ignore // ignore a test that shouldn't be used yet
        @Test
        public void testUnfinishedTest() { }
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Exceptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Junit offers a few different ways to test for exceptions in your tests:

.. code-block:: java

    public class ExceptionTests {

        @Test(expected=IndexOutOfBoundsException.class)
        public void test_exception_message() {
            new ArrayList<Object>().get(0);
        }
    }

.. code-block:: java

    public class ExceptionTests {

        @Test
        public void test_exception_message() {
            try {
                new ArrayList<Object>().get(0);
            } catch (IndexOutOfBoundsException ex) {
                assertThat(ex.getMessage(), is("Index: 0, Size: 0"));
            }
        }
    }

.. code-block:: java

    import static org.junit.JUnitMatchers.containsString;

    public class ExceptionTests {
        @Rule ExpectedException thrown = ExpectedException.none();

        @Test
        public void test_exception_message() {
            thrown.expect(IndexOutOfBoundsException.class);
            thrown.expectMessage("Index: 0, Size: 0");       // exact match
            thrown.expectMessage(containsString("Size: 0")); // using matchers

            new ArrayList<Object>().get(0);
        }
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Matchers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Junit includes the hamcrest matchers for more advanced matching which can be
used for better error messages and more readable tests:

.. code-block:: java

    import static org.hamcrest.CoreMatchers.allOf;
    import static org.hamcrest.CoreMatchers.anyOf;
    import static org.hamcrest.CoreMatchers.equalTo;
    import static org.hamcrest.CoreMatchers.not;
    import static org.hamcrest.CoreMatchers.sameInstance;
    import static org.hamcrest.CoreMatchers.startsWith;
    import static org.junit.Assert.assertThat;

    public class AssertTests {
        @Test
        public void test_hamcrest_matchers() {
            assertThat("good", allOf(equalTo("good"), startsWith("good")));
            assertThat("good", not(allOf(equalTo("bad"), equalTo("good"))));
            assertThat("good", anyOf(equalTo("bad"), equalTo("good")));
            assertThat(7, not(CombinableMatcher.<Integer> either(equalTo(3)).or(equalTo(4))));
            assertThat(new Object(), not(sameInstance(new Object())));
        }
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There is one rule for creating temporary folders that are created and cleaned
before each test is run:

.. code-block:: java

    public static class HasTempFolder {
      @Rule
      public TemporaryFolder folder = new TemporaryFolder();

      @Test
      public void testUsingTempFolder() throws IOException {
        File createdFile = folder.newFile("myfile.txt");
        File createdFolder = folder.newFolder("subfolder");
        // ...
      }
    } 

ExternalResource allows one to create and tear down an external resource like
a file, socket, etc:

.. code-block:: java

    public static class UsesExternalResource {
      Server myServer = new Server();

      @Rule
      public ExternalResource resource = new ExternalResource() {
        @Override
        protected void before() throws Throwable {
          myServer.connect();
        };

        @Override
        protected void after() {
          myServer.disconnect();
        };
      };

      @Test
      public void testFoo() {
        new Client().run(myServer);
      }
    }

`ErrorCollector` allows one to collect all errors from a test instead of
stopping on the first error:

.. code-block:: java

    public static class UsesErrorCollectorTwice {
      @Rule
      public ErrorCollector collector= new ErrorCollector();

      @Test
      public void example() {
        collector.addError(new Throwable("first thing went wrong"));
        collector.addError(new Throwable("second thing went wrong"));
      }
    }

`TimeoutRule` applies the same global timeout to all the tests in a class:

.. code-block:: java

    public static class HasGlobalTimeout {
      public static String log;

      @Rule
      public TestRule globalTimeout = new Timeout(20);

      @Test
      public void testInfiniteLoop1() {
        log+= "ran1";
        for(;;) {}
      }

      @Test
      public void testInfiniteLoop2() {
        log+= "ran2";
        for(;;) {}
      }
    }

--------------------------------------------------------------------------------
Guice
--------------------------------------------------------------------------------

http://code.google.com/p/google-guice/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--------------------------------------------------------------------------------
Mockito
--------------------------------------------------------------------------------

http://code.google.com/p/mockito/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Basic Actions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Example of verification of method invocations:

.. code-block:: java

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);

    mock.add("one");
    mock.clear();

    verify(mock).add("one");

Example of stubbing methods from an interface (by default, mockito returns the
appropriate default values for various types: null for references, empty
collections, or the default primitive value) (methods are stubbed uniquely by
<method-name, argument>, so if the same pair is stubbed multiple times, only
the last stub will be persisted):

.. code-block:: java

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    when(mock.get(0)).thenReturn("first");
    when(mock.get(1)).thenThrow(new RuntimeException());

    mock.get(0); // returns "first"
    mock.get(1); // throws

Example of using argument matchers:

.. code-block:: java

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    when(mock.get(anyInt())).thenReturn("first");

    mock.get(999);

    verify(mock).get(anyInt());

Example of mocking a method that returns void:

.. code-block:: java

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    doThrow(new RuntimeException()).when(mock).clear();

    mock.clear();

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can verify that a method was called with some matcher a number of different
ways:

.. code-block:: java

    verify(mock).add("one"); // times(1) is the default
    verify(mock, times(1)).add("one");
    verify(mock, times(3)).add("three");
    verify(mock, never()).add("never");
    verify(mock, atLeastOnce()).add("ten");
    verify(mock, atLeast(4)).add("five");
    verify(mock, atMost(5)).add("three");

    // to verify calls happened in order on a single mock
    InOrder order = inOrder(mock);
    order.verify(mock.add("first"));
    order.verify(mock.add("second"));

    // to verify calls happened in order on a multiple mocks
    InOrder order = inOrder(mock1, mock2);
    order.verify(mock1.add("first"));
    order.verify(mock2.add("second"));

    // to verify that no other mocks interacted with a method
    verify(mock1).add("one");
    verifyZeroInteractions(mock2, mock3);

    // to verify that nothing more happened
    mock.add("one");
    verify(mock).add("one");
    verifyNoMoreInteractions(mock);

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito / Hamcrest Matchers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use argument matchers, then all arguments must be supplied by matchers,
otherwise an exception will be thrown (setup and verification). What follows is
a list of the various available matchers:

* `eq(<T>)` - matchers for all primitives and object equality testing
* `any()` - matches anything
* `any(Class<T>)` - matches any instance of the given class
* `any*()` matchers for all the java common types (ex: `anyInt()`)
* `argThat(org.hamcrest.Matcher)` can be used for custom matchers
* `isA(Class<T>)` - matches any object that implements a class
* `isNull()` - matches any null
* `isNontNull()` - matches any not null
* `refEq(<T>, ...excludedFields)` - matches a given reference with excluded fields
* `startsWith(String)` - matches a string that starts with a value
* `endsWith(String)` - matches a string that ends with a value

Custom matchers can be supplied with the `argThat()` matchers. Simply supply a
matcher that extends ArgumentMatcher<T>:

.. code-block:: java

    class IsListOfTwoElements extends ArgumentMatcher<List> {
        public boolean matches(Object list) {
            return ((List)list).size() == 2;
        }

        public static List isListOfTwoElements() {
            return argThat(new IsListOfTwoElements());
        }
    }

    import java.util.List;
    import static org.mockito.Mockito.*;
    import static IstListOfTwoElements.*;

    List mock = mock(List.class);

    when(mock.get(isListOfTwoElements())).thenReturn("first");

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Stubbing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to stub consecutive calls, use the iterator style stubbing:

.. code-block:: java

    // can mix and match results like return and throw
    when(mock.get("arg"))
        .thenReturn("example")
        .thenThrow(new RuntimeException());

    // can use shorthand; note after 3rd call, every further call will return c
    when(mock.get("arg"))
        .thenReturn("a", "b", "c");

If you need to add side effects to your call, then you can use the `Answer`
interface:

.. code-block:: java

    when(mock.method(any())).thenAnswer(new Answer() {
        Object answer(InvocationOnMock invocation) {
            Object[] args = invocation.getArguments();
            Object mock = invocation.getMock();
            return "called with arguments: " + args;
        }
    });

If the method returns void (or does something a little weird), then you can use one
of the following:

.. code-block:: java

    doReturn("value").when(mock).call();
    doNothing()).when(mock).clear();
    doCallRealMethod()).when(mock).clear();
    doThrow(new RunTimeException()).when(mock).clear();
    doAnswer(new Answer() { ... }).when(mock).clear();

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of manually wiring up the mocks in each call, mockito allows interfaces
to be annotated with `@Mock` and then autowirted with a startup call:

.. code-block:: java

    public class ExampleServiceTest {
        @Mock private ServiceClient client;
        @Mock private ServiceDatabase database;
        @Mock private ServiceConfiguration config;

        @InjectMocks private ExampleService service;

        @Before public void setup() {
            MockitoAnnotations.initMocks(this);
            // inject mocks basically does the following
            // service = new ExampleService(client, database, config);
        }
    }

There are also a few other annotations that can be used:

* `@Spy` to easily create a spy
* `@Mock` to easily create a mock
* `@Captor` to easily create a captor
* `@InjectMocks` to use available mocks to initialize a test class

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Spying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mockito basically allows AOP style spying on real objects (calling through).
This can be used to verify invocations on objects as follows (note, final
methods cannot be mocked):

.. code-block:: java

    import java.util.List;
    import static org.mockito.Mockito.*;

    // this creates a copy of the instance to spy on
    List spy = spy(New LinkedList());

    // cannot use the other method to mock calls
    doThrow(new RuntimeException()).when(spy).add("two");

    verify(spy).add("one");
    verify(spy).add("two");

You can also use the argument captor for post call verification:

.. code-block:: java

    ArgumentCaptor<Person> argument = ArgumentCaptor.forClass(Person.class);
    Person mock = mock(Person.class);
    verify(mock).contact(argument.capture());
    assertEquals("John", argument.getValue().getName());

--------------------------------------------------------------------------------
PowerMock
--------------------------------------------------------------------------------
http://code.google.com/p/powermock/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: finish notes
