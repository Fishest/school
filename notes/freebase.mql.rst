=================================================
Freebase: MQL
=================================================

-------------------------------------------------
Queries
-------------------------------------------------

Queries with MQL are JSON documents of the form::

    {
      "query": {
        "type": "/music/artist", # find object in db of this type
        "name": "The Police",    # whose name is "The Police"
        "alubm": []              # and populate the list of albums
      }
    }

The result of this is::

    {
      "status": "200 OK", 
      "code": "/api/status/ok", 
      "transaction_id":"cache;cache01.p01.sjc1:8101;2008-09-18T17:56:28Z;0029",
      "result": {
        "type": "/music/artist", 
        "name": "The Police",
        "album": [
          "Outlandos d'Amour", 
          "Reggatta de Blanc", 
          "Zenyatta Mondatta", 
          "Ghost in the Machine", 
          "Synchronicity"
        ]
      }
    }

-------------------------------------------------
`Architecture <http://mql.freebaseapps.com/ch02.html`_
-------------------------------------------------

Metaweb is stored as a graph database for the metadata
nodes and their relationships and the documents are stored
in a key value content store as `sha2(content) -> content`.

Each node has a unique identifier and a record of when and
by whom it was created.  The rest of the information is stored
in the content-store. Examples of various types of relationships::


    ----------------------------------------------------------------------------------
    From                  Property             To                    Value
    ----------------------------------------------------------------------------------
    /en/the_police        /type/object/name    /lang/en              The Police
    /en/zenyatta_mondatta /type/object/name    /lang/en              Zenyatta Mondatta
    /guid/1234	          /type/object/name    /lang/en              Driven to Tears
    /en/zenyatta_mondatta /music/album/artist  /en/the_police	
    /guid/1234            /music/track/album   /en/zenyatta_mondatta	
    /guid/1234            /music/track/length                        200.266

The properties (which define destinations) are objects themselves
and furthermore, users can define new destinations at anytime.
It should be noted that very few relationships are defined by the
Metaweb architecture; usually just the names starting with `type`.
An example of deinfining new destination types::

    ----------------------------------------------------------------------------------
    From                  Property               To                  Value
    ----------------------------------------------------------------------------------
    /type/object/name     /type/object/name      /lang/en            Name
    /music/album/artist   /type/object/name      /lang/en            Artist
    /music/track/album    /type/object/name      /lang/en            Appears On
    /music/album/artist   /type/property/unique                      true
    /music/track/album    /type/property/unique                      false  # default value

The Metaweb graph is a directed graph, but we can usually search
like the links are bidirectional.  In the foward search, MQL will
search for the tuple `(from, propty, _)` and report the `to` results.
In the reverse query, it will search for the tuple `(_, proprty, to)`
and report the `from` results. This can be explicitly stated as::
    
    ----------------------------------------------------------------------------------
    From                  Property                      To                  Value
    ----------------------------------------------------------------------------------
    /music/track/album    /type/propty/reverse_property /music/album/track

Each node can have many names, but only one per language. You can
use `/common/topic/alias` to define some nicknames. Furthermore, names
are not unique (only identifiers are). As an example the following three
ids have the name `English`:

* `/lang/en` - the english language
* `/en/english_people` - the english nationality
* `/authority/gnis/57724` - a town in Arkansas

Each identifier is a triple of: the node that is identified, a namespace,
and a key within that namespace. Identifiers can use somewhat named ids such
as `/en/the_police` or they can simply use `/guid/{guid}` if a coherent name
cannot be made. Identifiers are unique within a namespace and can only point
to a single node. Furthermore, identifiers are not immutable: nodes can be
given new identifiers and identifiers can be pointed to new nodes.

Every node has a numeric guid that uniquely identifies it and _is_ immutable.
The tuples in the metaweb graph refer to nodes by their guids, not by their
identifiers.

Although the database stores items in terms of tuples, it is helpful to view
the graph in terms of objects; for example::

    {
      id: "/en/the_police",
      name: "The Police",
      /music/artist/album: {
        id: "/en/zenyatta_mondatta",
        name: "Zenyatta Mondatta",
        /music/album/track: {
          name: "Driven to Tears",
          /music/track/length: 200.266
        }
        /music/album/track: {
          name: "Canary in a Coalmine",
          /music/track/length: 146.506
        }
      }
    }

