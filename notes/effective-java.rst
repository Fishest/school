------------------------------------------------------------
1. Use a static factory instead of a constructor
------------------------------------------------------------

* better naming
* implement specific version behind the scenes (LinkedList, ArrayList, etc)
* Generics!

How to use a factory to provide generic type inferrence::

    public static <K, V> HashMap<K, V> newInstance() {
      return new HashMap<K, V>();
    }
    
    ...
    Map<String, List<String>> m = HashMap.newInstance();

------------------------------------------------------------
... skip ...
------------------------------------------------------------

------------------------------------------------------------
8. Obey the equality rules
------------------------------------------------------------

* by default, equals checks if two instances are equal
* override only if you need to logically compare value types
* @Override public boolean equals(Object o) {}

------------------------------------------------------------
9. Always override hashCode when you override equals
------------------------------------------------------------

* equal objects must have equal hash codes
* if object is immutable, hashed a lot, etc memoize the hashCode
*
------------------------------------------------------------
10. Always override toString (64)
------------------------------------------------------------

* be wary of the format, people may come to depend on it

------------------------------------------------------------
11. Use clone judiciously
------------------------------------------------------------

* don't provide a clone, instead make a copy constructor

------------------------------------------------------------
12. Consider implementing Comparable
------------------------------------------------------------

If you implement this interface, you can get a whole lot of
power out of the java platform libraries::

    public interface Comparable<T> { 
        int compareTo(T t);
    }

* if your type exhibits natural ordering characteristics

------------------------------------------------------------
13. Minimize the Accessibility of classes and members (80)
------------------------------------------------------------

* never return a reference to a static final array, it is
  still mutable. Return a copy or an ummodifiable list::

    private static final Thing[] PRIVATE_VALUES = { ... };
    public static final List<Thing> VALUES =
        Collections.unmodifiableList(Arrays.asList(PRIVATE_VALUES));


------------------------------------------------------------
14. Use accessors, not public fields
------------------------------------------------------------

* public
* private
* protected
* module private (default)

------------------------------------------------------------
15. Minimize mutability
------------------------------------------------------------

Since they cannot be changed, they are thread safe. You can
create static final versions of commonly used values and you
can also create a factory to cache and share instances.

* don't provide any mutators
* mark the class as final to prevent extension
* mark all fields as final
* make all fields private
* operations should return a new instance or view
* don't have to make defensive copies; no clone needed

------------------------------------------------------------
16. Favor composition over inheritence
------------------------------------------------------------

* use decorators, delegation, or forwarding classes

------------------------------------------------------------
17. Design and document for inheritence, or prohibit it
------------------------------------------------------------

* document implementation so users don't stomp existing code
* test by writing a subclass while looking for friction
* don't call overridable methods in the constructor
* don't make serializable or cloneable
* don't "self use" other methods, move that code to a private helper function

------------------------------------------------------------
18. Prefer interfaces to abstract classes
------------------------------------------------------------

* make abstract classes for nontrivial interfaces
* simulated multiple inheritance (implement interface and
  delegate to abstract instance).
* optionally supply a SimpleImplementation
* abstract classes are very easy to extend in the future

  - existing sub classes just get new methods
  - much harder for interfaces (everyone needs to implement)

------------------------------------------------------------
19. User interfaces only to define types
------------------------------------------------------------

* don't write constant interfaces
  - instead use a static utility class
  - can import from that like `import static come.Something.ClassName.*;`

------------------------------------------------------------
20. Prefer class hierarchies to tagged classes
------------------------------------------------------------

------------------------------------------------------------
21. Use function objects to represent strategies
------------------------------------------------------------

Examples::

    // with classes and interfaces
    public class StringLengthCompare implements Comparator<String> {
        private StringLengthCompare() {}
        private static final StringLengthCompare INSTANCE
            = new StringLengthCompare();

        public int compare(String left, String right) {
            return left.length() - right.length();
        }
    }

    // with anonymous classes
    Arrays.sort(array, new Comparator<String() {
        public int compare(String left, String right) {
            return left.length() - right.length();
        }
    });

You can also implement a static member class::

    class Something {
        private static class StrLenCmp
            implements Comparator<String>, Serializeable { ... }
        public static final Comparator<String> STRING_LENGTH_COMPARATOR
            = new StrLenCmp();

        // ...
    }

* someday they will have lambdas/closures

------------------------------------------------------------
23. Favor static member classes over nonstatic
------------------------------------------------------------

* types of nested classes: static member, nonstatic member, anonymous, local

------------------------------------------------------------
36. Consistently use the Override annotation
------------------------------------------------------------

* you can use this for abstract and interface methods (say as
  a form of documentation).
* otherwise you are possibly overloading::

    @Override public boolean equals(Object o) {
        if (!(o instanceof Bigram))
            return false;
        Bigram b = (Bigram)o;

        return (b.first == first)
            && (b.second == second);
    }

------------------------------------------------------------
37. Use marker interfaces to define types
------------------------------------------------------------

* there are no methods on these interfaces, but they mark
  that certain behavior is exhibited in this class.
* if you want to limit a method to a type or if you are
  okay about not extending the interface later, use a marker
  interface.
* if you want to extend the mark later, use marker annotations

------------------------------------------------------------
38. Check parameters for validity
------------------------------------------------------------

------------------------------------------------------------
39. Make defensive copies of references
------------------------------------------------------------

* if the input parameter or return value is mutable, copy it
* perform copies of the values and then do validation
  (time of check/time of use attack)
* don't use clone to create a new instance

------------------------------------------------------------
40. API ideas
------------------------------------------------------------

* use a two element enum instead of a bool (can move some
  helper methods to the enum values)

------------------------------------------------------------
41. Use overloading judiciously
------------------------------------------------------------

* selection of overloaded methods is static, selection of
  overridden methods is dynamic.
* usually only overload with a different number of params
* be wary of autoboxing/unboxing

------------------------------------------------------------
42. Use varargs judiciously
------------------------------------------------------------

Here is how it is defined::

    static int sum(int... values) {
        int sum = 0;
        for (int value : values)
            sum += value;
        return sum;
    }

    // better
    static int sum(int first, int... values) {
        int sum = first;
        for (int value : values)
            sum += value;
        return sum;
    }

* To save the cost of creating an array, create overloads for
  the cases of 1-3 parameters and have a forth that adds the
  varargs.

------------------------------------------------------------
43. Return empty arrays or collections, not null
------------------------------------------------------------

* create one static final instance and return it instead
* Collection.toArray(T[]) will always return that instance so
  you can have your safety.
* Collections.emptyList, Collections.emptySet.

------------------------------------------------------------
44. Write doc comments for all exposed api methods
45. Minimize the scope of local variables
46. Prefer for each loops to traditional for loops
------------------------------------------------------------

The old way::
    for (Iterator i = c.iterator(); i.hasNext(); )
        doSomething((Element) i.next()); // (No generics before 1.5)

    for (int i = 0; i < a.length; ++i)
        doSomething(a[i])

The new way::

    for (Element e : elements)
        doSomething(e);

* cases where you have to revert to the old way
  1. filtering (need iterator.remove)
  2. transforming (so you can set that value)
  3. parallel iteration (two iterators at once)

------------------------------------------------------------
47. Know and use the libraries
48. Avoid float and double if you need exact answers
------------------------------------------------------------

* use BigDecimal, int, or long (fixed point)
* 9 decimal points for int, 18 for long (a good guide)

------------------------------------------------------------
49. Prefer primitives to boxed primitives
------------------------------------------------------------

* == on boxed primitives does not unbox and will compare instance
  - unbox manually with local variables to be sure.
* must use the boxed primitives for elements, values, and keys in
  collections.
* unboxing can throw a null pointer exception if the reference is
  not set already.

------------------------------------------------------------
50. Avoid strings where other types are appropriate
51. Beware string concatenation performance
------------------------------------------------------------

* long story short, use the stringbuilder

------------------------------------------------------------
52. Refer to objects by their interfaces
53. Prefer interfaces to reflection
------------------------------------------------------------

------------------------------------------------------------
2. Use a builder for lots of parameters
------------------------------------------------------------

* better than telescoping constructors
* can make defaults, and immutable final

example::

    public class Something {
      private final int example;

      public static class Builder {
        private int example;

        public Builder() {}
        public Builder example(int val) {
          example = val; return this;
        }
        public Something build() {
          return new Something(this);
        }
      }

      private Something(Builder builder) {
        example = builder.example;
      }
    }

    Something handle = Something.Builder()
      .example(22).build();

------------------------------------------------------------
3. Singletons a la Java
------------------------------------------------------------

The classical version::

    public class Example {
      public static final Example Instance = new Example();
      private Example() {}
      private Object readResolve() {
        return Instance;
      }

      public void someMethod() { }
    }
   }

A new interesting version in 1.5::

    public enum Example {
      Instance;

      public void someMethod() { }
    }

------------------------------------------------------------
4. Force a class to be noninstantiable
------------------------------------------------------------

In case you don't want the class to be an instance and also
prevent the class from being subclassed::

    public class Example {
      private Example() { }
    }

------------------------------------------------------------
5. Don't create extra instances
------------------------------------------------------------

Immutable objects can always be reused (say factory methods
that return the same intances). Mutable objects can as well
if we know they won't be modified. You can do things once
like this::

    public class Example {
      private final Date birthday;
      private static final Date start;
      private static final Date end;

      static {
        Calendar cal = Calendar.getInstance(TimeZone.getTimeZone("GMT"));
        cal.set(1946, Calendar.JANUARY, 1, 0, 0, 0);
        _start = cal.getTime();
        cal.set(1964, Calendar.JANUARY, 1, 0, 0, 0);
        _end = cal.getTime();
      }

      public boolean isInRange() {
        return birthday.compare(start) >= 0 &&
               birthday.compare(end)   <  0;
      }
    }

------------------------------------------------------------
6. Don't hold on to unused references
------------------------------------------------------------

You can help by assigning them to null so they can be
garbage collected. Do this only when you need to though, as
otherwise you are wasting your time. The best way to manage
references is to give them the smallest scope needed and let
them fall out and be collected. In short, if your code is
managing its own memory, help the GC out.

* WeakHashMap for caches
* Register events and callbacks wrapped in WeakReference

------------------------------------------------------------
7. Avoid Finalizers
------------------------------------------------------------

Instead, just make sure you provide a cleanup method for the
instance in question and have it run in a finally block.

Here is a way to guarantee a subclassed finalizer is called::

    // ideally you should do this
    public class SubFoo : Foo {
      @Override protected void finalize throws Throwable {
        try {
          ... cleanup here
       } finally {
         super.finalze();
       }
      }
      ...
    }

    // however this forces the cleanup with a finalizer guard
    public class Foo {
      // Sole purpose of this object is to finalize outer Foo object
      private final Object finalizerGuardian = new Object() {
        @Override protected void finalize() throws Throwable {
        ... // Finalize outer Foo object
        }
      };
    }

------------------------------------------------------------
23. Don't use raw types in new code
------------------------------------------------------------

How to iterate through java collections::

    for (Item it : collection) {
        ... do something
    }

    for (Iterator<Item> t = collection.iterator(); t.hasNext();) {
         Item it = i.next();
         ... do something
    }

* unbounded wildcard lets you ignore generic type `List<?>`

------------------------------------------------------------
25. Prefer lists to arrays
------------------------------------------------------------

* arrays are covariant, lists are invariant
* arrays are reified (runtime type check), lists use type
  erasure (compile time check)
* arrays and generics don't mix

------------------------------------------------------------
28. Use bounded wildcards to increase flexability
------------------------------------------------------------

* generics are invariant (List<String> != List<Object>)
* note, every type is a subtype of itself...
* do not use wildcard types for returns
* we can force this using ?::

    public class Stack<E> {
        public void pushAll(Iterable<? extends E> source) {
            for (E el : source) {   // producer extends
                push(el);
            }
        }

        public void popAll(Collection<? super E> destination) {
            while (!isEmpty()) {    // consumer super
                destination.add(pop());
            }
        }
        ...
    }

    // to force the type instead of type inferrence
    Set<Number> numbers = Union.<Number>union(integers, doubles);

* use this with producer/consumer code
* if a type parameter appears only once in a method declaration,
  replace it with a wildcard

* <? extends T> - has to be a subtype of some type (upper bound)
* <? super T> - has to be an ancestor of some type (lower bound)
* <?> (<? extends Object>) - can be any type

------------------------------------------------------------
29. Use typesafe heterogeneous containers
------------------------------------------------------------

Example::

    public class Favorite {
        private Map<Class<?>, Object> favorites = new HashMap<Class<?>, Object>();

        public <T> void put(Class<T> type, T instance) {
            if (type == null)
                throw new NullPointerException("arg can't be null");
            favorites.put(type, type.cast(instance)); // forces type safety
        }

        public <T> T get(Class<T> type) {
            return type.cast(favorites.get(type));
        }
    }

 * this trick is used by the checkedX collections (useful for
   mixing legacy and new code)
 * can't be used with non-reifiable types (super type tokens?)

------------------------------------------------------------
30. Use enums instead of int constants
------------------------------------------------------------

* constants are substituted at compile time (libraries need to recompile
  if a change occurs). Not type safe.
* enum is a singleton that exposes a public final field for each enum
  entry. They are classes that cannot be extended.
* they impelemnt all object methods correctly, serializable, comparable
* can contain methods!
* can enumerate all entries with `Planet.values()`

You can provide a constructor for each element in the enum, make fields
final though as this is a singleton::

     public enum Planet {
         MERCURY(3.302e+23, 2.439e6),
         VENUS (4.869e+24, 6.052e6),
         EARTH (5.975e+24, 6.378e6),
         MARS (6.419e+23, 3.393e6),
         JUPITER(1.899e+27, 7.149e7),
         SATURN (5.685e+26, 6.027e7),
         URANUS (8.683e+25, 2.556e7),
         NEPTUNE(1.024e+26, 2.477e7);

         private final double mass; // In kilograms
         private final double radius; // In meters
         private final double surfaceGravity; // In m / s^2
         // Universal gravitational constant in m^3 / kg s^2
         private static final double G = 6.67300E-11;

         // Constructor
         Planet(double mass, double radius) {
             this.mass = mass;
             this.radius = radius;
             surfaceGravity = G * mass / (radius * radius);
         }

         public double mass() { return mass; }
         public double radius() { return radius; }
         public double surfaceGravity() { return surfaceGravity; }
         public double surfaceWeight(double mass) {
             return mass * surfaceGravity; // F = ma
         }
     }

 Can define behavior for each element by using an abstract method
 (constant specific method implementations)::

    public enum Operation {
        PLUS { double apply(double x, double y){return x + y;} },
        MINUS { double apply(double x, double y){return x - y;} },
        TIMES { double apply(double x, double y){return x * y;} },
        DIVIDE { double apply(double x, double y){return x / y;} };

        abstract double apply(double x, double y);
    }

* if you override the toString, consider writing a fromString to
  convert it back (say with a static final HashMap for speed).
* for semi common implementations, can implememnt an inner
  private class (possibly with private enum) to select behavior
  as opposed to defaulting to a concrete method or using a
  switch on the current value type.

------------------------------------------------------------
31. Use a backing field instead of the enum ordinal value
------------------------------------------------------------

------------------------------------------------------------
32. Use EnumSet instead of bit fields
------------------------------------------------------------

* if you have less than 64 elements, the storage is a single
  long value.

Example of usage::

    public class Text {
        public enum Style { BOLD, ITALIC, UNDERLINE }
        public void applyStyles(Set<Style> styles);
    }
    ...
    text.applyStyles(EnumSet.of(Style.BOLD, style.UNDERLINE));

------------------------------------------------------------
33. Use EnumMap instead of ordinal ordering
------------------------------------------------------------

------------------------------------------------------------
34. Emulate extensible enums with interface
------------------------------------------------------------

This can be used to allow for clients to specify their own
opcode mappings for a framework::

    public interface Operation {
         double apply(double x, double y);
    }

    public enum BasicOperation implements Operation {
    ...
    }

    // can do logical generic constraint operations
    private static <T extends Enum<T> & Operation> void test(
        Class<T> opSet, double x, double y)
    {
        // can get all the enumerations of a class type
        for (Operation op : opSet.getEnumConstants())
            System.out.printf("%f %s %f = %f%n", x, op, y, op.apply(x, y));
    }

------------------------------------------------------------
35. Prefer annotations to naming patterns
------------------------------------------------------------

Example annotation with meta-annotations::

    // Marker annotation type declaration
    import java.lang.annotation.*;

    /**
    * Indicates that the annotated method is a test method.
    * Use only on parameterless static methods.
    */
    @Retention(RetentionPolicy.RUNTIME)
    @Target(ElementType.METHOD)
    public @interface Test { }

------------------------------------------------------------
53. Prefer interfaces to reflection
------------------------------------------------------------

* don't use reflection in normal operation
* if you have a parameterless constructor, you can use
  Classname.newInstance to get an instance.

------------------------------------------------------------
54. Use native methods judiciously
55. Optimize judiciously
56. Adhere to naming conventions
57. Use exceptions for exceptional cases
58. Use the correct exception for the job
------------------------------------------------------------

* three types of exceptions: checked exceptions,
  runtime exceptions, and errors.
* use checked excepetions for cases where the client can recover
* use runtime exceptions to indicate programming errors
  - make these subclass RuntimeException directly or indirectly

------------------------------------------------------------
59. Avoid unnecessary checked exceptions
60. Favor the use of standard exceptions
61. Throw exceptions appropriate to the abstraction
------------------------------------------------------------

* higher level code should catch and translate lower level
  exceptions.
* can then get inner exception with getCause (make the
  constructor take the throwable to wrap and base to base)

------------------------------------------------------------
62. Document all exceptions thrown by code
------------------------------------------------------------

* with javadoc @throws and the throws clause
  - use javadoc for checked and unchecked
  - use throws clause for checked

------------------------------------------------------------
63. Include relevant data in exception
------------------------------------------------------------

* including parameters that caused the exception

------------------------------------------------------------
64. Strive for failure atomicity
65. Don't ignore exceptions 
------------------------------------------------------------

* if an instance throws, it should revert back to the state
  it was in before it threw.

------------------------------------------------------------
66. Synchronize access to shared mutable data
------------------------------------------------------------

* ensures that changes in one thread are viewed from another
  thread and that the thread doesn't read in an inconsistent
  state.
* reading a writing a variable is atomic unless it is of
  type long or doulbe.
* even though these operations are atomic, the volatile state
  may not be observed without the synchronize statement (the
  value could be optimized away or hoisted)::

    // using synchronized (slower)
    private static boolean stopRunning;
    private static synchronized void doStop() {
        stopRunning = true;
    }
    private static synchronized bool isStopped() {
        return stopRunning;
    }

    // using volatile
    private static volatile boolean stopRunning;

 * use the java.util.concurrent.atomic types if needed instead
   of synchronized.
 * do as little work as possible in a syncronized block

------------------------------------------------------------
68. Prefer executors to threads
------------------------------------------------------------

Here is an example::

    ExecutorService executor = Executors.newFixedThreadPool();
    ExecutorService executor = Executors.newCachedThreadPool();
    ExecutorService executor = Executors.newSingleThreadExecutor();

    executor.execute(runnable);
    executor.shutdown();

* two types of tasks:
  1. Runnable(does not return a value)
  2. Callable(returns a value).

* can use ScheduledThreadPoolExecutor instead of Timer

------------------------------------------------------------
69. Prefer concurrency utilities to wait and notify
------------------------------------------------------------

* use executor framework, concurrent collections, and
  synchronizers::

    public static long time(Executor executor, int concurrency,
        final Runnable action) throws InterruptedException {
        final CountDownLatch ready = new CountDownLatch(concurrency);
        final CountDownLatch start = new CountDownLatch(1);
        final CountDownLatch done  = new CountDownLatch(concurrency);
        for (int i = 0; i < concurrency; i++) {
            executor.execute(new Runnable() {
                public void run() {
                    ready.countDown(); // Tell timer we're ready
                    try {
                        start.await(); // Wait till peers are ready
                        action.run();
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                    } finally {
                        done.countDown(); // Tell timer we're done
                    }
                }
            });
        }
        ready.await(); // Wait for all workers to be ready
        long startNanos = System.nanoTime();
        start.countDown(); // And they're off!
        done.await(); // Wait for all workers to finish
        return System.nanoTime() - startNanos;
    }

    // The standard idiom for using the wait method
    synchronized (obj) {
        while (<condition does not hold>)
            obj.wait(); // (Releases lock, and reacquires on wakeup)
        ... // Perform action appropriate to condition
    }

------------------------------------------------------------
70. Always document thread safety
71. Use lazy initialization judicuosly
------------------------------------------------------------

The following will not be initialized unless the class is
initialized::

    // Lazy initialization holder class idiom for static fields
    private static class FieldHolder {
        static final FieldType field = computeFieldValue();
    }
    static FieldType getField() { return FieldHolder.field; }

* use the double check pattern for lazy initialization

------------------------------------------------------------
72. Don't use non-portable thread facilities
------------------------------------------------------------

* The following are not portable and are not guranteed to do
  anything across JVM impelemntations:

  - Thread.yield
  - Thread.sleep(0)
  - Thread priorities

------------------------------------------------------------
73. Don't use thread groups
74. Implement serializeable judiciously
------------------------------------------------------------
