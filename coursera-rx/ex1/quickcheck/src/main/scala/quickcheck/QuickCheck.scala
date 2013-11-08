package quickcheck

import common._

import org.scalacheck._
import Arbitrary._
import Gen._
import Prop._

abstract class QuickCheckHeap extends Properties("Heap") with IntHeap {
  
  /**
   * Given two heaps, copy the left to the right
   */
  def copyHeap(source: H, dest: H): H =
      if (isEmpty(source)) dest
      else copyHeap(deleteMin(source), insert(findMin(source), dest))
       
  /**
   * Given two heaps, determine if they are equal
   */
  def areEqual(h1: H, h2: H): Boolean =
	if (isEmpty(h1) && isEmpty(h2)) true
	else if (isEmpty(h1) || isEmpty(h2)) false
	else findMin(h1) == findMin(h2) &&
	       areEqual(deleteMin(h1), deleteMin(h2))
      
  /**
   * Given a heap and a previous smaller value,
   * determine if the heap is ordered or not.
   */
  def isOrdered(heap: H): Boolean =           
    areEqual(heap, copyHeap(heap, empty))
  
  /**
   * Given a heap, determine its total size
   */
  def size(h: H, count: Int=0): Int =
    if (isEmpty(h)) count
    else size(deleteMin(h), count + 1)
  
  lazy val genHeap: Gen[H] = for {
	v <- arbitrary[Int]
    heap <- oneOf(value(empty), genHeap)
  } yield insert(v, heap)

  implicit lazy val arbHeap: Arbitrary[H] = Arbitrary(genHeap)
    
  property("findMin(h1) == min(a)") = forAll { a: Int =>
    val heap = insert(a, empty)
    findMin(heap) == a
  }
  
  property("insert(a, b, empty) == min(a, b)") = forAll { (a: Int, b: Int) =>
    val heap = insert(b, insert(a, empty))
    findMin(heap) == ord.min(a, b)
  }

  property("isSorted") = forAll { heap: H =>
    isOrdered(heap)
  }
  
  property("meld(h1, h2) isSorted") = forAll { (heap1: H, heap2: H) =>
    val heap = meld(heap1, heap2)
    isOrdered(heap)
  }
  
  property("size(meld) == size(h1) size(h2)") = forAll { (heap1: H, heap2: H) =>
    val heap = meld(heap1, heap2)
    size(heap) == size(heap1) + size(heap2)
  }
  
  property("deleteMin(h1) isEmpty") = forAll { a: Int =>
    val h1 = insert(a, empty)
    val h2 = deleteMin(h1)
    isEmpty(h2)
  }
  
  property("meld(h1, h2) ==  min(a, b)") = forAll { (heap1: H, heap2: H) =>
    val min1 = findMin(heap1)
    val min2 = findMin(heap2)
    val heap = meld(heap1, heap2)
    findMin(heap) == ord.min(min1, min2)
  }
}
