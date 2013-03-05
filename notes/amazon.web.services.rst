================================================================================
Amazon Web Services (AWS)
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------
The currently available services supplied by AWS are as follows:

* **Computing**

  - Elastic Compute Cloud (EC2)
  - Elastic Map Reduce (EMR)
  - AutoScaling
  - Elastic Load Balancing
  - Amazon Mechanical Turk

* **Networking**

  - AWS Direct Connect
  - Amazon Route 53
  - Amazon VPC

* **Database**

  - Amazon DynamoDB
  - Amazon RDS
  - Amazon Redshift
  - Amazon ElastiCache
  - Amazon SimpleDB

* **Storage**

  - Amazon Simple Storage Service (S3)
  - Amazon Glacier
  - Amazon CloudFront
  - AWS Storage Gateway
  - AWS ElastiCache

* **Management**

  - AWS Elastic Beanstalk
  - AWS CloudFormation
  - Amazon CloudWatch
  - AWS Data Pipeline
  - AWS Identity and Access Management
  - AWS OpsWorks

* **Application Services**

  - Amazon Elastic Transcoder
  - Amazon Simple Queue Service (SQS)
  - Amazon Simple Notification Service (SNS)
  - Amazon Simple Email Service (SES)
  - Amazon Simple Workflow Service (SWF)
  - Amazon CloudSearch

--------------------------------------------------------------------------------
Libraries
--------------------------------------------------------------------------------

The following are mature libraries that can be used with various languages:

* `bash`: https://github.com/aws/aws-cli
* `java`: https://github.com/aws/aws-sdk-java
* `javascript`: https://github.com/aws/aws-sdk-js
* `.net`: https://github.com/aws/aws-sdk-net
* `python`: https://github.com/boto/boto
* `ruby`: https://github.com/aws/aws-sdk-ruby

--------------------------------------------------------------------------------
Amazon DynamoDB
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dynamo is a NoSql database that shards its data over a number of hosts running
SSDS to meet the requested capacity required by the use case. The size of each
database are virtually limitless and the data is automatically replicated
across different availability zones in a region to provide built in high
availability and data durability.

You can scale up or down your request capacity for any table without downtime or
performance degredation. It supports:

* Atomic counters and strong read consistency
* Schemaless database design with rich data model
* Integration with EMR

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Data Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In DynamoDB, the database is defined as follows:

1. Database is a collection of tables
2. Table is a collection of items
3. Item is a collection of attributes

There is a size limit of 64KB on each item size, but other than that each item
can have any number of fields. The only thing that must remain constant are the
keys (primary and range). Each attribute on an item is a key value pair. Empty
or null string attribute values are not allowed.

There are two types of keys that can be used in a table:

1. `Hash Type Primary Key` which dynamo builds an unorderd hash index on
2. `Hash and Range Primary Key` which dynamo builds an unordered hash index on
   the first key and a sorted range index on the secondary key.

Dynamo also sorts a number of data types:

* `scalars`: Number, String, and Binary
* `collections`: String Set, Number Set, Binary Set

.. note:: Sets are not ordered and empty sets are not allowed

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Operations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of different operations supported in the dynamo API:

* `Table Operations`: create, update, and retrieve table information
* `Item Operations`: add, update, and delete items from a table
* `Single or Multiple Items`: get(1..N) items, or query many tables in batch
* `Query And Scan Operations`: get items by keys or perform a table scan
* `Filtered Query`: can apply filters to query and scan operations

You can also request that operations occur in two forms of consistency:

* `Eventually Consistent Read` data may be out of date, but will be consistent
* `Consistent Read` dynamo waits until quorum before returning data

Can also perform conditional writes to ensure two concurrent clients don't stomp
each others updates. You supply a condition that must be met on the current data,
otherwise, the write results in an error and will not be persisted (it must be
retried).

--------------------------------------------------------------------------------
Amazon Simple Queue Service (SQS)
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SQS offeres reliable and scalable hosted queues for storing messages:

+ Stored in fail-safe queues
+ Ensures delivery at least once:

  However, if a server fails, it may deliver the same message
  again, so it is up to the application to be idempotent with regards
  to each message. This is because a copy of the message is stored on
  multiple servers for redundancy.

+ Supports multiple readers/writers on same queue
+ Redundant infrastructure
+ Configurable settings per queue
+ Batch operations for most methods
+ Variable message size (max of 64 kb):

  For larger messages, srot them in S3 or SimpleDB and send the
  URI of the resource as the message.

+ ACLs on the queue (who can send and who can receive):

  This is implemented in the `Aspen` library which directly queries
  and sets data in the metadata service.

+ Delay queues are supported (delay before visible to retrieve):

  For individual messages, use MessageTimers on the message

- Does not guarantee FIFO message delivery (best effort):

  Ideally message order should not matter as messages should stand on
  their own, however, if order is needed, sequencing information can be 
  included in the messages and order can be dealt with on the application
  side.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Operation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before a queue can be used, it much be named (store this name and do not rebuild
it each time)::

    http://<aws-region>.amazonaws.com/<aws-account>/<queue-name>
    http://sqs.us-east-1.amazonaws.com/123456789012/queue2

Each message is also referred to by a unique ID in response to a `SendMessage`
request. The maximum length of this identifier is 100 characters. Finally, each
time you receive a message from the queue, you receive a receipt handle for that
message. To delete a message or change its visibility, you will use that handle
and not the message ID (so you must always receive a message before you can
delete it). The maximum length of this ID is 1024.

When a client receives a message, it is not deleted; it is instead hidden for
a given amount of time so that other workers do not process the message at the
same time. When a worker is finished processing a message, they must manually
delete it. If they do not, then the message is made visible again for another
worker to process (after the visibility timeout is passed which means the
orginal worker is stalled or failed). The default timeout is 30 seconds,
however it should be set to the average time it takes to process and delete an
item in the queue.

If you have messages that take different amounts of time to complete:

1. Create a number of queues to handle the range of timing cases
2. Send all messages to a single consuming queue
3. That queue will forward each type of message to the time dependent queue
4. Processors consume messages with the appropriate Visibility Timeout set

When processing a message, you can give yourself more time by calling
`ChangeMessageVisibility`. This gives a worker a bit more time to finish
processing that single message without failing to another worker (in case the
worker knows it can finish in the new quantum). If you set the new visibility
timeout to 0, the worker effectively hands the message over to another worker
to process.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Polling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Can retrieve messages by polling in two variations:

* **Short Polling (default)**

  Will sample a subset of the servers (based on a weighted random distribution)
  and returns messages from just those servers. This means that not all the
  current messages may be returned or if you have a small number of messages
  enqueued (less than 1000), they query may return no messages. Repeated
  retrieve calls will sample all the servers and retrieve your messages though.

  Short polling occurs when the `WaitTimeSeconds` parameter in the
  `ReceiveMessage` call is set to `0`. If this value is not set, then the
  default of the queue, `ReceiveMessageWaitTimeSeconds` is supplied.

* **Long Polling**

  Will reduce the number of empty response messages (when there are no messages
  in the queue). A `ReceiveMessage` request will return at least one available
  message (if there are any) and up to the maximum specified in the call.
  When using Long Polling, all of the servers are queried. A maximum value of
  `20` seconds is advised for waiting on messages. If you have higher demands,
  then simply set the value as low as `1` second.

  If long polling is used for multiple queues, it is recommended to use a thread
  per queue for long polling to get messages from each queue as fast as
  possible.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Architecture
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The architecture looks something like this::

    client -> VIP -> load balancers -> SQSFrontEnd -> SQSMetadata
                                    |> SQSBackEnd  |> S3
                                    |> AMP Cluster
