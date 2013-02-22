================================================================================
Amazon Web Services (AWS)
================================================================================

--------------------------------------------------------------------------------
Amazon Dynamo
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
