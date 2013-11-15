//------------------------------------------------------------
// Video 1
//------------------------------------------------------------
/**
 * Solutions that are side effect free do not concern themselves
 * with time. Mutations take time into account.
 *
 * Rewriting can be done anywhere in a term and all rewritings
 * that terminate lead to the same solution. This is an important
 * result of lambda calculus (the theory of functional programming).
 * This is referred to as confluence (Church-Russel Theorum).
 *
 * An object has state if its behavior is influenced by its history.
 */

//------------------------------------------------------------
// Video 2
//------------------------------------------------------------

/**
 * Referential transparency means that the following are equal
 */
def E: ...
val x = E; val y = E
val x = E; val y = x

/**
 * The property of being the same is known as operationl
 * equivalence, and means that given x and y there is no
 * possible test that can show x and y are different.
 *
 * If they are not equal, we can no longer use the substitution
 * model to reason about programs.
 */
val x = E
val y = E
/**
 * This may be an infinite amount of tests to prove they
 * are equal, but only needs one case to prove they are
 * not equal.
 */
def f[U,T](a: U, b: T): Boolean = ...
f(x, y) == f(x, x)

//------------------------------------------------------------
// Video 3
//------------------------------------------------------------
/**
 * Variables are enough to model all imperitive programs. Loops
 * and control statements can be modeled with functions.
 *
 * In this case, the condition and the command must be passed
 * by name so they can be called each time. This is also tail
 * recursive so that it can be implmemented in constant stack
 * space using a simple jump.
 */
def WHILE(condition: => Boolean)(command: => Unit): Unit =
  if (condition) {
    command
    WHILE(condition)(command)
  } else ()

/**
 * We can also do a do { ... } (condition) loop
 */
def REPEAT(command: => Unit)(condition: => Boolean): Unit =
    command
  if (condition) ()
  else REPEAT(command)(condition)

REPEAT {
  ...
} (condition)

/**
 * And we can use a little bit of scala DSL magic to
 * get a full do { ... } until (condition) loop.
 */
def DO(command: => Unit)(condition: => Boolean) = new {
  def UNTIL(condition => Boolean) {
    command
    if (condition) () else UNTIL(condition)
  }
}

/**
 * Scala for loops are simply translated to foreach methods on
 * the collection.
 */
for (i <- 1 until 10; j <- "abc") {
  println(i + " " + j)
}

// translates to
(1 until 10) foreach (i =>
  "abc" foreach (j =>
      println(i + " " + j)))

//------------------------------------------------------------
// Video 4
//------------------------------------------------------------

def inverter(a: Wire, o: Wire): Unit
def orGate(a: Wire, b: Wire, o: Wire): Unit
def andGate(a: Wire, b: Wire, o: Wire): Unit
def halfAdder(a: Wire, b: Wire, s: Wire, c: Wire): Umit = {
  val d, e = new Wire
  orGate(a, b, d)
  andGate(a, b, c)
  inverter(c, e)
  andGate(d, e, s)
}
def fullAdder(a: Wire, b: Wire, cin: Wire, sum: Wire, cout: Wire): Unit = {
  val s, c1, c2 = new Wire
  halfAdder(b, cin, s, c1)
  halfAdder(a, s, sum, c2)
  orGate(c1, c2, cout)
}

//------------------------------------------------------------
// Video 5
//------------------------------------------------------------

trait Simulation {
  def currentTime: Int = ???
  def afterDelay(delay: Int)(block: Unit) = ???
  def run(): Unit = ??
}

class Wire {
  private var signal = false
  private var actions: List[Action] = List()
  def getSignal: Boolean = signal
  def setSignal(value: Boolean): Unit =
    if (value != signal) {
      signal = value
      actions foreach (_())
    }

  def addAction(action: Action): Unit = {
    actions = action :: actions
    action()
  }
}

//------------------------------------------------------------
// Video 6
//------------------------------------------------------------

/**
 * The agenda is sorted by order of events to be fired
 * so that most recent events pop off first.
 */
trait Simulation {
  type Action = () => Unit
  case class Event(time: Int, action: Action)
  private type Agenda = List[Event]
  private var agenda: Agenda = List()
  private var curtime = 0

  def currentTime: Int = curtime

  def afterDelay(delay: Int)(block: => Unit): Unit = {
    val item = Event(currentTime + delay, () => block)
    agenda = insert(agenda, item)
  }

  def run(): Unit {
    afterDelay(0) {
      println("simulation started at " + currentTime)
    }
    loop()
  }

  private def insert(agenda: List[Event], event: Event): List[Event] = agenda match {
    case first :: rest if first.time <= event.time =>
      first :: insert(rest, event)
    case _ => event :: agenda
  }

  private def loop(): Unit = agenda match {
    case first :: rest =>
      agenda = rest
      curtime = first.time
      first.action()
      loop()
    case Nil =>
  }
}

/**
 * Put the basic level gates in here
 */
abstract class Gates extends Simulation {

  def InverterDelay: Int
  def AndGateDelay: Int
  def OrGateDelay: Int

  def probe(name: String, wire: Wire): Unit {
    def action(): Unit = {
      println(s"$name $currentTime value = ${wire.getSignal}")
    }
    wire addAction action
  }

  def nandGate(a: Wire, b: Wire, output: Wire): Unit = {
    def action(): unit = {
      val signala = a.getSignal
      val signalb = b.getSignal
      afterDelay(AndGateDelay) { output setSignal !(signala & signalb) }
    }
    a addAction action
    b addAction action
  }

  def norGate(a: Wire, b: Wire, output: Wire): Unit = {
    def action(): unit = {
      val signala = a.getSignal
      val signalb = b.getSignal
      afterDelay(AndGateDelay) { output setSignal !(signala | signalb) }
    }
    a addAction action
    b addAction action
  }

  def inverter(input: Wire, output: Wire): Unit = {
    def action(): unit = {
      val signal = input.getSignal
      afterDelay(InverterDelay) { output setSignal !signal }
    }
    input addAction action
  }

  def andGate(a: Wire, b: Wire, output: Wire): Unit = {
    def action(): unit = {
      val signala = a.getSignal
      val signalb = b.getSignal
      afterDelay(AndGateDelay) { output setSignal (signala & signalb) }
    }
    a addAction action
    b addAction action
  }

  def orGate(a: Wire, b: Wire, output: Wire): Unit = {
    def action(): unit = {
      val signala = a.getSignal
      val signalb = b.getSignal
      afterDelay(AndGateDelay) { output setSignal (signala | signalb) }
    }
    a addAction action
    b addAction action
  }
}

/**
 * Put the higher order circuits in here.
 */
abstract class Circuits extends Gates {

}

/**
 * Put timing parameters in here.
 */
trait Parameters {
  def InverterDelay = 2
  def AndGateDelay  = 3
  def OrGateDelay   = 5
}

/**
 * To run this in a worksheet add the following
 */
object simulation extends Circuits with Parameters
import simulation._

val in1, in2, sum, carry = new Wire
halfAdder(in1, in2, sum, carry)
probe("sum", sum)
probe("carry", carry)

in1 setSignal true
run()

in2 setSignal true
run()

in1 setSignal false
run()
