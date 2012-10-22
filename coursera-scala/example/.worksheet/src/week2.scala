object week2 {import scala.runtime.WorksheetSupport._; def main(args: Array[String])=$execute{;$skip(190); 
  /**
   * recursive sum abstraction with pluggable map function
   */
  def sum(f: Int => Int)(a: Int, b: Int) : Int = {
    if (a > b) 0
    else f(a) + sum(f)(a + 1, b)
  };System.out.println("""sum: (f: Int => Int)(a: Int, b: Int)Int""");$skip(24); val res$0 = 
  sum(x => x * x)(3, 4);System.out.println("""res0: Int = """ + $show(res$0));$skip(190); 
  
  /**
   * recursive product abstraction with pluggable map function
   */
  def product(f: Int => Int)(a: Int, b: Int): Int = {
    if (a > b) 1
    else f(a) * product(f)(a + 1, b)
  };System.out.println("""product: (f: Int => Int)(a: Int, b: Int)Int""");$skip(24); val res$1 = 
  product(x => x)(3, 4);System.out.println("""res1: Int = """ + $show(res$1));$skip(271); 
  
  /**
   * recursive map reduce abstraction with pluggable map/reduce functions
   */
  def mapReduce(combine: (Int, Int) => Int, zero: Int)(f: Int => Int, a: Int, b: Int) : Int = {
    if (a > b) zero
    else combine(f(a), mapReduce(combine, zero)(f, a + 1, b))
  };System.out.println("""mapReduce: (combine: (Int, Int) => Int, zero: Int)(f: Int => Int, a: Int, b: Int)Int""");$skip(136); 
  /**
   * sum implemented with map reduce
   */
  def mrsum(f: Int => Int)(a: Int, b: Int) =
    mapReduce((x,y) => x + y, 0)(f, a, b);System.out.println("""mrsum: (f: Int => Int)(a: Int, b: Int)Int""");$skip(26); val res$2 = 
  mrsum(x => x * x)(3, 4);System.out.println("""res2: Int = """ + $show(res$2));$skip(149); 
    
  /**
   * product implemented with map reduce
   */
  def mrproduct(f: Int => Int)(a: Int, b: Int) =
    mapReduce((x,y) => x * y, 1)(f, a, b);System.out.println("""mrproduct: (f: Int => Int)(a: Int, b: Int)Int""");$skip(26); val res$3 = 
  mrproduct(x => x)(3, 4);System.out.println("""res3: Int = """ + $show(res$3))}
}