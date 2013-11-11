================================================================================
Datomic Database
================================================================================

--------------------------------------------------------------------------------
Datalog
--------------------------------------------------------------------------------

http://www.learndatalogtoday.org/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Introduction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Queries are written in extensible data notation (edn) similar to JSON, but more
complete:

* numbers:  `42. 3.14159`
* string:   `"this is a string"`
* keywords: `:kw, :namespace/kw, :foo.bar./baz`
* symbols:  `max, +, ?title`
* vectors:  `[1 2 3], [:find ?foo ...]`
* lists:    `(3.14 :foo [:bar :baz]), (+ 1 2 3 4)`
* instants: `#inst "2013-02-26"`

A query is a vector with four elements (this query returns all the movie
titles currently in the database):

* keyword: `[:find`
* symbol:   `?title`
* keyword:  `:where`
* vector:   `[_ :movie/title ?title]]`

All entries in dataomic are based on atomic facts called datoms. These
are 4-tuples consisting of:

* entity identifier
* attribute
* value
* transaction identifier

A database can thus be thought of as a flat set of datoms (in the following
all the datoms were added in the same transaction, and datoms with the same
e-id are attributes on the same entity)::

    [<e-id>  <attribute>      <value>          <tx-id>]
    ...
    [ 167    :person/name     "James Cameron"    102  ]
    [ 234    :movie/title     "Die Hard"         102  ]
    [ 234    :movie/year      1987               102  ]
    [ 235    :movie/title     "Terminator"       102  ]
    [ 235    :movie/director  167                102  ]
    ...

A query is thus a vector that matches all or part of the datom. Parts that
are not cared about can be marked with `_`, so the following finds all
entities that have `:person/name` of `James Cameron` (the trailing `-`
is a match for the tx-id and can be omitted):

.. code-block:: clojure

    [:find ?e
     :where
     [?e :person/name "James Cameron" _]]

Multiple data patterns can be issued in a single `:where` clause, however
they must be bound by a common pattern variable so the query planner can
resolve what query to make. For example, to find all the actors that
starred in `Terminator`:

.. code-block:: clojure

    [:find ?name
     :where
     [?m :movie/title "Terminator"]
     [?m :movie/cast  ?p]
     [?p :person/name ?name]]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Parameterized queries can be created by using the `in` clause which accepts
a parameter to query by and the database to query against (implicit if there is
no `in` clause):

.. code-block:: clojure

    [:find ?title
     :in $ ?name                      // $ id the database to use
     :where 
     [?p :person/name ?name]          // ?name is the query parameter
     [?m :movie/cast ?p]              // ?p is the eid transative match
     [?m :movie/title ?title]]        // ?title is the bound result

    (q query db "Sylvester Stallone") // find all movies of Stallone's

In the previous, the `$` is actually implicitly included in each data pattern
as a 5-tuple. This is what code is actually implemented:

.. code-block:: clojure

    [:find ?title
     :in $ ?name
     :where 
     [$ ?p :person/name ?name]
     [$ ?m :movie/cast ?p]
     [$ ?m :movie/title ?title]]

One can also supply multiple query arguments or tuple arguments that can be
destructured:

.. code-block:: clojure

    [:find ?title
     :in $ [?director ?actor]    // can also be :in $ $director $actor
     :where 
     [?d :person/name ?director]
     [?a :person/name ?actor]
     [?m :movie/director ?d]
     [?m :movie/cast ?a]
     [?m :movie/title ?title]]

One can also bind in external data to return in the query (here we pass in
actor and a relation of `[movie, rating]`, note that `?rating` is not bound
in any data pattern):

.. code-block:: clojure

     [:find ?title ?rating
      :in $ ?actor [[?title ?rating]]
      :where
      [?p :person/name ?actor]
      [?m :movie/cast ?p]
      [?m :movie/title ?title]]

One can also query by collections to implement a logical `or` query:

.. code-block:: clojure

    [:find ?title
     :in $ [?director ...]
     :where
     [?p :person/name ?director]
     [?m :movie/director ?p]
     [?m :movie/title ?title]]

One can query all the available attributes for a given entity (the first
query just returns the attribute ids associate with `:person`, the second
returns the names):

.. code-block:: clojure

    [:find ?attr
     :where 
     [?p :person/name]
     [?p ?attr]]

    [:find ?attr
     :where
     [?p :person/name]     // given one entity attribute
     [?p ?a]               // find other attributes of this eid
     [?a :db/ident ?attr]] // and match those ids to names

To print the entire database schema that is currently installed:

.. code-block:: clojure

    [:find ?attr ?type ?card
     :where
     [_ :db.install/attribute ?a]
     [?a :db/valueType ?t]
     [?a :db/cardinality ?c]
     [?a :db/ident ?attr]
     [?t :db/ident ?type]
     [?c :db/ident ?card]]

It is also possible to issue queries about transactions and time such as:

* when was a fact asserted
* when was a fact retracted
* which facts were part of the same transaction

We can query on this by using the fourth value of the tuple:

.. code-block:: clojure

    [:find ?timestamp
     :where
     [?p :person/name "James Cameron" ?tx] // the txid for this datom
     [?tx :db/txInstant ?timestamp]]       // the time of this txid

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Query Functions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One can use other predicates in the data patterns besides equals. One can use
any clojure function or java method to perform this filtering. The basic clojure
functions `(<, >, <=, >=, =, not=)` can be used directly, but other functions
must be fully namespace qualified like `(my.namespace/awesome? ?movie)`:

.. code-block:: clojure

    [:find ?title
     :where
     [?m :movie/title ?title]   // get the title
     [?m :movie/year ?year]     // of all movies
     [(< 1984 ?year)]]          // before 1984

    [:find ?name
     :where 
     [?p :person/name ?name]    // get the names of all people
     [(.startsWith ?name "M")]] // whose name starts with "M"

One can also use transformation functions to generate new query vaules to bind
to (note, these functions must be pure and have the shape
`[(<fn> <arg1> <arg2> ...) <result-binding>]`). Also, transformation functions
cannot be nested; each expression must be stored to a temporary binding before
being applied to the next function:

.. code-block:: clojure

    (defn age [birthday today]
      (quot (- (.getTime today)
               (.getTime birthday))
            (* 1000 60 60 24 365)))

    [:find ?age
     :in $ ?person ?today
     :where
     [?p :person/name ?name]
     [?p :person/born ?born]
     [(tutorial.fns/age ?born ?today) ?age]]

There are also aggregate functions that can be used to combine results
into a singular result. These include `sum, max, avg, etc` and they are
written in the `:find` clause:

.. code-block:: clojure

    [:find (max ?date)
     :where
      ...]

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Rules allow one to abstract away reusable parts of datalog queries that can be
grouped into meaningful units with names. For example:

.. code-block:: clojure

    [(actor-movie ?name ?title)  // can be used to find actor name given title
     [?p :person/name ?name]     // or movie title given actor name
     [?m :movie/cast ?p]         // supplying both, or one will filter the results
     [?m :movie/title ?title]]   // supplying neither will return all combinations

    [:find ?name
     :in $ %                     // database, collection of rules
     (actor-movie ?name "The Terminator")]

The same name can be bound to numerous rules to provide a type of `or` query
(the first matching rule will be used and following rules will not be
processed):

.. code-block:: clojure

    [[(associated-with ?person ?movie)
      [?movie :movie/cast ?person]]
     [(associated-with ?person ?movie)
      [?movie :movie/director ?person]]]

    [:find ?name
     :in $ %
     :where
     [?m :movie/name "Predator"]
     (associated-with ?p ?m)
     [?p :person/name ?name]]

Rules can also call themselves (as long as they terminate):

.. code-block:: clojure

    [[(friends ?p1 ?p2) [?m :movie/cast ?p1] [?m :movie/cast ?p2]]
     [(friends ?p1 ?p2) [?m :movie/cast ?p1] [?m :movie/director ?p2]]
     [(friends ?p1 ?p2) (friends ?p2 ?p1)]]

    [[(sequels ?m1 ?m2) [?m1 :movie/sequel ?m2]]
     [(sequels ?m1 ?m2) [?mn :movie/sequel ?m2] (sequels ?m1 ?mn)]]
