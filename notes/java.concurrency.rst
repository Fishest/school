============================================================ 
Chapter 2
============================================================ 

One can use the java.util.concurrent.atomic types to perform
atomic operations using the most performant native operations
available: cas, load linked/store conditional, or spin locks:

* AtomicReference<T>
* AtomicInteger
* AtomicLong
* AtomicBoolean
* AtomicReferenceFieldUpdater<T,V>
* AtomicReferenceArray<T>

The java syncronized block performc implicit locking of any
reference type (which can be used as implicit locks) this
protects all mutable state in the instance::

    syncronized(lock) { ... }

    // can also use the java machinery
    public synchronized void service() { ... }

There are a number of annotations that can be added to the java
code to allow thread documentation and can also be used by
FindBugs to identify threading bugs::

    @GuardedBy
    @ThreadSafe
    @NotThreadSafe
    @Immutable

Reentrant locks associate an entry count with a current thread
id. If the same thread id is recorded with an entry count > 0,
then it is allowed to increment the entry count. Otherwise it
is blocked.


------------------------------------------------------------
Section Keynotes:
------------------------------------------------------------

* To preserve state consistency, update related state
  variables in a single atomic operation.
* For every invariant that involves more than one variable,
  all the variables involved in that invariant must be
  guarded by the same lock.

============================================================ 
Chapter 3
============================================================ 

Not only do we want to make sure atomic operations are
synchronized, we also want to make sure other threads see
the results of other thread operations (volatile). For example,
a status variable that must be seen between threads::

    volatile boolean do_sleep;
    ...
    while (do_sleep) {
        countSomeSheep();
    }

64 bit values (long and double) are not safe to use outside
of being synchronized or volatile. Synchronized also
gurantees that operations in the block are made visible to
other reading threads.

If you are going to start a thread from a constructor, don't
start the thread in the constructor, expose a start or
initialize method instead (so the thread doesn't see an object
that isn't fully constructed). If you need to register an
event listener, use a factory method::

    public class SafeListener {
        private final EventListener listener;

        private SafeListener() {
            listener = new EventListener() {
                public void onEvent(Event e) {
                    doSomething(e);
                }
            };
        }

        public static SafeListener newInstance(EventSource source) {
            SafeListener safe = new SafeListener();
            source.registerListener(safe.listener);
            return safe;
        }
    }

An easy way to make data thread safe is to simply confine it
to a single thread's view. This is done in GUI event threads
and connection pools (thread confinement). Local variables
are confinement using the stack. Can also use `ThreadLocal<T>`
to create confined singletons or globals (use sparingly)::

    /*
     * data is stored in the Thread instance so it is garbage
     * collected when the thread exits
     */
    private static ThreadLocal<Connection> connectionHolder =
        new ThreadLocal<Connection>() {
            public Connection initialValue() {
                return DriverManager.getConnection(DB_URL);
            }
    };

    public static Connection getConnection() {
        return connectionHolder.get();
    }

Can store state in immutable objects and then simply replace
that instance with a new immutable object when the state
changes. In order to make completely immutable objects:

* Its state cannot be modified after construction
* All fields must be marked `final`
* It is properly constructed (`this` doesn't escape during ctor)

To publish an object safely, both the reference to the object
and the object's state must be made visible to other threads
at the same time. Safest way is with a static initializer (if
possible).  A properly constructed object can be safely published by:

* Initializing an object reference from a static initializer
* Storing a reference to it into a volatile field or AtomicReference
* Storing a reference to it into a final field of a properly constructed object
* Storing a reference to it into a field that is properly guarded by a lock


------------------------------------------------------------
Section Keynotes:
------------------------------------------------------------

* In the absence of synchronization, the compiler, processor,
  and runtime can do some downright weird things to the order
  in which operations appear to execute. Attempts to reason
  about the order in which memory actions "must" happen in
  insufficiently synchronized multithreaded programs will
  almost certainly be incorrect.
* Locking is not just about mutual exclusion; it is also
  about memory visibility. To ensure that all threads see
  the most up to date values of shared mutable variables,
  the reading and writing threads must synchronize on a
  common lock.
* Do not allow the this reference to escape during construction.
* Immutable objects are always thread safe.
* Just as it is a good practice to make all fields private unless
  they need greater visibility [EJ Item 12], it is a good practice
  to make all fields final unless they need to be mutable.
* Immutable objects can be used safely by any thread without
  additional synchronization, even when synchronization is not
  used to publish them.
* Safely published effectively immutable objects can be used
  safely by any thread without additional synchronization.

============================================================ 
Chapter 4
============================================================ 

The design process for a thread safe class should include
these three basic elements:

* Identify the variables that form the object's state
* Identify the invariants that constrain the state variables
* Establish a policy for managing concurrent access to the
  object's state.

The state of an object with N-primitive fields is just the
N-tuple of those fields. The number of ways to modify these
is the state space range. The smaller the state space, the
easier it is to reason about the data (ideally immutable
objects with 1 state).

Can encapsulate data to prevent concurrent access by:

* protecting in local lexical scope
* a private member field
* or between thread methods

Can make collections thread safe by using collection
decorator factories (implement the java monitor pattern):

* Collections.synchronizedList
* Collections.synchronizedMap
* Collections.synchronizedCollection
* Collections.synchronizedSet
* Collections.unmodifiable*

To make collections thread-safe, we need to return more than
an unmodifieable copy, because the underlying referenced
objects can still be changed.  We need to make a deepCopy
each time if we can't verify user code (defensive copies).
If the entries are immutable, then a shallow copy is fine::

    @ThreadSafe
    public class DelegatingVehicleTracker {
        private final ConcurrentMap<String, Point> locations;
        private final Map<String, Point> unmodifiableMap;

        public DelegatingVehicleTracker(Map<String, Point> points) {
            locations = new ConcurrentHashMap<String, Point>(points);
            unmodifiableMap = Collections.unmodifiableMap(locations);
        }

        public Map<String, Point> getLocations() {
            return unmodifiableMap;
        }

        public Point getLocation(String id) {
            return locations.get(id);
        }

        public void setLocation(String id, int x, int y) {
            if (locations.replace(id, new Point(x, y)) == null)
                throw new IllegalArgumentException("invalid vehicle name: " + id);
        }
    }

    /**
     * Can also return a static view of the data instead of a
     * live one
     */
    public Map<String, Point> getLocations() {
        return Collections.unmodifiableMap(
            new HashMap<String, Point>(locations));
    }

Note about private constructor capture idiom.

If you extend a collection to add new composite atomic methods
to it, you have to make sure that you are all using the same
lock for the operations (intrinsic vs explicit) otherwise
the atomic gurantee cannot be held::

    @ThreadSafe
    public class ListHelper<E> {
        public List<E> list =
            Collections.synchronizedList(new ArrayList<E>());

        public boolean putIfAbsent(E x) {
            synchronized (list) {
                boolean absent = !list.contains(x);
                if (absent)
                    list.add(x);
                return absent;
            }
        }
    }

    // a better example with composition
    @ThreadSafe
    public class ImprovedLis<T> implements List<T> {
        private final List<T> list;

        public ImprovedList(List<T> list) { this.list = list; }
        public synchronized boolean putIfAbsent(E x) {
            boolean absent = !list.contains(x);
            if (absent)
                list.add(x);
            return absent;
        }

        // and other methods delegated as such
        public synchronized void clear() { list.clear(); }
    }


------------------------------------------------------------
Section Keynotes:
------------------------------------------------------------

* You cannot ensure thread safety without understanding an
  object's invariants and post conditions. Constraints on the
  valid values or state transitions for state variables can
  create atomicity and encapsulation requirements.
* Encapsulating data within an object confines access to the
  data to the object's methods, making it easier to ensure that
  the data is always accessed with the appropriate lock held.
* If a class is composed of multiple independent thread safe
  state variables and has no operations that have any invalid
  state transitions, then it can delegate thread safety to
  the underlying state variables.
* Document a class's thread safety guarantees for its clients;
  document its synchronization policy for its maintainers.


