================================================================================
Graph Representations
================================================================================

--------------------------------------------------------------------------------
Web Graph: http://webgraph.di.unimi.it/
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
Netflix Graph: https://github.com/Netflix/netflix-graph
--------------------------------------------------------------------------------

All verticies are converted to ordinal integer indexes and the directed
relationships are represented as a map[ordinal, list[ordinal]]::

    [2] -> [3,5,7]  // orginal 2 directed to 3,5,7
    [3] -> [5]      // orginal 3 directed to 5
    [5] -> [3, 7]   // orginal 5 directed to 3,7

The internal representation uses two arrays: an integer array and a byte
array.  The integer array index represents the ordinal and the value at
that index represents the offset into the byte array which is a
delta-encoded variable-byte integers representation::
   
   ------------------------------------------------------------
   ordinals -> byte array
   ------------------------------------------------------------
         [3, 5, 7, 5, 3, 7]
   0:[x]  |        |  |
   1:[x]  |        |  |
   2:[0] -|        |  |
   3:[3] ----------|  |
   4:[x]              |
   5:[7] -------------|

If the byte array values are represented in sorted order, then we can
store the delta between the previous version and thus be able to store
the integer ordinal value in less memory (say one byte)::

    [1, 2, 3, 5, 7, 11, 13]  // the sorted ordinal index
    [1, 1, 1, 2, 2,  4,  2]  // the delta  ordinal index

To add attributes to each node, the user must first define a schema which
exhaustively lists the properties that are available for each node. After
the connections are encoded as groups, they are preceded by an integer
representing how many bytes that property in the schema took allowing easy
iteration to the next property if the user is not interested in them::

   ------------------------------------------------------------
   an example idea of a schema
   ------------------------------------------------------------
   schema Video {
        characters
        genres
        tags
    }

   ------------------------------------------------------------
   for an example query of get('superman', 'tags')
   where ordinal(superman) -> 2
   [4,1,1,2,3] -> 4 entries -> [1, 2, 4, 7]
   ------------------------------------------------------------
          {characters}{generes}{tags}
          [4,1,1,2,3   3,1,1,2, 2,1,1]
    0:[x]  |
    1:[x]  |
    2:[0]--|


At runtime, when the user needs to find the set of connections over
some property for a given object, we go through the following steps: 

1. find the object's ordinal.
2. look up the pointer into our byte array for this object.
3. find the first property for the node type of this object in our schema.
4. while the current property is not the property where interested in:

  a. read how many bytes are used to represent this property.
  b. increment our pointer by the value discovered in (a).

5. move to the next property in the schema.
6. iteratively decode values from the byte array, each time adding the
   current value to the previous value.
7. look up the connected objects by the returned ordinals.

Determining if an object is connected to another object is O(n) instead
of the hashmap solution which is O(1).

--------------------------------------------------------------------------------
OrientDB Graph: https://github.com/nuvolabase/orientdb
--------------------------------------------------------------------------------


--------------------------------------------------------------------------------
Neo4j Graph: http://www.neo4j.org/learn/production
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
FlockDB Graph: https://github.com/twitter/flockdb
--------------------------------------------------------------------------------
http://engineering.twitter.com/2010/05/introducing-flockdb.html
