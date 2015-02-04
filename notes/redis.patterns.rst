================================================================================
Redis Patterns
================================================================================
http://www.slideshare.net/dvirsky/kicking-ass-with-redis
http://redis.io/documentation
http://shop.oreilly.com/product/0636920020127.do
http://www.paperplanes.de/2010/2/16/a_collection_of_redis_use_cases.html
https://developer.mozilla.org/en-US/docs/Mozilla/Redis_Tips

--------------------------------------------------------------------------------
Todo
--------------------------------------------------------------------------------

.. todo:: finish these examples

* locks
* pub/sum message bus
* user cardinality
* score board

--------------------------------------------------------------------------------
Write Buffer
--------------------------------------------------------------------------------

This creates a simple write buffer such that incoming writes are batched in
memory before they are written to storage (if redis goes down, durability is
lost).  When a new write comes in:

1. Create a hash key bound to the given entity
2. Increment 'counter' using `HINCRBY`
3. `HSET` any various LWW data (such as "last time seen")
4. `ZADD` the hash key to a pending set using the current timestamp

Every so often, say 10 seconds, the buffered values should be dumped (fanout writes):

1. Get all keys using `ZRANGE`
2. Fire off a job into a message queue for each pending key
3. `ZREM` the given keys

The backing message queue job will be able to fetch and clear the hash, and the
pending update has already been popped off of the set. A few extra notes about
this implementation:

* A sorted set can be used for the case where one only needs to pop off a set
  number of items (e.g. we want to process the 100 oldest)
* If multiple queued jobs to process a key, one could get no-oped due to another
  already processing and removing the hash.
* The system scales consistently on many Redis nodes simply by putting a pending
  key on each node.

This model mostly guarantees that only a single row in SQL is being updated at
once, which alleviates a bit of locking contention from bursty data that all ends
up grouping together (say metrics for the same counter).

--------------------------------------------------------------------------------
Throttle
--------------------------------------------------------------------------------

A simple throttling client can be constructed as follows:

.. code-block:: python

    def incr_and_check_limit(user_id, limit):
        ''' The following uses redis pipelines to throttle'''
        key = '{user_id}:{epoch}'.format(user_id, int(time() / 60))

        pipe = redis.pipeline()
        pipe.incr(key)
        pipe.expire(key, 60)
        current_rate, _ = pipe.execute()

        return int(current_rate) > limit

    def incr_and_check_limit(user_id, limit):
        ''' A similar approach can be done in memcache '''
        key = '{user_id}:{epoch}'.format(user_id, int(time() / 60))

        if cache.add(key, 0, 60):
            return False

        current_rate = cache.incr(key)

        return current_rate > limit
