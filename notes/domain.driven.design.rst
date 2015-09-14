================================================================================
Domain Driven Design
================================================================================

--------------------------------------------------------------------------------
Introduction
--------------------------------------------------------------------------------

Software needs to incorporate the core concepts and
elements of the domain, and to precisely realize the
relationships between them.  Software has to model the
domain. We need to communicate the model

A core principle of domain-driven design is to use a
language based on the model. Since the model is the common
ground, the place where the software meets the domain, it is
appropriate to use it as the building ground for this
language: the Ubiquitous Language.

Therefore, partition a complex program into LAYERS. Develop 
a design within each LAYER  that  is cohesive and  that depends 
only on  the  layers below. Follow standard architectural patterns 
to provide loose coupling to the layers above. Concentrate all the 
code related to the domain model in one layer and isolate it from 
the  user  interface,  application,  and  infrastructure  code.  The 
domain  objects,  free  of  the  responsibility  of  displaying 
themselves, storing themselves, managing application tasks, and 
so  forth, can be  focused on expressing  the domain model. This 
allows a model to evolve to be rich enough and clear enough to 
capture essential business knowledge and put it to work.

--------------------------------------------------------------------------------
Seperation of Layers
--------------------------------------------------------------------------------

A common architectural solution for domain-driven designs 
contain four conceptual layers:

* User Interface (Presentation Layer) 

  Responsible for presenting information to the user and
  interpreting user commands. 

* Application Layer 

  This is a thin layer which coordinates the application 
  activity. It does not contain business logic. It does not 
  hold the state of the business objects, but it can hold 
  the state of an application task progress. 

* Domain Layer

  This layer contains information about the domain. This 
  is the heart of the business software. The state of 
  business objects is held here. Persistence of the 
  business objects and possibly their state is delegated to 
  the infrastructure layer. 

* Infrastructure Layer 

  This layer acts as a supporting library for all the other 
  layers. It provides communication between layers, 
  implements persistence for business objects, contains

--------------------------------------------------------------------------------
Entities
--------------------------------------------------------------------------------

There is a category of objects which seem to have an identity, 
which remains the same throughout the states of the software. 
For these objects it is not the attributes which matter, but a 
thread of continuity and identity, which spans the life of a 
system and can extend beyond it. Such objects are called Entities

Usually the identity is either an attribute of the object, a
combination of attributes, an attribute specially created to
preserve and express identity, or even a behavior. It is important
for two objects with different identities to be to be 
easily distinguished by the system, and two objects with the 
same identity to be considered the same by the system. If that 
condition is not met, then the entire system can become 
corrupted.

--------------------------------------------------------------------------------
Value Objects
--------------------------------------------------------------------------------

There are cases when we need to contain some attributes of a 
domain element. We are not interested in which object it is, but 
what attributes it has. An object that is used to describe certain 
aspects of a domain, and which does not have identity, is named 
Value Object.

It is highly recommended that value objects be immutable. They 
are created with a constructor, and never modified during their 
life time. When you want a different value for the object, you 
simply create another one. This has important consequences for 
the design. Being immutable, and having no identity, Value 
Objects can be shared. That can be imperative for some designs. 
Immutable objects are sharable with important performance 
implications. They also manifest integrity, i.e. data integrity.

--------------------------------------------------------------------------------
Services
--------------------------------------------------------------------------------

There are three characteristics of a Service: 

  1. The operation performed by the Service refers to a domain 
     concept which does not naturally belong to an Entity or Value
     Object. 
  
  2. The operation performed refers to other objects in the domain. 
  
  3. The operation is stateless. 
  

--------------------------------------------------------------------------------
Modules
--------------------------------------------------------------------------------

Modules are used as a method of organizing related concepts 
and tasks in order to reduce complexity.

Designers are accustomed to creating modules from the outset. 
They are common parts of our designs. After the role of the 
module is decided, it usually stays unchanged, while the 
internals of the module may change a lot. It is recommended to 
have some flexibility, and allow the modules to evolve with the 
project, and should not be kept frozen. It is true that module 
refactoring may be more expensive than a class refactoring, but 
when a module design mistake is found, it is better to address it 
by changing the module then by finding ways around it.

--------------------------------------------------------------------------------
Aggregates
--------------------------------------------------------------------------------

An Aggregate is a group of associated objects which are considered
as one unit with regard to data changes. The Aggregate is demarcated
by a boundary which separates the objects inside from those outside.
Each Aggregate has one root. The root is an Entity, and it is the only 
object accessible from outside. The root can hold references to 
any of the aggregate objects, and the other objects can hold 
references to each other, but an outside object can hold 
references only to the root object. If there are other Entities 
inside the boundary, the identity of those entities is local, 
making sense only inside the aggregate.

The root Entity has global identity, and is responsible for 
maintaining the invariants. Internal Entities have local identity.


--------------------------------------------------------------------------------
Factories
--------------------------------------------------------------------------------

These are used to build complex entities, values, or
aggregates.


--------------------------------------------------------------------------------
Repositories
--------------------------------------------------------------------------------

The purpose of the Repository is to encapsulate all the
logic needed to obtain object references. The domain objects
won't have to deal with the infrastructure to get the needed
references to other objects of the domain. They will just get
them from the Repository and the model is regaining its
clarity and focus.

We should not mix a Repository with a Factory. The Factory
should create new objects, while the Repository should find
already created objects. When a new object is to be added to
the Repository, it should be created first using the Factory,
and then it should be given to the Repository which will store
it.

================================================================================
Refactoring
================================================================================

It is very important to have expressive code that is easy
to read and understand. From reading the code, one should be
able to tell what the code does, but also why it does it. 
Only then can the code really capture the substance of the
model.


================================================================================
Preserviing Model Integrity
================================================================================

Instead of trying to keep one big model that will fall apart
later, we should consciously divide it into several models.
Several models well integrated can evolve independently as
long as they obey the contract they are bound to. Each model
should have a clearly delimited border, and the relationships
between models should be defined with precision.

--------------------------------------------------------------------------------
Bounded Context
--------------------------------------------------------------------------------

A model should be small enough to be assigned to one team.

--------------------------------------------------------------------------------
Shared Kernel
--------------------------------------------------------------------------------

Some subset of the domain model that the two teams agree to
share. Of course this includes, along with this subset of
the model, the subset of code or of the database design 
associated with that part of the model. This explicitly
shared stuff has special status, and shouldn' be changed
without consultation with the other team.

--------------------------------------------------------------------------------
Customer Supplier
--------------------------------------------------------------------------------

There are times when two subsystems have a special 
relationship: one depends a lot on the other. The contexts in 
which those two subsystems exist are different, and the 
processing result of one system is fed into the other. They do not 
have a Shared Kernel, because it may not be conceptually 
correct to have one, or it may not even be technically possible 
for the two subsystems to share common code. The two 
subsystems are in a Customer-Supplier relationship.

--------------------------------------------------------------------------------
Conformist
--------------------------------------------------------------------------------

Basically the customer supplier, except the customer is tied
to the whims of the supplier.

--------------------------------------------------------------------------------
Anticorruption Layer
--------------------------------------------------------------------------------

Facade in front of legacy system to provide consistent
interface to new system. Will also need an adapter. Objects
and data are converted with translators.

--------------------------------------------------------------------------------
Open Host Service
--------------------------------------------------------------------------------

If many clients are using your subsystem, and you don't want
to have facades for all of them, hoist your system to an open
system and give a unified service interface that other's can
use.

================================================================================
Command Query Responsibility Seperation (CQRS)
================================================================================
