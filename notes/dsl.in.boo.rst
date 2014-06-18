============================================================
DSLs in Boo
============================================================

------------------------------------------------------------
Chapter 1: Why Write DSLs
------------------------------------------------------------

//The main purpose of an internal DSL is to reduce the amount of work required to
make the compiler happy and increase the clarity of the code in question. That’s the
syntactic aspect of it, at least. The other purpose is to expose the domain. A DSL
should be readable by someone who is familiar with the domain, not the programming language.//

DSL Types:

* external - sql
* internal/embedded - rake/rails/etc
* fluent - NHibernate
* graphical - uml for example

------------------------------------------------------------
Chapter 2: An Overview of Boo
------------------------------------------------------------

Quick overview:

* grammer level list, hash, array, object initialization, re,
  and string formatting.
* automatic variable declaration and type inference
* implicit type casting
* duck typing
* compiler extensibility with AST attributes
* significat-whitespace or whitespace-agnostic (python vs ruby)
* semicolons are optional
* T* is IEnumerable<T>
* string interpolation (like ruby "#{variable}") -> StringBuilder
* is, and, not, or, isa -> ==, &&, !, ||, is
* if, elif, else
* parameters optional (ruby)
* lambda => list.ForEach do(i): print i
* lambda (no arguments) => list.ForEach: print "nothing"
* statement modifiers (ruby: return nil if test)
* if, unless, and while can be used like this
* extension methods/properties
* IQuackFu -> dynamic dispatch (method_missing)

DSL Tips:

* Choose names appropriately and make sure the make sense
* Use underscores instead of PascalCase

------------------------------------------------------------
Chapter 3: The Drive Towards DSLs (39)
------------------------------------------------------------

*One technique that I have found useful is to pretend that I
have a program that can perfectly understand intent in plain
English and execute it.*

*This syntax should cover a single scenario, not all
scenarios. The scenario should also be very specific. Then
flesh out the DSL in small stages.*

*After this step, it’s a matter of turning the natural
language into something that you can build an internal DSL on.*

Two(ish) types of DSLs:

  * **imperative dsl** specifies a list of steps to execute (what you
    want to do). Example: build scripts.
  * **declarative dsl** is a specification of a goal (what you want
    done). Example: sql, regex.
  * hyrbrid of the two

A DSL is composed of the following:

  * **syntax** - the core language of the syntax extensions
  * **api** - the api used in the dsl
  * **model** - the existing code base or facade to back up to
  * **engine** - the runtime engine that processes our dsl

------------------------------------------------------------
DDD and DSLs (55)
------------------------------------------------------------

.. todo:: page 55
