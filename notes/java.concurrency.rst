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


============================================================ 
Chapter 5
============================================================ 

The synchronized collections include Vector, Hashtable, and
the Collections.synchronizedXxx factory wrappers. These guard
each single method, however, compound methods may need extra
guards. In order to lock these, we must aquire the collections
intrinsic lock before performing these actions (the same is
true for iteration)::

    public static Object getLast(Vector list) {
        synchronized(list) {
            int lastIndex = list.size() - 1;
            return list.get(lastIndex);
        }
    }

    public static Object deleteLast(Vector list) {
        synchronized(list) {
            int lastIndex = list.size() - 1;
            return list.remove(lastIndex);
        }
    }

The new collections will throw a ConcurrentModificationException
if they detect that the underlying collection has been
altered during iteration. This is done without synchronization so
the iterator altering detection may be stale. One way to prevent
this is to lock while iterating, or one can clone the enire
collection (best if this is rare and the collection size is small).
One must also be aware of hidden iterators (like converting a
collection toString).

The synchronized wrappers are thread safe, but suffer a
performance penalty from single locks.  The Concurrent
collections are designed to be used from many threads at once
with high performance (they also add a number of compound
operations that are guranteed to be atomic):

* Queue - queue interface (LinkedList implements Queue)
* BlockingQueue - blocks is empty (for consumer) or full (bounded producer)
* PriorityQueue - non concurrent heap
* ConcurrentMap - Interface for a concurrent map
* ConcurrentHashMap - uses lock striping to be more efficient
* CopyOnWriteArraySet - create a new set for modification
* CopyOnWriteArrayList - old list reference is safe for iteration
* ConcurrentLinkedQueue
* ConcurrentSkipListMap - Concurrent SortedMap (synchronized TreeMap)
* ConcurrentSkipListSet - Concurrent SortedSet (synchronized TreeSet)

The concurrent iterators are weakly consistent: they allow modifications
while they are being iterated over and may include modifications into
a current iterator while it is being traversed. Also, size and isEmpty
have been relaxed to give "estimates" for greater performance. Also,
the intrinsic lock of concurrent collections will not lock the entire
collection::

    public interface ConcurrentMap<K,V> extends Map<K,V> {
        // Insert into map only if no value is mapped from K
        V putIfAbsent(K key, V value);
        // Remove only if K is mapped to V
        boolean remove(K key, V value);
        // Replace value only if K is mapped to oldValue
        boolean replace(K key, V oldValue, V newValue);
        // Replace value only if K is mapped to some value
        V replace(K key, V newValue);
    }

The CopyOnWrite collections are useful for event notification
systems (collections of listeners).

BlockingQueues add the `put` and `take` methods that are useful
for producer and consumers. The queues can be bounded or
unbounded (a put on a bounded queue will block if full, but
a put on an unbounded queue will never block). This can be
used to make a simple work queue with a thread pool (which
is basically the Executor task execution framework):

* DelayQueue
* LinkedBlockingQueue - LinkedList implementation
* ArrayBlockingQueue - ArrayList implementation
* PriorityBlockingQueue - PriorityQueue implementation using
  the underlying implemented Comparable or a Comparator
* SynchronousQueue - No storage, just threads waiting to be
  assigned their next item.

Deque collections allow for efficient work stealing queues.
Each consumer has their own Deque. If any consumer finishes
off their own queue, they can steal work from the tail of
another worker's Deque (rather than the head). This results
in less contention as not every thread is vieing for the
same queue. These are well suited to the case where a producer
is also a consumer: for example a web crawler that produces
more pages to crawl every time it sees new pages or any geneal
graph traversal problem (gc heap for example):

* Deque - A double ended queue that can insert/remove from both ends
* ArrayDeque - An array implementation of Deque 
* BlockingDeque - A blocking Deque
* LinkedBlockingDeque - A linked list BlockingDeque

If you implement runnable, you cannot ignore the InterruptedException
that may be thrown when a thread blocking call has been made::

    public class TaskRunnable implements Runnable {
        BlockingQueue<Task> queue;
        ...
        public void run() {
            try {
                processTask(queue.take());
            } catch (InterruptedException ex) {
                // restore interrupted status
                Thread.currentThread().interrupt();
            }
        }
    }

There are a number of synchronization primitives available
in the java bcl:

* CountDownLatch
* Future - Interface for an async computation
* FutureTask - Implementation of `Future`
* CyclicBarrier
* Semaphore

Latches are a gate to block threads until some event
happens, and then allow threads to proceed (can only block
once). Can use a CountDownLatch to make sure all threads
are initialized before starting their work::

    public class TestHarness {
        public long timeTasks(int nThreads, final Runnable task)
            throws InterruptedException {

            final CountDownLatch startGate = new CountDownLatch(1);
            final CountDownLatch endGate = new CountDownLatch(nThreads);

            for (int i = 0; i < nThreads; i++) {
                Thread t = new Thread() {
                    public void run() {
                        try {
                            startGate.await();
                            try {
                                task.run();
                            } finally {
                                endGate.countDown();
                            }
                        } catch (InterruptedException ignored) { }
                    }
                };
                t.start();
            }
            long start = System.nanoTime();
            startGate.countDown();
            endGate.await();
            long end = System.nanoTime();
            return end-start;
        }
    }

FutureTask implements `Future` and runs a `Callable`. It can
be in one of three states: waiting to run, running, or
completed. Once it is completed, it will stay completed.
If the task is completed, `get` returns the result of the
operation immediately.  Otherwise, it will block until:
the task completes, the get times out, or the task throws (one of
checked exception thrown by the callable, a runtime exception, or
an Error)::

    public ExpensiveObject preload() throws ExecutionException, InterruptedException {
        FutureTask<ExpensiveObject> future = new FutureTask<ExpensiveObject>(
            new Callable<ExpensiveObject>() {
                public ExpensiveObject call() throws Exception {
                    Thread.sleep(5000);
                    return generateResult();
                }
        });

        Thread thread = new Thread(future);
        thread.start();
        // do other work here
        return future.get();
    }

Semaphore can be used to implement a counting semaphore to
control the number of activies that can access a certain
resource at the same time (can implement resource pools).
Can also use this to create blocking bounded collections.
The number of permits is specified in the constructor:
release returns a count to the semaphore and acquire
gets a single count from the semaphore or blocks if the
count is zero.  A binary semaphore (with a count of 1)
is a mutex to allow for mutual exclusion (non-reentrant).
The semaphore is not limited to the number of permits it
is initialized with and another thread can release for
any other thread (no permit association) for things like
deadlock prevention (which locks do not allow)::

    public class BoundedHashSet<T> {
        private final Set<T> set;
        private final Semaphore sem;

        public BoundedHashSet(int bound) {
            this.set = Collections.synchronizedSet(new HashSet<T>());
            this.sem = new Semaphore(bound);
        }

        public boolean add(T item) throws InterruptedException {
            sem.acquire();
            boolean wasAdded = false;

            try {
                wasAdded = set.add(item);
                return wasAdded;
            } finally {
                if (!wasAdded)
                    sem.release();
            }
        }

        public boolean remove(Object item) {
            boolean wasRemoved = set.remove(item);
            if (wasRemoved)
                sem.release();
            return wasRemoved;
        }
        // and the rest of the implementation follows
    }

CyclicBarrier implements a thread barrier that cannot be
passed until all the threads arrive (latches are for waiting
for events, barriers are for waiting for threads). When a thread
reaches the barrier, it calls `await` and waits until all the
other threads arrive. After all threads arrive, the barrier
can be reset and used again. A `Runnable` can be supplied to
be run after all the threads have arrived, but before they are
released.  Also, each thread is given an arrival order id that
can be used for leader election. A barrier is useful in breaking
concurrent problems down into smaller subproblems: n-body
particle simulations (update new position of each particle
before next step). Exchanger is another barrier that allows
two threads to exchange some data as the barrier step.

------------------------------------------------------------
Section Keynotes:
------------------------------------------------------------

* For CPU bound problems #CPU or #CPU + 1 is the ideal number
  of threads to use to parallelize a problem. More threads
  will not help.
