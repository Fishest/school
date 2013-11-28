//------------------------------------------------------------
// Video 1: From Future to Observables
//------------------------------------------------------------
/**
 * Future[T] and Try[T] are duals as if we reverse future,
 * then we get try:
 *
 * Future[T] = (Try[T] => Unit) => Unit
 * Try[T]    = Unit => (Unit => Try[T])
 *           = () => (() => Try[T])
 *           ~ Try[T]
 */
def asynchronous: Future[T] { ... } // passes callback of (Try[T] => Unit)
def synchronous: Try[T] { ... }     // recieves and blocks on Try[T]

/**
 * Iterable[T] and Observable[T] are also duals
 * Iterable[T] is also a monad (all the base combinators like
 * map, filter, flatMap, etc are * defined on this trait in the
 * scala library)
 *
 * Iterable[T] can be seen as a pull model of iterator. This is
 * bad when we are say pulling lines from file as we will hit
 * the disc everytime we call next:
 */
trait Iterable[T] {
  def iterator(): Iterator[T]
}

trait Iterator[T] {
  def hasNext: Boolean;
  def next: T
}

val iterator: Iterator[String] = Source.fromFile(path).getLines
while (iterator.hasNext) {
  println(iterator.next)
}

/**
 * Can we convert this to using asynchronous IO by converting
 * this to its dual Observable[T]
 *
 * Iterable[T] = ()  => // returns a new iterator
 * Iterator[T] = (() => // function model of an iterator
 *   Try[               // hasNext can throw or return true
 *     Option[T]])      // next can have a value or not
 *
 * If we reverse this, we recieve the following which can be
 * pattern matched by the possible values it can return:
 * (Try[Option[T]] => Unit) => Unit
 *
 * (case T => Unit         // option returns a value
 *  case Throwable => Unit // try returned exception
 *  case () => Unit        // options returns no value (complete)
 * ) => Unit               // returns a new observable
 */
// This subscribes the supplied callbacks to an event
trait Observable[T] {
  def subscribe(observer: Observer[T]): Subscription
  def observeOn(scheduler: Scheduler): Observable[T]
}

// This is the collection of async callbacks that deal
// with the supplied values.
trait Observer[T] {
  def onNext(value: T): Unit
  def onError(t: Throwable): Unit
  def onComplete(): Unit
}

// This allows the calling code to cancel the subscription
// when it no longer wants to recieve values form a possibly
// infinite sequence.
trait Subscription[T] {
  def unsubscribe(): Unit
}

/**
 * So comparing the two async computations together, although
 * can both return a value or throw, Observable[T] can also
 * possibly not return a value which lets it return one or more
 * values::
 *
 * Future[T]     = (Try[       T]  => Unit)
 * Observable[T] = (Try[Option[T]] => Unit)
 */
val ticks: Observable[Long] = Observable.interval(1 seconds)
val evens: Observable[Long] = ticks.filter(t => t % 2 == 0)
val buffs: Observable[Seq[Long]] = ticks.buffer(2, 1)
val sub = buffs.subscribe(b => println(b))
readline()
sub.unsubscribe()

//------------------------------------------------------------
// Video 2: Combinators on Observable Collections
//------------------------------------------------------------

/**
 * All the basic combinators exist on the observables, except
 * that they are implemented a little bit differently.
 */
trait Observable[T] {
  def map(f : T => Observable[T]): Observable[T] = ???
  def flatMap[S](f : T => Observable[S]): Observable[S] = { map(f).flatten() }

  /**
   * This will fifo the N observables until they are all finished
   * or until any of them throws an exception.
   */
  def flatten(os: Observable[Observable[T]]): Observable[T] = ???

  /**
   * This will buffer all the output values until the first observable
   * is complete, then output it before outputting the next stream, etc.
   * This is dangerous if one of the streams is infinite.
   */
  def concat(os: Observable[Observable[T]]): Observable[T] = ???

  def groupBy[K](selector: T => K): Observable[(K, Observable[T])]
}

val xs:Observable[Int] = Observable(3, 2, 1)
val ys:Observable[Observable[Int]] = xs.map(x => Observable.Interval(x seconds).map(_ => x).take(2))
val za:Observable[Int] = ys.flatten()

/**
 * Example of a real world example
 */
val quakes = usgs()
val major  = quakes.
    map(q => (q.location, Magnitude(q.magnitude))).
    filter { case (loc, mag) => mag >= Major }

major.subscribe({ case (loc, mag) => {
  println($"Magnitude ${mag} Location ${loc}")
}})


val withCountry: Observable[Observable[(Earthquake, Country)]] = usgs().map(quake => {
  val country: Future[Country] = reverseGeocode(quake.location)
  Observable(country.map(c => (quake, c)))
})

// get the earthquakes in their occurrance order
val merged = withCountry.concat
val byCountry: Observable[(Country, Observable[(Earthquake, Country)]] = withCountry.flatten.groupBy { case (q, c) => c }

//------------------------------------------------------------
// Video 3: Subscriptions
//------------------------------------------------------------

/**
 * There are hot and cold observables:
 * - hot are the same observable shared by many subscribers (mouse events)
 * - cold subscribers each have their own private source (stream from api)
 *
 * This means the unsubscribe does not mean cancellation as their may be
 * more subscriptions. Observers can be smart and stop the computation if
 * there are no more subscribers.
 */
trait Subscription {
  // this must be idempotent
  def unsubsribe: Unit
}
object Subscription {
  def apply(unsubscribe: Unit): Subscription
}

/**
 * There are various types of subscriptions
 */
trait BooleanSubscription {
  def isUnsubscribed: Boolean
}

trait CompositeSubscription extends Boolean Subscription {
  def +=(subscription: Subscription): this.type
  def -=(subscription: Subscription): this.type
}

trait MultipleAssignmentSubscription extends BooleanSubscription {
  def subscription: Subscription
  def subscription_=(that: Subscription): this.type
}

/**
 * Using this subscriptions
 */
val subscription = Subscription { println("hello subscription") }
subscription.unsubscribe

val bsubscription = BooleanSubscription { println("hello subscription") }
println(bsubscription.isUnsubscribed)
bsubscription.unsubscribe
println(bsubscription.isUnsubscribed)

val a = Subscription { println("hello subscription a") }
val b = Subscription { println("hello subscription b") }
val csubscription = CompositeSubscription(a, b)
println(csubscription.isUnsubscribed)
csubscription.unsubscribe
println(csubscription.isUnsubscribed)
println(a.isUnsubscribed && b.isUnsubscribed)
// adding to an already unsubscribed composite will eagerly
// unsubscribe from added subscriptions
csubscription += Subscription { println("hello subscription c") }

val a = Subscription { println("hello subscription a") }
val b = Subscription { println("hello subscription b") }
val msubscription = MultipleAssignmentSubscription(a, b)
println(msubscription.isUnsubscribed)
msubsription.subscription = a
msubsription.subscription = b
msubscription.unsubscribe
println(msubscription.isUnsubscribed)
println(b.isUnsubscribed)
// adding to an already unsubscribed composite will eagerly
// unsubscribe from added subscriptions
msubscription.subscription = Subscription { println("hello subscription c") }

/**
 * Also, unsubscribing from a child will not unsubscribe the
 * parent subscription.
 */
val a = Subscription { println("hello subscription a") }
val b = BooleanSubscription { println("hello subscription b") }
val csubscription = CompositeSubscription(a, b)
b.unsubscripe
b.isUnsubscribed // true
c.isUnsubscribed // false

//------------------------------------------------------------
// Video 4: Creating Rx Streams
//------------------------------------------------------------

//------------------------------------------------------------
// Video 5: Schedulers 1
//------------------------------------------------------------

// iterables are lazy
def nats(): Iterable[Int] = new Iterable[Int] = {
  var i = -1
  def iterator: Iterator[Int] = new Iterator[Int] {
    def hasNext: Boolean = true
    def next: Int = { i += 1; i }
  }
}

/**
 * We must run the iterable on its own thread so that
 * we can cancel an infinite sequence.
 */
def from[T](seq: Iterable[T])(implicit scheduler: Scheduler) : Observable[T] = {
  Observable(observer => {
    val it = seq.iterator
    scheduler.schedule(self =>
      if (it.hasNext) { observer.onNext(it.next()); self() }
      else { observer.onCompleted() }
    )
  })
}

val infinite: Iterable[Int] = nats()
val subscription = from(infinite).subscribe(x => println(x))
subscription.unsubscribe

/**
 * Simple example of using schedulers
 */
// mirrors the java thread pool (cannot cancel tasks)
trait ExecutionContext {
  def execute(runnable: Runnable): Unit
}

// the scala rx way, now we can cancel the task
trait Schedule {
  // 1. this schedules a thunk on the thread pool
  def schedule(work: => Unit): Subscription
  // 2. this schedules some work, and taps in the scheduler used
  def schedule(work: Scheduler => Subscription): Subscription
  // 3. this schedules a thunk that takes its next continutation
  def schedule(work: (=> Unit) => Unit): Subscription = {

    // this calls (2) so a recursion can be setup with the same scheduler
    // the MASubscription is a pointer to the current subscription
    val subscription = new MultipleAssignmentSubscription
    schedule(scheduler => {
      // This recursively calls (1) if the thunk calls the continuation
      // Everything it needs is capturd in the closure.
      def loop: Unit = {
        subscription.subscription = scheduler.schedule { work { loop } }
      }
      loop()
      subscription
    })

    //
    // After each loop in the recursion, the next thunk is scheduled
    // on the thread pool and the subscription is updated to reflect
    // the current thread pool subscription to be cancelled.
    //
    subscription
  }
}

val scheduler = Schedule.NewThreadScheduler
val subscription = scheduler.schedule { println("hello world") }

/**
 * This returns an infinite stream of unit ticks.
 * Rx Contract: (onNext)*(onError | onCompleted)?
 */
object Observable {
  def apply() (implicit scheduler: Scheduler): Observable[Unit] = {
    Observable(observer => {
      scheduler.schedule(self => {
        observer.onNext(())
        self()
      })
    })
  }
}

//------------------------------------------------------------
// Video 6: Schedulers 2
//------------------------------------------------------------

implicit val scheduler: Scheduler = Scheduler.NewThreadScheduler

def range(start: Int, count: Int)(Implicit scheduler: Scheduler): Observable[Int] = {
  Observable(observer => {
    var i = 0;
    // this uses the implicit scheduler and the unit stream defined above
    Observable().subscribe(_ => {
      if (i < count) { observer.onNext(start + i); i += 1 }
      else { observer.onCompleted() }
    })
  })
}

/**
 * This will run the observable 10 times into the callback
 * and when it is completed it will unsubscribe from the
 * observable.
 */
range(0, 10).subscribe(x => println(x))
