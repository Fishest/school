================================================================================
Linkedin Papers
================================================================================

http://linkedin.github.io/

--------------------------------------------------------------------------------
Linkedin Distributed Log Summary
--------------------------------------------------------------------------------

http://engineering.linkedin.com/distributed-systems/log-what-every-software-engineer-should-know-about-real-time-datas-unifying

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At the core of every distributed system is a log (transaction, commit, event-
source, write-ahead, etc). A log is an append only totally-ordered sequence of
records ordered by time. Records are appended to the right and reads happen
from left to right. Each entry is given a unique sequential log entry number.

The ordering of the records defines a notion of "time" as entries to the left
are older than entires to the right. The log entry number is essentially a
timestamp that is decoupled from a physical clock.

Except for application logic, the content of the log entries is not important.
The log was originally created to atomically sync the data on database servers
before updating the system data structures. This log was then able to be used
to synchronize slave replicas and push a stream of updates to third parties.

The guiding architecture of a distributed log system is the replicated state
machine: if two identical deterministic processes begin in the same state and
apply the same updates in the same order, they must be in the same end state.
The replicas can then be described with a single number: the maximum log
entry number it has seen.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
System Integration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tables support data at rest and logs capture changes. The log is a complete log
of the changes so one can create the final version or any preceding version as 
well. It can be thought of as a backup of every previous state of the table.
Also, the log can be used to realize any number of representations. At the core
of the distributed system problem is the ability to have many machines playback
history at their own rate in a deterministic manner:

* a failed system can catch back up when it restarts
* real time systems can read log events as fast a possible
* data warehouses can batch in writes every hour or so

You can think of the log as acting as a kind of messaging system with durability
guarantees and strong ordering semantics; generally known as atomic broadcast.
The great thing about having a centralized log is that it becomes the point of
integration for producing and sourcing data. All systems simply have to write
code to connect to one system instead of N. Furthermore, the log affords one
the ability to transform the data in three places:

* by the data producer prior to adding the data to the company wide log

  - this is the best option as the data producer knows the data best
  - this should remove all vestigual artifacts from the parent system
  - this transform should be lossless and reversible

* as a real-time transformation on the log (which in turn produces a new, transformed log)

  - this is the best option if some value added processing needs to be done
  - adding session data or derived data fields for example

* as part of the load process into some destination data system

  - only aggretation that the final system needs should be done here
  - usually this is just schema -> schema transformation

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scalability
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Linkedin used a few tricks in Kafka to support a large scale system:

* partitioning the log
* optimizing throughput by batching reads and writes
* avoiding needless data copies

Each partition is a totally ordered log, but there is no global ordering between
partitions (except some wall clock time that may be in the messages). The write
to each partition is controlled by the users and is generally based on hashing
a record key. Partitioning allows log appends to occur without co-ordination
between shards and allows the throughput of the system to scale linearly with the
cluster size.

Each partition is replicated across a configurable number of replicas, each of
which has an identical copy of the partition's log. At any time, a single one of
them will act as the leader; if the leader fails, one of the replicas will take
over as leader.

A log, like a filesystem, is easy to optimize for linear read and write patterns.
The log groups small reads and writes together into larger, high-throughput
operations. Batching occurs from client to server when sending data, in writes to
disk, in replication between servers, in data transfer to consumers, and in
acknowledging committed data.

Finally, Kafka uses a simple binary format that is maintained between in-memory
log, on-disk log, and in network data transfers. This allows them to make use of
numerous optimizations including zero-copy data transfer.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
State
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The article makes mention that their is a duality between a log and a table. As
such, a log stream can be realized in a local table (database) in order to keep
state. This state can then be produced as a changelog.

It may be unweildy to keep the log records forever. In this case, it may be
neccessary to compact the log over time. For event data, a window can be defined
that will simply dump records after they exit the time window. For keyed data,
only the most recent value update can be kept, thus keeping the current value
of the key.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Use Cases
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The article mentions the following use cases for a distributed log:

* handle data consistency by sequencing concurrent updates to nodes
* provide data replication between nodes
* provide commit semantics to the writer (the record was saved to disk)
* provide the external data subscription feed from the system
* provide the capability to restore failed replicas or bootstrap new replicas
* handle rebalancing of data between nodes

.. todo:: read the supplied links

http://cs.brown.edu/research/aurora/hwang.icde05.ha.pdf
http://cs.brown.edu/research/aurora/vldb03_journal.pdf
http://data.linkedin.com/blog/2009/06/building-a-terabyte-scale-data-cycle-at-linkedin-with-hadoop-and-project-voldemort
http://data.linkedin.com/projects/search
http://db.cs.berkeley.edu/papers/cidr03-tcq.pdf
http://docs.hortonworks.com/HDPDocuments/HDP2/HDP-2.0.0.2/ds_Hive/orcfile.html
http://engineering.linkedin.com/52/autometrics-self-service-metrics-collection
http://engineering.linkedin.com/real-time-distributed-graph/using-set-cover-algorithm-optimize-query-latency-large-scale-distributed
http://parquet.incubator.apache.org/
http://project-voldemort.com/
http://www.quora.com/LinkedIn-Recommendations/How-does-LinkedIns-recommendation-system-work
http://www.teradata.com/
https://highlyscalable.wordpress.com/2013/08/20/in-stream-big-data-processing/
https://www.ibm.com/developerworks/library/j-zerocopy/
http://www.cs.berkeley.edu/~matei/papers/2012/hotcloud_spark_streaming.pdf
http://research.microsoft.com/apps/pubs/?id=201100
http://infolab.usc.edu/csci599/Fall2002/paper/DML2_streams-issues.pdf
http://www.amazon.com/Replication-Practice-Lecture-Computer-Theoretical/dp/3642112935
http://arxiv.org/abs/1309.5671
http://www.mpi-sws.org/~druschel/courses/ds/papers/cooper-pnuts.pdf
http://www.cs.utexas.edu/~lorenzo/papers/SurveyFinal.pdf
http://www.cs.cornell.edu/fbs/publications/smsurvey.pdf
http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.20.5896

--------------------------------------------------------------------------------
Kafka Distributed Log
--------------------------------------------------------------------------------

http://kafka.apache.org/
http://kafka.apache.org/documentation.html#design
http://sites.computer.org/debull/A12june/pipeline.pdf

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Samza
--------------------------------------------------------------------------------

http://samza.apache.org/learn/documentation/latest/
http://samza.apache.org/learn/documentation/latest/introduction/background.html
http://engineering.linkedin.com/samza/apache-samza-linkedin%E2%80%99s-stream-processing-engine
https://engineering.linkedin.com/data-streams/apache-samza-linkedins-real-time-stream-processing-framework
http://samza.apache.org/learn/documentation/0.7.0/container/state-management.html

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Espresso
--------------------------------------------------------------------------------

http://dl.acm.org/citation.cfm?id=2465298
http://www.slideshare.net/amywtang/li-espresso-sigmodtalk
http://data.linkedin.com/projects/espresso
http://engineering.linkedin.com/espresso/introducing-espresso-linkedins-hot-new-distributed-document-store

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Databus
--------------------------------------------------------------------------------

https://github.com/linkedin/databus

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Datafu
--------------------------------------------------------------------------------

https://github.com/linkedin/datafu
http://engineering.linkedin.com/datafu/datafus-hourglass-incremental-data-processing-hadoop

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Norbert
--------------------------------------------------------------------------------

https://github.com/rhavyn/norbert

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Azkaban
--------------------------------------------------------------------------------

http://azkaban.github.io/azkaban/docs/2.5/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this

--------------------------------------------------------------------------------
Voldermort
--------------------------------------------------------------------------------

http://www.project-voldemort.com/voldemort/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: notes on this
