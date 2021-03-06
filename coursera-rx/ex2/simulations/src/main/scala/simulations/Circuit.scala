package simulations

import common._

class Wire {
  private var sigVal = false
  private var actions: List[Simulator#Action] = List()

  def getSignal: Boolean = sigVal
  
  def setSignal(s: Boolean) {
    if (s != sigVal) {
      sigVal = s
      actions.foreach(action => action())
    }
  }

  def addAction(a: Simulator#Action) {
    actions = a :: actions
    a()
  }
}

abstract class CircuitSimulator extends Simulator {

  val InverterDelay: Int
  val AndGateDelay: Int
  val OrGateDelay: Int

  def probe(name: String, wire: Wire) {
    wire addAction {
      () => afterDelay(0) {
        println(
          "  " + currentTime + ": " + name + " -> " +  wire.getSignal)
      }
    }
  }

  def inverter(input: Wire, output: Wire) {
    def invertAction() {
      val inputSig = input.getSignal
      afterDelay(InverterDelay) { output.setSignal(!inputSig) }
    }
    input addAction invertAction
  }

  def andGate(a1: Wire, a2: Wire, output: Wire) {
    def andAction() {
      val a1Sig = a1.getSignal
      val a2Sig = a2.getSignal
      afterDelay(AndGateDelay) { output.setSignal(a1Sig & a2Sig) }
    }
    a1 addAction andAction
    a2 addAction andAction
  }

  def orGate(a1: Wire, a2: Wire, output: Wire) {
    def action() {
      val a1Sig = a1.getSignal
      val a2Sig = a2.getSignal
      afterDelay(OrGateDelay) { output.setSignal(a1Sig | a2Sig) }
    }
    a1 addAction action
    a2 addAction action
  }
  
  def orGate2(a1: Wire, a2: Wire, output: Wire) {
    val n1, n2, n3 = new Wire
    inverter(a1, n1)
    inverter(a2, n2)
    andGate(n1, n2, n3)
    inverter(n3, output)
  }

  def demux(in: Wire, ctrl: List[Wire], out: List[Wire]) {
    ctrl match {
      case Nil => andGate(in, in, out(0))
      case c::cs =>
        val cv, o1, o2 = new Wire
        val (ol, oh) = out.splitAt(out.length / 2)
  
        andGate(in, c, o1)
        inverter(c, cv)
        andGate(in, cv, o2)
      
        demux(o1, cs, ol)
        demux(o2, cs, oh)
    }
  }
}

object Circuit extends CircuitSimulator {
  val InverterDelay = 1
  val AndGateDelay = 3
  val OrGateDelay = 5

  def andGateExample {
    val in1, in2, out = new Wire
    andGate(in1, in2, out)
    probe("in1", in1)
    probe("in2", in2)
    probe("out", out)
    in1.setSignal(false)
    in2.setSignal(false)
    run

    in1.setSignal(true)
    run

    in2.setSignal(true)
    run
  }

  def orGateExample {
    val in1, in2, out = new Wire
    orGate(in1, in2, out)
    probe("in1", in1)
    probe("in2", in2)
    probe("out", out)
    in1.setSignal(false)
    in2.setSignal(false)
    run

    in1.setSignal(true)
    run

    in2.setSignal(true)
    run
  }
  
  def demuxExample {
    val in, c, o1, o2 = new Wire
    demux(in, List(c), List(o1, o2))
    probe("in", in)
    probe("c", c)
    probe("out1", o1)
    probe("out2", o2)
    in.setSignal(false)
    run

    in.setSignal(true)
    run

    o1.setSignal(true)    
    run
    
    o2.setSignal(true)
    run 
  }
}

object CircuitMain extends App {
  Circuit.andGateExample
  Circuit.orGateExample
  Circuit.demuxExample
}
