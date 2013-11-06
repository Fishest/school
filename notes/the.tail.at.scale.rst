The Tail At Scale
-------------------------------------------------

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Component Variability
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Limit queuing effects on the inner-most systems by keeping
only a very small queue of work to do. Otherwise, this will
multiply throughout the system. Furthermore, having a priority
queue (interactive reqeusts vs background reqeusts) can increase
the performance of the system.

Large service requests can be broken into a number of smaller
cheap requests that can be interleaved and run concurrently. Time
slicing can prevent a few large requests from slowing down the
execution of a large number of small concurrent requests.

If you have large background tasks, break them into smaller
more granular pieces, throttle them, and run them during periods
of lower overall load.  It may be usefull to synchronize such
background activies across the fleet to create a quick burst
of activity across the fleet simultaneously (slowing down activity
during that period), otherwise all requests' tail is pushed out
by constant background activity.

Caching will not reduce the tail latency unless the
cache configuration can contain the entire working set
of the application.


^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Within Request Short Term Adaptations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For within short term requets, a way to reduce the tail
latency is to make the initial request and then hedge a
second request if the first request has not returned in
the 95th percentile expected latency. When the first of
these requests returns, cancel the other request. This
will result in increasing the overall load in the system
by 5%.

Another way to perform this is to "tie" a request to 
another server. This works by queueing a reqeust to two
servers at once (as a hedge), but including in the message
the other server the request was sent to.  Then the first
server to dequeue the request in question sends a cancellation
message to the other server to prevent it from doing the same
work.  This approach works better than random queueing, examining
the queue of the service (to put on the smallest queue), and
other techniques. In order to prevent the case where both
servers pop the request at the same time and send cancellation
messages to each other (say when the queues are empty), the
client should introduce a small bit of random timeout between
sending the two messages; a small delay of two times the average
network message delay (1 ms in modern data centers).

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Cross-Request Long-Term Adaptions
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To combat imbalance, create a number of mircro partitions instead
of large partitions per server.  Google uses say 20 partitions per
machine (much more than the size of a single machine partition) 
which allows it to shed load in 5% increments in 1/20th of 
the time. These are then dynamically assigned and load balanced to
specific servers.  Load balancing is then a matter of moving
responsibility of these partitions from one machine to another.

If the service can detect or predict a hot item, additional replicas
of these items can be created and stored in a number of partitions.
This way, load can be balanced without having to move partitions around
the system.

Finally, a system that is consistently perfoming slowly (say as it is
constantly overload) can be put on probation and not actively used until
its situation improves. The request server can then issue shadow requests
behind the scenese to collect updated statistics about the machine in
probation until is situation improves and it can be reincorperated.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Large Information Retrieval Systems
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Speed is a key quality metric in a large IR system, and as such it may
be better to return a response that is "good enough" instead of the best
response.  As such, some systems may be able to be returned before all of
the responses they issue are returned if we can deem that it has taken too
long and the result is "good enough." This scheme can also be used to ignore
nonessential subsystems to improve responsiveness (ads, spelling correction).

If a system has a number of edge cases that have not been exercised, it may
be a good idea to send out a "canary request" to one system and wait to see
if it returns before fanning the request out among the fleet to prevent a DoS
and to provide an extra layer of robustness.

It may be appropriate to tolerate critical mutations of data as these generally
take less time to process then the related read requests (which need to perform
processing).  Also, most updates can be done off the critical path (async). Finally,
for systems that request consistent updates, the quorum based algorithms are
inherently tail tolerant as slow systems (2 out of 5) don't assist in the quorum.
