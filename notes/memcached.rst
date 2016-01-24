================================================================================
Memcache
================================================================================

http://memcached.org/
https://github.com/memcached/memcached/wiki

.. TODO:: add more protocol notes

--------------------------------------------------------------------------------
Storage Commands (set, add, replace, append, prepend, cas)
--------------------------------------------------------------------------------

.. code-block:: text

    set <key> <flags> <expiry> <datalen> [noreply]\r\n<data>\r\n
    add <key> <flags> <expiry> <datalen> [noreply]\r\n<data>\r\n
    replace <key> <flags> <expiry> <datalen> [noreply]\r\n<data>\r\n
    append <key> <flags> <expiry> <datalen> [noreply]\r\n<data>\r\n
    prepend <key> <flags> <expiry> <datalen> [noreply]\r\n<data>\r\n
    
    cas <key> <flags> <expiry> <datalen> <cas> [noreply]\r\n<data>\r\n
    
    where,
    <flags>   - uint32_t : data specific client side flags
    <expiry>  - uint32_t : expiration time (in seconds)
    <datalen> - uint32_t : size of the data (in bytes)
    <data>    - uint8_t[]: data block
    <cas>     - uint64_t

--------------------------------------------------------------------------------
Retrival Commands (get, gets):
--------------------------------------------------------------------------------

.. code-block:: text

    get <key>\r\n
    get <key> [<key>]+\r\n
    
    gets <key>\r\n
    gets <key> [<key>]+\r\n

--------------------------------------------------------------------------------
Delete Command (delete):
--------------------------------------------------------------------------------

.. code-block:: text

    delete <key> [noreply]\r\n

--------------------------------------------------------------------------------
Arithmetic Commands (incr, decr):
--------------------------------------------------------------------------------

.. code-block:: text

    incr <key> <value> [noreply]\r\n
    decr <key> <value> [noreply]\r\n
    
    where,
    <value> - uint64_t

--------------------------------------------------------------------------------
Misc Commands (quit)
--------------------------------------------------------------------------------

.. code-block:: text

    quit\r\n
    flush_all [<delay>] [noreply]\r\n
    version\r\n
    verbosity <num> [noreply]\r\n

--------------------------------------------------------------------------------
Statistics Commands
--------------------------------------------------------------------------------

.. code-block:: text

    stats\r\n
    stats <args>\r\n

--------------------------------------------------------------------------------
Error Responses:
--------------------------------------------------------------------------------

.. code-block:: text

    ERROR\r\n
    CLIENT_ERROR [error]\r\n
    SERVER_ERROR [error]\r\n
    
    where,
    ERROR means client sent a non-existent command name
    CLIENT_ERROR means that command sent by the client does not conform to the protocol
    SERVER_ERROR means that there was an error on the server side that made processing of the command impossible

--------------------------------------------------------------------------------
Storage Command Responses:
--------------------------------------------------------------------------------

.. code-block:: text

    STORED\r\n
    NOT_STORED\r\n
    EXISTS\r\n
    NOT_FOUND\r\n
    
    where,
    STORED indicates success.
    NOT_STORED indicates the data was not stored because condition for an add or replace wasn't met.
    EXISTS indicates that the item you are trying to store with a cas has been modified since you last fetched it.
    NOT_FOUND indicates that the item you are trying to store with a cas does not exist.

--------------------------------------------------------------------------------
Delete Command Response:
--------------------------------------------------------------------------------

.. code-block:: text

    NOT_FOUND\r\n
    DELETED\r\n

--------------------------------------------------------------------------------
Retrival Responses:
--------------------------------------------------------------------------------

.. code-block:: text

    END\r\n
    VALUE <key> <flags> <datalen> [<cas>]\r\n<data>\r\nEND\r\n
    VALUE <key> <flags> <datalen> [<cas>]\r\n<data>\r\n[VALUE <key> <flags> <datalen> [<cas>]\r\n<data>]+\r\nEND\r\n

--------------------------------------------------------------------------------
Arithmetic Responses:
--------------------------------------------------------------------------------

.. code-block:: text

    NOT_FOUND\r\n
    <value>\r\n
    
    where,
    <value> - uint64_t : new key value after incr or decr operation

--------------------------------------------------------------------------------
Statistics Response
--------------------------------------------------------------------------------

.. code-block:: text

    [STAT <name> <value>\r\n]+END\r\n

--------------------------------------------------------------------------------
Misc Response
--------------------------------------------------------------------------------

.. code-block:: text

    OK\r\n
    VERSION <version>\r\n

--------------------------------------------------------------------------------
Notes:
--------------------------------------------------------------------------------

  - set always creates mapping irrespective of whether it is present on not.
  - add, adds only if the mapping is not present
  - replace, only replaces if the mapping is present
  - append and prepend command ignore flags and expiry values
  - noreply instructs the server to not send the reply even if there is an error.
  - decr of 0 is 0, while incr of UINT64_MAX is 0
  - maximum length of the key is 250 characters
  - expiry of 0 means that item never expires, though it could be evicted from the cache
  - non-zero expiry is either unix time (# seconds since 01/01/1970) or,
    offset in seconds from the current time (< 60 x 60 x 24 x 30 seconds = 30 days)
  - expiry time is with respect to the server (not client)
  - <datalen> can be zero and when it is, the <data> block is empty.
