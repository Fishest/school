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
// Video 2: Monads and Effects
//------------------------------------------------------------
