------------------------------------------------------------
Threat Model
------------------------------------------------------------

The basic threat model should make sure the following threats
are secured against (**STRIDE**):

* **Spoofing** - assume the identity of another actor
* **Tampering** - change data while it is in transit
* **Repudiation** - validate the integrtiy of the data / source
* **Information Disclosure** - gather extra system information
* **Denial of Service** - deny service to legitimate users
* **Elevation of Privilege** - gain hightened permissions

------------------------------------------------------------
Data Flow Diagram (DFD)
------------------------------------------------------------

The data flow of a system can be modeled using the following
UML like diagram components:

* **Process** -
* **Complex Process** -
* **External Interactor (I/O)** -
* **Data Store** -
* **Data Flow** -
* **Boundary** -

------------------------------------------------------------
Internal Tools
------------------------------------------------------------

* AAA / Odin / AuthPortal / DPAPI

------------------------------------------------------------
Security Utilities
------------------------------------------------------------

* **strace**
* **burp suite**
* **nmap**
* **wireshark**
* hashcat
* beef xss
* owasp zap
* wireshark / fiddler / nmap / netcat / hping3

------------------------------------------------------------
Thing To Look For
------------------------------------------------------------

In order to build a threat model, you have to find threats
to look for. What follows is a handy list of points to start
your search and possibly reduce where all you have to look:

* validation for all input into the system
  - not just user input, think of hidden input as well
  - registry, config values, system values, storage values
  - crypto configuration
* start at every entry / exit point and trust boundaries
  - look where the user calls into the system
  - command line, web service call, any I/O
  - look at an data storage code (clients, DAOs, etc)
* xss -> input filtering / output encoding
* all SQL should use parameterize prepared statements
* check that all configuration files have the correct permissions
  - `/etc`, `/etc/init.d`, `/var/logs`, and local
  - each service should have its own user, not root
  - each user should have least privledge assigned to it
  - each user should have its environment jailed
* credentials leakage (hard-coded in source)
* check that the default configuration values are sane
* session-id -> login / logout
* authenticating -> session or action
* hidden APIs -> for debug or testing
* secrets in config
* input -> control code + user input
* weak / bad / no crypto
* check for any information disclosure
  - this can be in console output, logs, or web server
  - this can be in leaked exceptions
  - don't tell the user anything that they don't need to know
* check all third party software versions
  - are they up to date with the latest versions
  - do the versions have an vulnerabilities and solutions

* firefox { tamper data, web dev, firebug }
* fortify / grep common / code smells (build process)
* scanners / manual code inspection
* audit workbench
* brakeman (Ruby On Rails)
* IBM Rational AppScan
* XSS Cheat Sheet
* OWASP Top 10

------------------------------------------------------------
How To Build A Threat Model
------------------------------------------------------------

At the end of the review, you should have a thread model and
an incident response plan as deliverables. In order to generate
these, following these steps:

* find risks to be mitigated or accepted at every stage
* follow the anvil reviews
* use a design review template or checklist
* use an anvil thread modeling template
* identify input data and output data and its flow
* identify data classifications and its flow
* identification, authorization, authentication
* check that test modules and code is disabled or removed
