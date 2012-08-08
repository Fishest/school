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
