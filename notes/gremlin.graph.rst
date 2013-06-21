================================================================================
Gremlin Graphs
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

After setting up the gremlin server, initialize the graph that we will be
operatin on:

.. code-block:: groovy

    g = TinkerGraphFactory.createTinkerGraph()
    g.V.name          # the names of all the vertices
    g.V.map           # the properties of all the vertices
    g.E               # the edges in the graph
    g.out('label')    # all the nodes with out['label'] edges
    g.in('label')     # all the nodes with in['label'] edges
    n = g.v(1)        # get the node with id[1]
    n.outE            # get all the outgoing edges from n
    n.name            # get the value of property name of n
    n.outE.has('weight', T.lt, 0.5).inV  # filter inV with weight < 0.5
    n.outE.filter{ it.weight < 0.5 }.inV # equivalent

--------------------------------------------------------------------------------
Query Patterns
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Backtrack
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some queries will need to move forward to determine if some predicate is
reached. In these cases it may be helpful to backtrack. For example, here are
some queries that are answered by backtracking:

.. code-block:: groovy

    #------------------------------------------------------------
    # What are the ages of the people that know people that are
    # 30+ years old?
    #------------------------------------------------------------
    g.V.out('knows').has('age', T.gt, 30).back(2).age

    #------------------------------------------------------------
    # What are all the songs following dark star(89) in concert
    # that were sung by Jerry Garcia?
    #------------------------------------------------------------
    g.v(89).out('followed_by').out('sung_by').has('name','Garcia').back(2).name

    #------------------------------------------------------------
    # In order to figure out how many steps back to take, use
    # println to debug.
    #------------------------------------------------------------
    println g.v(89).out('followed_by').out('sung_by').has('name','Garcia')
    [StartPipe, OutPipe(followed_by), OutPipe(sung_by), PropertyFilterPipe(name,EQUAL,Garcia)]

    #------------------------------------------------------------
    # You can also name points to go back to instead of using
    # integer steps using the as(name) pipe.
    #------------------------------------------------------------
    g.v(89).out('followed_by').as('x').out('sung_by').has('name','Garcia').back('x').name

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Except / Retain
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Flow Rank
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Path
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Loop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Split / Merge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Map / Reduce
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Pattern Match
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tree
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The traversal path through the graph can be viewed and represented as a tree.
