================================================================================
Java Libraries
================================================================================

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

Example of verification of method invocations::

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
the last stub will be persisted)::

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    when(mock.get(0)).thenReturn("first");
    when(mock.get(1)).thenThrow(new RuntimeException());

    mock.get(0); // returns "first"
    mock.get(1); // throws

Example of using argument matchers::

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    when(mock.get(anyInt())).thenReturn("first");

    mock.get(999);

    verify(mock).get(anyInt());

Example of mocking a method that returns void::

    import java.util.List;
    import static org.mockito.Mockito.*;

    List mock = mock(List.class);
    doThrow(new RuntimeException()).when(mock).clear();

    mock.clear();

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Verification
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can verify that a method was called with some matcher a number of different
ways::

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
Mockito/Hamcrest Matchers
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
matcher that extends ArgumentMatcher<T>::

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

If you need to stub consecutive calls, use the iterator style stubbing::

    // can mix and match results like return and throw
    when(mock.get("arg"))
        .thenReturn("example")
        .thenThrow(new RuntimeException());

    // can use shorthand; note after 3rd call, every further call will return c
    when(mock.get("arg"))
        .thenReturn("a", "b", "c");

If you need to add side effects to your call, then you can use the `Answer`
interface::

    when(mock.method(any())).thenAnswer(new Answer() {
        Object answer(InvocationOnMock invocation) {
            Object[] args = invocation.getArguments();
            Object mock = invocation.getMock();
            return "called with arguments: " + args;
        }
    });

If the method returns void (or does something a little weird), then you can use one
of the following::

    doReturn("value").when(mock).call();
    doNothing()).when(mock).clear();
    doCallRealMethod()).when(mock).clear();
    doThrow(new RunTimeException()).when(mock).clear();
    doAnswer(new Answer() { ... }).when(mock).clear();

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mockito Annotations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of manually wiring up the mocks in each call, mockito allows interfaces
to be annotated with `@Mock` and then autowirted with a startup call::

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
methods cannot be mocked)::

    import java.util.List;
    import static org.mockito.Mockito.*;

    // this creates a copy of the instance to spy on
    List spy = spy(New LinkedList());

    // cannot use the other method to mock calls
    doThrow(new RuntimeException()).when(spy).add("two");

    verify(spy).add("one");
    verify(spy).add("two");

You can also use the argument captor for post call verification::

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
