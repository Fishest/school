object week2 {
  /**
   * recursive sum abstraction with pluggable map function
   */
  def sum(f: Int => Int)(a: Int, b: Int) : Int = {
    if (a > b) 0
    else f(a) + sum(f)(a + 1, b)
  }                                               //> sum: (f: Int => Int)(a: Int, b: Int)Int
  sum(x => x * x)(3, 4)                           //> res0: Int = 25
  
  /**
   * recursive product abstraction with pluggable map function
   */
  def product(f: Int => Int)(a: Int, b: Int): Int = {
    if (a > b) 1
    else f(a) * product(f)(a + 1, b)
  }                                               //> product: (f: Int => Int)(a: Int, b: Int)Int
  product(x => x)(3, 4)                           //> res1: Int = 12
  
  /**
   * recursive map reduce abstraction with pluggable map/reduce functions
   */
  def mapReduce(combine: (Int, Int) => Int, zero: Int)(f: Int => Int, a: Int, b: Int) : Int = {
    if (a > b) zero
    else combine(f(a), mapReduce(combine, zero)(f, a + 1, b))
  }                                               //> mapReduce: (combine: (Int, Int) => Int, zero: Int)(f: Int => Int, a: Int, b:
                                                  //|  Int)Int
  /**
   * sum implemented with map reduce
   */
  def mrsum(f: Int => Int)(a: Int, b: Int) =
    mapReduce((x,y) => x + y, 0)(f, a, b)         //> mrsum: (f: Int => Int)(a: Int, b: Int)Int
  mrsum(x => x * x)(3, 4)                         //> res2: Int = 25
    
  /**
   * product implemented with map reduce
   */
  def mrproduct(f: Int => Int)(a: Int, b: Int) =
    mapReduce((x,y) => x * y, 1)(f, a, b)         //> mrproduct: (f: Int => Int)(a: Int, b: Int)Int
  mrproduct(x => x)(3, 4)                         //> res3: Int = 12
}