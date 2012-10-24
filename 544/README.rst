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

* abstract preference to work with:
  - discrete set
  - discrete list with count
    - with and without repeats
  - real resource

* abstract resources
  - can we make this generic for the algorithms?
  - refactor preference with this
