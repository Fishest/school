============================================================
Time in Distributed Systems
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Time is an ordering of events in a sequential order. Events
can happen before each other (in either order) or even at 
the same time::

    E1 -> E2 // e1 happens before e2
    E2 -> E1 // e2 causes e1
    E2 || E1 // e1 and e2 happen at the same time

    // or more generically
    E_past -> E_now
    E_now  -> E_future
    E_now || E_concurrent
    E_concurrent || E_concurrent

Using clocks adds Lamport's Clock Condition::

   E1 happens at T1 // event1 happens at time1
   E2 happens at T2 // event2 happens at time2
   E1 -> E2         // event1 causes event2
   then T2 > T1     // time2 is larger than time1

However, if you change your frame of reference and thus your
clock, you change the number's assigned to events and perhaps
the ordering of concurrent events (but never causal events so
partial ordering is maintained).

.. notes::

   "Time is what keeps keeps everything from happening at once"
   "Clocks assign numbers to events"
   Cache Coherency Protocol (SMP Caches)

--------------------------------------------------------------------------------
Lamport Clocks
--------------------------------------------------------------------------------

There are three cases that need to be handled:

1. The clock has to be incremented after an event (by any amount)
2. After sending a message, time can stay the same, however, after
   receiving a message, the receive event must come from the future
   of the source and destination.
3. Unrelated concurrent processes do not need to sync times

This can be seen as follows::

    Case 1:
    ---[24]A[25]------[88]B[89]------------>


    Case 2:
    --------[13]---[26]-------------------->
                  /
    --------[25]---[25]-------------------->


    Case 3:
    --------[13]---A[14]------------------->

    --------[25]---B[26]------------------->

Lamport Clocks only deal with messages in their own systems
which causes a lot of problem cases dealing with:

* Complexity
* Failure
* Covert Channels

--------------------------------------------------------------------------------
ALF Locks
--------------------------------------------------------------------------------

Using distributed locks removes the case of concurrent events;
there is only past and present (before and after `unlock`).
The problem with this is that it can introduce innefficieny
into the system.

In the case of network partition, we have the following solutions:

* Block indefinately to wait for an unlock
* ALF releases the lock after some time (but the user may come back
  thinking it still has the lock and doing writes).
* Introduce transactions into the database system (integrating ALF and
  S3 into database).
* ALF gives a lock with a timeout duration (not a timeout time because
  of Segal's Law: "a man with a watch always knows the time. A man
  with two watches is never sure.")

System clocks are horrible for ordering; unix clock can go back in
in time, can be reset, and have horrible precision. Instead use the
chip clock (rdtsc) which can be used to compute duration (but not
global time)::

    T*   Ts                Tu
    ------- [E]---------------------------->
         < /   wait time   >
    -----[lock]------------[unlock]-------->

    * Ts is the staleness that occurs because of the time to
      transmit the message (it cuts into the wait time). When
      you hear some news, it is already old.

    * Tu is the forced unlock time where both parties know that
      the lock is no longer held (Ts + delta)

In paxos, the lock is achieved at some time before the requesting
node is alerted of it. This is the start of the staleness. In order
to determine a tight bound of the staleness (impossible to be exact)
the relation between previous events must be used to generate a delta
with the chip clock.

In practice, a delta is not given, but instead ALF keeps pinging the
client to let them know that the lock is still valid (and the staleness
is reset). When the ALF client thinks that you are failed, it will
revoke the lock, which means that the staleness is starting to be
computed. When the maximum wait time is achieved, the client is supposed
to cancel its work as it no longer has the lock. The programming model
hides this heartbeating behind a call-back when the failure happens::

    // assume we are now partitioned as our staleness is too high
    alf_client.on_failure = (error) ->
      stop_using_locks()

============================================================
Why Distributed Transactions Suck
============================================================

The relative speed of operations::

                     Cycles      Seconds       Scaled
    -------------------------------------------------
    CPU Register        1        0.33 ns         1 s
    L1 cache            3        1 ns            3 s
    L2 cache           14        4.7 ns         14 s
    RAM               250        83 ns         4.2 m
    Network         6 mil        2 ms        69 days
    Disk Write    7.8 mil        2.6 ms      90 days
    Disk Read      15 mil        5 ms       173 days

--------------------------------------------------------------------------------
Write Ahead Logging
--------------------------------------------------------------------------------

Write ahead logging can be used to write transaction
details as they occur. If the transaction fails because
of failure, when the DB comes back up, it will look for
commit messages. If they are found, the transaction is
recovered, else they are dropped::

    TxnA start  -> TxnA change -> TxnB start -> TxnC commit
    TxnA commit -> TxnB change -> TxnB commit

This is optimized for writing and thus is bad for queries.
So all the transactions need to be in RAM and the transactions
must be committed ASAP.  Also, if the log fills up, then
everyone is blocked.

--------------------------------------------------------------------------------
Two Phase Commit
--------------------------------------------------------------------------------

Distributed Transaction Minimums::

    Wt = 2 + 2D
    Mt = 4D

    D = databases
    W = writes
    M = messages

--------------------------------------------------------------------------------
Why They Suck
--------------------------------------------------------------------------------

In any distributed system, messaging will fail. The only way
to ensure operations are done is to retry them, so every
operation must be tried multiple times:

* Inefficient use of database resources
* Scaling of the transaction coordinator
* Availability is the intersection of all systems involved
* Idempotent operations don't need distributed transactions

Examples of idempotent examples:

* non-mutating read: don't make any changes
* assignment or replacement: aaaabbbb
* order safe: ababaabb

To make operations idempotent, the following must be done:

* Assign every operation an ID
* Define a DAG for every possible state
* Track what the operations affect
* Define compensation policies
* Define rules for how different operations can combine

This no longer needs distributed transactions and can be
performed across databases. Customers must now know that
transfers may be in process.

--------------------------------------------------------------------------------
Techniques
--------------------------------------------------------------------------------

Explicit Transactions handle all the requirements in the
application

Optimistic Locking works as follows:

* Keep a current revision number
* increment revision number on update
* require revision number with every update
* if number passed in is not current value, reject
* parallel operations are disallowed

Immutable Versions works as follows:

* Need two systems: base and detail
* detail depends on base data
* base data needs to change
* best if base is read before detail

Herd workflow engine

============================================================
POA Gems
============================================================

--------------------------------------------------------------------------------
Endemic Spreading
--------------------------------------------------------------------------------

Choose a network peer at random and exchange data with each
other via push/pull gossip udp messages::

    a -> status -> b
    b -> status -> a
    # continue until consensus is statistically correct

--------------------------------------------------------------------------------
CAP
--------------------------------------------------------------------------------

Given consistency, availability, and partition tolerance:

* **CA**: single site database, database clusters
* **CP**: majority protocols, distributed locking and
  databases if you are on the wrong side of the partition
  you cannot make progress, otherwise you are good to go.
* **PA**: caching, dns, dynamo

--------------------------------------------------------------------------------
Scalable Architecture
--------------------------------------------------------------------------------

* Partition your use cases (users, batch/live, etc) so that problems in
  one will not break the other
* Plan for the worst case, but have your system run at the common case (elastic)
* Fail fast and restart instead of browning out
* Logging does not scale (IO starts to be a killer)
* Dig into unusual outages as there may be more there that meets the eye.

============================================================
Load Balances Don't Have To Suck
============================================================

--------------------------------------------------------------------------------
OSI 7-Layer Model:
--------------------------------------------------------------------------------

* (7) Application
* (6) Presentation
* (5) Session
* (4) Transport (TCP/IP)
* (3) Network
* (2) Data Link
* (1) Physical

The load balancer for HTTP operates at layer 7, and the
servers can be balanced by being pointed to with a VIP.
The load balancer can do a number of things to help
backend services:

* header injection (X-Forward)
* SSL processing

The load balancer for services operates at layer 4 and
has no knowledge about the content of the request/service.
This will forward SSL processing to the backend service
and can increase performance of the load balancer.

--------------------------------------------------------------------------------
Common load balancing policies:
--------------------------------------------------------------------------------

* Round Robin

  This take turns between different servers.
  This doesn't take into account the variations in request
  type such as get current time vs encode an entire movie
  (i.e. server load). 

* Random

  This just chooses the next server at random.
  This has no way to prevent hot spots, we can choose
  the same host every time or more often than the others.

* Max Connections

  This associates the next request with any server that
  has and number of connections left (defined max connections
  for worst case).
  This has the same problem as Round Robin.

* Least Connections

  This associates the next request with the server with
  the least available connections to it.
  This has no way to prevent routing requests to a broken
  server.

--------------------------------------------------------------------------------
Policies for Managing overloaded load balancers:
--------------------------------------------------------------------------------

* Surge Connection Queue

  If any max connection load balancer is full, then the
  connections are queued and delivered when there is an
  open connection (connections may be dropped by client
  but work is still done; don't use).

* Spillover

  If the request cannot be assigned, just return an error
  and let the client try again.

--------------------------------------------------------------------------------
How can we make a better load balancer (JLB):
--------------------------------------------------------------------------------

* Distributed load balancer
* Scales to infinity (horizontal)
* Better fault tolerance
* Simple load balancing strategy
* Cheap hardware
* Open software that we can maintain

                     /=> Switch (Juniper iEX4500)
    Cisco 3750-e => JLB-E
                     \=> Router (Quanta SW)

* Equal Cost Multi-Path (ECMP)

  Takes in large quantaties of data to a VIP and basically
  uses consistent hashing to distribute load across the
  hosts behind it.

* Intel DPDK
* Yet Another Network Node (YANN)

  Internal kernel module that accepts Ncap/Dcap packets
  and reinterprets them as the initial packets. It detects
  overload and accepts configuration.

--------------------------------------------------------------------------------
The JLB Process
--------------------------------------------------------------------------------

1. Ingress packets arrive at ingress server that wraps packet
2. It sends the fake packet to a primary flow tracker
3. This forwards it to a secondary flow tracker
4. This is fowarded to the web server
5. The web server YANN decodes the packet and sends it back up the chain
6. Once back to ingress, ingress can forward all queued data directly
   to the web server.
7. Web server sends fake packets to egress server to flow the data out.

a. On failure, the new ingress server contacts the primary flow tracker
   and gets current state (if it exists) or starts the process again.
b. All SSL happens on the host machine
c. The ingress server is chosen by consistent hashing
d. The YANN knows its own state, and on close publishes updates to the 
   flow servers.

In the YANN module IRQ handler, we can quickly check if we can handle
the packet or not (CPU utilization, message queue, etc), and if not,
it sends a reject message back through the flow trackers which choose
another host to route to:

* A TTL is added to the message so that it isn't rejected forever

============================================================
Quorums and Chains: Consensus Beyond Paxos
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

What if the central storage fails (durability)::

    client -> writer(n) -> storage
    client -> reader(n) -> storage

We can add a copy or backup of the data on every committ;
what if we get too much load to continue this (availability)::

    client -> writer -> storage -> backup
    client -> writer -> xxxxxxx -> backup
                     -> storage <- backup
    client -> writer -> storage -> backup

We can add a hot stand by, but what if those get out of sync
or are partitioned::

    client -> writer -> storage -|
    client -> reader -> storage -|

--------------------------------------------------------------------------------
Chain Architecture
--------------------------------------------------------------------------------

Nodes chain off of each other and effectively serialize the
events.

--------------------------------------------------------------------------------
Quorum
--------------------------------------------------------------------------------

On write, the writer must contact a majority of the storage
nodes, if it does, it is granted a write quorum and is
allowed to write. The same is true for a reader.

With (3) storage nodes, the reader and writer need 2 nodes
for quorum and thus there will be node intersection between
the two events.

To handle which version of the data is correct, simply use
timestamps to retrieve the latest version of the data. And
for writers, the latest time writer gets the ability to
write. Problems:

* out of sync clocks
* bad timestamps
* what is the specification (what does "works" mean)

Can do a two phase write where we get the current highest
write version and then make ours higher (so the order is
preserved).

--------------------------------------------------------------------------------
Atomic Register Specification
--------------------------------------------------------------------------------

The best way to determine if a distributed system works is
to create a model and:

* establish if it works (correctness)
* establish when it works (liveness)
* establish theoretical peformance

There exists one such partial order such that each read
operation sees the last write operation:

* The operations are serializable (isolated)
* A_e -> B_s <=> A -> B (operations are partially ordered)
* (A -> B) ^ ~(B -> A) <=> A || B (concurrent operations)

Then look at the possible states as a graph (acyclic if
possible) then determine:

* can take a step from every state (liveness)
* no infinite traces (termination)
* every trace is correct (correctness; automate with TLA+)

Problems with atomic registers (dynamo doesn't use them):

* no atomic test and set
* write does not return the previous value
* no way to lock

--------------------------------------------------------------------------------
Asyncronous Message Passing
--------------------------------------------------------------------------------

Given a collection of processes that can receive messages:

1. select a message
2. deliver the mssage
3. update the process state machine with message
4. process can send new messages

a. process may fail and no longer receive messages
b. null messages are ok (to change state of machine)
c. can deliver in a finite number of steps (messages are not dropped)

This model is completely deterministic given the order of
message delivery, failure detection is impossible, and
the messaging is asynchronous meaning it cannot handle timeouts.

To reason about the system, define the state machiens for
the processes and apply the model::

    Reader Process
    ---------------------------------------------------
    state    message     new state           messages
    ---------------------------------------------------
    any      write       if T > t, update    ack
    any      read        no change           time,value

    Writer Process
    ---------------------------------------------------
    state    message     new state           messages
    ---------------------------------------------------
    init     write(x)    reading             read
    reading  time,value  if Q, writing       write(T, x)
    writing  ack         if Q, done          reply

    T = new time (higher time)
    t = existing time
    Q = quorum

--------------------------------------------------------------------------------
ABD Algorithm
--------------------------------------------------------------------------------

Here is how a writer works in the ABD algorithm:

1. Client puts a message in buffer requesting a write
2. Writer pulls a message from the buffer and processes it
3. The writer sends a number of read messages to get a quorum
4. Any storage node gets a read message and sends a message with
   the read value.
5. Once the writer gets its quorum, it sends the write messages
   to the buffer.
6. The write message gets delivered to a storage node (all of
   them in time). And They each return an ack message to the
   buffer.
7. The writer gets back its quorum of acks and then sends a
   response back to the client.

--------------------------------------------------------------------------------
Analysis
--------------------------------------------------------------------------------

**Correctness**

* every trace through the states is correct
* can prove with TLA+
* can manually do pen / paper analysis

**Liveness**

* system can always take a step

**Termination**

* system will eventually terminate (no infinite traces)

--------------------------------------------------------------------------------
Consensus
--------------------------------------------------------------------------------

Powered by Replicated State Machines:

* A write once abstraction
* proposers all attempt to write values, only one succeeds
* readers get the recent value or none at all
* required properties: valid, correct

This can easily be created with a chain replication:

* just ignore all but the first write
* allows pipelining (writes can quickly flow without blocking)
* but not fault tolerant

--------------------------------------------------------------------------------
Paxos Consensus
--------------------------------------------------------------------------------

* Quorum based algorithm
* proposer is two rounds and does not always succeed
* not guranteed to terminate; FLP Impossibility Proof
* storage nodes host the state machine
* Chubby, alf, zookeeper
* no pipelining (batching and windowing)
* requires redrives in the event of contention

--------------------------------------------------------------------------------
Dynamic Configuartion
--------------------------------------------------------------------------------

* each node in the chain has an active config prefix (not all)
* can create a dynamic chain architecture
* swami decides on join and leave events
* chain nodes upgrade at their own pace
* no reconfiguration event

============================================================
Moving Fast
============================================================

How to make a great team that can deliver great projects on
time and fast:

1. Invest in being able to move fast
2. Have the right people
3. The key is to learn as fast as possible 
4. Minimize coordination costs
5. Localize decision making
6. Have an appetite for risk

How to minimize coordination costs ("Even well meaning
gatekeepers slow innovation"):

1. Gate keepers don't scale, remove them
2. Decentralize and decouple
3. Self service APIs between teams

Understanding risk in a project:

1. The point is to not minimize risk
2. Think of risk as a currency

* If you have a simple today, how long would it take to be
  live? What stands in your way?
* Are you using or moving towards continuous deployment
* Do changes required coordination with other people on an
  hours to days schedule or a seconds-to-minutes schedule.
* Are there gatekeepers that are not scaling
* Is measurement and experimentation built into my product
* Is is easy to learn what is working and what is not

============================================================
How to Design a Good API and Why it Matters
============================================================

Public APIs are forever, you only get one chance to get it
right. Bad APIs result in lots of support calls. Characteristics
of a good API are:

* easy to learn (feels natural)
* easy to use (even without documentation)
* hard to misuse
* easy to read and maintain code that uses it
* sufficiently powerful to satisfy requirements
* easy to extend
* appropriate to audience

Start writing to your API as soon as possible:

* bounce spec of as many people as possible
* flesh it out as you gain confidence in the API
* saves you from implementing things that you will throw away
* prevents nasty suprises and backed in corners
* provides unit tests as you go along (TDD)
* examples live on as the default copy and paste code
* if you provide a service provider interface, write at least
  three plugins before you release it.

Maintain realistic expectations:

* most API designs are constrained
* you will not please everyone
* displease everyone evenly
* you will make mistakes in the first version (real world use
  will flesh out the edge cases)
* design to evolve

API should do one thing and do it well. Functionality should
be easy to explain:

* if it is hard to name, it is a bad sign
* good names drive development
* always be ameneable to splitting/merging details

API design should be as small as possible, but no smaller:

* API should satisfy its requirements
* when in doubt, leave it out
* you can always add, but you cannot remove
* conceptual weight is more important than bulk
* resuse interfaces to reduce bulk

Implementation should not affect the API; these confuse the
users and inhibit the freedom to change implementation:

* do not overspecify the behavior of methods
* do not specify hash functions
* all tuning parameters are suspect
* don't let implementation details to leak to the outside:
  (exceptions, wire-format, on-disk-storage, implements
  Serializable)

Minimize accessibility of everything:

* make classes and members as private as possible
* public classes should have no public fields (except constants)
* this maximizes information hiding
* this minimizes coupling

Names matter a lot; it is like a little language for your API:

* be consistent
* names should be largely self explanitory
* strive for consistency (don't have delete and remove)
* strive for symmetry (add, remove)

Documentation matters (Parnas) "Even when we see good design,
it will not be used without good documentation":

* if it isn't documented, then the user will guess or will use
  the code as the documentation which couples your design to
  your internals.
* fully document public api (class, method, exception, parameter
  interface, constructor)
* class: what an instance represents
* method: contract between method and clients (preconditions,
  postcondidtions, side effects)
* parameter: units, ownership, form
* document state space carefully if mutability is involved

Consider perfomance with API design:

* bad api decisions can limit performance
* do not warp api to gain performance

API must coexist with the platform:

* do what is customary
* take advantage of API friendly features
* know and avoid api traps and pitfalls
* never simply transliterate APIs

Minimize mutability:

* classes should be immutable unless there is a good reason otherwise
* if mutable, keep the state space small and well defined

Subclass only when it makes sense (Liskov)
Document and design for inheritance or else prohibit it:

* make all concrete classes final

Don't make the client do anything the module could do (avoid
as much boilerplate code as possible).

Don't violate the principal of least astonishment (users of API
should not be suprised of behavior).

Fail fast and report errors as soon as they occur (ideally at
compile time is best with static typing and generics). Otherwise,
the first method call should fail.

Provide programmatic access to all data available in string form,
for example exception messages should provide getters for fields
in exception message.

Overload with care; avoid ambiguous overloads.

* Don't have multiple overloads with the same number of arguments
* Just because you can, doesn't mean you should
* Sometimes giving something another name is a better idea

Use appropriate parameter and return types:

* favor interface types over classes for parameter types
* use most specific possible input type
* don't use string if a better option exists
* don't use floating point for monetary values
* use double instead of float

Use consistent parameter ordering across methods. Especially if
the parameter types are identical.

Avoid long parameter lists:

* keep them below two or three parameters
* break up methods
* use classes to help create parameters (builder)

Avoid return values that require exceptional processing
(empty list instead of a null).

============================================================
Designing 100K Services
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Given performance, maintainability, and time to market, ideally
choose two to optimize for but realistically choose one.

Caching solutions used to increase throughput:

* use redbox style local proxy to remote cache
* AF_UNIX sockets
* fewer threads
* out of order pipeline
* binary protocol (to increase CPU pipelining)
* CacheOut/CacheIn use linked list of fixed size memory pages
 
  - this fixes evictions for cases when using sequential memory
  - results in very little memory fragmentation

============================================================
SWF Oracle to DynamoDB
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* Tasks and Decisions go on AMP
* processor picks them up and gathers state form database
* updates state based on decisions
* possibly issue new decisions to AMP
* partitioning was easy with Oracle (just use hash function on keys)
* repartitioning was hard with Oracle (...)
* how to do transactions: write ahead log

  - log is append only
  - log schema: { seq_id, entry, writer }
  - rebuild in memory state with log replay if box failure
  - use checkpointing to reduce log replay size

* have a routing table to have sticky backends handling requests

  - got too big, so had to shard the system
  - shards model the entire hashable space of workflows (fixed)
  - backend system then uses consistent hashing to map shards
  - this is fixed and easy to cache

* when a backend host goes down, shard is rebalanced to a new backend

  - this is implemented with alf to detect ownership change
  - alf maintains list with heartbeats
  - when a host goes down, alf pushes new system list to backends
  - backends take over responsibility of shards (consistent hashing)

* in case of network partitions

  - use conditional check of dynamo to write log (won't stomp state)
  - prevents logging of old owners with a lease window
  - will take N write spots in the log (how many writes per operation)
  - if a user goes down, we write "sealed" into down service spots
  - this prevents a CAS write by the down spot

* can extend performance of the system by just adding dynamo capacity

============================================================
Amazon Kinesis
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* elastic beanstalk
* streaming map reduce
* stream composed of data records, partitioned by a key into shards
  each shard hits a worker, sequence numbers on data records handle
  ordering, final result hits some datastore
* source -> kinesis -> kinesis application -> RDBMS
* client library handles creating shard counts (implement `IRecordProcessor`)
  - stored in local dynamoDB table
  - each worker locks a shard in dynamo to take ownership
  - workers are in ec2 autoscaling groups (scaled with cloudwatch)
  - workers that are unbalanced weighted coin toss rebalance
  - failed workers have their shard locks time out; eventually rebalance
  - can have multi-datacenter with two autoscaling groups (datacenter)
* checkpoint / replay design pattern (appendlog)
  - application desides when to checkpoint
  - checkpoint is specific to a application and shard
  - checkpoint hash is `shardId-seqNum`
  - lock table is { shardId, lock, seqNum }
  - on failure, new shard gets stale lock and takes over
  - Then reads seqNum, restores state, and reads records after seqNum
* dynamic resharding
  - md5_hash(string) % shard_count
  - Put(record)  -> VIP -> proxy-server
  - proxy-server -> VIP -> Get(...)    
  - split overloaded hash bucket (next bit of md5 hash)
  - explicit ordering: s2 > s1            (seq are ordered)
  - implicit ordering: s3 > { s2, s1 }    (close seq are near each other)
  - seqNum: {epoch}.{shardId}.{subSeqNum} (preservers order after shard)
  - each shard has an id generator (snowflake) (epochs can be different across shards)
  - on reshard a new epoch boundary is created (increment epoch)
  - these shard epochs can then diverge (think of shards as split queues)
  - if a shard is closed (passed final epoch), a redirect is returned
  - redirect instructs client to requeue a record to the supplied queue
  - on finishing a shard, worker checkpoints and gets a new shard
* big data architecture
  - kinesis -> (kinesis apps) -> s3 -> redshift
  - archive data into s3 (to replay / audit)
  - generate reports to redshift for customers
  - generate results to third-party services (ec2)
  - easy to write `connectors` from kinesis
  - allows for easy transformations of data to third-party

.. code-block:: java

    // pseudo worker code
    iterator = getShardIterator(stream, shardId, sequence);
    while (true) {
        [records, iterator] = getRecords(stream, iterator)
        process(records)
    }

============================================================
QLDB - AppendLog
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

The QLDB (Quantum Logging – Quantum as in atomic transactions)
provides three features:

* implements atomic multi-item transactions over Dynamo-DB
* provides tools to maintain real time alternate views of the data
* provides a change journal with every change made to the store

History is roughly:

* Cards -> Random Disk Access -> BTree -> ISAM file (BDB)
* ACID Transactions (All or None, , Don't Lose My Data)
* SQL, Transaction Log / Locks, CAP
* BASE Transactions (Be Sure to Answer, Sort of Right, Eventually Consistent)
  - Riak, Cassandra, Voldermort, DynamoDB
  - key-value store     -> per item transactions and CAS
  - pessimistic locking -> aquire lock, modify, release lock
  - optimistic locking  -> read item and version, write one version higher if unchanged
 
Use the transaction log to specify intent to modify the data
in the specified table. Write modify intents and commit in
the log for each modification. Use locks on the table to prevent
multiple concurrent modifications to the database.

Solution is QueryLog(QL). Code is visually the same, but it is
wrapped in a transaction closure and executed in a query manager.

* reads simply read from the database (DynamoDB)
* writes write commands to a log context (not to the system)
* uncommitted writes are stored to Alf Bus as punch cards in a buffer
* committed writes are stored on a linear tape
* a reader process reads the tape asynchronously and writes to the database
* snapshots aggregated are stored in the datastore (versioned)
* snapshot isolation
  - reads happen at the requested snapshot (sequence number of snapshot)
  - read set, write set (from database), and commands are the context
  - alf bus takes this total context and attempt to write to the tape
  - can only write if anything in the tape after snapshot will be in conflict
  - failures must simply be tried again (CAS)
* QueryLog is now the datastore and database is now a convenient cache
  - can always rebuild any snapshot by applying all log entries
  - can have as many datastores as we want with different views of the data
  - can materialize views with precomputed queries
  - optimistic locking is great for low contention
  - high contention writing must essentially be serialized (with lots of retries)
* Result is QLDB -> { QLDB, QLDynamoDB, QLDDBExample }
  - can be a client library or a coral service

============================================================
Timer Service
============================================================

.. todo:: architecture

------------------------------------------------------------
Summary
------------------------------------------------------------

============================================================
Big Data Stream Processing
============================================================

------------------------------------------------------------
Summary
------------------------------------------------------------

There are some differences in design that must be handled with big data processing:

* can only see data once and then it is gone
* need to be able to react to streams in real time
* not a general messaging framework, work queue, amp, or sqs
* no message acknolowedgements
* no message retries

How to design a stream processing system:

* create a stream 
* create N stream processors
  - load balance the streams
  - send streams to routher of hash(key) -> processor
  - router also queues the incoming streams to be delivered
  - create many partitions and assign M partitions to each processor
  - load balancing is just assigning a partition piece to a new machine
  - have in memory locality of all data for a given key (hashmaps)
* time is maintained by sliding windows
  - partition aggregate data in 10 minute windows
  - to get hour queries, just sum the last 6 buckets
  - to add a new window, drop the oldest bucket and create a new one
* results can then be published in a number of ways
  - create a new stream to be consumed
  - support online queries to the store
  - publish to memcached or dynamodb
  - poller on the processor -> stores in file db -> dumps to s3

Design consdierations:

* model your data messages to know the overall stream size
  - small size is better (compression)
  - low delay is also better (batching)
* failure and replication
  - compure the model twice by sending the same partition to M hosts
  - this handles single node failures
  - to handle hot deploys, checkpoint current model to disk with timestamp
  - when loading, check if the checkpoint is still valid
  - sending too fast causes receiver to get behind (old data) or drop data

* flow control
  - communicate delays between systems and queue between sources
  - sleep between sends for X ms to control rate
  - maintain rate by additive increase and multiplicative decrease
  - start slow and ramp up quickly
  - maintain a current failure rate
  - randomly drop data in proportion to failure rate

============================================================
Time and Order in Kinesis
============================================================

The main takeaways from this talk on distributed systems are:

* ordering events is a hard problem in distributed systems
* tracking additional information may be the solution
* solutions to ordering are imperfect and come with tradeoffs

------------------------------------------------------------
Summary
------------------------------------------------------------

Capacity is managed in kinesis by using shards. To scale out,
we simply create more shards. There is a point of time when
this sharding should happen. We can order events by reading
from shard_1 and then shard_2:

* we can mark this time split with system time
* if a clock is after the threshold, write to shard_2
* but time in distributed systems is not consistent
* this will not produce a correct ordering

A client writing to the frontend works as follows (the client is
the user and the frontend is the kinesis service):

* The first write can be sent using the frontend system time
* the frontend returns a token of the time it wrote with
* The second write is sent with the original token
* The next frontend makes sure the new time is slightly larger
* This is the case even if it's system time is lower
* This is a client sequencer / sequence number (monotonically increasing)

The kinesis analysis server can then read from the shards
by maintaining an offset pointer. It then reads latest by
supplying its offset and getting all new writes after it as
well as its new offset.

* client sequencers do not solve the read after write order (analysis server)
* the analysis server may have already read past the client write point
* we can bound clock skew to <= 1 second
* report writes as faield if they take more than ~1 second
* we delay reads to 2 seconds in the past
* The 2 seconds is to account for the clock skew and read timeout (1 + 1)

The time can be managed by a conductor who publishes the
current time which is read by all the frontends. The time
is monotonically increasing based on write events.

* only increment once a second, and only increment by 1
* we only need a counter as time will be delayed by operations
* don't need real time, we need a logical clock (epoch counter)
* shift to new shard is based on an epoch count
* conductor writes epochs to a well known row in dynamo that frontends read
* conductor is a distributed system, but can scale independing of frontends

Can we understand how far the analysis server is behind
actual time, in terms of seconds instead of epochs?

* we can see the frontends current epoch and alaysis offset
* publish this as a graph of diffs (how many epochs is it behind)
* we can publish three epochs (current, current - 1, current - 2)
* we can read two epochs in the past instead of 2 seconds ago
* for outage, new epoch is (07:05:31, 07:05:01, 07:05:00)
* system can catch up to latest in two epochs
* metrics can be published in real time instead of epochs
* this is simply keeping a bounded amount of epoch history

============================================================
DynamoDB with Kinesis
============================================================

------------------------------------------------------------
Summary
------------------------------------------------------------

* data plane
* control plane
* update streams
* chain replication
* alfbus required signature and forbidden signature
  - reject if FS exists
  - fail if RS does not exist
  - these signatures are a sliding window of hashset
  - can verify ordering and de-duplication for an N size window
* pipelined puts to alfbus
  - asynchronous stumpy
  - persistent connections to services
* storage nodes stream to an agnostic set of alfbus
  - demux makes an order window buffer
  - debux then uses control plane to write to table specific stream
  - this is exposed through the read stream
  - alf is used to manage the fleet and elect a scheduler node

================================================================================
Distributed Data Structures
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Can we reduce distributed programming to a single primitive
that is backed by research: distributed hash table. These can
scale as long as gear can be supplied:

* unlimited keys
* unlimited cumulative data
* unlimited cumulative TPS
* unlimited DHT functionality: `get`, `set`, `delete`
* limited single key TPS (cannot scale a single machine)
* limited non DHT functionality: `list-keys`

We can model any existing data structure in a DHT as all memory allocations
are just a key to value pair with memory address to data. There are a number
of problems that we have to overcome with this new solution though:

* **Keys Are Shared**

  If we do not do anything to control it, multiple systems will write to the
  same keys and collide with each others data. We can avoid namespace collision
  by first prefixing the node with a type flag (stack, node, etc). Furthermore,
  if we want to hide a node until the operation it is involved in is complete, we
  can temporarily assign it a randomized name (uuid) until we are finished:

  * `stack/application-name` -> `node/A0`
  * `2341234sadf23` -> `node/A1`

* **Data Is Permanent**

  In a single process application in memory, if the application fails, memory
  is cleared and can simply be started again. In a DHT the data will not be
  cleaned up and may stay forever. One way to solve this problem is to perform
  a best effort cleanup with garbage collection. Simply save the keys that were
  created during the operation and then delete them on a rollback. Otherwise,
  they can simply be ignored if we can afford the extra space. Comprehensive
  scan otherwise if we can understand the linkage of the system (linked list).

* **Concurrency Happens**

  Blocking distributes badly if say another piece takes a lock and fails. We
  could use time based locks or some other method, otherwise we can use the
  `CAS` primitive. If we know the state of the world, we are allowed to
  update it. If not, we will fail. This update happens atomically. At first
  we can simply spin-loop to try and update the value until we can get through.
  However, if we have the knowledge to complete the state of the system, we can
  complete the work for the other threads which gets us to *Lock Free* systems.
  The value changes we will monitor are the version of the values:

  - `get(key) -> (value, version)`
  - `put(key, version) -> version`
  - `del(key, version) -> version`

.. note:: Papers to read

   Dijkstra (all locking primitives reduce to CAS)
   Maurice Herilhy (all primitives can be wait free)

* **Multiple Operations**

  Create a new virtual head node `transaction-<id>`. It can be in three states:
  open, committed, cancelled. The nodes involved with the transaction are made
  to point to the head node. They have a condition that:

  * if the txn is open or cancelled, the value is the original
  * if the txn is committed, the value is the new value

  New nodes can simply interpret the new values based on the txn values or clean
  up at some time to resolve the new values. Any node can do this as the values
  are encoded in the txn node. So if the original node crashes during the
  transaction, the node will go to cancelled and a new reading node can then
  remove the transaction reference and delete the transaction node.

.. code-block:: javascript

    // original
    { account: a, balance: $100 }
    { account: b, balance: $0   }

    // during transaction
    { transaction: a-b, state: open }
    { account: a, balance: $100, tx: { id: a-b, committed-value: $90 } }
    { account: b, balance: $0, tx: { id: a-b, committed-value: $10 } }

    // after transaction (and CAS cleanup)
    { transaction: a-b, state: committed }
    { account: a, balance: $90 }
    { account: b, balance: $10 }

* **Isolation**

  Can use copy on write to provide isolation. Simple create a new copy that
  you can operate on as much as you want. When you are finished simply `CAS`
  the head pointer of the new tree with the existing one.

  For graph changes, create a new temporary node transaction, add both edges,
  then commit. Cleanup involves updating the original structure after the 
  commit or after another thread performs a read.

  If there are two transactions going on at once, if a second transaction
  comes along and sees another node is already involved in the first
  transaction, it can `CAS` swap the first transaction to cancelled and
  then remove its reference to the node question. When the second transaction
  comes back and tries to CAS update its transaction to complete, it will
  fail and have to start over with a new state of the world.
 
* **Performance**

  To keep performance, use structure sharing of immutable structures to
  avoid copying large portions of a structure. So maximize immutability!
  If a value is not under contention, we don't have to use `CAS`. We
  can also use the garbage collector to clean up after rollback and success
  instead of having to write the values ourselfs after transactions.

  If a node is a single point (say a tree head), then we need to distribute
  the heat across the keys (load balancing). We can do this by creating a new
  parent node which points to immutable child trees. Hosts can then balance
  on the sub-tree keys instead of the main root nodea (host-a handles left,
  host-b handles right). This can continue down the tree to scale.

--------------------------------------------------------------------------------
Datastructures
--------------------------------------------------------------------------------

How can we create a stack:

.. code-block:: python

    // ------------------------------------------------------------
    // To add a value to the stack, we add it and point
    // to the first node value. We then change the head
    // pointer to point to the new value (two steps):
    //     stack -> a
    //         b -> a
    //     stack -> b -> a
    // ------------------------------------------------------------

    stack = new Stack() // stack -> k:node0
    stack.push("a")     // node0 -> v:"a", k:node1
    stack.push("b")     // node1 -> v:"b"

How can we create a tree:

.. code-block:: python

    // ------------------------------------------------------------
    // To add a value to the tree, we add the new node pointing to
    // nothing. Then as long as we do not have to rebalance, we
    // simply change the pointer (left or right) of the node where
    // this should be inserted at:
    //     tree -> a -> None
    //        b
    //     tree -> a -> b
    // ------------------------------------------------------------

    stack = new Tree()  // tree  -> K:node0
    stack.push(5)       // node0 -> V:5, L:node1, R:node2
    stack.push(2)       // node1 -> V:2
    stack.push(7)       // node2 -> V:7

How can we create an undirected graph:

.. code-block:: python

    // ------------------------------------------------------------
    // We make this an undirected graph such that all edges between
    // two nodes are added as edges in the edge list of both nodes.
    // ------------------------------------------------------------

    stack = new Graph()  // node-a -> E:[b, c]
    stack.link("a", "b") // node-b -> E:[a]
    stack.link("a", "c") // node-c -> E:[a]

================================================================================
Amazon Instant Video
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Codecs are a compressor / decompressor (like gzip) which convert pixel values
into the frequency domain. It can roughly be thought of one big FFT:

* sharp edges get converted to high frequencies
* a flat region is converted to low frequencies
* heavy use of interframe prediction to take advantage of redundancy

Movies are a collection of Group Of Pictures (GOP). GOPs are a collection of
frames that are composed of the following frame types:

* **I** - Self contained (intra coded); largest
* **P** - Predicted frames; reference previous I or P frames
* **B** - BiDirectional reference frames, reference prior or future I or P frames
* **b** - non reference B frames - reference prior or future I, P, or B frames

Classic streaming of movies attempted to make the internet work like television:

* assumed multicast was available; tuned over UDP and fallback to custom TCP
* HTTP was the worst case fallback protocol
* streaming logic was shared between the server and the client (heavy on server)
* this made scaling horrible; no proxy or load balancing
* bitrates switch down with congestion, but not back up
* stateful protocol represented as a stream of packets
* customers could play, pause, etc (state on the server)

This didn't work well at all, so now we tried *Adaptive Streaming* which attempted
to make TV work like the internet:

* small HTTP requests that fit into the edge caches (globally unique fragments)
* each HTTP request was one fragment containing a GOP
* bitrate switches happen between fragments (choose the next one we should get)
* all logic is on the client, the server just sends fragments
* bitrate is measured via size and download time of each request
* every fragment download allows us to adjust the bitrate we need in real time

Current AIV settings:

* H.264 encoded with Harmonic ProMedia Carbon - behind the state of the art
* Microsoft Smooth Streaming - not written with networking in mind
* Constant Bitrate (CBR) encoding - wastes a lot of unneccessary bits
* Fixed 2 second GOP and fragment size - wastes a lot of space on I frames
* 150 - 10,000 Kbps - fixed GOP causes keyframe strobing
* up to 1980x1080 (1080p)
* up to 30 fps (24 fps is common)

Future AIV settings:

* x264 encoding (format is H.264); tuned by video quality focused pirates
* variable chunk size - aligned with biggest scene change (2.5s - 5s)
* capped VBR - specify max bitrate and visual quality; use only needed bits
* anamorphic encoding - not all pixels are square
* enhanced encoding heuristics
  - time to first byte and time to last byte (get bandwidth and latency)
  - calculate latency and bandwidth seperately
  - concurrent downloads (download with current latency before finished)
  - can log quality and max bitrate for GOP
  - Rate Distortion Optimization (RDO) problem (minimize rsme)
* support for HEVC
  - 25% slower to decode (is more parallizable / GPU)
  - much slower to encode (can move to hardware asic)
  - hierarchical quad tree with varying block size
  - asymetric partitions


================================================================================
Amazon Datastore Tradeoffs
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

When scaling to reach a specified SLA, first make stateless layers redundant, but
if the weakest point is less than that SLA, you can never make to total SLA unless
you scale the weakest point. This leads to CAP (each point is a range, not boolean).

The tradeoff between each point in CAP can be different for different services /
components, different workloads, or event different entities! In choosing a
datastore, these tradeoffs need to be evaluated to select the best data store
for that workload:

* the velocity of requests coming in
* the average item size (volume)
* the ratio of writes vs reads for the workflow
* the data types (structure / schema) (variety)
* the volume of data on the store (horizontal scaling)
* the cost of using the datastore (use the storage calculator)
* the temperatue of the data:

  - hot (active real time data)

    * volume in MB or GB, item size of  B to KB
    * latency in milliseconds
    * low to high durability
    * very high request rate
    * $1.00 - $10.0 per GB

  - warm (accessed regularly in soft time)

    * volume in GB or TB, item size of KB to MB
    * latency in milliseconds or seconds
    * high durability
    * high request rate
    * $0.10 - $1.00 per GB

  - cold (archived low use data)

    * volume in TB or PB, item size of KB to TB
    * latency in minutes or hours
    * very high durability
    * low request rate
    * $0.01 per GB

The temperature can be though of as how often the data is accessed, how recent
it is, and how soon it is needed.

--------------------------------------------------------------------------------
Database Choices
--------------------------------------------------------------------------------

Amazon has created a number of datastores to handle different collections of
the above tradeoffs which can be tuned for different workloads:

* **Amazon EMR**
  
  - 100s of petabytes of storage volume (dynamodb or hdfs)
  - data is cold to warm
  - low velocity of reads / writes
  - optional schema on read (mapreduce = no, hive = yes)

* **Amazon Redshift**

  - low petabytes of storage volume
  - data is cold to warm
  - low velocity of reads / writes
  - low data variety (strong schema)

* **Amazon S3**

  - virtulally unlimited storage volume
  - data is cold to warm depending on use case
  - medium/high velocity of reads / writes
  - high data variety (key / value)

* **Amazon Elasticache**

  - 100s of gigabytes of storage volume (in memory)
  - is used only for hot data (expensive in memory)
  - very high velocity of reads / writes
  - high data variety (key / value)

* **Amazon Kinesis**

  - low 10s of terabytes of storage volume (how much per 24 hours)
  - is used only for hot data (data only held for 24 hours)
  - very high velocity of writes
  - high data variety (key / value)

* **Amazon SimpleDb**

  - 10 gigabytes per domain (250 max)
  - data is hot or warm depending on the use case
  - very high velocity of reads depending on consistency
  - high data variety (primary key required, rest is column store)

* **Amazon DynamoDb**

  - virtulally unlimited storage volume (but slower partitions)
  - data is hot or warm depending on the use case
  - very high velocity of reads depending on consistency
  - medium data variety (some schema required hash / range keys)

* **Amazon RDS**

  - 3 terabytes of storage volume
  - data is warm
  - medium velocity of reads / writes
  - low data variety (strong schema)

* **Amazon Glacier**

  - virtulally unlimited storage volume
  - data is mostly cold storage
  - very low velocity of reads / writes (but high volume write)
  - high data variety (key / value)

* **Amazon Cloudsearch**

  - 100s of gigabytes of storage volume (in memory)
  - data is warm
  - medium velocity of reads / writes
  - medium data variety (some schema required search keys)

* **Amazon Cloudfront**

  - virtulally unlimited storage volume
  - data is warm to hot
  - very high velocity of reads
  - high data variety (key / value)

--------------------------------------------------------------------------------
Database Usage
--------------------------------------------------------------------------------

A single workload may need to use many different datastores for its workload.
Say a video upload and streaming service:

* the raw file is stored in S3
* some metadata is stored in dynamodb with a pointer to S3
* metadata needed for searching is stored in cloudsearch
* user permissions are stored in RDS
* hot files can be moved to cloudfront
* hot metadata can be moved to elasticache

When sharding a database to increase scale, one has a few options:

* federation - putting different data sets on different databases (orders, customers)
* partition  - split data based on a field (date, type)
* sharding   - split data based on a field range or hash (customers a-l, m-z)
* copying    - many read-only copies of the same data in different databases
* clustering - pieces of data split between many databases 


============================================================
Transaction on DynamoDB
============================================================

https://github.com/awslabs/dynamodb-transactions

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

============================================================
Dynamo: Amazon’s Highly Available Key-value Store 
============================================================

http://www.allthingsdistributed.com/2007/10/amazons_dynamo.html

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* DHTs
* consistent hashing
* versioning
* vector clocks
* quorum
* anti-entropy based recovery

============================================================
Searching Large Dynamic Datasets
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

============================================================
Taking Distributd Algorithms to Production
============================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

================================================================================
Dynamo Retrospective
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* let the smallest system control its rate

  Instead of having a large fleet that is polled on, instead create a smaller
  fleet that pushes its latest changes up the pipe to the frontend hosts. This
  lets the smaller fleet fully saturate the pipe instead of having to overload
  it and thus having to deal with retries, exponential backoff, etc.

.. code-block:: text

    database -> control plane -> alfbus -> front end caches

* colocate inverse workloads (reads / writes / store) and pass savings on to
  the customers.

* spread the load into segregated pods that will not affect other customers.

  You can also spread a customer to a fixed set of vips that segregat their
  load to individual cells. This allows customers to only take down a small
  amount of the total capacity.Can also add hooks to VPC endpoints (can spread on
  a per customer basis)

.. code-block:: text

    customer -> vip (proxy) -> vip -> frontend -> dataplane
    customer -> vip -> hub <- (token, endpoint)
             -> vip -> frontend -> dataplane


* don't throw away work

  If you hit a backing store that returns an error (say you pull an invalid key),
  don't throw away that error and instead _that_ can be cached if it is correct.

* do work proportional to the system
* watch for exponential backoff plateaus

  Make sure to chomp the delay at some point so you don't block a user for an hour.

* use shuffle sharding

  This allows for horizontal sharding while at the same time preventing a single
  customer from browning out a large number of hosts.

* beware of modal behaviour

  Eliminate it if possible (no caching) as you are usually just testing the 99%
  case and then the 1% will pop out and have problems. It is better to have consitent
  behaviour than behaviour that usually works.

  If it is too [slow / complex / etc] to [blank] when things are going well, why would
  it be ok to [blank] when things start going wrong? One solution to this is the chaos
  monkey philosophy so that rare paths are constantly exercised.

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* create tight low level APIs that can be scripted manually and then combine them
  into a workflow system for the public APIs.
* put all configuration in the control plane and push it in one blob (not brazil
  config / opconfig / etc).
