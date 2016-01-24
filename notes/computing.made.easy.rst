================================================================================
How to Explain Computing to Anyone
================================================================================

* We need an interface to talk to a computing device

  - these can be computers, phones, cars, microwaves, etc
  - we have electricity and magnetism (mostly the same thing)
  - 1 or (+) is above some level of voltage, 0 or (-) is below
  - we can use bits to encode various pieces of data
  - explain: int, float, char, string, struct, field, etc

* We store this data in hard-drives and memory

  - memory needs voltage to stay stored, disks do not
  - think of memory as a library
  - the card catalog points to where we store each book (data)
  - the card is not the data, but just a pointer
  - when we need to store a new book, we find an empty spot
  - then we store and add a new card to the catalog
  - if we change a book, we change the card

* What is in the memory

  - as far as we know, it is just a collection of bits
  - depending on the type of computer, these are 32 bits, 64, bits
  - the data may even be multiple slots together or separate
  - think of encylopedias: too big for one book, or magazines
  - to know what is in the memory, we need types
  - text: those bits are a reading book, image: those bits are pictures

* usually when we are computing, we need many of those types, not just one

  - this lets us do a task many times or perform more complex tasks
  - say we have a collection of magazines (one for each month)
  - we would call this a list; it can keep growing
  - if the list cannot keep growing, we call it an array or vector
  - we can also have a custom type: say a book and its erratta
  - so we would have a List[(Book, Erratta)]
  - this is a struct or class or simply a type
  - we can make as many of these as we want
  - thes are data structures

* There are other data structures that present the data in handy ways

  - heap - if we want the best or worst of something (say books by rating)
  - queue - if we want to do things in order (list of books to read)
  - stack - if we need to go back in order (say a choose your own adventure)
  - tree / sorted list - if we need everything in order (books sorted by author)
  - map - if we need some type keyed by a unique value (all books by each author)
  - graph - if we need complex organization of data (all books linked by themes, author, etc)
  - and many more!

* Programming is simply perfoming operations on data represented by types

  - the language is arbitrary, but each language has trade offs
  - low level, dynamic typing, speed, hardware independence, specific tasks
  - regardless, the languages map to low level operations supplied by the CPU
  - we can combine them very much like types to produce more complicated operations
  - join two strings, print text to a monitor, write to a file (book)

* The process of software design is

  - take a high level real world problem
  - break it down into smaller problems
  - keep doing this until we know how to map each small problem onto an operation
  - either one we know how to do or one the language / computer lets us do
  - these are called algorithms, and there are a number of standard ones
  - sorting data, exploring data, finding data, etc
  - add all these things together and we have solved the problem

* Although languages look scary, anyone can learn them; it just takes a little time

  - after that they read mostly like english
  - think about learning any speaking language / same thing, but more abstract
  - the languages are much more limited than speaking language
  - computers cannot operate on something as complex as english
  - that problem is actually convert(english) -> computer language and is what google does

* After a while there may be many pieces of code talking together

  - this is software architecture
  - there are tradeoffs to be made based on what all code to put together
  - we have a number of design patterns that help us make these decisions
  - usually learned through experience (what worked / what did not)
  - tradeoffs are: performance, ease of maintainence, ease of upgrading, etc
  - at this point we have to start talking about distributed computing and operation systems

* Distributed computing is when more than one program is working together

  - this gets hard to do as there are many ways to solve this problem
  - just think of all the ways humans have communicated over history
  - to help this, we have a number of other programs that do some of this for us
  - databases: expose the same memory across a number of programs in a structured way
  - protocols: expose a consistent way to trade memory between computers
  - messaging systems: expose a standard way for programs to talk together
  - servers: expose a standard way for other programs to talk to ours
  - APIs: expose a standard way for other programs to tell our programs some data
  - filesystems: expose a way to store large amounts of data in easy to use ways

* There are a lot of problems that can occur when many programs are working at the same time

  - time skew: my watch says it is 5 and yours says it is 4; so what time is it?
  - ordering: we both got in line at the same time, so who is first?
  - corruption: you sent me a garbled message, but it looked okay to me, now your money is gone
  - errors: I have no clue what you did, but now I don't work
  - security: I didn't lock my library, and now you stole all my books or changed some
  - availability: I am broken or asleep and now you cannot get your work done
  - partitioning: I can't talk to you or you to me, so we are making decisions without each other
  - complexity: I cannot finish this work unless I make it simpler
  - performance: I cannot do this work each time and keep up, can we make it generic
  - caching: I saved some work to re-use it...when do I do the work again

* These are where the really hard problems are and we have no great way to solve all these problems

  - there is no silver bullet, trade offs have to be made
  - CAP is one guiding principal, but there are more
  - there is complex software that helps solve some of these problems
  - we can stack software on top of other pieces that solve these in a hierarchy
  - TCP/IP, journaled database, RPC frameworks
  - there is a lot of theory about many of these problems
  - a number of them have formal descriptions (how hard, how long, how much memory, protocols, etc)
  - some problems rely on testing the software (correctness, performance, resources)
  - some simply cannot be solved

* Those problems that cannot be solved have an interesting property

  - generally, we can convert a number of problems in CS to another problem
  - for example: given some arbitrary text, is it a valid program that will eventually complete
  - most problems can be converted to this (factor this large prime number)
  - so if we can solve just one of these really hard problems, then we have solved them all
