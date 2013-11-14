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
