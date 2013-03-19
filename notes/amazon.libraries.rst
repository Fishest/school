============================================================
Amazon Libraries Knowledge
============================================================

------------------------------------------------------------
Amazon Coral
------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Types
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Service data is described in terms of shapes that can be
reused, adorned with traits, documentation, constraints, and
more. The primitive shapes that are defined are:

* Boolean(true, false)
* Byte[-127, 127]
* Timestamp(millis since epoch)
* Character[UTF8]
* Double[IEEE 754 double]
* Float[IEEE 754 float]
* Integer[-2^32, +2^32]
* Long[-2^64, +2^64]
* Short[-2^16, +2^16]
* String[unlimited chars]
* Blob[unlimited bytes]
* BigInteger[arbitrary int]
* BigDecimal[arbitrary decimal]
* Envelope[container for other shapes]

There are also complex shape collections:

* List - homogeneous collection
* Map - key => value
* Structure - collection of fields

Finally, there are service shapes:

* Operation - a service operation
* Service - describes a service; collection of operations

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Defining Model
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The simplest model that can be defined is as follows:
.. code-block:: xml

    <definition version="1.0" assembly"com.amazon.sharing.service">
      <integer name="first-name" />
    </definition>

To add elements to a structure, use the member name:
.. code-block:: xml

    <!-- can be referenced with users$member -->
    <!-- can be referenced with com.amazon.sharing.service#users$member -->
    <definition version="1.0" assembly"com.amazon.sharing.service">
      <list name="users">
        <member target="member" />
      </list>
    </definition>


