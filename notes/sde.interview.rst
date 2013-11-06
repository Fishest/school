=================================================
SDE (I/II) Interview Script
=================================================

-------------------------------------------------
Initial 10 to 15 minutes
-------------------------------------------------

* Get familiar with the developers resume / experience
* Introduce yourself, ask if you were expected
  - is this still a good time to do the interview, if not reschedule
  - make sure you are interviewing for the correct position
* Ask about current work / job history; just fluff to ease the interview
* Ask a few soft probing questions
  - Why do you want to work for amazon
  - What amazon products have you used (AWS) / What do you like about amazon
  - Why are you leaving your current position
  - What is the hardest project you have worked on, why?
  - What is the worst project you have worked on, why? 
  - What kind of work do you like doing (backend / frontend)

-------------------------------------------------
Middle 40 minutes
-------------------------------------------------

* Try and find a passionate project to dig deep on (play dumb / dig deep on these)
  - what was the architecture (dig deep to see if they actually know it)
  - what technologies were used (can you explain them)
  - explain it to me like I am five (communication and understanding)
  - what did they actually do (dive deep for them to prove it)
  - What was the development methodology / specification (agile, waterfall)
  - What did you learn / What would you change / What else about this project
  - What unit test framework do you use
  - What third party libraries do you use
  - What source control have you used
  - How did you deploy to production
  - What editors / IDEs do you use
  - How do you do documentation
  - What was the business knowledge of the system

* Computer Science Questions
  - What languages do you know (quick dive on concepts to test)
  - Linux / Windows / Unix knowledge (quick probes to test)
  - Name some design patterns you have used (not singleton)
  - Talk a bit about OO (class vs object, interface, polymorphism)
  - What scripting languages do you use
  - Static typing (generics) / dynamic typing (duck typing)
  - Tell me some datastructures you use / explain how they work
  - Talk about concurrency / distributed systems
  - Talk about services (SOAP / REST) and how to structure them

* Pick a coding question and have them code it in collabedit

-------------------------------------------------
Last 5 minutes
-------------------------------------------------

* Wrap up and allow them to ask questions
  - Is there anything you would like to know about Amazon, my group, etc.
  - sell the company


=================================================
Subject Matter Questions
=================================================

-------------------------------------------------
Concurrency
-------------------------------------------------

Talk about some concurrency primitives:

* mutex

  - implement a reader / writer lock
  - wakes up all writers when the write is free: use condition per writer
  - locks do not happen in order: use a condition queue
  - readers starve writers: don't allow reads while a writer exists
  - writers starve readers: randomly choose to wake up reader / writer
  - pure read workloads cause contention: do a no lock happy path or use lock free

* semaphore

  - how is this different from a mutex
  - implement with a condition variable and a mutex

* condition variable
* event flags
* atomic variables

  - implement this with a mutex
  - implement this with CAS

* threads / processes

  - what is the difference between a thread and a process

* synchronization barriers
* STM
* actors

  - how are actors different than threads
  - what is the actor protocol

-------------------------------------------------
Data Structures
-------------------------------------------------

Give me a structure that has:

* O(1) insert/lookup (tradeoff between hash and list)
* O(N) insert/lookup (how to make O(1) insert, lookup)
* O(logN) insert/lookup (what tree tradeoffs can you make)

What are the various ways to implement a list:

* array
* single / double linked list
* skip list

-------------------------------------------------
General
-------------------------------------------------

If you were given the time to move your experience to the next level:

* What subject would you learn
* How would you deep dive into the language you use
* What would you like to build


