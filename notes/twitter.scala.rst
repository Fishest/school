============================================================ 
Twitter Scala School
============================================================ 

------------------------------------------------------------
Basics
------------------------------------------------------------

* almost everything is an expression
* can give expressions a name with val and var:
  - `val two = 1 + 1` is readonly
  - `var two = 1 + 1` can be modified
* can define named and anonymous functions::

    // can be called as three() or three
    def three() 1 + 2
    def four() : Int = {
        println("adding four")
        2 + 2
    }

    // the two following are equivalent
    def add(a: Int, b:Int) : Int = a + b
    val add = (x: Int, y: Int) => x + y

* can partially apply and curry methods::

    // can partially apply a function
    val add2 = add(2, _:Int)
    add2(4)

    // can curry explicitly in the function definition
    def mult(a: Int)(b: Int) : Int = a * b
    mult(2)(3)
    val double = mult(2) _
    double(4)

    // can convert a function to be curried
    val cadder = (add _).curried
    cadder(2)(4)

* variable length arguments are defined as follows::

    // we can supply as many string arguments as we like
    def capitalize(args: String*) = args.map { _.capitalize }

* can define generic types (basics) as follows::

    trait Cache[K, V] {
        def get(key: K) : V
        def set(key: K, value: V)
        def del(key: K)

        // can add on methods too
        def remove[J](key: J)
    }

------------------------------------------------------------
Concurrency
------------------------------------------------------------

* Can use the JVM concurrency model with threads
  - trait Runnable { def run(): Unit }
  - trait Callable[V] { def call(): V }
  - example::

    val thread = new Thread(new Runnable {
        def run() {
            println("hello world")
        }
    })
    thread.start

* A simple service::

    import java.net.{Socket, ServerSocket}
    import java.util.concurrent.{Executors, ExecutorService}
    import java.util.Date
    
    class NetworkService(port: Int, poolSize: Int) extends Runnable {
      val serverSocket = new ServerSocket(port)
      val pool: ExecutorService = Executors.newFixedThreadPool(poolSize)
    
      def run() {
        try {
          while (true) {
            val socket = serverSocket.accept()
            pool.execute(new Handler(socket))
          }
        } finally {
          pool.shutdown()
        }
      }
    }
    
    class Handler(socket: Socket) extends Runnable {
      def message = (Thread.currentThread.getName() + "\n").getBytes
    
      def run() {
        socket.getOutputStream.write(message)
        socket.getOutputStream.close()
      }
    }
    
    (new NetworkService(2020, 2)).run

* To get non blocking results, use a Future::

    val future = new FutureTask[String](new Callable[String]() {
      def call(): String = {
        searcher.search(target);
    }})
    executor.execute(future)

    val blockingResult = future.get()
  
