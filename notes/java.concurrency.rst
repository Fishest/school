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

