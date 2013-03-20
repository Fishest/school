============================================================
Distributed Systems
============================================================

------------------------------------------------------------
Chapter 1: Introduction
------------------------------------------------------------

A distributed system is a collection of independent computers
that appear to its users as a single coherent system:

- The differences between computers and how they communicate
  is transparent to the users
- The internal organization of the system is hidden from the users
- The users of the system can interact with the system in a
  consistent way regardless of where and when the interaction
  takes place.

A distributed system should achieve four(4) things:

1. Makes resources easily available
2. Hide the fact that the resources are distributed
3. The system should be open
4. The system should be scalable

There are a number of forms of transparency::

    ------------------------------------------------------------------
    Transparency | Description
    ------------------------------------------------------------------
    Access       | Hide differences in data representation and access
    Location     | Hide where a resource is located (use logical names)
    Migration    | Hide that a resource may move locations
    Relocation   | Hide that a resource may move location while in use
    Replication  | Hide that a resource is replicated
    Concurrency  | Hide that a resource may be shared by several users
    Failure      | Hide the failure and recovery of a resource

Systems in which resrouces using logical names can be moved provide
migration transparency. If a resource can be moved while it is in use,
the system provides relocation tranparency. Sometimes it makes more
sense to lower the transparency of the system to make situations
explicit to developers.

page:8 
