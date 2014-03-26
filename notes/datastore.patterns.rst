================================================================================
Datastore Patterns
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* Eventually consistent using gossip or reflected memory
* versioned graph of data (store multiple versions)
* hyperplane version compaction with garbage collection of aging policy
* monoid / lattices merge policy (statistical relaxation) -> must know storage type
* document / datastructure views (graph)
* journal of writes for replay and sync
* compact BTree / Graph database storage (or log replay)
* otherwise a write coordinator is needed (datomic)
