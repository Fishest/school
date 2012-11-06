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
Utilties
------------------------------------------------------------

* Preference
  - unit value of resouce
  - check if valid preferences
  - value_of_resource

------------------------------------------------------------
Todo
------------------------------------------------------------

* add settings for algorithms
  - test them with the utility methods
  - test with non-trivial parameters
* 
* Wrap Ron's implementation in a preference
  - does this need a new resource?
* Algorithms
  - lone divider
  - sealed bids
  - dutch auction
