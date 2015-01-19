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

Every object is linked to a prototype object from which it inherits
properties. All object literals are linked to `Object.prototype` by
default. One can force another object to be the prototype of:

.. code-block:: javascript

    if (typeof Object.create != 'function') { // can use like Object.create(stooge);
        Object.create = function(o) {         // changes to the new instance will not
            var F = function() {};            // affect the original.
            F.prototype = o;
            return new F();
        };
    }

If we try to retrieve a value from an object and it doesn't exist,
we will delegate to its prototype and up the chain. The object chain
is dynamic:

.. code-block:: javascript

  var a_stooge = Object.create(stooge);
  a_stooge.name; // undefined
  stooge.name = "larry";
  a_stooge.name; // larry


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Reflection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

We can get the type of a given variable with `typeof`. This will
delegate to the prototype chain.

`_.hasOwnProperty` will return `true` or `false` if the immediate
object has a given property (this will not perform any delegation).

`for (name in object)` will iterate through every property and function
in the object with delegation up the property chain with the caveats:

* no specific order is guranteed
* functions can be filtered with `typeof`
* if you need order or just specific properties, create an array
* the array can be filitered, looped, etc

.. code-block:: javascript

    var props = ["name", "age", "nickname"];
    for (i = 0; i < props.length; i += 1) {  // this doesn't pull up the
        console.log(a_stooge[props[i]]);     // prototype chain of array
    }

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Delete
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Delete will remove a property if the object has it without affectecting
the prototype linkage (downwards). This will cause the next prototype
instance to be examined (think virtual overrides).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Global Abatement (25)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One way to avoid global pollution is to create a single global
variable for your application and have it contain all your code. This
will cause less interaction with frameworks and libraries. It will
also make your code easier to understand:

.. code-block:: javascript

    var myapp = {}
    myapp.stooge = { name: "lary", age: "56" };

---------------------------------------------------------------------
Chapter 4 - Functions (26)
---------------------------------------------------------------------

Functions are first class objects. They are created and linked to
`Function.prototype` which is then linked to `Object.prototype`. They
can be thought of an object with a constructor (the function itself).
Since functions are actually just objects, they can methods as well!
A function literal has four parts:

.. code-block:: javascript

    var add = function _add(a, b) {
      return a + b;
    };
    // 1. the reserved word function
    // 2. an optional name for debugging and recursion
    // 3. zero or more arguments
    // 4. a function body

Inner functions can be created in functions and they have access to
all objects in the scope of the closure. The function is passed
`this` and arguments (two additional hidden parameters). If more
arguments are passed to the function, they are ignored. If less
are passed, the parameters are set to `undefined`. The value of
`this` is determined by the invocation pattern which there are 
four:

* **method** - member function of an object; binding happens at invocation.
* **function** - called as a free function (not a property of an object)
  will make `this` be bound to the gloval object (`window`). This will
  not have access to function inner scope (it must be wrapped and saved):

.. code-block:: javascript

    mine.double = function() {
      var that = this;
      var helper = function() { that.value = add(that.value, that.value); };
      helper();
    };
    mine.double();
    mine.value;

* **constructor** - called with `new` and convention is to use Uppercase names.
* **apply** - apply an array of arguments to a function. The first argument
  is the `this` context to use, second argument is the argument array. The 
  argument array can be used to supply extra arguments to a function.

.. code-block:: javascript

    var sum = add.apply(null, [1,2,3]);

A function always returns. If a value is not supplied, then it will
return `undefined` by default. If the function is a constructor and
nothing is returned, `this` is returned by default.

.. todo:: finish notes

---------------------------------------------------------------------
Chapter 5 - Inheritence (46)
---------------------------------------------------------------------

---------------------------------------------------------------------
Chapter 6 - Arrays (58)
---------------------------------------------------------------------

Javascript really doesn't have arrays in the traditional sense, they
are really dictionaries. Arrays can be of mixed type and they inherit
from `Array.prototype` instead of `Object.prototype`. There are no
maximum bounds to the array. Adding to a higher index will cause the
array to be dynamically extended to that new index length. It has
a length method which can be assigned to:

* making it larger does not increase the array size
* making it smaller will delete all objects past the new size

Elements can be deleted from arrays, but a gap will be left. If an
element needs to be removed, use the `array.splice` method.

.. code-block:: javascript

    array[array.length] = el; // both of these add a new element
    array.push(el);           // to the array

---------------------------------------------------------------------
Chapter 7 - Regular Expressions
---------------------------------------------------------------------

This is simply a reshash of regular expressions. If you know them,
then you can mostly skip this chapter.

---------------------------------------------------------------------
Chapter 8 - Methods
---------------------------------------------------------------------

This is a list of common *good* methods one should use. Simply
reading the W3C tutorials or the mozilla documentation is just as
useful as taking notes:

* http://www.w3schools.com/js/
* https://developer.mozilla.org/en-US/docs/Web/JavaScript

---------------------------------------------------------------------
Chapter 9 - Style
---------------------------------------------------------------------

This is a simple style guide that really doesn't differ too much
from the style I already use.

---------------------------------------------------------------------
Chapter 10 - Beautiful Features
---------------------------------------------------------------------

This is mostly covered by the included json parser at the end of the
book.

---------------------------------------------------------------------
Appendix - The Bad Parts
---------------------------------------------------------------------

* javascript scope rules
* semicolon insertion
* the reserved words
* falsey, NaN, etc values (coercion sucks!)
* using global scope and global variables
* using eval
* using `==`
* using the `with` statement
* a lot of personal style issues (Crockford)

.. todo:: finish copying notes

---------------------------------------------------------------------
Json Parser
---------------------------------------------------------------------

This is the json parser included at the end of the book that
demonstrates the flexibility of the javascript language:

.. code-block:: javascript

    var json_parse = (function () {
        "use strict";

    // This is a function that can parse a JSON text, producing a JavaScript
    // data structure. It is a simple, recursive descent parser. It does not use
    // eval or regular expressions, so it can be used as a model for implementing
    // a JSON parser in other languages.

        var at,     // The index of the current character
            ch,     // The current character
            escapee = {
                '"':  '"',
                '\\': '\\',
                '/':  '/',
                b:    '\b',
                f:    '\f',
                n:    '\n',
                r:    '\r',
                t:    '\t'
            },
            text,


    // Call error when something is wrong.
            error = function (m) {
                throw {
                    name:    'SyntaxError',
                    message: m,
                    at:      at,
                    text:    text
                };
            },


            next = function (c) {
    // If a c parameter is provided, verify that it matches the current character.
                if (c && c !== ch) {
                    error("Expected '" + c + "' instead of '" + ch + "'");
                }

    // Get the next character. When there are no more characters,
    // return the empty string.
                ch = text.charAt(at);
                at += 1;
                return ch;
            },


    // Parse a number value.
            number = function () {
                var number,
                    string = '';

                if (ch === '-') {
                    string = '-';
                    next('-');
                }
                while (ch >= '0' && ch <= '9') {
                    string += ch;
                    next();
                }
                if (ch === '.') {
                    string += '.';
                    while (next() && ch >= '0' && ch <= '9') {
                        string += ch;
                    }
                }
                if (ch === 'e' || ch === 'E') {
                    string += ch;
                    next();
                    if (ch === '-' || ch === '+') {
                        string += ch;
                        next();
                    }
                    while (ch >= '0' && ch <= '9') {
                        string += ch;
                        next();
                    }
                }
                number = +string;
                if (!isFinite(number)) {
                    error("Bad number");
                } else {
                    return number;
                }
            },


    // Parse a string value.
            string = function () {
                var hex,
                    i,
                    string = '',
                    uffff;

    // When parsing for string values, we must look for " and \ characters.
                if (ch === '"') {
                    while (next()) {
                        if (ch === '"') {
                            next();
                            return string;
                        }
                        if (ch === '\\') {
                            next();
                            if (ch === 'u') {
                                uffff = 0;
                                for (i = 0; i < 4; i += 1) {
                                    hex = parseInt(next(), 16);
                                    if (!isFinite(hex)) {
                                        break;
                                    }
                                    uffff = uffff * 16 + hex;
                                }
                                string += String.fromCharCode(uffff);
                            } else if (typeof escapee[ch] === 'string') {
                                string += escapee[ch];
                            } else {
                                break;
                            }
                        } else {
                            string += ch;
                        }
                    }
                }
                error("Bad string");
            },


    // Skip whitespace.
            white = function () {
                while (ch && ch <= ' ') {
                    next();
                }
            },


    // true, false, or null.
            word = function () {
                switch (ch) {
                case 't':
                    next('t');
                    next('r');
                    next('u');
                    next('e');
                    return true;
                case 'f':
                    next('f');
                    next('a');
                    next('l');
                    next('s');
                    next('e');
                    return false;
                case 'n':
                    next('n');
                    next('u');
                    next('l');
                    next('l');
                    return null;
                }
                error("Unexpected '" + ch + "'");
            },

            value,  // Place holder for the value function.


    // Parse an array value.
            array = function () {
                var array = [];

                if (ch === '[') {
                    next('[');
                    white();
                    if (ch === ']') {
                        next(']');
                        return array;   // empty array
                    }
                    while (ch) {
                        array.push(value());
                        white();
                        if (ch === ']') {
                            next(']');
                            return array;
                        }
                        next(',');
                        white();
                    }
                }
                error("Bad array");
            },


    // Parse an object value.
            object = function () {
                var key,
                    object = {};

                if (ch === '{') {
                    next('{');
                    white();
                    if (ch === '}') {
                        next('}');
                        return object;   // empty object
                    }
                    while (ch) {
                        key = string();
                        white();
                        next(':');
                        if (Object.hasOwnProperty.call(object, key)) {
                            error('Duplicate key "' + key + '"');
                        }
                        object[key] = value();
                        white();
                        if (ch === '}') {
                            next('}');
                            return object;
                        }
                        next(',');
                        white();
                    }
                }
                error("Bad object");
            };


    // Parse a JSON value. It could be an object, an array, a string, a number,
    // or a word.
        value = function () {

            white();
            switch (ch) {
            case '{':
                return object();
            case '[':
                return array();
            case '"':
                return string();
            case '-':
                return number();
            default:
                return ch >= '0' && ch <= '9' ? number() : word();
            }
        };

    // Return the json_parse function. It will have access to all of the above
    // functions and variables.
        return function (source, reviver) {
            var result;

            text = source;
            at = 0;
            ch = ' ';
            result = value();
            white();
            if (ch) {
                error("Syntax error");
            }

    // If there is a reviver function, we recursively walk the new structure,
    // passing each name/value pair to the reviver function for possible
    // transformation, starting with a temporary root object that holds the result
    // in an empty key. If there is not a reviver function, we simply return the
    // result.

            return typeof reviver === 'function'
                ? (function walk(holder, key) {
                    var k, v, value = holder[key];
                    if (value && typeof value === 'object') {
                        for (k in value) {
                            if (Object.prototype.hasOwnProperty.call(value, k)) {
                                v = walk(value, k);
                                if (v !== undefined) {
                                    value[k] = v;
                                } else {
                                    delete value[k];
                                }
                            }
                        }
                    }
                    return reviver.call(holder, key, value);
                }({'': result}, ''))
                : result;
        };
    }());
