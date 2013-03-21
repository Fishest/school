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

Transparency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

Monolithic systems tend to be closed instead of open as micro systems
generally have well defined interfaces (perhaps defined via a formal
IDL).

Scalability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are three forms of scalability:

1. Scalable with respect to size (can add more resources to system)
2. Scalable with respect to geography (can run from anywhere)
3. Scalable with respect to ease of administration

Scalable systems' size is generally hampered by centralized services,
centralized data, and centralized algorithms. Generally, distributed
algorithms have the following qualities:

1. No machine has the complete information about the machine state
2. Machines make decisions based only on local information
3. Failure of one machine does not ruin the algorithm
4. There is no implicit assumption that a global clock exists

The three basic techniques for scaling are:

1. **Hiding Communication Latencies** - Do as much async as possible
   or move some of the processing to the client.

2. **Distribution** - Take a component, split it into smaller pieces,
   and spread those parts across the system.

3. **Replication** - Copy the system data for better availability and
   load balancing. Having a nearby copy can reduce latency (caching).
   Replication can lead to inconsistencies between data copies.

Pitfalls
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following are false assumptions made during distributed
system development (when developing non-distributed applications,
many of this situations will not arise):

1. The network is reliable
2. The network is secure
3. The network is homogeneous
4. The topology does not change
5. Latency is zero
6. Bandwidth is infinite
7. Transport cost is zero
8. There is one administrator

The problems with Remote Method Invocation (RMI) and Remote
Procedure Calls (RPC) led to the development of Message
Oriented Middleware (MOM):

1. Caller and Callee have to be up at the same time
2. They have to know how to call and respond to each other
3. Very tight coupling of systems

Devices can be configured by their owners, but it is better
for them to discover their environment and settle in without
administration. Thus pervasive applications need to do the
following:

1. Embrace contextual change (environment can change whenever)
2. Encourage Ad-Hoc composition
3. Recognize sharing as the default

page 26
