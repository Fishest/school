================================================================================
Amazon Alf
================================================================================

https://blogs.amazon.com/alf_gossip/archive/2010/10/
https://w.amazon.com/index.php/Alf

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Alf is a lock service developed at Amazon. It enables processes in a distributed
application to do the following things:

* advertise themselves
* discover other processes (which are advertising themselves)
* synchronize resources using locks
* detect when process fail or become unreachable
* share small amounts of data

--------------------------------------------------------------------------------
Alf Bus
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Alf Server / Alf Registry Server
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Boots
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Boots is a simple service for setting up configuration to be fetched later on
and also for finding endpoints for a service:

* configuration - clients connect to boots during startup, get their configuration,
  and then startup. The clients can then continue to poll boots to see if any
  configuration has changed. This fixes the issue with static configuration systems
  when your configuration can change throughout the system's life.

* endpoints - endpoints that need to be discovered are simply added to boots and
  then heart-beated every hour so clients can connect to live instances. Clients
  can filter endpoints based on certain conditions. This fixes the staleness issue
  that exists in DNS as well as issuing advanced queries that DNS cannot answer.

Boots works by simply writing to and from DynamoDB, but keeping an disk based cache
on the local server so common queries can be answered if DynamoDB is down (making
DynamoDB a soft dependency). The backend can also be changed (with a little work).

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The underlying structure of Boots is as follows:

* **product**  - a computer system that does something useful
* **service**  - is an implementation of a product (product:implementation)
* **clique**   - a group that cannot handle requests for another clique (prod, test, devel)
* **endpoint** - a network port a client can connect to (a service can have many endpoints)
* **host**     - is a computer on the network that can host an endpoint (FQDN)

These ideas are tied together as follows:

#. A host can serve a bunch of services
#. A service can be hosted by a bunch of hosts
#. A service can be exposed by a bunch of endpoints.
#. A product is a collection of services that fall under its umbrella.
#. Each entity can have a configuration of its own.
#. Any configuration is represented by a map of string -> string
#. An endpoint has another special config (lets call it discovery-config).
#. Endpoints heartbeat every once in a while (say once every hour).

When a software relevant for a given product starts up on a host, it can query boots
to determine which services it should join. For each service the host is part of,
it can retrieve the configuration which would ideally be handled in the service-specific
way. For example, when an "customer" server starts (with software relevant to product "customer"),
it needs to know which services is it part of (something like customr:na.customer.amazon.com).
On getting that info, it can query the configuration for the service which includes things
like seed nodes. It can optionally also get configuration for the itself (the host) if any.
To configure this information, a simple tool can be used apriori to setup all configuration.

Endpoints for a service are retrieved by making a query to a Boots server. The simplest query
simply returns all active endpoints for the service. You can make your query more sophisticated.
For example, you can restrict to endpoints with particular configuration (aka discovery-config),
or the ones that have heartbeated recently.

Each endpoint is responsible for periodically sending Boots a heartbeat for each endpoint, so
that Boots knows the endpoint is alive. The idea here is not to detect transient failures, but
instead to detect when endpoints have been out of service for more than one day.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Design
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
