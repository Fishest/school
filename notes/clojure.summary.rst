============================================================
Clojure Introduction
============================================================

------------------------------------------------------------
Documentation
------------------------------------------------------------

Can look up documentation strings a la python::

    (doc when)              ; get docstring for when
    (find-doc "sequence")   ; search for docstrings with sequence
    (apropos "map")         ; find methods with map
    (source take)           ; print source of method take
    (dir clojure.repl)      ; list methods in this namespace

------------------------------------------------------------
Literals
------------------------------------------------------------

* string:       "hello"
* char:         \e
* long:         42
* double:       6.022e23
* bigdecimal:   1.0m
* bigint:       12345N
* ratio:        22/7
* regex:        #"hel+o"
* null:         nil
* boolean:      true/false
* symbol"       println
* keyword:      :beta
* list:         (1 2 3)         # singly linked, grow at front
* vector:       [1 2 3]         # indexed, grow at end
* map:          {:a 1, :b 20}   # key/value pairs
* set:          #{1 2 3}        # unordered, unique
* comments:     ;;; file level, ;; block level (indented), ; line level
* whitespace:   , \t \n 

------------------------------------------------------------
Semantics
------------------------------------------------------------

* Invokable list special forms:
  - def if fn let
  - loop recur do
  - new . throw try
  - set! quote var

* The following is how s-expressions work::

    list symbol string
       |      |      |
       (println "hello world")
       |      |          |
    call function argument

* To define a function::

    (defn greet                         ; function name(list)
      " returns a friendly greeting"    ; docstring(string)
      [name]                            ; arguments(vector)
      (str "hello, " name))             ; function body

* example statement blocks::

    (if condition then-expr)
    (if (even? 42) "even")

    (if condition then-expr else-expr)
    (if (even? 42) "even" "odd")

    (do *expressions)
    (do (println 42)(println 43))

    (when condition *expressions)
    (if condition (do *expressions))

    (quote form)    ; 'form
    (quote (1 2 3)) ; '(1 2 3)
    (list 1 2 3)

    (let [*bindings] *expressions)      ; can rebind values later
    (let [x 6, y 7] (* x y))            ; alias values with bindings
    (let [x 6, y (* 2 x)] (* x y))      ; reference earlier bindings

    (fn [*params] *expressions)         ; compiled function
    (fn ([*params] *expressions)+)

    (defn symbol [*params] *expressions)
    (def symbol (fn [*params] *expressions)+)

    (defn greet                         ; how to deal with arity
      ([] (greet "example" "programmer"))
      ([name] (greet name "programmer"))
      ([fname lname] (println fname " " lname "programmer")))

    (defn greet                         ; how to deal with variadic
      ([name] (println name "programmer"))
      ([name & others] (println name "and" others)))

------------------------------------------------------------
Working with Data 
------------------------------------------------------------

* lists and vectors implement value equality::

    (= [1 2 3] [1 2 3])             ; true
    (= [1 2 3] '(1 2 3))            ; true

* for references, use identical?::

    (identical? [1 2 3] [1 2 3])    ; false
    (identical? :a :a)              ; true

* methods that work on collections::

    (count [:a :b :c])              ; 3
    (coll? [:a :b :c])              ; true
    (vector? [:a :b :c])            ; true
    (list? [:a :b :c])              ; false
    (first [:a :b :c])              ; :a
    (second [:a :b :c])             ; :b
    (nth [:a :b :c] 2)              ; :c
    (rest [:a :b :c])               ; (:b :c)
    (conj (:a :b :c] :n)            ; (:a :b :c :n)
    (conj (:a :b :c) :n)            ; (:n :a :b :c)

* associative map methods::

    (def m {:a 1 :b 2})
    (get m :a)                      ; 1
    (m :a)                          ; 1
    (:a m)                          ; 1
    (keys m)                        ; (:a :b)

    (def hm (hash-map :a 1 :b 2))
    (assoc hm :c 3 :d 4)            ; a new map with added values
    (assoc hm :a 17)                ; a new map with updated values
    (dissoc hm :a)                  ; a new map with key removed
    (conj hm [:c 3])                ; a new map with added key/value
    (merge hm {:c 4 :d 5})          ; a new map with merged keys/values
    (zipmap [:a :b :c] [1 2 3])     ; zips into a map


    (def person
       {:name {:first "first" :last "last" }
        :address {:city "brooklyn" :state "NY" }})
    (:first (:name person))
    (get-in person [:name :first])
    (assoc-in person [:name :first] "new first")
    (update-in person [:name :first] #(.toUpperCase %))

    (def vv [:a :b :c])             ; vectors are associative with index
    (assoc vv 1 "hello")            ; [:a "hello" :c]

* set methods::

    (def ss #{1 2 3 4})
    (confj ss 17)                   ; new set with added element
    (confj ss 2)                    ; returns same set reference
    (set [1 2 3 1 2])               ; #{1 2 3}
    (contains? ss 3)                ; returns true
    (ss 4)                          ; 4
    (ss 7)                          ; nil

------------------------------------------------------------
Destructuring Data
------------------------------------------------------------

* easy ways to work with data::

    (def stuff [1 2 3 4])
    (let [[a b c d] stuff           ; (3 7)
      (list (+ a b) (+ c d)))
    (let [[a & others] stuff        ; (1 (2 3 4))
      (list a others))

    (def mm {:a 7 :b 8})
    (let [{a :a, b :b} mm]          ; [7 8]
      [a b])
    (let [{:keys [a b]} mm]         ; [7 8]
      [a b])
    (let [{:keys [a b c]} mm]       ; [7 8 nil]
      [a b c])
    (let [{:keys [a b c]            ; [7 8 3]
           :or {c 3}} mm]
      [a b c])

------------------------------------------------------------
Higher Order Functions
------------------------------------------------------------

* a number of common higher order functions exist::

    (println 1 2 3)
    (apply println [1 2 3])

    (map (fn [x] (* 5 x )) [1 2 3])
    (map #(* 5 %) [1 2 3])          ; shorthand lambda
    (map vector [:a :b :c] [1 2 3]) ; ([:a 1] [:b 2] [:c 3])

    (reduce + [1 2 3 4])            ; 10
    (reduce + 100 [1 2 3 4])        ; 110 (initial seed value)

    (filter even? [1 2 3 4 5])      ; (2 4)
    (filter identity [1 2 3 4 5])   ; (1 2 3 4 5)
    (filter (set "aeiou") "hello")  ; (\e \o)
    (remove (set "aeiou") "hello")

    (def add (fnil + 0))            ; replace nil with 0
    (add nil 3)                     ; 3
    (def m {:foo {:a 1 :b 2})
    (update-in m [:foo :a] inc)     ; {:foo {:a 2 :b 2})
    (update-in m [:baz :d] (fnil inc 0)) ; {:foo {:a 1 :b 2} :baz {:d 1})

    (frequencies "a short sharp")   ; character frequencies

------------------------------------------------------------
Sequences
------------------------------------------------------------

* there are a number of functions for working with sequences::

    (range 1 5)                     ; (1 2 3 4 5) (lazy)
    (range)
    (range end)
    (range start end)
    (range start end step)

    (map vector (range) [:a :b :c])
    (map-indexed vector [:a :b :c])
    (zipmap [:a :b :c] (range))

    (repeat 5 :a)                   ; limited repeat
    (take 10 (repeat :b))           ; infinite repeat

    (seq [1 2 3])                   ; (1 2 3)
    (seq #{1 2 3})                  ; (1 2 3)

* lazy vs strict::

    (with-open [file]
      (line-seq file))              ; lazy evaluation

    (with-open [file]
      (doall (line-seq file)))      ; strict evaluation

    (doall sequence)                ; get all elements of lazy sequence, list
    (dorun sequence)                ; force side effects of sequence, nil
    (doseq [symbol sequence] body)  ; roughly foreach to force side effects, nil
    (for [symbol sequence] body)    ; foreach, returns lazy list

------------------------------------------------------------
Interopping with Java
------------------------------------------------------------

* can examine the class type and hierarchy::

    (class "hello")                 ; java.lang.String
    (ancestors (class "hello"))     ; ... java.lang.Object
    (javadoc java.io.Writer)        ; url writer
    (javadoc "hello)                ; url for string

    (. object field)
    (. object method arguments*)
    (. class static-field)
    (. class static-method arguments*)

    (. "hello" charAt 0)            ; instance methods
    (.charAt "hello" 0)

    (. Long valueOf "42")           ; static methods
    (Long/valueOf "42")

    (. Math PI)                     ; static fields
    Math/PI

    (new java.io.File "/home")      ; constructors
    (java.io.File. "/home")

    (import (package classes*))     ; imports
    (import (java.net URL URI))

* exception handling a la Java::

    (try
       ... expressions ...
       (catch Class name
          ... handle exception ...)
       (finally
          ... finally code ... ))

    (throw exception)               ; print stack trace with (pst)
    (throw (Exception. "Boom!"))    ; view exception in REPL with *e

------------------------------------------------------------
Tools
------------------------------------------------------------

* clojure uses the default maven directory structure:
  - leiningen(project.clj)
  - cake
  - maven(pom.xml)
  - ant

* can find libraries at a number of locations
  - search.maven.org
  - jarvana.com
  - clojars.org

* included with clojure
  - clojure-contrib (lots of stuff)
  - clojure-bcl

------------------------------------------------------------
Namespaces
------------------------------------------------------------

* the repl displays the current namespace you are in::

    user => (ns my.cool.thing)        ; $CLASSPATH/my/cool/thing.clj    
    my.cool.thing => ...
    
    (ns my.cool.thing-doer)           ; $CLASSPATH/my/cool/thing_doer.clj    
    
    (foo.bar/hello)                   ; namespace qualified symbol
    
    (ns name references*)
    (ns name
      (:require [name :as foo]))      ; namespace aliasing
    (foo/function-in-foo)
    
    (ns name
      (:use [name :only (A B)]))      ; unqualified includes
    (A)                               ; don't need namespaces
    (B)
    
    (ns name
      (:use name))                    ; unqualified * include
    
    (ns name
      (:import (java.io File Writer))); import java classes
    
    (use 'clojure.string)             ; in repl, arguments must be quoted
    (require '[clojure.set :as set])

------------------------------------------------------------
Concurrency
------------------------------------------------------------

* parallelism implies many separate threads of execution
* concurrency implies many threads operating on some state
* generally one should deal with immutable values
* ref, atom, var, and agent are mutable references::

    (def tick (atom 1))             ; atomic CAS references
    (deref tick)                    ; 1
    (swap! tick inc)                ; 2
    (swap! tick + 10)               ; 12

    (def a (ref 1))                 ; STM references
    (def b (ref 10))
    (dosync
      (alter a inc)
      (alter b + 10))

    (def c (agent 1))               ; like an actor with behavior as message
    (send a inc)                    ; messages are processed in order

------------------------------------------------------------
Macros
------------------------------------------------------------

* basically let us do things after the parser::

    (read-string "(println 1 2 3)")
    (eval *1)

    (defmacro when [test & body]    ; code for (when [] ...)
      (list 'if test (cons 'do body)))
    (macroexpand '(when a b c d))   ; see macro result

    `(syntax-quoted ~unquoted       ; think of like cpp escapes
                    ~@splice-unquoted)
    (gensym "foo")                  ; generates a unique foo symbol
    `(let [x# 1] x#)                ; # shortcut

------------------------------------------------------------
Recursion
------------------------------------------------------------

* common examples of solving problems with recursion::

    (defn gcd [x y]                 ; x >= y
      (if (zero? y) x
        (gcd y (rem x y))))

    (defn gcd [x y]                 ; tail call version
      (if (zero? y) x
        (recur y (rem x y))))       ; no native tail call optimization

    (defn fib-step [a b n]          ; traditional method
      (if (= 1 n) b
        (recur b (+ a b)(dec n))))
    (defn fib [n]
      (fib-step 0 1 n))

    (defn fib [n]                   ; using loop/recur
       (loop [a 0, b 1, i n]
         (if (= 1 i) b
           (recur b (+ a b)(dec i)))))

    (loop [initialization]          ; general template
      (if termination-condition
        return-value
        (recur updated-variables)))
