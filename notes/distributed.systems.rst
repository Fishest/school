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

Distributed sensor networks and querying of all the nodes can
be achieved with a tree organization and a tree query algorithm
(an example is TinyDB). An alternate solution is to have all the
nodes send their results to a single centralized host.

------------------------------------------------------------
Chapter 2: Architectures
------------------------------------------------------------

A distributed system can be made adaptable by monitoring its
own status in a feedback loop and taking appropriate actions
as neccessary (autonomic systems).

A `component` is a modular unit with a well defined, required
and provided interfaces that are replaceable within its
environment. A `connector` is a mechanism that mediates
communication, coordination, or cooperation among components.

Architecural Styles
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Using these two units, we can define a number of archicecture
styles such as (which all aim to achieve distribution transparency):

* **Layered Architecture** - components are orgainzed in a layered
  fashion such that a component at layer L_1 is allowed to call
  components at layer L_-1 but not the other way around. Requests
  go down the layers and results go back up.

* **Object Based Architecture** - Components are based around objects
  which have RPC calls. This is a generalization of the client server
  model.

* **Data Centered Architecture** - Components communicate through a
  single collective data repository (such as a distributed file
  system) that is passive or active.

* **Event Driven Architecture** - Components communicate through
  sending events, usually in a publish/subscribe architecture. The
  middleware takes care of routing published events to the current
  subscribers and effectively decouples all systems. If we combine
  event driven and data centric, we get event driven systems where
  components are decoupled from time; meaning that a component
  doesn't have to be around when the message is issued. Many systems
  use a SQL like interface to describe what they want rather than an
  explicit reference.

System Architectures
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When an operation can be repeated many times without any
side effects, it is said to be idempotent.

Client server architecture can be connection based (TCP),
or connectionless end and forget (UDP). The previous works
best in WAN networks where transmission failures may be
more common, while the latter may be preferred (and more
performnat) in LANs.

page 37
