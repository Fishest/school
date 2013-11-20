package simulations

import math.random
import scala.util.Random.shuffle

class EpidemySimulator extends Simulator {

  protected[simulations] object SimConfig {
    val population: Int          = 300
    val roomRows: Int            = 8
    val roomColumns: Int         = 8
    
    val transmissionRate: Double = 0.40
    val airplaneRate: Double     = 0//0.01
    val prevalenceRate: Double   = 0.01
    val dieRate: Double          = 0.25
    val vaccineRate: Double      = 0//0.05
    
    val moveTime: Int            = 5
    val incubationTime: Int      = 6
    val dieTime: Int             = 14
    val immuneTime: Int          = 16
    val healTime: Int            = 18
    
    val retardMovement: Boolean  = false
  }

  import SimConfig._
  
  /**
   * A collection of randomization functions to help
   * run the probabilities.
   */
  def coinToss()              = (random <= 0.50)
  def byChance(rate: Double)  = (random <  rate) 
  def randomBelow(i: Int)     = (random * i).toInt
  def randomDay(i: Int)       = ((random * i).toInt + 1) * (if (retardMovement) 2 else 1)

  /**
   * Initialize our beginning state
   */
  var initial = (prevalenceRate * population).toInt
  val persons: List[Person] = List.range(0, population) map  { id =>
    val person = new Person(id)
    if (coinToss && initial > 0) { 
      person.makeInfected // because we have to have _3_ infections
      initial -= 1
    }
    if (byChance(vaccineRate)) person.vaccinate
    person
  }

  /**
   * These are used to check the person grid against various status
   * conditions.
   */
  def checkRoomState(room: (Int, Int))(action: Person => Boolean): Boolean = room match {
    case (r, c) => persons.exists { p => p.row == r && p.col == c && action(p) }
  }
  def isRoomInfected(room: (Int, Int))  = checkRoomState(room) { p =>  (p.sick || p.dead || p.infected || p.immune) }
  def isRoomDangerous(room: (Int, Int)) = checkRoomState(room) { p =>  (p.sick || p.dead) }
  def isRoomSafe(room: (Int, Int))      = !isRoomDangerous(room)
  
  /**
   * Represents a single person in the simulation as well
   * as their current mutable state.
   */
  class Person (val id: Int) {
    var infected = false
    var sick     = false
    var immune   = false
    var dead     = false
    var row: Int = randomBelow(roomRows)
    var col: Int = randomBelow(roomColumns)
    
    /**
     * This updates the person's status based on the
     * infected people in the room. If the person becomes
     * infected, it starts the status cascade.
     */
    def updateStatus() {
      val susceptible  = byChance(transmissionRate)
      val transmitable = isRoomInfected((row, col))
      val infectable   = !(dead || immune || infected)
      if (infectable && transmitable && susceptible) { makeInfected }
    } 
    def makeInfected() { infected = true; afterDelay(incubationTime)(makeSick) }
    def makeSick()     { sick = true; afterDelay(dieTime - incubationTime)(makeDead) }
    def makeDead()     { if (byChance(dieRate)) { dead = true } else afterDelay(immuneTime - dieTime)(makeImmune) }
    def makeImmune()   { if (!dead) { immune = true; sick = false; afterDelay(healTime - immuneTime)(makeHealthy) } }
    def makeHealthy()  { if (!dead) { infected = false; immune = false } }
    def vaccinate()    { if (!dead) { immune = true; sick = false; infected = false }  }
    
    /**
     * This gets the next possible move that the person
     * will attempt to make. 
     */
    def getNextMove(): Option[(Int, Int)] = {
      def byFoot = List(
          (if (row == 0) (roomRows - 1) else row - 1, col),    // up
		  (row, if (col == roomColumns - 1) 0 else col + 1), // right
		  (if (row == roomRows - 1) 0 else row + 1, col),    // down
		  (row, if (col == 0) (roomColumns - 1) else col -1)   // left
        ).filter(isRoomSafe)
      
      def byAirplane = List(
        (randomBelow(roomRows), randomBelow(roomColumns))
      )
        
      val moves = if (byChance(airplaneRate)) byAirplane else byFoot
      shuffle(moves).headOption
    }
    
    /**
     * This updates the state of the person by issuing
     * the next move.
     */
	def move() {     
      if (!dead) {
        getNextMove() match {
          case Some((newRow, newCol)) =>
            row = newRow; col = newCol
            updateStatus // only update status on movement
          case None =>   // no safe room to move to
        }        
        afterDelay(randomDay(moveTime))(move)
      }      
    }
	
	/**
	 * This kicks of the simulation for the specified person
	 */
    afterDelay(randomDay(moveTime))(move)
  }
}
