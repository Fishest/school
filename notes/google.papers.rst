================================================================================
Google Papers
================================================================================

A collection of summaries of some of the google papers:
<http://research.google.com/pubs/papers.html>

--------------------------------------------------------------------------------
Dapper: Systems Tracing Infrastructure
--------------------------------------------------------------------------------

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

* example of adding tracing to a trace:

.. code-block:: java

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

--------------------------------------------------------------------------------
Chubby: Discovery and Configuration Service
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------
Tenzing: Sql on Mapreduce
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------
Dremel: Realtime Hadoop Queries
--------------------------------------------------------------------------------

.. todo:: notes

Opensource versions of dremel are:

* Impala from Cloudera
* Drill from Apache
* Shark from AMP lab

--------------------------------------------------------------------------------
Pregel: Large Scale Graph Processing
--------------------------------------------------------------------------------

The opensource Apache version is Giraph.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In summary: programs are expressed as a sequnce of iterations in each of which
a vertex and receive messages sent in the previous iteration, send messages to
other vertices, and modify its own state and outgoing edges or mutate the graph
topology. This is all wrapped in an expressive API that hides the complexities
of being efficient, scalable, fault tolerant, message passing between nodes in
the cluster, etc.

Efficiently running various algorithms over graphs has the following problems:

* poor locality of memory access
* minimal work per vertex
* changing degree of parallelism
* distributing graph cliques to nodes in a cluster
* the size of a graph for a single node (BGL)

Pregel addresses this with the following programming model:

* computations consist of a number of iterations (supersteps)
* during each superstep, a user defined function is run on each vertex
* this function operates on a single vertex `V` and single superstep `S`
* the function can read messages sent to `V` at `S - 1`
* the function can send messages sent to any `V` at `S + 1` (usually neighbors)
* the function can modify the state of `V` and its outgoing edges
* the API is presented as synchronous so concurrency concerns are mitigated

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Programming Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

What follows is the c++ api:

.. code-block:: c++

    //
    // Users subclass the following type to implement a pregel program
    // by overriding the Compute method.
    //
    // Although apparently limiting, the types can be made more flexible
    // by using things like protocol buffers
    //
    template <typename VertexValue, typename EdgeValue, typename MessageValue>
    class Vertex {
      public:
        virtual void Compute(MessageIterator* msgs) = 0;
        const string& vertex_id() const;
        int64 superstep() const;
        const VertexValue& GetValue();
        VertexValue* MutableValue();
        OutEdgeIterator GetOutEdgeIterator();
        void SendMessageTo(const string& dest_vertex, const MessageValue& message);
        void VoteToHalt();
    };

The input is a directed graph where each vertex has a unique `vertex identifier`
combined with a user defined mutable value. The edges are associated with their
source and have target vertexes as well as a user defined mutable value. Edges
are not first class citizens and have no computation associated with them. The
algorithm terminates when every vertex votes to halt. This is modeled as a two
state machine:

* *active* - all vertexes start active and remain so while there is still work.
* *halted* - when there is no further work; can be made active by external work.

  - once halted, the vertex will not be included in future supersteps
  - receiving a message will awaken a node
  - after receiving a message, the vertex must explicitly halt again

The output is the set of values explicitly output by the vertices. This is usually
a graph representation that is isomorphic to the orignal graph, but not neccessarly
so. For example, a graph mining algorithm may output statistics or a clustering
algorithm may output the cliques.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Aggregators and Combiners
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To reduce the overhead of message passing, users can define `Combiners` to
aggregate a number of messages intended for a single vertex into one message. For
example, the total sum of values.

Pregel also supports `Aggregators` to allow all vertices to perform global
communication. At superstep `S` all verticies can emit a value, all of which get
reduced and made available to all vertices in superstep `S + 1`. This can be used
for statistics and a number of `Aggregators` are already defined: min, max, sum.
The aggregator can be used for coordination by making an `and` aggregator and
running until all the vertices meet some predicate condition.  The aggregator can
exist for a single superstep, or can be sticky and last for the entire process.

Pregel was designed for sparse graphs, so graphs with high fan-in and fan-out
will suffer performance degredation. This may be combated with aggregators.
Large graphs will spill to disk and they have not found a reliable way to
partition the graph.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mutations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Mutations to the graph are messages that are sent out in superstep `S` and
applied before superstep `S + 1`. Since there can be conflicts in the operations
the following process is used:

* edge deletes are processed before edge additions
* removing a vertex remotes all the out edges
* for multiple create operations for the same data, one is chosen at random
* unless a handler is supplied which can choose the correct one
* global mutation is synchronized by applying the entire batch at once
* local mutation is inherently safe

The graph storage is backed by simple reader and writer interfaces which make it
easy to create a graph from whatever format or backing store a user needs. There
are default implementations for text files, bigtable, GFS.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pregel runs on the google cluster which is simple x86 machines stored in racks
with high intra-bandwidth. Persistant data is stored in GFS or bigtable and
temporary data like buffered messages is stored on local disk. The chubby name
server is used to refer to cluster instances instead of physical machines.

The graph is partitioned based on the vertex id. This is simply based on using
a `hash(id) mod N` with the number of servers in the cluster. This way all
servers know which node a vertex is on. This distribution can be overloaded
depending on the use case (web search for example may put all pages for the
same domain on the same cluster).

The user program is then run on `N` machines in the cluster with one of them
running as the master. The workers use the name service to look up the master
and send registration messages. The master decides how many partitions the
graph should have and assigns one or more partitions to each worker. Each
worker is given the complete set of assignments for all workers so that
messages can be coordinated between workers.

The graph input is then assigned in chunks to all the workers who will:

1. update their datastructures if the vertex belongs to them
2. enqueue a message to another worker if it does not
3. after all verticies are read, they are marked as active

The master then instructs each worker to begin a superstep:

1. they read and apply their enqueued messages
2. iterate through each vertex in their partitions
3. enqueue any messages that need to be delivered
4. send their number of active verticies to the master and finish this step
5. this is repeated as long as vertices are active or messages are in transit

After the computation halts, the master may inform each worker to persist
its portion of the graph.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fault Tolerance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Fault tolerance is achieved through checkpointing. At the beginning of each
superstep, the master tells the workers to save the state of their partitions to
persistant storage: edge values, vertex values, incoming messages. The master
saves the aggregator values.

Worker failures are detected with regular ping messages. If a worker does not
receive a ping within a certain time limit, it kills itself. If a master does
not receive a response from a worker in a certain time limit, it marks the
worker as failed.

When a worker is marked as failed, its partition is rebalanced across the
cluster and they are informed to reload their entire state (including the 
new values) from persistant storage. This may be many steps before the current
superstep. The checkpointing frequency is balanced by a cost value.

There is work in progress to recompute the state by keeping a log of outgoing
messages so all the state can be rebuilt just for the lost partitions. Non
deterministic algorithms can be made deterministic by seeding the generator
based on the superstep.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Worker Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The worker maintains its graph in memory that can be represented as follows:

.. code-block:: scala

    case class EdgeState[E](source: VertexId, state: E)
    case class VertexState[V, E](state: V, edges, List[EdgeState[E]],
      messages: Queue[Message], is_active: Boolean)

    type VertexId = String
    type Graph[V, E] = Map[VertexId, VertexState[V, E]]

The general work of each superstep is as follows:

.. code-block:: scala

    val updates = for {
      id, vertex <- graph.items(),
      if vertex.is_active or !vertex.messages.empty
    } yield compute(vertex.state, vertex.edges, vertex.messages)

There are two copies of the `isActive` and `messages`: one for the current
superstep and one for receiving updates for the next superstep. While the
current superstep is being processed, another thread is receiving the updates
for the next superstep from other workers.

The update messages are sent based on locality. If the update is to a local
vertex, it is placed directly in the queue of the vertex. If the update is
for a remote vertex, the messages are buffered until they reach a certain
size and then a single message is sent asynchronously (buffer size).

If combiners are used, they are applied when they are added to the outgoing
message queue and when they are received at the incoming message queue (local
and remote).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Master Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The master is responsible for knowing all the workers, their partitions, and how
to contact them and manage work. Its data structure sizes are proportional to
the number of partitions, so it can scale to very large graphs with a single
host. Each worker is assigned a unique identifier at registration along with
addressing information.

The master basically works as a barrier between supersteps. It sends out `N`
superstep compute messages and then waits for `N` responses before moving to
the next superstep. If it fails to get `N` responses, it moves to recovery mode.

The master also maintains statitics about the processing that it displays via
an HTTP web service:

* progress of the computation
* the total size of the graph
* a histogram of its distribution of out degrees
* the number of active vertices
* the timing and message traffic of recent supersteps
* the values of user defined aggregators

Aggregators work by having each worker compute its local global value for the
current superstep. The workers then communicate to reduce the global value by
forming a tree and reducing. The global values are then computed and sent to
the master who distributes them to all workers at the next superstep.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **page rank**

.. code-block:: c++

    class PageRankVertex : public Vertex<double, void, double> {
      public:
        virtual void Compute(MessageIterator* msgs) {
            if (superstep() >= 1) {
                double sum = 0;
                for (; !msgs->Done(); msgs->Next())
                sum += msgs->Value();
                *MutableValue() = 0.15 / NumVertices() + 0.85 * sum; //* rst
            }

            // normally this would run until convergence using aggregators
            if (superstep() < 30) {
                const int64 n = GetOutEdgeIterator().size();
                SendMessageToAllNeighbors(GetValue() / n);
            } else {
                VoteToHalt();
            }
        }
    };

* **shortest paths**

.. code-block:: c++

    class ShortestPathVertex : public Vertex<int, int, int> {
      public:
        virtual void Compute(MessageIterator* msgs) {
            int mindist = IsSource(vertex_id()) ? 0 : INF;
            for (; !msgs->Done(); msgs->Next())
                mindist = min(mindist, msgs->Value());

            if (mindist < GetValue()) {
                *MutableValue() = mindist; //* rst
                OutEdgeIterator iter = GetOutEdgeIterator();
                for (; !iter.Done(); iter.Next())
                    SendMessageTo(iter.Target(), mindist + iter.GetValue());
            }
            VoteToHalt();
        }
    };

    // A combiner can reduce the network traffic substantially
    class MinIntCombiner : public Combiner<int> {
        virtual void Combine(MessageIterator* msgs) {
            int mindist = INF;
            for (; !msgs->Done(); msgs->Next())
                mindist = min(mindist, msgs->Value());
            Output("combined_source", mindist);
        }
    };

* **bipartite matching**

  The code is not included, but it uses `superstep mod 4` to drive a state
  machine with the following steps:

  0. all left verticies send a join message to all their edges and then halt

     - if it is already matched or has no edges, it will never restart
     - otherwise it will recieve a response and restart

  1. each right vertex randomly responds true to one of the messages

     - it then sends false to all the other messages
     - it then halts

  2. each left vertex randomly responds true to one of the messages

     - if it is already matched, it wouldn't have sent a message in state 0

  3. each right vertex updates its state with the accept messages and halts

  The vertex value is a tuple of two flags (is_left and is_right) as well as
  the name of its matched vertex once known. The edges have no value, and the
  messages are boolean.

* **semi-clustering**

  The input is a directed weighted graph with edges in both directions. This
  can represent a communication graph (users who communicate more have higher
  weights). This will return at most `C_max` clusters where a vertex can be
  in more than one cluster.

  Each vertex maintains a list of members in its cluster (max C_max) sorted by
  score. The list is initialized by the vertex assigning itself to the cluster
  with a score of 1. The remainder of the algorithm is as follows:

  * the vertex broadcasts a message to all its neighbors
  * vertex `V` iterates over the clusters `c_1 .. c_k` sent to it

    - if `V` is not in `c` and `V_c < C_max`, `V` adds itself to `c`
    - this forms `c*`

  * the semi clusters `c_1 .. c_k` `c*_1 .. c*_k` are sorted by their scores

    - the best clusters are sent to their neighbors
    - vertex `V` updates its list of semi-clusters with the ones it is in

  * the algorithm is terminated when the clusters stop changing or after `N` steps
  * the list of semi-clusters are reduced to the global list of best clusters

  A semi cluser `c` is assigned a score as follows:

.. code-block:: text

    S_c = (I_c - f_b * B_c) / (V_c * (V_c - 1) / 2)

    I_c = sum of the weihts of all internal edges
    B_c = the sum of the weights of all boundary edges
    V_c = the number of vertices in the semi-cluser
    f_b = the boundary edge score factor (supplied 0..1)

    The score is normalized by the number of edges in the clique
    V_c so large clusters do not dominate.

.. todo:: references
[45]  Leslie G. Valiant, A Bridging Model for Parallel Computation
[31] Challenges in Parallel Graph Processing
[37] delta stepping method

--------------------------------------------------------------------------------
MapReduce: Embarrissingly Parallel Framework
--------------------------------------------------------------------------------

.. todo:: notes
* opensource version is hadoop

--------------------------------------------------------------------------------
Bigtable: Infinitely Scalable Column Store
--------------------------------------------------------------------------------

.. todo:: notes
* opensource version is cassandra, HBase

--------------------------------------------------------------------------------
Sawzall: SQL Queries on Hadoop
--------------------------------------------------------------------------------

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

--------------------------------------------------------------------------------
Thialfi
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
FlumeJava: Large Scale Data Mover
--------------------------------------------------------------------------------

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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
DistBelief Architecture Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Each node in the neural network has its computation defined
* The input data it needs is exposed via messaging (updard and downward)
* These can easily be partition arcross machines for large networks
* Speedups are great except for fully connected structure dominated by communication
* Slowest machine can be a bottleneck

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Architecture of DistBelief:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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


--------------------------------------------------------------------------------
References
--------------------------------------------------------------------------------

A comparison of join algorithms for log processing in MapReduce.

--------------------------------------------------------------------------------
The Tail At Scale
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Component Variability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Limit queuing effects on the inner-most systems by keeping only a very small
queue of work to do. Otherwise, this will multiply throughout the system.
Furthermore, having a priority queue (interactive reqeusts vs background
reqeusts) can increase the performance of the system.

Large service requests can be broken into a number of smaller cheap requests
that can be interleaved and run concurrently. Time slicing can prevent a few
large requests from slowing down the execution of a large number of small
concurrent requests.

If you have large background tasks, break them into smaller more granular pieces,
throttle them, and run them during periods of lower overall load. It may be
usefull to synchronize such background activies across the fleet to create a quick
burst of activity across the fleet simultaneously (slowing down activity during
that period), otherwise all requests' tail is pushed out by constant background
activity.

Caching will not reduce the tail latency unless the cache configuration can
contain the entire working set of the application.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Within Request Short Term Adaptations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For within short term requets, a way to reduce the tail latency is to make the
initial request and then hedge a second request if the first request has not
returned in the 95th percentile expected latency. When the first of these
requests returns, cancel the other request. This will result in increasing the
overall load in the system by 5%.

Another way to perform this is to "tie" a request to another server. This works
by queueing a reqeust to two servers at once (as a hedge), but including in the
message the other server the request was sent to. Then the first server to
dequeue the request in question sends a cancellation message to the other server
to prevent it from doing the same work. This approach works better than random
queueing, examining the queue of the service (to put on the smallest queue), and
other techniques. In order to prevent the case where both servers pop the request
at the same time and send cancellation messages to each other (say when the queues
are empty), the client should introduce a small bit of random timeout between
sending the two messages; a small delay of two times the average network message
delay (1 ms in modern data centers).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Cross-Request Long-Term Adaptions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To combat imbalance, create a number of mircro partitions instead of large
partitions per server.  Google uses say 20 partitions per machine (much more
than the size of a single machine partition) which allows it to shed load in 5%
increments in 1/20th of the time. These are then dynamically assigned and load
balanced to specific servers.  Load balancing is then a matter of moving
responsibility of these partitions from one machine to another.

If the service can detect or predict a hot item, additional replicas of these
items can be created and stored in a number of partitions.  This way, load can
be balanced without having to move partitions around the system.

Finally, a system that is consistently perfoming slowly (say as it is constantly
overload) can be put on probation and not actively used until its situation
improves. The request server can then issue shadow requests behind the scenese
to collect updated statistics about the machine in probation until is situation
improves and it can be reincorperated.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Large Information Retrieval Systems
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Speed is a key quality metric in a large IR system, and as such it may be better
to return a response that is "good enough" instead of the best response. As such,
some systems may be able to be returned before all of the responses they issue
are returned if we can deem that it has taken too long and the result is "good
enough." This scheme can also be used to ignore nonessential subsystems to
improve responsiveness (ads, spelling correction).

If a system has a number of edge cases that have not been exercised, it may be a
good idea to send out a "canary request" to one system and wait to see if it
returns before fanning the request out among the fleet to prevent a DoS and to
provide an extra layer of robustness.

It may be appropriate to tolerate critical mutations of data as these generally
take less time to process then the related read requests (which need to perform
processing).  Also, most updates can be done off the critical path (async). Finally,
for systems that request consistent updates, the quorum based algorithms are
inherently tail tolerant as slow systems (2 out of 5) don't assist in the quorum.

--------------------------------------------------------------------------------
MillWheel
--------------------------------------------------------------------------------

http://research.google.com/pubs/pub41378.html

.. todo:: take notes

--------------------------------------------------------------------------------
BigTable
--------------------------------------------------------------------------------

http://research.google.com/archive/bigtable.html

--------------------------------------------------------------------------------
Spanner
--------------------------------------------------------------------------------

http://static.googleusercontent.com/external_content/untrusted_dlcp/research.google.com/en/us/archive/spanner-osdi2012.pdf

.. todo:: take notes
