================================================================================
 Programming Clojure 
================================================================================

--------------------------------------------------------------------------------
Preface
--------------------------------------------------------------------------------

Compelling features of clojure:

* Clojure is elegant 
* Clojure is Lisp reloaded (power without historical baggage)
* Clojure is a functional language (without side effects)
* Clojure simplifies concurrent programming with alternatives to locking:

  - software transactional memory
  - agents
  - atoms
  - dynamic variables

* Clojure embraces Java (no translation layer between java calls)
* Clojure is fast (unlike many popular dynamic languages)

--------------------------------------------------------------------------------
Chapter 1: Getting Started
--------------------------------------------------------------------------------

Lisp reloaded features:

* literal syntax for more data structures than list
* commas are whitespace
* removes as many nested parenthesis as possible

REPL Notes:

* recent evaluations stored in `*1  *2  *3`
* `(.printStackTrace *e)` contains the last error message
* `(load-file "testing.clj")` to load large code files into the repl

Example of creating a mutable function::

    (def visitors (ref #{}))
    (dosync (alter visitors conj "mark"))
    (deref visitors) ;; same as @visitors

    (defn hello
      "writes hello to *out* and knows if you ahve visited before"
      [username]
      (dosync
        (let [past-visitor (@visitors username)]
          (if past-visitor
            (str "welcome back, " username)
            (do
              (alert visitors conj username)
              (str "hello, " username))))))

    (hello "mark")

Clojure code is compiled into libraries that belong to a given namespace.
In order to use the library, you would require the namespace as follows::

    (require `clojure.contrib.str-utils) ;; have to fully qualify names with ns
    (refer `clojure.contrib.str-utils)   ;; adds all library names into this ns
    (use `clojure.contrib.str-utils)     ;; requires then refers
    (use :reload-all `namespace)         ;; reload a library after changes

The REPL also includes utilities to view the documentation of the names in
a given namespace::

    (doc str)               ;; documentation for this exact name
    (find-doc "reduce")     ;; search for documentation matching regex
    (source identity)       ;; view the source code of the given name
    (show obj)              ;; show all java members of a java object
    (ancestors obj)         ;; show java hierarchy

What follows is a listing of common parameter names in clojure (to prevent
shadowing functions)::

    a     = a java array
    agt   = an agent
    coll  = a collection
    expr  = an expression
    f     = a function
    idx   = an index
    r     = a ref
    v     = a vector
    val   = a value

--------------------------------------------------------------------------------
Chapter 2: Exploring Clojure
--------------------------------------------------------------------------------

.. todo:: page 45

