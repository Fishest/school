package simulations

import org.scalatest.FunSuite

import org.junit.runner.RunWith
import org.scalatest.junit.JUnitRunner

@RunWith(classOf[JUnitRunner])
class CircuitSuite extends CircuitSimulator with FunSuite {
  val InverterDelay = 1
  val AndGateDelay = 3
  val OrGateDelay = 5
  
  implicit val int_to_bool: Int => Boolean = (_ == 1)
  implicit val bool_to_int: Boolean => Int = if (_) 1 else 0
  
  test("andGate example") {
    val in1, in2, out = new Wire
    andGate(in1, in2, out)
    in1.setSignal(false)
    in2.setSignal(false)
    run
    
    assert(out.getSignal === false, "and 1")

    in1.setSignal(true)
    run
    
    assert(out.getSignal === false, "and 2")

    in2.setSignal(true)
    run
    
    assert(out.getSignal === true, "and 3")
  }
  
  test("orGate example") {
    val in1, in2, out = new Wire
    orGate(in1, in2, out)
    in1.setSignal(false)
    in2.setSignal(false)
    run
    
    assert(out.getSignal === false, "or 1")

    in1.setSignal(true)
    run
    
    assert(out.getSignal === true, "or 2")

    in2.setSignal(true)
    run
    
    assert(out.getSignal === true, "or 3")  

    in1.setSignal(false)
    run 
    
    assert(out.getSignal === true, "or 4")
  }
  
  test("orGate2 example") {
    val in1, in2, out = new Wire
    orGate2(in1, in2, out)
    in1.setSignal(false)
    in2.setSignal(false)
    run
    
    assert(out.getSignal === false, "or 1.2")

    in1.setSignal(true)
    run
    
    assert(out.getSignal === true, "or 2.2")

    in2.setSignal(true)
    run
    
    assert(out.getSignal === true, "or 3.2")  

    in1.setSignal(false)
    run 
    
    assert(out.getSignal === true, "or 4.2")
  } 
  
  test("demux(0)") {
    val i, o = new Wire
    demux(i, List(), List(o))
    
    def truth(iv: Boolean, ov: Boolean) {
      i.setSignal(iv)
      
      run  
      
      assert(o.getSignal == ov, "demux(0).1")
    }
    
    //    I  O
    truth(0, 0)
    truth(1, 1)
  }

  test("demux(1)") {
    val i, c, o1, o2 = new Wire
    demux(i, List(c), List(o1, o2))
    
    def truth(iv: Boolean, cv: Boolean, ov1: Boolean, ov2: Boolean) {     
	    i.setSignal(iv)
	    c.setSignal(cv)
	    
	    run
	        
	    assert(o1.getSignal === ov1, "demux(1).1")
	    assert(o2.getSignal === ov2, "demux(1).2")
    }
        
    //    I  C O1 O2
    truth(0, 0, 0, 0)
    truth(0, 1, 0, 0)
    truth(1, 0, 1, 0)
    truth(1, 1, 0, 1)
  } 
  
  test("demux(2)") {
    val i, c1, c2, o1, o2, o3, o4 = new Wire
    demux(i, List(c1, c2), List(o1, o2, o3, o4))
    
    def truth(iv: Boolean, cv1: Boolean, cv2: Boolean,
        ov1: Boolean, ov2: Boolean, ov3: Boolean, ov4: Boolean) {     
      
	    i.setSignal(iv)
	    c1.setSignal(cv1)
	    c2.setSignal(cv2)
	    
	    run
	        
	    assert(o1.getSignal === ov1, "demux(2).1")
	    assert(o2.getSignal === ov2, "demux(2).2")
	    assert(o3.getSignal === ov3, "demux(2).3")
	    assert(o4.getSignal === ov4, "demux(2).4")
    }
        
    //    I  C1 C2 O1 O2 03 04
    truth(0, 0, 0, 0, 0, 0, 0)
    truth(0, 0, 1, 0, 0, 0, 0)
    truth(0, 1, 0, 0, 0, 0, 0)
    truth(0, 1, 1, 0, 0, 0, 0)    
    truth(1, 0, 0, 1, 0, 0, 0)
    truth(1, 0, 1, 0, 1, 0, 0)
    truth(1, 1, 0, 0, 0, 1, 0)
    truth(1, 1, 1, 0, 0, 0, 1)
  }  
  
  test("demux(3)") {
    val i, c1, c2, c3, o1, o2, o3, o4, o5, o6, o7, o8 = new Wire
    demux(i, List(c1, c2, c3), List(o1, o2, o3, o4, o5, o6, o7, o8))
    
    def truth(iv: Boolean, cv1: Boolean, cv2: Boolean, cv3: Boolean,
        ov1: Boolean, ov2: Boolean, ov3: Boolean, ov4: Boolean,
        ov5: Boolean, ov6: Boolean, ov7: Boolean, ov8: Boolean) {    
      
	    i.setSignal(iv)
	    c1.setSignal(cv1)
	    c2.setSignal(cv2)
	    c3.setSignal(cv3)
	    
	    run
	        
	    assert(o1.getSignal === ov1, "demux(3).1")
	    assert(o2.getSignal === ov2, "demux(3).2")
	    assert(o3.getSignal === ov3, "demux(3).3")
	    assert(o4.getSignal === ov4, "demux(3).4")
	   	assert(o5.getSignal === ov5, "demux(3).5")
	    assert(o6.getSignal === ov6, "demux(3).6")
	    assert(o7.getSignal === ov7, "demux(3).7")
	    assert(o8.getSignal === ov8, "demux(3).8")
    }
        
    //    I  C1 C2 C3 O1 O2 03 04 O5 O6 O7 O8
    truth(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)    
    truth(0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0)
    truth(1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0)
    truth(1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0)
    truth(1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0)
    truth(1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0)    
    truth(1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)
    truth(1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0)
    truth(1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0)
    truth(1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1)
  }   
}
