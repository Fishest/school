//------------------------------------------------------------
// Video 1: Monads and Effects
//------------------------------------------------------------
/**
 *           One           Many
 * ----------------------------------------        
 * Sync    T/Try[T]    T/Iterable[T]
 * Async   T/Future[T] T/Observable[T]
 */
trait Adventure {
  def collectCoins(): List[Coins] = {
    if (eatenByMonster(this))
      throw new GameOverException("you were eaten")
    return List(Gold, Gold, Silver)
  }

  def buyTreasure(coins: List[Coins]): Treasure = {
    if (coins.sumBy(_.value) < treasureCost)
      throw new GameOverException("not enough coins")
    Diamond
  }
}

/**
 * The following code only shows the happy path
 * of the code, not the "magic" path that can
 * happen with exceptions. We can enforce this with
 * the actual result type of the methods using Try[T]
 */
val adventure = new Adventure()
val coins = adventure.collectCoins() 
// block until we recieve the coins
// continue if there is no exception
val treasure = adventure.buyTreasure(coins)
// block until we recieve the treasure
// continue if there is no exception

/**
 * This is what try looks like
 */
abstract class Try[T]
case class Success[T](elem: T)  extends Try[T]
case class Failure(t: Throwable) extends Try[Nothing]

/**
 * And this is how we would use it to make the
 * exceptions clear in the code.
 */
import scala.util.{Try, Success, Failure}
trait Adventure {
  def collectCoins(): Try[List[Coins]]
  def buyTreasure(coins: List[Coins]): Try[Treasure]
}

/**
 * Now we have to be explicit about the errors, but
 * we can make this cleaner using the higher order functions
 * on the try type. "Monads are types that guide you through
 * the happy path"
 */
val adventure = new Adventure()
adventure.collectCoins() match {
  case Success(coins) => adventure.buyTreasure(coins)
  case failure @ Failure(t) => failure
}

// with flatmap
adventure.collectCoins() flatMap { coins =>
  adventure.buyTreasure(coins)
}

// with for comprehensions
for {
  coins <- adventure.collectCoins()
  treasure <- adventure.buyTreasure(coins)
} yield treasure


//------------------------------------------------------------
// Video 2: Latency as an Effect (Future)
//------------------------------------------------------------

/**
 * A network computation that hides network and error effects
 */
trait Socket {
  def readFromMemory(): Array[Byte]
  def sendToEurope(packet: Array[Byte]): Array[Byte]
}
val socket = new Socket()
val packet = socket.readFromMemory()
// block for 50,000 nanoseconds
// continue unless there is an exception
val result = socket.sendToEurope(packet)
// block for 150,000,000 nanoseconds
// continue unless there is an exception

/**
 *
 * Approximate timing for various operations on a typical PC::
 * 
 *     execute typical instruction                    1/1,000,000,000 sec = 1 nanosec
 *     fetch from L1 cache memory                                         0.5 nanosec
 *     branch misprediction                                                 5 nanosec
 *     fetch from L2 cache memory                                           7 nanosec
 *     Mutex lock/unlock                                                   25 nanosec
 *     fetch from main memory                                             100 nanosec
 *     send 2K bytes over 1Gbps network                                20,000 nanosec
 *     read 1MB sequentially from memory                              250,000 nanosec
 *     fetch from new disk location (seek)seek                      8,000,000 nanosec
 *     read 1MB sequentially from disk                             20,000,000 nanosec
 *     send packet US to Europe and back       150 milliseconds = 150,000,000 nanosec
 */

/**
 * Future is the monad that takes care of exceptions and latency
 */
import scala.concurrent._
import scala.concurrent.ExecutionContext.Implicits.global

trait Future[T] {
  def onComplete(callback: Try[T] => Unit)
    (implicit executor: ExecutionContext): Unit
}

/**
 * Alternate designs of future
 */
trait Future[T] {
  def onComplete(success: T => Unit, failure: Throwable => Unit): Unit
  def onComplete(callback: Observer[T]): Unit
}

trait Observer[T] {
  def onNext(value: T): Unit
  def onError(error: Throwable): Unit
}

/**
 * Rewriting the original example with Future
 */
trait Socket {
  def readFromMemory(): Future[Array[Byte]]
  def sendToEurope(packet: Array[Byte]): Future[Array[Byte]]
}

val socket = new Socket()
for {
  packet <- socket.readFromMemory()
  result <- socket.sendToEurope(packet)
} yield result

/**
 * Example implementation of the Socket trait
 */
import scala.concurrent.ExecutionContext.Implicits.global
import akka.serializer._

val memory = Queue[EmailMessage](
  EmailMessage(from = "Erik", to = "Roland"),
  EmailMessage(from = "Gary", to = "Rogers"),
  EmailMessage(from = "Beth", to = "Harold"))

def readFromMemory(): Future[Array[Byte]] = Future {
  val email = memory.dequeu()
  val serializer = serialization.findSerializerFor(email)
  serializer.toBinary(email)
}

//------------------------------------------------------------
// Video 3: Combinators on Futures
//------------------------------------------------------------

trait Awaitable[T] {
  abstract def ready(atMost: Duration): Unit
  abstract def result(atMost: Duration): T
}

trait Future[T] extends Awaitable[T] {
  def map[U](f: T => U): Future[U]
  def filter(f: T => Boolean): Future[T]
  def flatMap[U](f: T => Future[U]): Future[U]
  def zip(a: Future[T], b: Future[T]): Future[(T, T)]

  def recover(f: PartialFunction[Throwable, T]): Future[T]
  def recoverWith(f: PartialFunction[Throwable, Future[T]]): Future[T]

  def fallbackTo(that: => Future[T]): Future[T] = this recoverWith {
    case _ => that recoverWith { case _ => this }
  }
}

// we can now wrap this to be safe
def sendTo(url: String, packet: Array[Byte]): Future[Array[Byte]] =
  Http(url, Request(package))
    .filter(response => response.isOk)
    .map(response => response.toByteArray)

// but this returns the wrong error message
def sendTo(packet: Array[Byte]): Future[Array[Byte]] =
  sendTo(mailServer.Europe, packate) recoverWith {
    case europeError => sendTo(mailServer.Usa, packat) recover {
      case usaError => usaError.getMessage.toByteArray
    }
  }

// this is redone using fallbackTo to return the correct error
def sendTo(packet: Array[Byte]): Future[Array[Byte]] =
  sendTo(mailServer.Europe, packate) fallbackTo {
    sendTo(mailServer.Usa, packat)
  } recover { case europeError => europeError.getMessage.toByteArray }

// We can now write an apply method on Try using futures
object Try {
  def apply(f: Future[T]): Future[Try[T]] =
    f.map(s => Success(s)) recover { case t => Failure(t) }
}

/**
 * To block synchronously, use await which will attempt
 * to resolve the result in the specified time and if not
 * then throw.
 */
import scala.language.postFixOps

// we can now write times using units!
object Duration {
  def apply(length: Long, unit: TimeUnit): Duration
}

val result = Await.result(future, 2 seconds)
println(result.toText)

//------------------------------------------------------------
// Video 4: Composing Futures
//------------------------------------------------------------
val socket = new Socket()
val result: Future[Array[Byte] = for {
  packet <- socket.readFromMemory()
  result <- socket.sendToEurope(packet)
} yield result

// using recursion
def retry(noTimes: Int)(block: => Future[T]): Future[T] = noTimes match {
  case 0 => Future.failed(new Exception("sorry"))
  case _ => block fallbackTo { retry(noTimes - 1) {  block } }
}

/**
 * using fold
 * List(a,b,c).foldLeft(d)(f)  = f(f(f(d, a), b), c)
 * List(a,b,c).foldright(d)(f) = f(a, f(b, f(c, d)))
 */
def retry(noTimes: Int)(block: => Future[T]): Future[T] = {
  val ns: Iterator[Int] = (1 to noTimes).iterator
  val attempts: Iterator[Future[T]] = ns.map(_ => () => block)
  val failed = Future.failed(new Exception)
 
  // using foldLeft: ((failed recoverWith block1) recoverWith block2) recoverWith block3
  attempts.foldLeft(failed) ((a, block) => a recoverWith { block })
  // using foldRight: block1 fallbackTo { block2 fallbackTo { block3 fallbackTo { failed }}}
  attempts.foldRight(() => failed) ((block, a) => () => { block() fallbackTo { a() }})
}

/**
 * We can make this a bit more simple
 */
import scala.async.Await._

def retry(noTimes: Int)(block: => Future[T]): Future[T] = async {
  var i = 0
  var result: Try[T] = Failure(new Exception)
  while (i < noTimes & result.isFailure) {
    result = await { Try(block) }
    i += 1
  }
  result.get
}

// filter in the scala repository
def filter(predicate: T => Boolean): Future[T] = {
  val p = Promise[T]()
  this onComplete {
    case Failure(f) => p.failure(f)
    case Success(x) => 
      if (predicate(x)) p.success(x)
      else p.failure(new NoSuchElementException)
  }
  p.future
}

// filter using await
def filter(predicate: T => Boolean): Future[T] = async {
  val result = await { this }
  if (!predicate(result)) {
    throw new NoSuchElementException()
  } else {
    result
  }
}

// F[S] = async
//   S  = await { f } 
// F[S] = f(t:T)
//   T  = await { this }
// F[T] = this
def flatMap[S](f: T => Future[S]): Future[S] = async {
  await { f( await { this } ) }
}

//------------------------------------------------------------
// Video 5: Promises
//------------------------------------------------------------

/**
 * Think of promise as a mailbox for a future. When you set a value
 * in the promise, the contained future is completed with the said
 * value.
 *
 * There are two complete methods as a future can only be completed
 * once. If it has already been completed, the first method throws,
 * the second one will return false.
 */
trait Promise[T] {
  def future: Future[T]
  def complete(result: Try[T]): Unit
  def tryComplete(result: Try[T]): Boolean

  def success(value: T): Unit = this.complete(Success(value))
  def failure(t: Throwable): Unit = this.complete(Failure(t))
}

trait Future[T] {
  def onCompleted(f: Try[T] => Unit): Unit
}

import scala.concurrent.ExecutionContext.Implicits.global

// the first future that completes will win setting the result
def race(left: Future[T], right: Future[T]): Future[T] = {
  val p = Promise[T]()
  left  onComplete { p.tryComplete(_) }
  right onComplete { p.tryComplete(_) }
  p.future
}

// zip using promises and pattern matchings
def zip[S, R](that: Future[S], f: (T, S) => R): Future[R] = {
  val p = Promise[R]()

  this onComplete {
    case Failure(e) => p.failure(e)
    case Success(x) => that onComplete {
      case Failure(e) => p.failure(e)
      case Success(y) => p.success(f(x, y))
    }
  }

  p.future
}

// using async and await
def zip[S, R](that: Future[S], f: (T, S) => R): Future[R] = async {
  f(await { this }, await { that })
}

// using foldRight
def sequence[T](fs: List[Future[T]]): Future[List[T]] = {
  val successful = Promise[List[T]]()
  successful.success(Nil)
  fs.foldRight(successful.future) {
    // f:Future[T], acc:Future[List[T]]
    (f, acc) => for { x <- f; xs <- acc } yield x :: xs
  }
}

// using async and await
def sequence[T](fs: List[Future[T]]): Future[List[T]] = async {
  var _fs = fs
  var r = ListBuffer[T]()
  while (_fs != Nil) {
    r += await { _fs.head }
    _fs = _fs.tail
  }
  r.result
}

