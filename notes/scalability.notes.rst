================================================================================
Scalability Notes
================================================================================

--------------------------------------------------------------------------------
Bitly Architecture
--------------------------------------------------------------------------------

`Bitly Architecture <http://highscalability.com/blog/2014/7/14/bitly-lessons-learned-building-a-distributed-system-that-han.html>`_

* **Expose knowledge about all parts of the system**

  The more you understand the properties of the things you are working with the
  better decisions you can make and the more efficiently you can work.

* **Fully expose leaky abstrations**
  
  If you are using a layer of abstraction that hides the underlying distributed
  nature of the system it will eventually bubble through.

* **Put it all on one box if you can**
  
  If you don’t need a distributed system then don’t build one. They are
  complicated and expensive to build.

*  **Degrade functionality in SOA, don't fail**
  
  In a Service Oriented Architecture failure means reduced functionality instead
  of going down.

* **Queues + Asynchronous Messaging is powerful**
  
  This approach isolates components, lets work happen concurrently, lets boxes fail
  independently, while still having components be easy to reason about.

* **Use synchronous requests when speed and consistency are paramount**
  
  Give users an error rather than a slow or wrong answer.

*  **Event style messages are better than command style messages**
  
  They allow for better isolation between systems and naturally support multiple
  consumers. Helps keep services focussed and not worried about anything beyond
  what the service is supposed to do.

* **Annotate rather than filter**
  
  Filters at the producer level bake in assumptions about what the downstream
  services care about. Instead, annotate an event and let services operate only
  on the kind of events they care about.

* **Services should play nice with each other**
  
  Use back pressure to prevent a service from being overloaded and route around
  failed services.
