============================================================
Cakery Class Assignment
============================================================

------------------------------------------------------------
Summary
------------------------------------------------------------

The cakery class assignment utility is an attempt to
perform fair division of a limited number of class
assignments between a number of students with non-uniform
preferences about the classes they would like to take. The
goal is to provide a class assignment that is proportional
among the students and if possible envy free.

The current algorithm being used to provide these gurantees
is Banach-Knaster's Trimming Algorithm.

------------------------------------------------------------
Resources
------------------------------------------------------------

The resources are simple wrappers around different "types"
of cake. Currently the following exist:

* collection:

  This represents a collection of discrete non-repeating
  items and can be used to model things like estate sales.

* counted:

  This represents a collection of discrete items that may
  be repeated one or more times. This can be used to
  represent things like course selection and registration.

* exact continuous:

  This represents a continuous resource that users may
  specify preference functions for. This can be used to
  represent divisible things like cakes. This is not as
  powerful as the piecewise continous, however, it is
  exact when rational numbers are used as the seed (can
  also use scaled integers and floats).

* piecewise continuous:

  This represents a continuous resource that users may
  specify preference functions for. This can be used to
  represent divisible things like cakes.

The general idea of the resource is to abstract the
following group methods: (from which we can build
higher level more general primitives that the algorithms
can use):

* append(piece)
* remove(piece)
* find_piece(preference, weight)
* as_collection()
* clone()
* actual_value()

Also for each resource, common methods are supplied that
allow each resource to be used generically by each of the
supplied algorithms:

* to_string()
* compare(that)
* create_pieces(user, count, weight)

------------------------------------------------------------
Preferences
------------------------------------------------------------

The preferences supply a mirror to each resource type that
is used to supply a few common functions around said resource
that are employed in the fair division algorithms:

* value_of:

  This is used to get the current value of a resource in the
  view of the current user in question.

------------------------------------------------------------
Algorithm Primitives
------------------------------------------------------------

Using the lower level methods supplied by the resource and
the preference interface, we can generalize the following
methods that allow the algorithms to be written in a much
higher level (and furthermore completely generically without
regards to the underlying resource type):

* randomize_items(items)
* choose_and_remove(items)
* choose_highest_bidder(users, item)
* choose_lowest_bidder(users, item)
* get_total_value(user, pieces)
* list_best_pieces(users, pieces)
* list_worst_pieces(users, pieces)
* choose_best_piece(user, pieces)
* choose_worst_piece(user, pieces)
* create_equal_pieces(user, cake, count)
* choose_next_piece(users, cake)
* trim_and_replace(user, cake, piece, weight)

------------------------------------------------------------
Algorithms
------------------------------------------------------------

The algorithms should mostly be generic and thus able to work
with any kind of resource/preference pair. Currently
implemented in this collection are:

* austin moving knife
* banach knaster
* divide and choose
* dubins spanier
* inverse divide and choose
* lone chooser
* sealed bids auction
* simple alternation
* inverse simple alternation
* balanced alternation
* inverse balanced alternation
* knaster sealed bids
* adjusted winner

------------------------------------------------------------
Class Interface
------------------------------------------------------------

The interface to the class project includes two things:

* preference files

  These are stored in the data directory and are specified
  as linear functions of `x-point y-value` that are
  monotonically increasing.

* algorithm listing

  This is listed in the algs file which is of the format
  `algorithm-file num-of-users` where num-of-users is the
  max supported number of users allowed in this algorithm.

------------------------------------------------------------
Todo
------------------------------------------------------------

* add settings for algorithms
  - test them with the utility methods
  - test with non-trivial parameters
* algorithms
  - fixed budget divider (budget based on bid count)
  - austin's moving knives
  - lucas method of markers
* algorithm unit tests
* algorithm stress tests
* unit test algorithm utilities for each resource
* choose_next_piece
  - find_piece must be at least 1/n (never under)
  - choose_next_piece chooses smallest value
  - choose_next_piece also wants smallest slice
  - for collections, knapsack problem?
* memoize value_of, find_piece?
* heavily work on the following:
  - stress_test_choose_next_piece
  - stress_test_create_equal_pieces
  - stress_test_trim_and_replace

------------------------------------------------------------
Links
------------------------------------------------------------

* http://ec2-184-72-151-84.compute-1.amazonaws.com/
* https://shell.cec.wustl.edu:8443/cse544_fl12/svn/group-cakery/
