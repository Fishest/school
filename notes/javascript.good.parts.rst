=====================================================================
Javascript: The Good Parts
=====================================================================

---------------------------------------------------------------------
Chapter 1 - Introduction
---------------------------------------------------------------------

There is only one number type which is a 64 bit float:

* `NaN` is an invalid number 
* it can be tested with `isNan(el)`.

Strings are immutable in javascript and there is no `char` type:

* can also be viewed as a collection of 16 bit unicode entries
* `'c' + 'a' + 't' === 'cat'`
* has common methods like `length` and `toUpperCase`

Javascript doesn't do any linking, but instead has one large global
namespace:

* `var` indicates private scope
* block `{ }` is not a new scope

The following values are false in javascript:

* `false`
* `null`
* `undefined`
* `0`, `NaN`
* everything else is true including the string `'false'`

The following is a terse description of the javascript language.

* `for (i; i < 0; i++) {}` and `for (value in collection)`
* `try { } catch()` and `throw`
* `typeof` (and array of anything is `[object]`)
* `+` is addition and concatenation
* `!` works on any type (implicit conversion to boolean)
* array literal `[]`, object literal `{}`, regexp literal `/ /`
* `function() {}` is a function literal and lambda
* function can have a name to call itself or can be anonymous

---------------------------------------------------------------------
Chapter 3 - Objects (20)
---------------------------------------------------------------------

The only available types are string, boolean, null, undefined, and
object:

* objects are mutable keyed collections

  - keys can be anything except undefined
  - values can be anything

* objects can contain other objects

  - they are class free
  - there is no limitation on property names
  - they contain a prototype *linkage* feature
  - can retrieve with dictionary notation: `obj['key']`
  - can retrieve with property notation: `obj.key`
  - can assign with either method
  - a new object will be created or an existing overrwritten
  - retrieving non-existant keys returns undefined
  - can short circuit like: `var result = obj.value || "default";`
  - dereferencing into an undefined will throw a `TypeError`
  - can short circuit like: `obj.value && obj.value.method`
  - objects are always passed by reference, never by value

* object literal is simply **json** 

  - quotes are needed for invalid javascript keys: `{ 'this name' : 'value' }`
  - otherwise they are not needed `{ this_name : "value" }`

---------------------------------------------------------------------
Chapter 4 - Functions (26)
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 5 - Inheritence (46)
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 6 - Arrays (58)
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 7 - Regular Expressions
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 8 - Methods
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 9 - Style
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 10 - Beautiful Features
---------------------------------------------------------------------

---------------------------------------------------------------------
Appendix - The Bad Parts
---------------------------------------------------------------------

.. todo:: finish copying notes
