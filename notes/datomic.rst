================================================================================
Datomic Database
================================================================================

http://www.learndatalogtoday.org/

--------------------------------------------------------------------------------
Datalog
--------------------------------------------------------------------------------

Queries are written in extensible data notation (edn) similar to JSON, but more
complete:

* numbers:  `42. 3.14159`
* string:   `"this is a string"`
* keywords: `:kw, :namespace/kw, :foo.bar./baz`
* symbols:  `max, +, ?title`
* vectors:  `[1 2 3], [:find ?foo ...]`
* lists:    `(3.14 :foo [:bar :baz]), (+ 1 2 3 4)`
* instants: `#inst "2013-02-26"`

A query is a vector with four elements:

* keyword: `[:find`
* symbol:   `?title`
* keyword:  `:where`
* vector:   `[_ :movie/title ?title]]`
