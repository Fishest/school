package simulations

import math.random

class EpidemySimulator extends Simulator {

  def coinToss()          = (random <= 0.50)
  def prob(rate: Double)  = (random <= rate) 
  def randomBelow(i: Int) = (random * i).toInt

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
  }

  import SimConfig._

  var initial = (prevalenceRate * population).toInt
  val persons = (0 until population) map  { id =>
    val person = new Person(id)
    if (coinToss && initial > 0) { 
      person.makeInfected // because we have to have _3_ infections
      initial -= 1
    }
    if (prob(vaccineRate)) person.vaccinate
    person
  }
  
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
      val susceptible  = prob(transmissionRate)
      val transmitable = persons.exists(p => (p.row == row) && (p.col == col) && p.infected) 
      val infectable   = !(dead || immune)
      if (infectable && transmitable && susceptible) { makeInfected }
    } 
    def makeInfected() { infected = true; afterDelay(incubationTime)(makeSick) }
    def makeSick()     { sick = true; afterDelay(dieTime - incubationTime)(makeDead) }
    def makeDead()     { if (prob(dieRate)) { dead = true } else afterDelay(immuneTime - dieTime)(makeImmune) }
    def makeImmune()   { immune = true; afterDelay(healTime - immuneTime)(makeHealthy) }
    def makeHealthy()  { sick = false; infected = false; immune = false }
    def vaccinate()    { immune = true; sick = false; infected = false  }
    
    /**
     * This is a predicate to check if a given room is dangerous
     * to enter or not.
     */
    def isRoomInfected(room: (Int, Int)): Boolean = room match {
      case (r, c) => persons.exists(p =>
        (p.row == r) && (p.col == c) && (p.sick || p.dead))
    }
    
    /**
     * This gets the next possible move that the person
     * will attempt to make. 
     */
    def getMove(): Option[(Int, Int)] = {
      def byFoot = {
        val moves = List(
          /* up   */ (if (row == 0) roomRows else row - 1, col),
		  /* right*/ (row, if (col == roomColumns) 0 else col + 1),
		  /* down */ (if (row == roomRows) 0 else row + 1, col),
		  /* left */ (row, if (col == 0) roomColumns else col -1)
        ).filter(isRoomInfected)
        
        if (moves.isEmpty) None else Some(moves(randomBelow(moves.size)))
      }
      
      def byAirplane =
        Some(randomBelow(roomRows), randomBelow(roomColumns))
        
      if (prob(airplaneRate)) byAirplane else byFoot
    }
    
    /**
     * This updates the state of the person by issuing
     * the next move.
     */
	def move() {     
      def action {
        getMove() match {
          case Some((newRow, newCol)) => row = newRow; col = newCol
          case None => // no room to move to
        }        
        updateStatus
        move
      }      
      afterDelay(randomBelow(moveTime)) { if (!dead) action }
    }
	
	/**
	 * This kicks of the simulation for the specified person
	 */
    move
  }
  
}