============================================================
Golang
============================================================

.. todo:: http://golang.org/doc/effective_go.html

------------------------------------------------------------
Introduction
------------------------------------------------------------

* allows complete separation of a type's data from its behavior
  - duck-typing - values are handled by functions based on provided methods
  - aggregation (has-a relationship) and delegation handled by structs
  - interfaces are built around implemented methods
  - can satisfy more interfaces by just implementing methods
  - no inheritance
  - named and unnamed types can be used interchangeably
  - unnamed types cannot have methods

------------------------------------------------------------
Importing
------------------------------------------------------------

* If a single file compiles, it will link
  - no linker flags needed
  - this are extracted from the import clause

examples::

    package main
    import "fmt"
    import format "fmt"

    func main() {
      fmt.Printf("hello world\n")
    }

------------------------------------------------------------
Types
------------------------------------------------------------

* can use unicode in variable names
* specify variables as follows::

    var name type
    var i int
    int_value := 42
    int_pointer := &i // also pass by reference like this
    new_int_pointer := new(int) // zeroed instance
    generic_channel := make(chan interface{}) // calls ctor

* empty `interface {}` can be used as a general reference::

    func printer(str string, args ...interface{})(int, error) {
        // unused variables can be set to _
        _, err := fmt.Printf(str, args...)
        return len(args), err
    }

* only post increment, and not an expression `i++`
* use `const { }` for enums, and `iota` as a counter
* types can export public and private fields
  - uppercase are exposed outside of package
  - lowercase are only exposed to the current package
  - no protected because there is not inheritance
* example struct types::

    type Example struct {
        Value string
        count int
    }

* implicit casting is not allowed; always explicit::

    type empty interface {}
    one := 1
    var empty = one
    var float float32
    // type conversion
    float = float32(one)

    // type switch statement
    switch i.(type) {
        default:
            fmt.Printf("type error!\n")
        case int:
            fmt.Printf(%d\n", i)
    }

    // type assertions checked at run time (dynamic_cast)
    fmt.Printf("%d\n", i.(example)) // this will panic
    fmt.Printf("%d\n", e.(empty).(int))


------------------------------------------------------------
Methods
------------------------------------------------------------

* can use pimped types without explicit casts
* can add methods to any named type (not primitives)::

    type integer int
    // here is the receiver (self or this)
    // is passed as a value (changes are not reflected)
    func (i integer) log() {
        fmt.Printf("%d\n", i);
    }

    // can take a pointer and modify values
    func (e *Example) log() {
        e.count++
        fmt.Printf("%d\n", e.count);
    }

* these are strongly typed for value vs reference
* interfaces and types can be defined in different packages
* think of using interface where you would use c++ templates
* although no inheritence, there is interface composition::

    // single method interfaces add -er to method name
    type Printer interface {
        Print()
    }

    type Point interface {
        Printer // composes printer interface
        X() float64
        Y() float64
    }

------------------------------------------------------------
Closure
------------------------------------------------------------

* closures can bind to variables in their scope::


    func main() {
        count := 1
        closure := func(msg string) {
            fmt.Printf("%d %s\n", count, msg)
            count++
        }
        closure("Hello")
        closure("World")
    }

------------------------------------------------------------
Looping
------------------------------------------------------------

* the only looping construct is the for loop::

    loops := 0
    for loops > 0 {
        // while loop
        continue
    }
    for i := 0; i < loops; i++ {
        // traditional for loop
    }
    for {
        // infinite loop
        break
    }
    EXIT:
    for {
        break EXIT // goto
    }

------------------------------------------------------------
Numbers
------------------------------------------------------------

* explicit sizes (int16, int32, etc)
* defaults are at least 32 bits (int, uint)
* convert between formats with strconv
* `math/big` contains arbitrary length int and rational numbers
* can convert between pointers and ints with the unsafe package

------------------------------------------------------------
Patterns (chapter 4)
------------------------------------------------------------

.. todo:: chapter 4
