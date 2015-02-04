================================================================================
Graph Databases
================================================================================

--------------------------------------------------------------------------------
Chapter 1: Introduction
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Chapter 2: The NoSQL Phenomenon
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Chapter 3: Graphs and Connected Data
--------------------------------------------------------------------------------

* R-Trees

--------------------------------------------------------------------------------
Chapter 4: Working With Graph Data
--------------------------------------------------------------------------------

* http://databaserefactoring.com/

The two most popular graph formats are the property graph model and
the triple store (RDF). The following is true for property graphs:

* nodes are repositories for properties (string keys and arbitrary values)
* relationships connect nodes and are directed; each relationship has a label
* relationships can also have properties

The common graph query languages are:

* gremlin (imperitive path based)
* SPARQL (RDF based)
* cypher (neo4j declaritive based)

What follows is a summary of the cyper language::

    START   # specifies one or more graph starting points
    MATCH   # using ascii notation, declare the traversal
    RETURN  # specifies what data to return from the query
    WHERE   # provides criteria for filtering portions of a pattern
    CREATE  # creates nodes and relationships
    DELETE  # removes nodes, relationships, and properties 
    SET     # set property values
    FOREACH # performs an update action for each element in a list
    WITH    # divides a query into multiple distinct parts

    # example query for the plays written by shakespeare
    START bard=node:authors('firstname:"William" AND lastname:"Shakespeare"')
    MATCH (bard)-[:WROTE]->(plays) # (node-from)-[:RELATIONSHIP]->(node-to)
    RETURN plays

    # example query for more complex graph
    START theater=node:theatre(name = 'Theatre Royal'),
          newcastle=node:city(name = 'Newcastle'),
          bard=node:author('firstname:"William" AND lastname:"Shakespeare"')
    MATCH (newcastle)<-[:STREET|CITY*1..2]-(theater) 
          <-[:VENUE]-()-[:PERFORMANCE_OF]->()-[:PRODUCTION_OF]
          ->(play)<-[:WROTE_PLAY]-(bard)
    RETURN DISTINCT play.title AS play

.. todo:: page 64
