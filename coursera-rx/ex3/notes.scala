//------------------------------------------------------------
// Video 1
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
// Video 2
//------------------------------------------------------------

//------------------------------------------------------------
// Video 3
//------------------------------------------------------------

//------------------------------------------------------------
// Video 4
//------------------------------------------------------------

//------------------------------------------------------------
// Video 5
//------------------------------------------------------------
