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
  - Kinesis

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

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tips
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can get the best performance if your hash key is such that it can be split
between N partitions evenly so that you can get the performance of parallel IO
from multiple hosts (if you do parallel queries)::

    hash_key  = hash(range_key) % partitions
    range_key = "%s/%s" % (record_date, record_id)

    queries = (0 to N).par.map(x => client.query(key=x, range=date)
    sorteds = queries.map(qs => qs.sort())
    merged  = merge_sort(queries)

If you need to create two indexes (a -> b and b -> a), then you will have to
do one of the following to assure that the transaction occurs:

1. Create an event store using SQS, file-system, or REDO log (dynamo)
2. Write to one table and slowly scan the other for inconsistencies

To get the ability to do a `ENDS_WITH` query, simply create a secondary index
on a new stored field which is the reversed value of a word and do a `STARTS_WITH`
query on it.

To implement a cluster master, heartbeat to an item and have cluster members
periodically read from that item (say logical time).  If the heartbeat stops
or doesn't update in a specific amount of time, have a new master grab the
item lock (the member id guid is sufficient) with a CAS and continue heartbeating.
The other cluster members will fail to grab the CAS and will continue listening.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ACID Implementation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

By default, dynamo only provides two of the four ACID gurantees: consistency and
durability. Within a single item, one also gets atomicity and isolation, however
when one needs to operate on more than one item at once, they no longer have
these gurantees. However, using the optimistic concurrency control offered by
dynamo, these guarantees can be met:

* strategy is a multi phage commit protocol
* to avoid losing state on failure, the coordinater state is stored in dynamodb
* to avoid the need for failure detection, multiple coordinates can be active
* multiple coordinates can be working on the same transaction
* isolation canbe available at many different levels

https://github.com/awslabs/dynamodb-transactions/blob/master/DESIGN.md

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

  For larger messages, store them in S3 or SimpleDB and send the
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

--------------------------------------------------------------------------------
Amazon Simple Workflow Service (SWF)
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SFW is a distributed workflow system that is composed of logical units of work
(tasks) and controllers (deciders). It manages task delivery and maintaining
state between tasks. Every piece of the system is distributed and can be
restarted in the case of failure exactly where it left off. It handles all the
plumbing like concurrency, durability, task retrying, consistency, etc.

The history of each workflow is recorded and stored for up to 90 days. It is
programatically accessed as a JSON document of a collection of attributes::

    [
      {
        "eventId": 11,                           # unique event id
        "eventTimestamp": 123456789,             # time event started
        "eventType": "WorkflowExecutionStarted", # type of event
        "workflowExecutionStartedAttributes": {  # attributes for event type
          ...        
        }
      },
    ]


.. notes::

   - Tasks are durably stored and guranteed to be delivered at most once
   - Task results (success or failure) are stored durably
   - Task lists are automatically load balanced via dynamic consistent queues
   - New tasks arrive via HTTP long poll
   - Can associate a workflow with a unique id, it also generates a unique run id
   - Each workflow's history is recorded and stored for up to 90 days

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The basic units of a SWF process are: deciders, workers, and workflow starters.
The workflow starter is any part of an application that can kick off a new
workflow: website, mobile application, etc.

The decider, whos job it is to control the workflow coordination logic, takes
over. After every action in SWF, a decider is chosen and fed the history of
the workflow up to that point. The decider then returns a `Descision` back to
SWF which indicates the next portion of the workflow to start. This can mean
scheduling the next task to start, starting a child workflow, failing, or marking
this workflow as complete.

The activity worker is a process or thread that performs activity tasks which
are the units of work of the workflow. Each worker polls SWF for its next task
to perform. A worker can be for a specific task or for a range of tasks.

Data can be exchanged between parts of the system by way of strings that are
user defined:

* Workers can receive data from and return data to SWF
* Deciders can do the same
* Pointers to larger data (say stored in S3) can be passed around
 
Workflows are registered in domains (namespaces). There can be one or more
workflows per domain, however only workflows in the same domain can operate
with each other.

The system artifacts are created as follows:

* `RegisterWorkflowType(domain, name, version)`
* `RegisterActivityType(domain, name, version)`
* `token = PollForDecisionTask()`
* `token = PollForActivityTask()`
* `StartWorkflowExecution(domain, workflowId, runId)`

Tasks(activity, decision) are scheduled by putting them on a specific task
list queue. The workers can then poll on the default queue for their type
or they can poll a specific queue. By placing tasks on different queues, you
are effectively routing tasks through the system. You can have systems like
the following:

* One worker polling 1 or more tasks lists (each list unique for a task)
* One worker polling 1 task list (that may contain many task types)
* Many workers polling 1 or more of tasks lists (of same or differnet tasks)

Once a workflow has started, it is in the open state. It can then be
transitioned to the following states:

* **complete** - `CompleteWorkflowExecution`
* **canceled** - `CancelWorkflowExecution`
* **failed** - `FailWorkflowExecution` (used if the workflow has entered a
  state outside of the realm of normal completion)
* **timed-out**
* **continued** - `ContinueAsNewWorkflowExecution` (for long running workflows
  with very large histories)
* **terminated** - `TerminateWorkflowExecution` (stopped in the AWS console)

Workers recieve new tasks by way of long polling. They call the SWF service
when they are able to process a new task. If a task is available in the queue
they specify, it is returned. If not, SFW will hold the connection open for
60 seconds and if after that time there is no task, it will return a task
with an empty taskToken which is an indication to start another long poll.

Finally, you can set timeouts on the following workflow portions:

* Workflow start to close
* Decision task start to close
* Activity task start to close
* Activity heartbeat
* Activity task scheduled to start
* Activity task scheduled to close (usually less than sum of scheduled to start
  and start to close)

.. note::
   - A task is assigned to only one activity worker
   - Tasks are ordered on a best effort basis, but order is not guranteed

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Advanced
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The decider can start a timer that will fire and add an event to the execution
history before proceeding. This can be useful for adding delays to the system
or pauses to wait for signals to arrive:

1. Create and start a timer to wait for a signal
2. When a decision is received check if it is a signal or the timer
3. If it was the signal, cancel the timer and process the signal
4. Note that both can happen at once, so interpret this how you want
5. If the timer fires before the signal, fail or carry on with your logic

The decider can perform workflow splits based on the results of tasks.

Signals can be sent to a running workflow to inject information or let the
workflow know about information changes. This can be done by calling the
`SignalWorkflowExecution` method which will add an event to the history log
and scheduling a new decision task.

Markers can be added in the workflow history to add extra information to the
deciders.

You can tag workflows with up to five(5) tags that can be used when querying
as filters (say with `ListOpenWorkflowExecutions`).

.. note:: If a signal is sent to a workflow that is not open will result in
   a `SignalWorkflowExeception`.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
SWF API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Activity workers `PollForActivityTask` to get a new task. After it has operated
on the task, it responds using `RespondActivityTaskCompleted` if successful or
`RespondActivityTaskFailed` if failed. It can also cancel a task with
`RespondActivityTaskCanceled`

Deciders `PollForDecisionTasks` to get a new task. After viewing the history and
making a decision, the decider responds with `RespondDecisionTaskComplete` to
complete the task and return zero or more next decisions.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Flow Framework
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The flow framework attempts to hide a lot of the workflow boilerplate in the form
of an AOP library using aspectJ. In order to interface with it, simply decorate
the interfaces with appropriate annotations:

.. code-block:: java

    //------------------------------------------------------------
    // Task Activities Definition
    //------------------------------------------------------------
    // The framework will generate a client off of this interface
    // automatically that can be used by the workflow. It should
    // be noted that although tasks that are related should be 
    // defined in the same interface, they do not have to operate
    // in the same worker process.
    //------------------------------------------------------------
    @Activities(version="1.0")
    @ActivityRegistrationOptions(
        defaultTaskScheduleToStartTimeoutSeconds = 60, 
        defaultTaskStartToCloseTimeoutSeconds = 5)
    public interface HelloWorldActivities {
        public String getName();
        public void printGreeting(String greeting);
    }

    public class HelloWorldActivitiesImpl implements HelloWorldActivities {

        @Override
        public String getName(){
            try {
                Thread.sleep(10000); 
            }
           catch(InterruptedException e){
                System.out.println("Thread interrupted");   
            }
            return "World";
        }

        @Override
        public void printGreeting(String greeting) {
            System.out.println(greeting);
        }

    }

    //------------------------------------------------------------
    // Workflow Definition
    //------------------------------------------------------------
    // There should be a single method decorated with @Execute
    // which is the entry point for the workflow. This code is run
    // within a decider entity which polls for tasks and starts
    // the workflow entry.
    //------------------------------------------------------------
    @Workflow
    @WorkflowRegistrationOptions(defaultExecutionStartToCloseTimeoutSeconds = 60)
    public interface HelloWorldWorkflow {

        @Execute(version = "1.0")
        void startHelloWorld();
    }

    public class HelloWorldWorkflowImpl implements HelloWorldWorkflow {
        // this client is generated automatically by the framework
        private HelloWorldActivitiesClient activitiesClient
             = new HelloWorldActivitiesClientImpl(); 

        @Override
        public void startHelloWorld() {
            //------------------------------------------------------------
            // This is not a future per-say, it should be passed
            // to a method decorated with @Asynchronous to be processed.
            // The framework will make sure the method call happens when
            // the result is received and not before (simply calling get
            // here will throw an exception, it will not block).
            //------------------------------------------------------------
            Promise<String> name = activitiesClient.getName();
            printGreeting(name);
        }
       
        // This method will be called when the promise is ready
        // not before (the call to get will succeed, not block).
        @Asynchronous
        private void printGreeting(Promise<String> name) {
            activitiesClient.printGreeting("Hello " + name.get() + "!");
        }
    }

It should be advised that the workflow section of the code is replayed
each time a task is complete and all the code in it must be deterministic
(long story short, keep it simply and defer as much as possible to the
activity tasks):

1. The entry point is replayed until it reaches async methods that have
   not been completed; tasks are scheduled for these.
2. As the arguments to the tasks become available, they are are called
   (this happens by checking the history). Tasks without arguments are
   simply called. Both of these operations can result in more tasks.
3. When all the tasks that can be completed are, the framework reports
   back with a list of tasks to schedule. If there are no more tasks
   to schedule, the workflow is marked as complete.

Data is marshalled to and from SWF using a `DataConverter`, the default
of which is the Jackson JSON processor. Results from activities are
returnd in `Promise<T>`. Sending signals is allowed by marking a signal
handler with `@Signal` along with the signals it can handle.

.. note::
   - When you change a workflow or activity, bump its version number
   - Make the task lists version dependent by appending the version to its name

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Flow Framework Under the Hood
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The magic behind activities in the workflow is that they are all wrapped in
`Task`, so the hello world defined about can also be written like this:

.. code-block:: java

    @Override
    public void startHelloWorld() {
        final Promise<String> greeting = client.getName();
        new Task(greeting) {
            @Override
            protected void doExecute() throws Throwable {
                client.printGreeting("Hello " + greeting.get() + "!");
            }
        };
    }

If the method is returning a `Promise<T>`, it should use a `Functor`:

.. code-block:: java

    @Override
    public void startHelloWorld() {
        final Promise<String> greeting = new Functor<String>() {
            @Override
            protected Promise<String> doExecute() throws Throwable {
                return client.getGreeting();
            }
        }
        client.printGreeting(greeting);
    }


--------------------------------------------------------------------------------
Amazon Kinesis
--------------------------------------------------------------------------------

http://aws.amazon.com/kinesis/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: read up


--------------------------------------------------------------------------------
Amazon RDS
--------------------------------------------------------------------------------

http://aws.amazon.com/rds/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. todo:: read up

--------------------------------------------------------------------------------
Amazon Sable
--------------------------------------------------------------------------------

.. todo:: read up

--------------------------------------------------------------------------------
Amazon Jiffy
--------------------------------------------------------------------------------

.. todo:: read up

--------------------------------------------------------------------------------
Amazon S3
--------------------------------------------------------------------------------

http://aws.amazon.com/s3/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tips
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In order to allow S3 to evenly shard your data, try not to
use keys of the form `<database>/<date>/<name>` as you will
eventually hit a scaling load (when a lot of keys hash to the
same bucket). Instead, you can do something like::

    key = "#{database}/#{date.now}/#{name}"
    key = hash(key) + "/" + key

Which will allow your keys to be evenly distributed throughout
S3 for as long as you are using it.

--------------------------------------------------------------------------------
Amazon Simple Deployment Service (SDS)
--------------------------------------------------------------------------------

http://aws.amazon.com/sds/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In summary, it has a similar architecture as Apollo.

It comes with the following features:

* repeatable and reliable deployment
* zero downtime rolling updates
* abort and rollback deployments
* reuse existing scripts that you know work
* auto scaling, ELB, cloud formation
* multiple AWS accounts, instance types, and private VPC subnets
* support for windows and linux

Works by running an SDS agent on your EC2 instances and applying the neccessary
tags for each instance (test, prod, etc). Then define an aspect configuration
file with your code (a YAML file). Next, push your code to S3 and then tell the
SDS service to deploy that revision. You can now orchestrate your deployment to
your test tagged environments and when you are sure they are working correctly,
simply tell SDS to push to production tagged instances.

The configuration file has a number of hooks to tie into the lifecycle of the
application.  These can be any executable which the hook defines to run as a
given user with a timeout for how long until the execution has failed. If the
script does not return an error, it is assumed to succeed:

* start
* application stop
* <download>
* before install
* <install>
* after install
* application start
* validate service
* end

One downside at the moment is that the data that is pushed to S3 is defined
per the application (say installer for windows, rpm/deb for linux, etc).
Also, in the future, they hope to enable things like
`Blue Green Deployment <http://martinfowler.com/bliki/BlueGreenDeployment.html>`_.

--------------------------------------------------------------------------------
Amazon SimpleDB
--------------------------------------------------------------------------------

* http://docs.aws.amazon.com/AmazonSimpleDB/latest/DeveloperGuide/Welcome.html
* http://boto.readthedocs.org/en/latest/simpledb_tut.html
* http://aws.amazon.com/articles/1394

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SimpleDB works by creating domains for application data. Domains are similar to
database tables, except that you cannot perform functions across multiple
domains, such as querying multiple domains or using foreign keys. This should be
planned for in architecture design. Data can be stored in different domains and
then searched or joined at the application layer, otherwise it should be in the 
same domain.

The following components of SimpleDB correspond to each part of a spreadsheet:

* aws account - an entire spreadsheet
* sdb domain - represents a worksheet
* sdb items - represent spreadsheet rows (contain one or more key/value pairs)
* sdb attributes - represent spreadsheet columns (categories of data assigned to items)
* sdb values - represent spreadsheet cells (instances of item attributes)

Unlike a spreadsheet, simpleDB cells can have multiple values associated with them.
However like a spreadsheet, new fields can be added to an entry and SimpleDb will
correctly index them into the structure.

Each AWS account can have up to 250 domains with each domain holding up to 10 GB
per domain. A good method of scaling SimpleDB up is to partition data between a
different domain (and thus different clusters).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Service API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SimpleDB has a simple ReST interface based on the operation to be performed:

* `CreateDomain` - Create domains to contain your data (up to 250)
* `DeleteDomain` - Delete any of your domains
* `ListDomains` - List all domains within your account
* `PutAttributes` - Add, modify, or remove data within your Amazon SimpleDB domains
* `BatchPutAttributes` - Generate multiple put operations in a single call
* `DeleteAttributes` - Remove items, attributes, or attribute values from your domain
* `BatchDeleteAttributes` - Generate multiple delete operations in a single call
* `GetAttributes` - Retrieve the attributes and values of any item id that you specify
* `Select` - Query the specified domain using a SQL `select` expression
* `DomainMetadata` - View information about the domain: creation date, item count / size, schema

Simply perform a standard HTTP `GET` or `POST` request with the required fields:

.. code-block:: python

    request = [
        "https://sdb.eu-west-1.amazonaws.com/",              # endpoint
        "?Action=PutAttribute",                              # action
        "&DomainName=MyDomain",                              # database domain
        "&&AWSAccessKeyId=<your_access_key>",                # authentication
        "&ItemName=Item123",                                 # primary key
        "&Attribute.1.Name=Color&Attribute.1.Value=Blue",    # attribute
        "&Attribute.2.Name=Size&Attribute.2.Value=Med",      # attribute
        "&Attribute.3.Name=Price&Attribute.3.Value=0014.99", # attribute
        "&Version=2009-04-15",                               # SimpleDB api version
        "&Signature=<valid_signature>",                      # message signature
        "&SignatureVersion=2",                               # signature version
        "&SignatureMethod=HmacSHA256",                       # method of signing
        "&Timestamp=2010-01-25T15%3A01%3A28-07%3A00",        # timestamp of action
    ]   
    response = http_client.get(''.join(request))
    # <PutAttributesResponse>
    #   <ResponseMetadata>
    #     <StatusCode>Success</StatusCode>
    #     <RequestId>f6820318-9658-4a9d-89f8-b067c90904fc</RequestId>
    #     <BoxUsage>0.0000219907</BoxUsage>
    #   </ResponseMetadata>
    # </PutAttributesResponse>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Consistency
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

All operations in SimpleDB are eventually consistent. To achieve high performance
and durability, multiple copies of each domain are kept. Read operations can be
performed in a consistent or inconsistent manner with the tradeoff being performance
for the gurantee of the most up to date version of a value. In general if two clients
are writing data (w_1 and w_2) and two readers are reading (r_1, r_2):

.. code-block:: text

    # read overlaps a write (when does write2 complete?)
    w_1 r_1       r_1 == (C=[w_1 w_2], NC=[w_1 w_2, None])
    ------------
        w_2  r_2  r_2 == (C=[w_2], NC=[w_1 w_2, None])

    # no overlapping operations (linear)
    w_1   r_1     r_1 == (C=[w_2], NC=[w_1 w_2, None])
    ------------
       w_2  r_2   r_2 == (C=[w_2], NC=[w_1 w_2, None])

    # overlapping writes (which wins?)
    w_1   r_1     r_1 == (C=[w_1 w_2], NC=[w_1 w_2, None])
    ------------
     w_2    r_2   r_2 == (C=[w_1 w_2], NC=[w_1 w_2, None])

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Scaling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To scale a dataset, simply split it into different domains which can be queried
in parallel. The partition can be made based on the type of data or based on
an easily split primary key (ex: customer identifier).

In cases where data sets do not partition easily (e.g., logs, events, web crawler
data), you can use hashing algorithms to create a uniform distribution of items
among multiple domains.  For example, you can determine the hash of an item name
using a well-behaved hash function, such as MD5 and use the last 2 bits of the
resulting hash value to place each item in a specified domain:

* If last two bits equal `00`, place item in `Domain0`
* If last two bits equal `01`, place item in `Domain1`
* If last two bits equal `10`, place item in `Domain2`
* If last two bits equal `11`, place item in `Domain3`

To extend this to more partitions, simply use more bits of the resutling hash
(3 to 8 domains, 4 to 16, etc).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Security
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To validate that the request came from the correct authorized party, SimpleDB
requests that an HMAC signature be included in the message as well as the user's
public api key:

1. create the request to issue to SimpleDB
2. create an HMAC-SHA hash of the request + your secret key
3. send the request to AWS with the signature and your access key
4. AWS looks up your secret key with your supplied access key
5. it creates the same HMAC-SHA hash of the request using your secret key
6. it compares the two signatures and if they are different, the request fails
7. if the signatures are the same, the request is issued to the underlying data store

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Optmistic Concurrency Control
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To make sure your write does not stomp another write, you can use conditional
operations based on an attribute for an item. It is suggested that writers use
a version number or timestamp field that can be tested. to write a new value,
simply read the current value, then write a new value with the expectation of
the old value:

.. code-block:: python

    request = [
        # ...
        &Attribute.2.Name=VersionNumber
        &Attribute.2.Value=31
        &Attribute.2.Replace=true
        &Expected.1.Name=VersionNumber
        &Expected.1.Value=30
        # ...
    ]

This same technique can be used for:

* versioning
* atomic counters
* attribute existence checks (transaction, locks, etc)
* delete attributes (transaction cleanup / rollback)
* delete item (garbage collection)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Querying
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

SimpleDB presents a SQL query API that implements most of the common SQL operations
as well as a few unique qualities:

* select multiple values from an attribute
* intersection of queries
* range queries

Large queries, like count, will run for at most 5 seconds before returning their
current results along with a token that can be used to make another request to
continue the operation for the next 5 seconds. To get the total result, simply
keep querying until a continuation token is not returned and aggregate the results.

It should be noted that all values stored in SimpleDB are stored as UTF8 strings.
This means that for numeric data, all comparisons are performed lexicographically.
As such, AWS recommends:

* use negative number offsets (store all numbers as positive, add smallest possible value)
* use zero padding (add leftmost zeros up to largest value in the dataset)
* store dates in the appropriate format (ISO 8601 with neccessary granularity)

All attributes are indexed individually, however querying where two attributes are
true may produce two large sets that have to be reduced to one quite small result.
To prevent this case (where it is needed), create a joint attribute:

.. code-block:: sql

    -- instead of hitting two indexes, combine them to make one
    select * from myDomain where Type = 'Book' and Price < '9'
    select * from myDomain where TypePrice > 'Book' and TypePrice < 'Book9'

    -- instead of sorting a non-predicated attribute, combine them into one a prefix query
    select * from myDomain where user_id = '1234' and bill_time is not null order by bill_time limit 100
    select * from myDomain where user_id_bill_time like '1234|%' order by user_id_bill_time limit 100

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Throttling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you attempt to query the serivce to fast, SimpleDB will start returing 5xx
errors. In this case, one should perform an exponential backoff and retry as
follows:

.. code-block:: java

    boolean shouldRetry = true;
    int retries = 0;
    do {
      try {
        // Submit request to Amazon SimpleDB
        if (status == HttpStatus.SC_OK) {
          shouldRetry = false;
          // Process successful response from Amazon SimpleDB
        } else {
          if (status == HttpStatus.SC_INTERNAL_SERVER_ERROR
             || status == HttpStatus.SC_SERVICE_UNAVAILABLE) {
        shouldRetry = true;
        long delay = (long) (Math.random() * (Math.pow(4, retries++) * 100L));
        try {
          Thread.sleep(delay);
        } catch (InterruptedException iex){
          log.error("Caught InterruptedException exception", iex);
        }
          } else {
        shouldRetry = false;
        // Process 4xx (Client) error
          }
        }
      } catch (IOException ioe) {
        log.error("Caught IOException exception", ioe);
      } catch (Exception e) {
        log.error("Caught Exception", e);
      } finally {
        // Perform clean-up as necessary
      }
    } while (shouldRetry && retries < MAX_NUMBER_OF_RETRIES);

