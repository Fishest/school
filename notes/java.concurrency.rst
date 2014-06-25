============================================================
Java Concurrency In Practice
============================================================

-------------------------------------------------------------
Chapter 2
-------------------------------------------------------------

One can use the java.util.concurrent.atomic types to perform
atomic operations using the most performant native operations
available: cas, load linked/store conditional, or spin locks:

* `AtomicReference<T>`
* `AtomicInteger`
* `AtomicLong`
* `AtomicBoolean`
* `AtomicReferenceFieldUpdater<T,V>`
* `AtomicReferenceArray<T>`

The java syncronized block performs implicit locking of any
reference type (which can be used as implicit locks) this
protects all mutable state in the instance:

.. code-block:: java

    syncronized(lock) { ... }

    // can also use the java machinery
    public synchronized void service() { ... }

There are a number of annotations that can be added to the java
code to allow thread documentation and can also be used by
FindBugs to identify threading bugs:

.. code-block:: java

    @GuardedBy
    @ThreadSafe
    @NotThreadSafe
    @Immutable

Reentrant locks associate an entry count with a current thread
id. If the same thread id is recorded with an entry count > 0,
then it is allowed to increment the entry count. Otherwise it
is blocked.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* To preserve state consistency, update related state
  variables in a single atomic operation.
* For every invariant that involves more than one variable,
  all the variables involved in that invariant must be
  guarded by the same lock.

-------------------------------------------------------------
Chapter 3
-------------------------------------------------------------

Not only do we want to make sure atomic operations are
synchronized, we also want to make sure other threads see
the results of other thread operations (volatile). For example,
a status variable that must be seen between threads:

.. code-block:: java

    volatile boolean do_sleep;
    //...
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
event listener, use a factory method:

.. code-block:: java

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
to create confined singletons or globals (use sparingly):

.. code-block:: java

    // data is stored in the Thread instance so it is garbage
    // collected when the thread exits
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


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

-------------------------------------------------------------
Chapter 4
-------------------------------------------------------------

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
If the entries are immutable, then a shallow copy is fine:

.. code-block:: java

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

    // Can also return a static view of the data instead of a
    // live one
    public Map<String, Point> getLocations() {
        return Collections.unmodifiableMap(
            new HashMap<String, Point>(locations));
    }

Note about private constructor capture idiom.

If you extend a collection to add new composite atomic methods
to it, you have to make sure that you are all using the same
lock for the operations (intrinsic vs explicit) otherwise
the atomic gurantee cannot be held:

.. code-block:: java

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


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


-------------------------------------------------------------
Chapter 5
-------------------------------------------------------------

The synchronized collections include Vector, Hashtable, and
the Collections.synchronizedXxx factory wrappers. These guard
each single method, however, compound methods may need extra
guards. In order to lock these, we must aquire the collections
intrinsic lock before performing these actions (the same is
true for iteration):

.. code-block:: java

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
collection:

.. code-block:: java

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
that may be thrown when a thread blocking call has been made:

.. code-block:: java

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
are initialized before starting their work:

.. code-block:: java

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
an Error):

.. code-block:: java

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
deadlock prevention (which locks do not allow):

.. code-block:: java

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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* For CPU bound problems #CPU or #CPU + 1 is the ideal number
  of threads to use to parallelize a problem. More threads
  will not help.

-------------------------------------------------------------
Chapter 6: Task Execution
-------------------------------------------------------------

java.util.concurrent provides a flexible thread pool
implementation based on the Executor framework that accepts
new tasks to perform in the pool:

.. code-block:: java

    public interface Executor {
        void execute(Runnable command);
    }

The Executor implementations also provide lifecycle support
and hooks for adding statistics gathering, application management,
and monitoring. It is based on the producer/consumer model:

* **Producers** - These are the application codes that submit new
  jobs to be performed in the pool.
* **Consumers** - These are the the executing threads consume new
  tasks off the work queue.


Can make a custom Executor, for example one that makes a new
thread for each task or a single threaded implementation:

.. code-block:: java

    public class ThreadPerTaskExecutor implements Executor {
        public void execute(Runnable command) {
            new Thread(command).start();
        }
    }

    public class SingleThreadedExecutor implements Executor {
        public void execute(Runnable command) {
            command.run();
        }
    }

The Executor allows one to easily change the execution policy
for a set of task:

* In what thread will tasks be executed?
* In what order should tasks be executed (FIFO, LIFO, priority order)?
* How many tasks may execute concurrently?
* How many tasks may be queued pending execution?
* If a task has to be rejected because the system is overloaded,
  which task should be selected as the victim.
* How should the application be notified of this victim?
* What actions should be taken before or after executing a task?

There are a number of predefined thread pool implementations in the
Executors static class:

* **newFixedThreadPool** - Creates threads as tasks arrive and then keeps
  the threads alive up to the max requested number of threads.
* **newCachedThreadPool** - There is no upper thread bound on this pool,
  but it makes an attempt to reap idle threads and create new ones when
  the demand is high.
* **newSingleThreadExecutor** - Create a single worker thread that can
  gurantee that tasks are operated on in the supplied manner (LIFO, FIFO,
  priority, etc).
* **newScheduledThreadPool** - A fixed sized thread pool that supports
  delayed or periodic tasks (similar to Timer but should be though of
  as its replacement, however it doesn't support absolute times, only
  relative).

To address managing Executor instances, the ExecutorService interface
extends Executor to add a number of lifecycle methods:

.. code-block:: java

    public interface ExecutorService extends Executor {
        void shutdown(); // gracefully finish all tasks and stop
        List<Runnable> shutdownNow(); // just stop everything now
        boolean isShutdown();
        boolean isTerminated();
        boolean awaitTermination(long timeout, TimeUnit unit)
            throws InterruptedException;

        // ... and more
    }

If you need to build a schedule service, you can use a delay queue
which associates a delay time with an object that must wait until
it can be dequeued.

One can create result bearing tasks with the `Callable<T>` interface
(to not return a value, use `Callable<Void>`. Tasks can be in one of
four states: Created, Submitted, Started, and Completed. Tasks that
have not been started can easily be cancelled, while tasks that have
started may be able to if they are responsive to interruption. Results
are represented as a Future:

.. code-block:: java

    public interface Future<V> {
        boolean cancel(boolean mayInterruptIfRunning);
        boolean isCancelled();
        boolean isDone();
        V get() throws InterruptedException, ExecutionException, CancellationException;
        V get(long timeout, TimeUnit unit) throws InterruptedException,
            ExecutionException, CancellationException, TimeoutException;
    }

Can get a future by calling ExecutorService.submit with
a `Callable` or `Runnable` or manually wrapping the two
with a `FutureTask`. Can also overload `newTaskFor` in the
ExecutorService implementation which allows one to change
how the `FutureTask` is generated (Can make more secure
tasks with `PriviledgedAction`):

.. code-block:: java

    protected <T> RunnableFuture<T> newTaskFor(Callable<T> task) {
        return new FutureTask<T>(task);
    }

If there are many Futures that are being submitted and one would
like the next result as it becomes available, they can use a
`CompletionService` which combines an `ExecutorService` with a
`BlockingQueue` (`ExecutorCompletionService`). One can now use
`take` and `poll` to query for the next completed future:

.. code-block:: java

    private class QueueingFuture<V> extends FutureTask<V> {
        QueueingFuture(Callable<V> c) { super(c); }
        QueueingFuture(Runnable t, V r) { super(t, r); }
        protected void done() { completionQueue.add(this); }
    }

One can even create a new ExecutorService that is private to
a new computation while reusing the existing Executor for more
control.

Can wait a certain amount of time for a task to finish (or just
discard the result) by using the timeout overload of `Future.get`.
If it timesout, it will raise a TimeoutException.  The task
should then be stopped to prevent an unused resource from using
CPU time:

.. code-block:: java

    Page renderPageWithAd() throws InterruptedException {
        long endNanos = System.nanoTime() + TIME_BUDGET;
        Future<Ad> f = exec.submit(new FetchAdTask());
        // Render the page while waiting for the ad
        Page page = renderPageBody();
        Ad ad;
        try {
            // Only wait for the remaining time budget
            long timeLeft = endNanos - System.nanoTime();
            ad = f.get(timeLeft, NANOSECONDS);
        } catch (ExecutionException e) {
            ad = DEFAULT_AD;
        } catch (TimeoutException e) {
            ad = DEFAULT_AD;
            f.cancel(true);
        }
        page.setAd(ad);
        return page;
    }

-------------------------------------------------------------
Chapter 7: Cancellation and Shutdown
-------------------------------------------------------------

Thread.stop and Thread.suspend should be avoided for managing
threads. Threads can be stopped for a variety of issues:

* **user cancellation** - A user clicked a close gui button
  or stopped a worker thread via a JMX interface.
* **time limited execution** - An application searches a
  space for the best solution and returns what it has when
  the time limit expires.
* **error conditions** - when an error occurs, all other
  involved threads must be stopped.
* **shutdown** - When an application is stopped, all in
  flight work must be finished and the application must
  shutdown gracefully.

There is no safe way to stop a thread unless the two threads
agree upon some stopping protocol like a cancellation requested
flag that is occasionally checked by the worker thread (cancelled
thread must be volatile to work correctly).

A thread can be interrupted by calling the interrupt method
and then checking the thread.isInterrupted flag. Blocking
methods will usually check the interrupted flag and if
so will call the interrupted static method to clear the
interrupt flag, and then throw an InterruptedException
to the calling code. There is no gurantee on how long this
will take to happen (although in practice it is usually
quick):

.. code-block:: java

    class PrimeProducer extends Thread {
        private final BlockingQueue<BigInteger> queue;
        PrimeProducer(BlockingQueue<BigInteger> queue) {
            this.queue = queue;
        }

        public void run() {
            try {
                BigInteger p = BigInteger.ONE;
                while (!Thread.currentThread().isInterrupted())
                    queue.put(p = p.nextProbablePrime());
            } catch (InterruptedException consumed) {
                // Allow thread to exit
            }
        }
        public void cancel() { interrupt(); }
    }

There are two ways to handle `InterruptionException`:

* propigate the exception up to higher code after cleanup
* reset the interrupted status so higher up code can worry

To do the first, simply add `InterruptionException` to the
exception specification:

.. code-block:: java

    BlockingQueue<Task> queue;
    ...
    public Task getNextTask() throws InterruptionException {
        return queue.take();
    }

If you cannot do this (ex: because you implement Runnable),
the standard solution is to restore the interruption status
by calling `interrupt()` again. To finish local work, save
the result of the interruption, continue looping until you
are finished with your work, and then set the current
interruped status before you exit:

.. code-block:: java

    public Task getNextTask(BlockingQueue<Task> queue) {
        boolean interrupted = false;
        try {
            while (true) {
                try {
                    return queue.take();
                } catch (InterruptedException ex) {
                    interrupted = true;
                }
            }
        } finally {
            if (interrupted)
                Thread.currentThread().interrupt();
        }
    }

The ThreadPoolExecutor detects interruption and then checks
if the pool is being shutdown. If so, it performs some
cleanup, otherwise it starts new threads to keep the pool
at the correct size.

Here is an example of correctly making a task that can be
run for a specified amount of time before being stopped
(this is implemented with Future):

.. code-block:: java

    public static void timedRun(Runnable r, long timeout, TimeUnit unit)
        throws InterruptedException {

        Future<?> task = taskExec.submit(r);
        try {
            task.get(timeout, unit);
        } catch (TimeoutException e) {
            // task will be cancelled below
        } catch (ExecutionException e) {
            // exception thrown in task; rethrow
            throw launderThrowable(e.getCause());
        } finally {
            // Harmless if task already completed
            task.cancel(true); // interrupt if running
        }
    }

Here is an example of overriding a thread's cancel method:

.. code-block:: java

    public class ReaderThread extends Thread {
        private final Socket socket;
        private final InputStream in;

        public ReaderThread(Socket socket) throws IOException {
            this.socket = socket;
            this.in = socket.getInputStream();
        }

        public void interrupt() {
            try { socket.close(); }
            catch (IOException ignored) { }
            finally { super.interrupt(); }
        }

        public void run() {
            try {
                byte[] buf = new byte[BUFSZ];
                while (true) {
                    int count = in.read(buf);
                    if (count < 0) break;
                    else if (count > 0)
                        processBuffer(buf, count);
                }
            } catch (IOException e) { } // Allow thread to exit
        }
    }

In order to empty a queue, you need an isShutdown flag and
then a reservation count that is incremented on publish and
decremented on consume:

.. code-block:: java

    public class LogService {
        private final BlockingQueue<String> queue;
        private final LoggerThread loggerThread;
        private final PrintWriter writer;
        @GuardedBy("this") private boolean isShutdown;
        @GuardedBy("this") private int reservations;

        public void start() { loggerThread.start(); }
        public void stop() {
            synchronized (this) { isShutdown = true; }
            loggerThread.interrupt();
        }

        public void log(String msg) throws InterruptedException {
            synchronized (this) {
                if (isShutdown)
                    throw new IllegalStateException(...);
                ++reservations;
            }
            queue.put(msg);
        }

        private class LoggerThread extends Thread {
            public void run() {
                try {
                    while (true) {
                        try {
                            synchronized (this) {
                                if (isShutdown && reservations == 0)
                                    break;
                            }
                            String msg = queue.take();
                            synchronized (this) { --reservations; }
                            writer.println(msg);
                        } catch (InterruptedException e) { }
                    }
                } finally {
                    writer.close();
                }
            }
        }
    }

    public class LogService {
        private final ExecutorService exec = newSingleThreadExecutor();

        public void start() { }
        public void stop() throws InterruptedException {
            try {
                exec.shutdown();
                exec.awaitTermination(TIMEOUT, UNIT);
            } finally {
                writer.close();
            }
        }

        public void log(String msg) {
            try {
                exec.execute(new WriteTask(msg));
            } catch (RejectedExecutionException ignored) { }
        }
    }

An easier way to shutdown a producer consumer is with a poison
message. This ensures that all the current messages are consumed
and nothing after the stop message is consumed. If there are N
consumers, then N poison messages must be placed on the queue.
It should be noted that this only works with unbounded queues
as if the queue is bounded, the stop message may block forever:

.. code-block:: java

    public class IndexingService {
        private static final File POISON_MESSAGE = new Flie("");
        private final IndexerThread consumer = new IndexerThread();
        private final CrawlerThread consumer = new CrawlerThread();
        private final BlockingQueue<File> queue;
        private final file root;

        public void start() {
            producer.start();
            consumer.start();
        }

        public void stop() { producer.interrupt(); }
        public void awaitTermination() throws InterruptionException {
            consumer.join();
        }
    }

    public class CrawlerThread extends Thread {
        public void run() {
            try {
                crawl(root);
            } catch (InterruptedException e) {
            } finally {
                while (true) {
                    try {
                        queue.put(POISON_MESSAGE);
                        break;
                    } catch (InterruptedException e) {
                }
            }
        }

        private void crawl(File root) throws InterruptedException {
            // ...
        }
    }

    public class IndexerThread extends Thread {
        public void run() {
            try {
                while (true) {
                    File file = queue.take();
                    if (file == POISON_MESSAGE)
                        break;
                    else indexFile(file);
                }
            } catch (InterruptedException ex) {}
        }
    }

If you have a number of one off tasks that must be completed
before the method is finished, just encapsulate the executor
inside of the method call and block:

.. code-block:: java

    boolean checkMail(Set<String> hosts, long timeout, TimeUnit unit)
        throws InterruptedException {

        ExecutorService exec = Executors.newCachedThreadPool();
        final AtomicBoolean hasNewMail = new AtomicBoolean(false);
        try {
            for (final String host: hosts) {
                exec.execute(new Runnable() {
                    public void run() {
                        if (checkMail(host))
                            hasNewMail.set(true);
                    }
                });
            }
        } finally {
            exec.shutdown();
            exec.awaitTermination(timeout, unit);
        }
        return hasNewMail.get();
    }

If you need to handle uncaught exceptions in an application,
subclass the uncaughtExceptionHandler that you provide via
a ThreadFactory:

.. code-block:: java

    public class UEHLogger implements Thread.UncaughtExceptionHandler {
        public void uncaughtException(Thread t, Throwable e) {
            Logger logger = Logger.getAnonymousLogger();
            logger.log(Level.SEVERE, "Thread terminated with exception: " + t.getName(), e);
        }
    }

JVM shutdown handlers can be added with `Runtime.addShutdownHook`,
there is no gurantee on the order these will be run in and if they
hang, so does the JVM shutdown. These should run fast, be very
defensive, and make no assumptions about the state of the service.
Can be used to delete temporary files, close log, etc. If the shutdown
handlers make use of mutual resources (a logger for example), then
run all the tasks in a single handler, otherwise each handler is run
concurrently:

.. code-block:: java

    public void start() {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            public void run() {
                try { LogService.this.stop(); }
                catch (InterruptedException ignored) {}
            }
        });
    }

Can also create normal threads that are children of the
current JVM, or daemon threads that can run after the JVM
parent shutdown.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* There is nothing in the API or language specification that
  ties interruption to any specific cancellation semantics,
  but in practice, using interruption for anything but
  cancellation is fragile and difficult to sustain in larger
  applications.
* Interruption is usually the most sensible way to implement
  cancellation.
* Because each thread has its own interruption policy, you
  should not interrupt a thread unless you know what
  interruption means to that thread.
* Only code that implements a thread's interruption policys
  may swallow an interruption request. General purpose task
  and library code should never swallow interruption requests.
* Provide lifecycle methods whenever a thread owning service
  has a lifetime longer than that of the method that created
  it.
* Daemon threads are not a good substitute for properly
  managing the lifecycle of services within an application.
* Avoid finalizers (they jack up the GC)

-------------------------------------------------------------
Chapter 8: Applying Thread Pools
-------------------------------------------------------------

If your thread pool is used to query JDBC, be wary of how
many connections are allowed in JDBC, otherwise one will be
limited by the other.

If a task is long running, avoid using the unbounded wait
methods, and instead use the time out versions.

Threadpool sizes should not be hardcoded, but instead should
be configured by some mechanism. For CPU intensive work, the
following formula should be sufficient::

    /**
     * given the following, the number of threads (N_th):
     * N_cpu = Number of CPUS
     * U_cpu = target CPU utilization 0 <= x <= 1
     * W/C   = ratio of wait time to compute time
     * N_th  = N_cpu * U_cpu * (1 + W/C)
     */
    int N_CPUS = Runtime.getRuntime().availableProcessors() + 1;

To allocate a pool for other finite pooled resources, simply
allocate the number of pool threads based on the minimum
available other resource (socket handles, file handles,
database connections).

If the factory methods for thread pools supplied by Executors
are not sufficient, you can use the ctor supplied by the
ThreadPoolExecutor (you can also use `prestartAllCoreThreads`):

.. code-block:: java

    public ThreadPoolExecutor(int corePoolSize,
        int maximumPoolSize,
        long keepAliveTime,
        TimeUnit unit,
        BlockingQueue<Runnable> workQueue,
        ThreadFactory threadFactory,
        RejectedExecutionHandler handler) { ... }

You can tune the corePoolSize and maximumPoolSize to control
the size and reaping of idle threads in the system (on the
supplied timeout, an idle thread will be reaped until
corePoolSize is reached):

* newFixedThreadPool: corePoolSize == maximumPoolSize
* newCachedThreadPool: corePoolSize = 0, maximumPoolSize =
  `Integer.MAX_VALUE` (uses a SynchronousQueue)

There are three options for the type of queue to supply for
work queue: unbounded, bounded, and synchronous handoff. The
default is a LinkedBlockingQueue. Another option is to use
an ArrayBlockingQueue, or a bounded LinkedBlockingQueue or
(however, policy must be set to handle when the queue is full).
If the thread pool is unbounded or very large, a SynchronousQueue
can be used to hand off tasks directly to the worker threads.
If FIFO order of tasks is not wanted, PriorityBlockingQueue can
be used to execute tasks based on some order (natural order if
the tasks implement `Comparable` or by using a `Comparator`).

When a bounded work queue fills up, the saturation policy
comes into play. This is supplied by the `RejectedExecutionHandler`
which can be changed after the fact.  There are a number of
existing ones that can be used:

* AbortPolicy (the default) which throws allowing the user to
  redefine their own policy easily.
* DiscardPolicy silently discards the new task if it cannot
  be enqueued.
* DiscardOldestPolicy discards the oldest task (the one closest
  to running), in the case of a priority queue, this is the
  highest priority item!
* CallerRunsPolicy issues a throttling policy by executing
  the newly submitted task on the calling thread (this
  would cause a webserver to stop accepting requests until
  the last task was executed). So as the service becomes
  overloaded, the overload is pushed outward, from the thread
  pool to the work queue, to the application, to the TCP
  layer, and eventually to the client.

The policy can be set as follows:

.. code-block:: java

    ThreadPoolExecutor executor = new ThreadPoolExecutor(
        N_THREADS, N_THREADS, 0L, TimeUnit.MILLISECONDS,
        new LinkedBlockingQueue<Runnable>(CAPACITY));
    executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());

A custom thread factory can also be specified to do things
like give threads custom names, add debug logging, etc;
simply implement the `ThreadFactory` interface:

.. code-block:: java

    public interface ThreadFactory {
        Thread newThread(Runnable task);
    }

    public class NamedThreadFactory implements ThreadFactory {
        private final String poolName;

        public NamedThreadFactory(String poolName) {
            this.poolName = poolName;
        }

        public Thread newThread(Runnable task) {
            return new NamedThread(runnable, poolName);
        }
        Thread newThread(Runnable task);
    }

Executors also includes a factory method, `unconfigurableExecutorService`
which wraps an existing ExecutorService such that it cannot
be configured after creation. Otherwise, all options can be
changed after the fact (except for the SingleThreadExecutor):

.. code-block:: java

    ExecutorService exec = Executors.newCachedThreadPool();
    if (exec instanceof ThreadPoolExecutor)
        ((ThreadPoolExecutor) exec).setCorePoolSize(10);
    else
        throw new AssertionError("Oops, bad assumption");

page 111


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Some tasks have characteristics that require or preclude a
  specific execution policy. Tasks that depend on other tasks
  require that the thread pool be large enough that tasks are
  never queued or rejected; tasks that exploit thread
  confinement require sequential execution. Document these
  requirements so that future maintainers do not undermine
  safety or liveness by substituting an incompatible execution
  policy.
* Whenever you submit to an Executor tasks that are not
  independent, be aware of the possibility of thread starvation
  deadlock, and document any pool sizing or configuration
  constraints in the code or configuration file where the
  Executor is configured.

-------------------------------------------------------------
Chapter 9: GUI Applications
-------------------------------------------------------------

Here is an example of creating a SwingUtility class using
the executor:

.. code-block:: java

    public class SwingUtilities {
        private static final ExecutorService exec =
            Executors.newSingleThreadExecutor(new SwingThreadFactory());
        private static volatile Thread swingThread;

        private static class SwingThreadFactory implements ThreadFactory {
            public Thread newThread(Runnable r) {
                swingThread = new Thread(r);
                return swingThread;
            }
        }

        public static boolean isEventDispatchThread() {
            return Thread.currentThread() == swingThread;
        }

        public static void invokeLater(Runnable task) {
            exec.execute(task);
        }

        public static void invokeAndWait(Runnable task)
            throws InterruptedException, InvocationTargetException {

            Future f = exec.submit(task);
            try {
                f.get();
            } catch (ExecutionException e) {
                throw new InvocationTargetException(e);
            }
        }
    }

And here is an example of creating an Executor using the
supplied SwingUtilities:

.. code-block:: java

    public class GuiExecutor extends AbstractExecutorService {
        // Singletons have a private constructor and a public factory
        private static final GuiExecutor instance = new GuiExecutor();

        private GuiExecutor() { }
        public static GuiExecutor instance() { return instance; }
        public void execute(Runnable r) {
            if (SwingUtilities.isEventDispatchThread())
                r.run();
            else
                SwingUtilities.invokeLater(r);
        }
        // Plus trivial implementations of lifecycle methods
    }

Here is an example of binding a long running task to a GUI
event:

.. code-block:: java

    ExecutorService backgroundExec = Executors.newCachedThreadPool();
    // ...

    button.addActionListener(new ActionListener() {
        public void actionPerformed(ActionEvent e) {
            backgroundExec.execute(new Runnable() {
                public void run() { doBigComputation(); }
        });
    }});


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The Swing single thread rule: Swing components and models
  should be created, modified, and queried only from the
  event dispatching thread.
* Consider a split model design when a data model must be
  shared by more than one thread and implementing a thread
  safe data model would be inadvisable because of blocking,
  consistency, or complexity reasons.


-------------------------------------------------------------
Chapter 10:
-------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* A program will be free of lock-ordering deadlocks if all
  threads acquire the locks they need in a fixed global
  order.
* Invoking an alien method with a lock held is asking for
  liveness trouble. The alien method might acquire other locks
  (risking deadlock) or block for an unexpectedly long time,
  stalling other threads that need the lock you hold.
* Strive to use open calls throughout your program. Programs
  that rely on open calls are far easier to analyze for
  deadlock freedom than those that allow calls to alien
  methods with locks held.
* Avoid the temptation to use thread priorities, since they
  increase platform dependence and can cause liveness problems.
  Most concurrent applications can use the default priority
  for all threads.


-------------------------------------------------------------
Chapter 11:
-------------------------------------------------------------

There are three ways to reduce lock contention:

* Reduce the duration for which locks are held
* Reduce the frequency with which locks are requested
* Replace exclusive locks with coordination mechanisms that
  permit greater concurrency.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Scalability describes the ability to improve throughput or
  capacity when additional computing resources (such as
  additional CPUs, memory, storage, or I/O bandwidth) are
  added.
* Avoid premature optimization. First make it right, then
  make it fast if it is not already fast enough.
* Measure, don't guess.
* Don't worry excessively about the cost of uncontended
  synchronization. The basic mechanism is already quite fast,
  and JVMs can perform additional optimizations that further
  reduce or eliminate the cost. Instead, focus optimization
  efforts on areas where lock contention actually occurs.
* The principal threat to scalability in concurrent
  applications is the exclusive resource lock.
* Allocating objects is usually cheaper than synchronizing.


-------------------------------------------------------------
Chapter 12:
-------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The challenge to constructing effective safety tests for
  concurrent classes is identifying easily checked properties
  that will, with high probability, fail if something goes
  wrong, while at the same time not letting the failure
  auditing code limit concurrency artificially. It is best
  if checking the test property does not require any
  synchronization.
* Tests should be run on multiprocessor systems to increase
  the diversity of potential interleavings. However, having
  more than a few CPUs does not necessarily make tests more
  effective. To maximize the chance of detecting timing
  sensitive data races, there should be more active threads
  than CPUs, so that at any given time some threads are running
  and some are switched out, thus reducing the predictability
  of interactions between threads.
* Writing effective performance tests requires tricking the
  optimizer into not optimizing away your benchmark as dead
  code. This requires every computed result to be used
  somehow by your program in a way that does not require
  synchronization or substantial computation.



-------------------------------------------------------------
Chapter 13:
-------------------------------------------------------------

Instead of using intrinsic locks, one can use explicit locks
which have the following interface:

.. code-block:: java

    public interface Lock {
        void lock();
        void lockInterruptibly() throws InterruptedException;
        boolean tryLock();
        boolean tryLock(long timeout, TimeUnit unit) throws InterruptedException;
        void unlock();
        Condition newCondition();
    }

Here is the general framework for using these locks:

.. code-block:: java

    Lock lock = new ReentrantLock();
    // ...
    lock.lock();
    try { 
        // update the object state
    } finally {
        lock.unlock();
    }

There are also read write locks which share the following
interface:

.. code-block:: java

    public interface ReadWriteLock {
        Lock readLock();
        Lock writeLock();
    }

And it can be used as follows:

.. code-block:: java

    public class ReadWriteMap<K,V> {
        private final Map<K,V> map;
        private final ReadWriteLock lock = new ReentrantReadWriteLock();
        private final Lock r = lock.readLock();
        private final Lock w = lock.writeLock();

        public ReadWriteMap(Map<K,V> map) {
            this.map = map;
        }

        public V put(K key, V value) {
            w.lock();
            try {
                return map.put(key, value);
            } finally {
                w.unlock();
            }
        }
        // Do the same for remove(), putAll(), clear()

        public V get(Object key) {
            r.lock();
            try {
                return map.get(key);
            } finally {
                r.unlock();
            }
        }
        // Do the same for other read-only Map methods
    }


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Performance is a moving target; yesterday's benchmark
  showing that X is faster than Y may already be out of date
  today.
* ReentrantLock is an advanced tool for situations where
  intrinsic locking is not practical. Use it if you need its
  advanced features: timed, polled, or interruptible lock
  acquisition, fair queuing, or non block structured locking.
  Otherwise, prefer synchronized.



-------------------------------------------------------------
Chapter 14: Building Custom Synchronizers
-------------------------------------------------------------

In order to block a queue on conditions instead of using a
check and then sleep operation, use condition queues:

.. code-block:: java

    @ThreadSafe
    public class BoundedBuffer<V> extends BaseBoundedBuffer<V> {
        // CONDITION PREDICATE: not-full (!isFull())
        // CONDITION PREDICATE: not-empty (!isEmpty())
        public BoundedBuffer(int size) { super(size); }

        // BLOCKS-UNTIL: not-full
        public synchronized void put(V v) throws InterruptedException {
            while (isFull())
                wait();
            doPut(v);
            notifyAll();
        }

        // BLOCKS-UNTIL: not-empty
        public synchronized V take() throws InterruptedException {
            while (isEmpty())
                wait();
            V v = doTake();
            notifyAll();
            return v;
        }
    }

The general structure of a state dependent method is as
follows:

.. code-block:: java

    void stateDependentMethod() throws InterruptedException {
        synchronized(lock) {
            while (!conditionPredicate())
                lock.wait();
            // object is now in desired state to perform work
        }
    }

When using condition waits (Object.wait or Condition.await):

* Always have a condition predicatesome test of object state
  that must hold before proceeding.
* Always test the condition predicate before calling wait,
  and again after returning from wait.
* Always call wait in a loop.
* Ensure that the state variables making up the condition
  predicate are guarded by the lock associated with the
  condition queue.
* Hold the lock associated with the the condition queue when
  calling wait, notify, or notifyAll
* Do not release the lock after checking the condition
  predicate but before acting on it.

Single notify can be used instead of notifyAll only when both
of the following conditions hold:

* Uniform waiters. Only one condition predicate is associated
  with the condition queue, and each thread executes the same
  logic upon returning from wait; and
* One in, one out. A notification on the condition variable
  enables at most one thread to proceed.

This is an example of a thread gate using the wait and notify
of the intrinsic lock:

.. code-block:: java

    @ThreadSafe
    public class ThreadGate {
        // CONDITION-PREDICATE: opened-since(n) (isOpen || generation>n)
        @GuardedBy("this") private boolean isOpen;
        @GuardedBy("this") private int generation;

        public synchronized void close() {
            isOpen = false;
        }

        public synchronized void open() {
            ++generation;
            isOpen = true;
            notifyAll();
        }

        // BLOCKS-UNTIL: opened-since(generation on entry)
        public synchronized void await() throws InterruptedException {
            int arrivalGeneration = generation;
            while (!isOpen && arrivalGeneration == generation)
                wait();
        }
    }

Here is a more granular example using explicit locks and
multiple condition variables:

.. code-block:: java

    @ThreadSafe
    public class ConditionBoundedBuffer<T> {
        protected final Lock lock = new ReentrantLock();
        // CONDITION PREDICATE: notFull (count < items.length)
        private final Condition notFull = lock.newCondition();
        // CONDITION PREDICATE: notEmpty (count > 0)
        private final Condition notEmpty = lock.newCondition();
        @GuardedBy("lock")
        private final T[] items = (T[]) new Object[BUFFER_SIZE];
        @GuardedBy("lock") private int tail, head, count;

        // BLOCKS-UNTIL: notFull
        public void put(T x) throws InterruptedException {
            lock.lock();
            try {
                while (count == items.length)
                    notFull.await();
                items[tail] = x;
                if (++tail == items.length)
                    tail = 0;
                ++count;
                notEmpty.signal();
            } finally {
                lock.unlock();
            }
        }

        // BLOCKS-UNTIL: notEmpty
        public T take() throws InterruptedException {
            lock.lock();
            try {
                while (count == 0)
                    notEmpty.await();
                T x = items[head];
                items[head] = null;
                if (++head == items.length)
                    head = 0;
                --count;
                notFull.signal();
                return x;
            } finally {
                lock.unlock();
            }
        }
    }

Here is an example of implementing a simple semaphore using
a lock:

.. code-block:: java

    @ThreadSafe
    public class SemaphoreOnLock {
        private final Lock lock = new ReentrantLock();
        // CONDITION PREDICATE: permitsAvailable (permits > 0)
        private final Condition permitsAvailable = lock.newCondition();
        @GuardedBy("lock") private int permits;

        SemaphoreOnLock(int initialPermits) {
            lock.lock();
            try {
                permits = initialPermits;
            } finally {
                lock.unlock();
            }
        }

        // BLOCKS-UNTIL: permitsAvailable
        public void acquire() throws InterruptedException {
            lock.lock();
            try {
                while (permits <= 0)
                permitsAvailable.await();
                --permits;
            } finally {
                lock.unlock();
            }
        }

        public void release() {
            lock.lock();
            try {
                ++permits;
                permitsAvailable.signal();
            } finally {
                lock.unlock();
            }
        }
    }

All of the concurrent primitives in java.util.concurrent are
implemented using the AbstractQueuedSynchronizer. They are
generally structured as follows:

.. code-block:: java

    boolean acquire() throws InterruptedException {
        while (state does not permit acquire) {
            if (blocking acquisition requested) {
                enqueue current thread if not already queued
                block current thread
            }
            else
                return failure
        }
        possibly update synchronization state
        dequeue thread if it was queued
        return success
    }

    void release() {
        update synchronization state
        if (new state may permit a blocked thread to acquire)
            unblock one or more queued threads
    }


Here is an example of implementing a simple binary latch
using the AQS:

.. code-block:: java

    @ThreadSafe
    public class OneShotLatch {
        private final Sync sync = new Sync();
        public void signal() { sync.releaseShared(0); }
        public void await() throws InterruptedException {
            sync.acquireSharedInterruptibly(0);
        }

        private class Sync extends AbstractQueuedSynchronizer {
            protected int tryAcquireShared(int ignored) {
                return (getState() == 1) ? 1 : -1;
            }

            protected boolean tryReleaseShared(int ignored) {
                setState(1);    // latch is now open
                return true;    // other threads may now acquire
            }
        }
    }

In short, if you need a shared lock you should override:
tryAcquireShared and tryReleaseShared.  If you need an
exclusive lock, override: tryAcquire, tryRelease, and
isHeldExclusively.

Here is the ReentrantLock tryAcquire implementation:

.. code-block:: java

    protected boolean tryAcquire(int ignored) {
        final Thread current = Thread.currentThread();
        int c = getState();
        if (c == 0) {
            if (compareAndSetState(0, 1)) {
                owner = current;
                return true;
            }
        } else if (current == owner) {
            setState(c+1);
            return true;
        }
        return false;
    }

Here is the implementation of Semaphore:

.. code-block:: java

    protected int tryAcquireShared(int acquires) {
        while (true) {
            int available = getState();
            int remaining = available - acquires;
            if (remaining < 0
                || compareAndSetState(available, remaining))
                return remaining;
        }
    }

    protected boolean tryReleaseShared(int releases) {
        while (true) {
            int p = getState();
            if (compareAndSetState(p, p + releases))
                return true;
        }
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Section Keynotes:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Document the condition predicate(s) associated with a
  condition queue and the operations that wait on them.
* Every call to wait is implicitly associated with a specific
  condition predicate. When calling wait regarding a particular
  condition predicate, the caller must already hold the lock
  associated with the condition queue, and that lock must also
  guard the state variables from which the condition predicate
  is composed.
* Whenever you wait on a condition, make sure that someone
  will perform a notification whenever the condition predicate
  becomes true.
* The equivalents of wait, notify, and notifyAll for Condition
  objects are await, signal, and signalAll. However, Condition
  extends Object, which means that it also has wait and notify
  methods. Be sure to use the proper versions await and signal.

-------------------------------------------------------------
Chapter 15: Atomic Variables and Non-Blocking Syn
-------------------------------------------------------------

Instead of using heavy weight locks, finer grained operations
can be used (which aer effectively used to implement the
higher level primitives):

* compare and swap (CAS) - cas(ref, old, new) sets the ref to
  the new value only if the current value is the old value.
  Otherwise it does nothing.  Regardless, it returns the
  current value of ref.
* compare and set - the same as above, but returns true if set
  and false otherwise.
* load linked/store conditional
* atomic increment/decrement/swap

In the case of failing a CAS operation, since it was not blocked
a defeated thread can try again (update with my result), perform
some recovery action (the current balance is different), or do
nothing (someone may have already done our work). This is an
example of a non-blocking counter using CAS (AtomicInteger would
have been a simpler solution):

.. code-block:: java

    @ThreadSafe
    public class CasCounter {
        private SimulatedCAS value;
        public int getValue() {
            return value.get();
        }

        public int increment() {
            int v;
            do {
                v = value.get();
            } while (v != value.compareAndSwap(v, v + 1));
            return v + 1;
        }
    }

There are four scalar Atomic types: AtomicInteger, AtomicLong,
AtomicBoolean, and AtomicReference.  To use other types, you
can cast them in and out and for float types, use
floatToIntBits or doubleToLongBits. These are all mutable and
do not extend the immutable primitives.

There are also the same types for atomic array operations.
This has volatile semantics for the array reference and the
array element (unlike volatile array which is just reference).

CAS performs better for lower levels of contention, locks
perform better for higher levels of contention.

What follows is a non-blocking stack using Treiber's algorithm:

.. code-block:: java

    @ThreadSafe
    public class ConcurrentStack<E> {
        private AtomicReference<Node<E>> top = new AtomicReference<Node<E>>();

        public void push(E item) {
            Node<E> newHead = new Node<E>(item);
            Node<E> oldHead;
            do {
                oldHead = top.get();
                newHead.next = oldHead;
            } while (!top.compareAndSet(oldHead, newHead));
        }

        public E pop() {
            Node<E> newHead;
            Node<E> oldHead;
            do {
                oldHead = top.get();
                if (oldHead == null)
                    return null;
                newHead = oldHead.next;
            } while (!top.compareAndSet(oldHead, newHead));
            return oldHead.item;
        }

        private static class Node<E> {
            public final E item;
            public Node<E> next;
            public Node(E item) { this.item = item; }
        }
    }

Here is an example of the Michael-Scott Non-Blocking Queue:

.. code-block:: java

    @ThreadSafe
    public class LinkedQueue<E> {
        private static class Node<E> {
            private E item;
            private AtomicReference<Node<E>> next;
            public Node(E item, Node<E> next) {
                this.item = item;
                this.next = new AtomicReference<Node<E>>(next);
            }
        }

        private final Node<E> dummy = new Node<E>(null, null);
        private final AtomicReference<Node<E>> head
            = new AtomicReference<Node<E>>(dummy);
        private final AtomicReference<Node<E>> tail
            = new AtomicReference<Node<E>>(dummy);

        public boolean put(E item) {
            Node<E> newNode = new Node<E>(item, null);
            while (true) {
                Node<E> curTail = tail.get();
                Node<E> tailNext = curTail.next.get();
                if (curTail == tail.get()) {
                    if (tailNExt != null) { // intermediate state, lets help
                        tail.compareAndSet(curTail, tailNext);
                    } else {
                        if (curTail.next.compareAndSet(nul, newNode)) {
                            tail.compareAndSet(curTail, newNode);
                            return true; // if this fails, the next thread will finish
                        }
                    }
                }
            }
        }
    }

If you are creating many AtomicXXX types, you can create a
single `AtomicReferenceFieldUpdater` that can be reused:

.. code-block:: java

    private class Node<E> {
        private final E item;
        private volatile Node<E> next;
        public Node(E item) { this.item = item; }
    }

    private static AtomicReferenceFieldUpdater<Node. Node> nextUpdater
        = AtomicReferenceFieldUpdater.newUpdater(Node.Class, Node.Class, "next");

In order to prevent the ABA problem (changing a value from A to
B and back to A) can be prevented by adding a version number to
the changed value. This can be performed by
`AtomicStampedReference` or `AtomicMarkableReference`

-------------------------------------------------------------
Chapter 16: Java Memory Model
-------------------------------------------------------------

The rules for happens before are:

* Program order rule: each action in a thread happens before
  every action in that thread that comes later in the program
  order.
* Monitor lock rule: an unlock on a monitor lock happens before
  every subsequent lock on that same monitor lock.
* Volatile variable rule: a write to a volatile field happens
  before every subsequent read of that same field.
* Thread start rule: a call to Thread.start on a thread happens
  before every action in the started thread.
* Thread termination rule: any action in a thread happens
  before any other thread detects that thread has terminated,
  either by successfully return from `Thread.join` or by
  `Thread.isAlive` returning false.
* Interruption rule: a thread calling interrupt on another
  thread happens before the interrupted thread detects the 
  interrupt (either by having InterruptedException thrown,
  or invoking isInterrupted or interrupted).
* Finalizer rule: the end of a constructor for an object
  happens before the start of the finalizer for that object.
* Transitivity: if A happens before B, and B happens before C,
  then A happens before C.

One can piggyback on the synchronization of other artifacts,
which is what the inner class of Future does:

.. code-block:: java

    // Inner class of FutureTask
    private final class Sync extends AbstractQueuedSynchronizer {
        private static final int RUNNING = 1, RAN = 2, CANCELLED = 4;
        private V result;
        private Exception exception;

        void innerSet(V v) {
            while (true) {
                int s = getState();
                if (ranOrCancelled(s))
                    return;
                if (compareAndSetState(s, RAN))
                    break;
            }
            result = v;
            releaseShared(0);
            done();
        }

        V innerGet() throws InterruptedException, ExecutionException {
            acquireSharedInterruptibly(0);
            if (getState() == CANCELLED)
                throw new CancellationException();
            if (exception != null)
                throw new ExecutionException(exception);
            return result;
        }
    }

With the exception of immutable objects, it is not safe to use
an object that has been initialized by another thread unless
the publication happens before the consuming thread uses it.

The following are a few methods of performing resource
initialization:

.. code-block:: java

    @ThreadSafe // heavyweight lazy initialization
    public class SafeLazyInitialization {
        private static Resource resource;

        public synchronized static Resource get() {
            if (resource == null)
                resource = new Resource();
            return resource;
        }
    }

    @ThreadSafe // lightweight eager initialization
    public class EagerInitialization {
        private static Resource resource = new Resource();

        public synchronized static Resource get() {
            return resource;
        }
    }

    @ThreadSafe // lightweight lazy initialization
    public class EagerInitialization {
        private static class ResourceHolder {
            public static Resource resource = new Resource();
        }

        public synchronized static Resource get() {
            return ResourceHolder.resource;
        }
    }

Initialization safety makes visibility guarantees only for
the values that are reachable through final fields as of the
time the constructor finishes.  For values reachable through
non-final fields, or values that may change after construction,
you must use synchronization to ensure visibility.
