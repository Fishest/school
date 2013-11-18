================================================================================
Strange Loop Talks
================================================================================

--------------------------------------------------------------------------------
The Trouble With Types - Martin Odersky
--------------------------------------------------------------------------------

* Pros and Cons of static / dynamic typing
* Great design is discovered not invented
* Great design is created with patterns and as a result of constraints:

  - patterns    -> abstractions
  - constraints -> static types
  - powerful patterns made safe by types
  - seen in functional collections and their generalizations (monads)
 
* simple types (no generics, not extensible)

  - simple tooling
  - highly normative (only one way to do a task)
  - users can all identify same design patterns

* richly languages languages

  - turing complete type systems
  - no boilerplate (type inference)
  - no type imposed limits to expressivess (can expliclitly use casts)

* Precision, Soundness, and Simplicity: pick two for a type system
* Abstractions:

  - parameters(positional, functional)
  - abstract members(named-based, object-oriented / modular)
  - modular and functional can be combined together

.. code:: scala

    scala.collection.BitSet       Named Type         |
    Channel with Logged           Compound Type      | = Modular 
    Channel { def close(): Unit } Refined Type       |

    List[String]                  Parameterized Type |
    List[T] forSome { type T }    Existential Type   | = Functional
    List                          Higher Kinded Type |

* DOT (calculus of dependent object types) and Dotty (scala with DOT at its core)

  - papers on these systems
  - No existential types or higher kinded types
  - Parameterized is redefined into modular types
  - parameters -> abstract members
  - arguments  -> refinements

.. code:: scala

    class Set[T] {}   -> class Set { type $T }
    Set[String]       -> Set { type $T = String }
    class List[+T] {} -> class List { type $T }
    List[String]      -> List { type $T <: String }

--------------------------------------------------------------------------------
Easy Simple - Rich Hickey
--------------------------------------------------------------------------------
And Others
--------------------------------------------------------------------------------
