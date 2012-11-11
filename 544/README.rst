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

Also for each resource, common methods are supplied that
allow each resource to be used generically by each of the
supplied algorithms:

* append(piece)
* remove(piece)
* find_piece(preference, weight)
* compare(that)
* clone()
* actual_value()
* as_collection()
* create_pieces(user, count, weight)
* rich comparison methods
* __str__

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
Algorithms
------------------------------------------------------------

The algorithms should mostly be generic and thus able to work
with any kind of resource/preference pair. Currently
implemented in this collection are:

* austin_moving_knife
* banach_knaster
* divide_and_choose
* dubins_spanier
* inverse_divide_and_choose
* lone_chooser
* sealed_bid_auction

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
* consolidate the algorithm utilities
  - put them in the algorithm file in question
  - make more generic and not one off
  - find 1/n of value for a resource
* algorithms
  - fixed budget divider (budget based on bid count)
