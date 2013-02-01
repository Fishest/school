============================================================ 
Paper Summaries
============================================================ 

A collection of summaries of the google papers value:
<http://research.google.com/pubs/papers.html>

------------------------------------------------------------
Dapper: Systems Tracing Infrastructure
------------------------------------------------------------

* opensource version is zookeeper
* pinpoint, magpie, and x-trace are similar systems
* requirements: ubiquitous deployment, continuous monitoring

  - monitoring should always be running
  - low overhead (low performance impact)(sampling)
  - application level transparency (programmer not aware)
  - scalability
  - data available for analysis quickly

* can make transparent by integrating into core libraries

  - threading, control flow, rpc, etc

* the total tracing packge has a few deliverables

  - code to collect traces
  - tools to visualize them
  - api to analyze large collections of traces

* black box based monitoring scheme

  - no additional tagging of data
  - infer relationships with statistical analysis

* annotation based

  - add extra annotations to make links explicit
  - say with global identifier tags
  - dapper uses trees, spans, and annotations

* the dapper trace tree

  - nodes are units of work (spans)
  - spans are log of start and end time of event, plus data
  - can add extra annotations to the span
  - take advantage of client/server ordering to fix clock skew
  - spans without a parent are root spans (say start of rpc)
  - span ids are probabilisticly unique 64 bit integers
  - edges are causual relationship b/t span and parent span

* arbitrary content is allowed to be traced

  - all traces are timestamped
  - can limit total logging with an upper bound (config)
  - also allow key/value traces for counters, binary messages, etc

* example of adding tracing to a trace::

    Tracer t = Tracer.getCurrentTracer();
    String request = ...;
    if (hitCache()) {
        t.record("cache hit for " + request);
    } else { t.record("cache miss for " + request); }

* the following describes the tracing pipeline:

 - span data is writting to local log files
 - a dapper daemon pulls data from log files
 - daemon pushes data to a dapper collector
 - dapper collector stores a trace as a row in bigtable
 - columns are spans (bigtable sparse table's helps here)
 - total median time is less than 15 seconds
 - dapper provides a simple api to read this data
 - data is traced and collected out of band (not with request)

* logging can be turned on and off dynamicaly
* annotations usage:

  - distributed debug log file
  - log bigtable requests with table being accessed
  - custom information near frontend
  - opt in security model (very few services don't trace)

* performance of the system

  - most expensive operation is writing to log file
  - is async and batches many writes at once
  - creating root span is expensive because of the guid
  - collector is running at lowest priority
  - 0.01% of network load and 1% of cpu load
  - for high performance machines, sampling is neccessary
  - generally 1/1024 uniform fx for 10,000 rps
  - low frequency services cana manually adjust sampling fx
  - sample every request for 12 rps
  - can the system manually adapt to the service usage
  - record this dynamic fx with the trace

* secondary filtering of data at collector

  - hash global trace id (all spans have this to 0 < z < 1
  - can set a global configuration value of the logging level
  - if less than global value, drop, otherwise log

* dapper api supplies the following:

  - retrieve trace by id
  - map/reduce on key of trace id
  - indexes to common values (service, host, timestamp)

* other monitoring services used

  - dapper real time metrics
  - centralized logging
  - centralized exception monitoring (metadata included with dapper)

* advanced uses of dapper

  - qa functional testing (fingerprinting)
  - debugging critical paths
  - dependency tracing and mapping (between clusters)
  - link with logs to find expensive queries
  - showing current most active network endpoints
  - can communicate directly with collectors for realtime data
  - useful in firefighting situations
  - service security accounting and rpc patterns checker
  - open api allowed new use cases to be created
  - how to add kernel tracing parameters to traces

* **adaptive sampling** - 1 request out of 1000 to be sampled
  gives correct data

------------------------------------------------------------
Chubby: 
------------------------------------------------------------

* opensource version is zookeeper
* purpose of the lock service is to allow clients to

  - synchronize thier activities
  - agree on basic information about their environment
  - reliability and availability were first concerns
  - performance was secondary

* interface is similar to a simple file system
* initial goal was for leader election (GFS, bigtable, etc)

  - distributed consensus problem (paxos)(synced clocks)
  - allow clients to find master
  - allow master to find servers it controls
  - store small amounts of metadata
  - use as distributed work lock

* lock service vs a paxos client library

  - service is easier to add after the fact
  - simpler to participate in service consensus
  - consistent client caching vs time based caching
  - has a similar feel to traditional locks
  - lock service needs 3 servers for consensus and 5 to be safe
  - client only needs one server for consensus

* intended for coarse (long held) locks instead of fine grained.

  - have event notification system for watching changes
  - can create fine grain locks with monotonic counters

* architecture is rpc server and client library

  - all communication is through client library
  - servers are organized into cells of 5 replicas
  - each cell votes for a master that does all reading/writing
    * election generally takes a few seconds
  - gurantees that a new master will not be elected for some time
  - replicas just copy the updates from the master (simple database)
  - replicas are also used to vote for consensus
  - clients find the master via dns query for replicas
  - replicas return current master identity
  - client directs all requests to master until

    * it fails to respond in a timely fashion
	* it indicates that a new master has been elected

  - database writes are distributed by the consensus protocal
  - data is written when a consensus is reached
  - database reads are only served by the master
  - when a replica fails and does not recover say in a few hours

    * a simple replacement process is started
    * the old machine is stopped and a fresh machine is started
	* the machine starts a new chubby binary
	* the server updates the dns tables (replaces old replica)
	* the current master polls the dns periodically
	* it notices the address change and updates its cells
	* the list is propigated to the other replicas
	* the new replica syncs its database to on file backups
	* finishes updates with active updates from replicas
	* once it has processed a master commit request, it can vote

* The data is a simple unix style file system interface

  - /ls/cellname/path/value (root is always ls)
  - the cellname is resolved to a chubby server via dns
  - local indicates that the local chubby cell should be used
  - no semantics to move files, modified times, or links
  - file only acls, no path dependent semantics
  - file/directory is known as nodes

* nodes can be permanent or ephemeral

  - nodes can be deleted explicitly
  - nodes are auto deleted if ephemeral and no client has them open
  - can be used as temporary files to indicate a client is alive
  - can be used for reader/writer locks

* there is various meta-data attached to the file

  - three acl lists: read, write, acl control
  - unless overwritten, inherits from parent
  - acls are stored as files in another directory (other services can use)
  - also includes four monotonically increasing 64 bit numbers
  - instance, content generation, lock generation, and acl generation number
  - also includes a 64 bit file-content checksum

* file handles are created by client and include:

  - check digits, sequence number, and mode information

* Files and directories can function as reader writer locks:

  - one client holds one in writier mode
  - many clients hold the lock in reader mode
  - can specify a lock delay to deal with faulty held locks (deadlock)
  - can create a sequencer that describes a held lock (like a token)
  - other services can validate that the sequencer is still valid

* Clients can register for chubby events via the library:

  - file contents modified (monitor service registered location)
  - child node added, removed, or modified (implement mirroring)
  - chubby master failover
  - a handle and its lock have become invalid
  - lock acquired (primary election)(usually followed by file modified event)
  - conflicting lock requests (caching of locks)
  - events are sent only after the event has taken place
    * user is guranteed to see result of operation

* The client library exposes the following API:

  - open() / close() - standard unix file handling
  - Poison() - allow the client to virtually operate (no data is sent)
  - GetContentsAndStat() - returns contents and metadata of a file
  - SetContents() - change the contents of a file
  - GetStat() - returns the metadata of a file
  - ReadDir() - returns the names and metadata of directory children
  - GetSequencer() - returns a sequencer that describes a lock handle
  - SetSequencer() - associates a sequncer with a handle
  - CheckSequencer() - check if a sequencer is still valid
  - SetACL() - changes ACLs on a file

* What follows is a leader election process:

  1. All potential primaries open the specified lock file
  2. They all attempt to aquire the lock, only one succeeds
  3. It becomes the primaries, the rest become replicas
  4. Primary writes its identity to the lock file (SetContents)
  5. Replicas read this with GetContentsAndStat (file modification event)
  6. Primary obtains a sequencer (GetSequencer)
  7. Communicates with servers with new token, they check with CheckSequencer

* To stay performant, chubby clients keep a write through cache in memory

  - of file data and fiel metadata
  - master sends file change events to clients who may be caching data
  - they flush the cache and respond with an ack (sits on keep alive rpc)
  - don't have to update (inefficient), just invalidate the cache
  - can also cache locks and file handles (if they can be reused)

* Cubby client sessions are maintained by a keep alive system:

  - engages in periodic keep alive handshakes
  - handles, locks, and cached data all remain valid while session is valid
  - session is automatically acquired on connetion
  - is terminated on close() or session idle (no handles and no work in a minute)
  - master promises a lease timeout interval (will not go into past, but may go into future)
  - client extends the timeout with a keep alive request
  - keep alive also contains events and cache invalidations (piggyback)
  - if potentially expired, enters jeopardy period (allowed a 4s grace keep alive)
  - result is either safe (session valid) or expired (session timed out)
  - jeopardy, safe, and expired are events that the library informs of

* used Berkeley DB, but later wrote their own to simplify needs and get tested record logs

  - every hour, the chubby master writes a snapshot of its db to GFS (in rotating buildings)

* Google uses a number of techniques to scale the chubby cluster

  - one master per 1000 machines
  - increase timeouts if under heavy load (less keep alive requests)
  - clients cache any data they can (a read is a cache miss)
  - protocol conversion servers to reduce protocol complexity:

    * one for java client -> chubbly client 
	* one to convert chubby dns requests

  - trusted proxy server to a chubby cell (consume keep alive traffic 93%)
  - partition data based on the cell
  - chubby data fits in system ram
  - store session in database on first write, not on connection
  - make open lightweight (cache open handle)
  - maximum size 256kb per file

* primary uses:

  - most popular was as a name server

------------------------------------------------------------
Tenzing: Sql on Mapreduce
------------------------------------------------------------

* opensource version is hive
* can query row stores, column stores, bigtable, GFS
* also text and pbuffers with sql exensions
* tenzing has four major components:

- worker pool

  These processes are constantly running services that take
  a query execution plan and executes the equivalent
  mapreduce. These consist of master and worker nodes and an
  overall gatekeeper called the master watcher.

  The workers manipulate the data for the tables in the
  metadata layer. Tenzing is a heterogeneous system allowing
  the backend to be a mix of: columnIO, bigtable, GFS files,
  mysql, etc.

- query server

  This is the gateway between the client and the worker pools.
  It parses the query, applies optimizations, and sends the
  plan to the master for execution.

- client interfaces

  There are several interfaces into tenzing incluing a cli,
  and a web UI. The cli allows advanced scripting. The web
  UI has query, table browsers, syntax highlighting and is
  geared toward novice users.

  There is also an API and a standalone binary that launches
  its own map-reduce jobs (no tenzing service needed).

- metadata server

  This provides an API to store and fetch metadata such as
  table names, schemas, pointers to underlying data, acls.
  Bigtable is used as the persistent backing store.

A typical Tenzing query goes through the following steps:

1. A user (or another process) submits the query to the
   query server through the Web UI, CLI or API.
2. The query server parses the query into an intermediate
   parse tree.
3. The query server fetches the required metadata from
   the metadata server to create a more complete
   intermediate format.
4. The optimizer goes through the intermediate format
   and applies various optimizations.
5. The optimized execution plan consists of one or more
   MapReduces. For each MapReduce, the query server finds
   an available master using the master watcher and
   submits the query to it. At this stage, the execution
   has been physically partitioned into multiple units of
   work(i.e. shards).
6. Idle workers poll the masters for available work.
   Reduce workers write their results to an intermediate
   storage.
7. The query server monitors the intermediate area for
   results being created and gathers them as they arrive.
   The results are then streamed to the upstream client.

* supports all major SQL92 and some SQL99 constructs
* also embeds the sawzall language for advanced usage

  - other languages like lua and R can easily be added

* hash table based aggregation rdbms (hash key is group by)
* joins search for best table to pull in memory (if able)

  - otherwise reverert to a serialized disk scheme
  - apply filters before load, to reduce rows
  - only load columns that are needed
  - create a single copy for multiple threads
  - join is cached to disk on the worker

* is not acid, but does allow isolation

  - inserts are batch appends
  - allows but does not enforce primary and foreign keys

* adapted mapreduce to use worker and master pooling

  - don't need to spin up new processes for each request
  - binaries are always loaded
  - tasks are processed froma fifo work queue
  - are working on priority queue
  - added network streaming between MR queries (no GFS)
  - colocate mapper/reducer to same process (save memory)
  - avoid compulsory sorting
  - if the dataset is small (<128 mb), it is done client side

------------------------------------------------------------
Dremel:
------------------------------------------------------------

------------------------------------------------------------
Pregel:
------------------------------------------------------------

------------------------------------------------------------
MapReduce
------------------------------------------------------------

* opensource version is hadoop

------------------------------------------------------------
Bigtable
------------------------------------------------------------

* opensource version is cassandra, HBase

------------------------------------------------------------
Sawzall
------------------------------------------------------------

* opensource is apache pig
* can we make awk distributed?
* find operations that are commutative and associative

  - order doesn't matter, can split work arbitrarily

* sawzall proccessing steps:

  - interpreter is started for each piece of data
  - each data record is operated on individually
  - output is primitive type or tuple of primitives types
  - this data is passed to aggregators
  - the aggregator output files are then collapsed to one file
  - smaller amount of machines run aggregators then sawzall

* depends on the following google infrastructure:

  - protocol buffers
  - gfs
  - workqueue (like condor)
  - mapreduce (sawzall is map phase, aggregate is reduce)

* language is type safe
* has code to parse various input formats
* aggregation is not allowed in the language

  - there are predefined aggregations allowed
  - collection -> `c: table collection of string;` 
  - sample -> `s: table sample(100) of string;` 
  - sum -> `s: table sum of { count: int, revenue: float };` 
  - maximum -> `s: table maximum(10) of string weight length:int;`
  - quantile -> `s: table quantile(101) of response_in_ms: int;`
  - top -> `s: table top(10) of language: string;`
  - unique -> `s: table unique(100) of string;`

* after validating, saw and dump programs are run

  - command line with flags
  - number of workqueue machines is determined from input/output

* sawzall is a conventional compiler written in c++

  - takes input source and compiles to byte code
  - byte code is then interpreted by same binary
  - starts one mapreduce job to get job parameters/info
  - second mapreduce job actually runs sawzall

* no memory between sawzall runs (arena memory)

  - only data that has been emitted is available
  - can create static instances that are shared (for init)
  - only value types, no references

* undefined values can be tested for with def(v)

  - can set a run time flag that causes undefined values to be skipped
  - these will be stored in a collected log
  - if the number of values in that log is low, computation will continue

* can define quantifiers of values

  - `when (i: some int; B(a[i])) function(i);`
  - `when (i: each int; j some int; query[i] == keywords[j]) emit keyword[j];`
  - also have some, each, all quantifiers

------------------------------------------------------------
 Thialfi
------------------------------------------------------------

------------------------------------------------------------
 FlumeJava
------------------------------------------------------------

--------------------------------------------------------------------------------
 Large Scale Distributed Deep Networks
--------------------------------------------------------------------------------

Increasing the scale of deep learning with respect to training examples and the
number of model parameters (or both) can drastically improve classification
accurracy. Using GPU's has shown great advances, however, the data must be
reduced to fit in the GPU memory (6GB):

* fine for smaller problems: acousting modeling for speech recognition
* bad for large number of examples and dimensions: high-resolution images

These problems can be solved with new software framework called `DistBelief` that
enables local machine parallelism (multithread) and distrubuted machines (message
passing):

* all communication, parallelism, and synchronization details handled by framework
* can use multiple replicas of a model to optimize a single objective (data parallelism)
* Downpour SGD (model replicas) and Sandblaster L-BFGS (distributed)
* with a modest cluster, can be faster than state of the art GPU

With larger datasets, the problem of scaling up SGD for convex problems become challenging:

* asynchronous SGD with lock-less parameter updates (Hogwild!)
* not know if this can easily be applied to non-convex problems with local minima
* cpu -> gpu conversion (Theano)
* create many small models on GPU farms and averaging their results
* MapReduce and GraphLap found insufficient (Mahout?)

DistBelief basically works as follows:

* Each node in the neural network has its computation defined
* The input data it needs is exposed via messaging (updard and downward)
* These can easily be partition arcross machines for large networks
* Speedups are great except for fully connected structure dominated by communication
* Slowest machine can be a bottleneck

Architecture of DistBelief:

* Downpour (online) and Sandblaster (batch)
* Both make use of a centralized shared parameter server to replicate models
* ameneable to variance in procesing speed and model failure (restarts of machines)
* test data is sharded into N replicas that are trained independently
* they use the parameter server to communicate updates
* at each round, each mini-batch pulls current parameters from server
* it runs its batch round using its shareded data
* it then sends its gradient to the server which applies it to the current parameters
* can reduce communication by only push/pulling updates every Npush or Nfetch steps.
* some stochasticity may be introduced
  - as gradients are updated on slightly old data
  - as a machine goes down and doesn't update its model
  - as parameter servers are slightly behind on updates
  - can be overcome with adagrad (seperate learning rate for each parameter):

    \eta_i,k \equiv \frac{\gamma}{\sqrt{\sum_{j=1}^k \Delta w_i,j^2}}
    \eta_i,k is the learning rate of the ith parameter at iteration k
    \Delta w_i,k is its gradient
    \gamma is the constant scaling fator for all learning rates
    \gamma is generally larger (order of magnitude) than largest rate without adagrad

* Sandblaster uses a coordination server that sends common math operation commands
  - dot product, scaling, vector addition, vector multiplication
* It sends these commands to independent parameter server shard to compute
* send 1/N of the computation to each shard
  - can send less to slower machines (that may bottleneck the total process)
  - can also send more to faster machines
  - runs multiple of the same computations at once, take the first to finish
* gets/sends parameter updates at lower frequency than Downpour


------------------------------------------------------------
 references
------------------------------------------------------------
A comparison of join algorithms for log processing in MapReduce.

