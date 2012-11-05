================================================================================
Apache Camel Introduction
================================================================================

--------------------------------------------------------------------------------
Configuration DSL
--------------------------------------------------------------------------------

The following three are equivalent::

    /* java */
    from("fiole:data/inbox".to("jsm:queue:order");
    
    /* spring */
    <route>
      <from uri="file:data:inbox" />
      <to uri="jms:queue:order" />
    </route>
    
    /* scala */
    from "file:data/inbox" -> "jms:queue:order"

There are also more advanced applications::

    from("file:data/inbox")
        .filter().xpath("/order[not(@test)]")
        .to("jms:queue:order");


--------------------------------------------------------------------------------
Messaging
--------------------------------------------------------------------------------

* org.apache.camel.Message - The fundamental data transfer entity

  - unique by protocol generate string or by default UID generator
  - camel attaches headers to message as needed for transport (String -> Object)
  - can also include attachments
  - the body is of type Object and can store any type of content
  - sender and receiver should understand how to interperet the content
  - a number of conversions happen automatically behind the scenes
  - a fault flag is also included

* org.apache.camel.Exchange - The abstract camel message exhange with in and out

  - basically the container for messages during routing
  - has a unique exchange id
  - identifies the message exchange patterns in use (InOnly, InOut)
  - Exception field if exceptions occur
  - Properties for the exchange
  - in message and out message (if InOut)

--------------------------------------------------------------------------------
CamelContext
--------------------------------------------------------------------------------

* The runtime container of camel
* Contains the components currently in use

  - can load on the fly, auto-discover, etc
  - these are the basic extension points of camel

* Contains the endpoints that have been created

  - these are the end of the message channel abstraction for camel
  - area neutral interface allowing systems to integrate
  - endpoints are specified by the uri dsl element

* Contains the routes that have been added

  - each route is unique and has a single input for messages
  - logging, debugging, monitoring, starting, stopping
  - route can be thought of as a graph of Processor nodes

* Contains the loaded type convertors
* Contains the loaded data formats
* Contains a registry to look up java beans (spring, osgi, jndi)
* Contains the loaded languages (xpath)

--------------------------------------------------------------------------------
Camel Endpoints
--------------------------------------------------------------------------------

The endpoint URI is disected as follows::

    file:data/inbox?delay=5000

    * file -> scheme selects FileComponent (factory)
    * data/inbox -> context path selects resource path
    * ?delay=500 -> extra options to supply
    
    The FileComponent is then supplied the remaining features to build
    a FileEndpoint. The endpoint is then a factory to creates Exchanges,
    Producers, and Consumers.

* The Producer is an entity cabable of creating and sending a message to the endpoint

  - when a message needs to be sent, creates an exchange
  - populates the exchange with compatible data from the supplied endpoint

    * a FileProducer will write the message to a file
    * a JmsProducer will map the message to a javax.jms.Message

  - sends the message along to be processed

* The Consumer is an entity cabable of receiving a message from the endpoint

  - when a message is received, wraps it in an exchange
  - populates the exchange with compatible data from the supplied endpoint
  - sends the message along to be processed
  - There are event driven and polling consumers (async and sync)

    * tcp/ip , jms queue are event driven consumers
    * file, ftp, and email are polling consumers


================================================================================
Routing with Camel
================================================================================

* A message router consumes messages from an input channel
* Depending on a set of conditions is sent to one or more output queues
* The conditions and processing steps between them are decoupled.

================================================================================
Transforming Data with Camel
================================================================================

* Data format transformation - the data format of the message is converted

  - csv record converted to xml

* Data type transformation - The data type of the message body is transformed

  - java.lang.String is transformed to a javax.jms.TextMessage

* This all occurs in the following typical six ways:

  - Data transformation in routes (Content Enricher EIPs)
  - Data transformation using components (eg. XSLT)
  - Data transformation using data formats (pair-wise conversion)
  - Data transformation using templates (eg. apache Velocity)
  - Data type transformation using Camel's type convertor mechanism (automatic)
  - Message transformation in component adapters

--------------------------------------------------------------------------------
Message Translator EIP (adapter pattern)
--------------------------------------------------------------------------------

Can perform this using a Processor, beans, or <transform>

* xslt -> chain.to("xslt://transform.xslt").to("jms:nextHop");

  - this searches in the classpath for the xslt file
  - can overload by specifying the prefix (file, http, etc)

* can marshall xml

  - chain.marshal().xstream().to("jms:nextHop");
  - chain.unmarshal().xstream().to("jms:nextHop");

* can also use the jaxb system

  - chain.marshal().jaxb().to("jms:nextHop");
  - chain.unmarshal().jaxb().to("jms:nextHop");
  - need to add a special file jaxb.index containing classes (one per line)

* Can add and use other data formats by implementing DataFormat (marshal, unmarshal)

  - crypto, csv, flatpack, gzip, jaxb, json, protobuf, soap
  - bindy maps csv to models (also FIX)
    
--------------------------------------------------------------------------------
Message Enricher EIP (decorator)
--------------------------------------------------------------------------------

Can perform this using two differnt methods in the DSL:

* pollEnrich - a consumer based enricher (supply a timeout)
* enrich - a producer based enricher

The enricher implements the AggregationStrategy interface.

--------------------------------------------------------------------------------
Type Conversion
--------------------------------------------------------------------------------

* The TypeConverter Registry contains a number of TypeConverter
* Has about 150 that are registered from scanning the class path
  - A listing of candidate jars is used to prevent scanning every jar in CP
  - META-INF/services/org/apache/camel/TypeConverter
* It works as follows::

    TypeConverter lookup(Class<?> toType, Class<?> fromType);
    T convertTo(Class<?> type, Object value);

    chain.convertBodyTo(String.class)

================================================================================
Camel with Beans
================================================================================

* Functions by using the Service Activator EIP (pg 98)
* The bean registry is pluggable (Spring is one such framework)

  - ApplicationContextRegistry (spring)
  - SimpleRegistry (used during unit testing or limited environments GAE)
  - JndiRegistry (can configure with spring)
  - OsgiServiceRegistry (can use with Spring Dynamic Modules)

* The camel registry is simple an adapter between the requester and the registry

  - A Service Provider Interface (SPI) at org.apache.camel.spi.Registry

* To select which method on the bean to call, camel goes through a semi-compilcated
  lookup algorithm with a number of rules. Long story short, either specify the
  bean method name, or decorate the bean method with a @Handler attribute.
* To select the parameters to bind to:

  - The camel core types will be automatically bound
  - Exchange, Message, CamelContext, TypeConverter, Registry, and Exception
  - The first method is bound to the message body
  - For other bindings, use the message annotations
  - @Body, @Header(name), @Property(name), @Properties, @Attachments
  - @Headers <for request InOnly>, @OutHeaders <for request response InOut>
  - The @OutHeaders Map is empty on the method invocation (save needed headers)

* Can also use language annotations (@XPath to @Groovy)

  - These can be used to specify how input parameters are created

================================================================================
Handling Exceptions in Camel (pg 120)
================================================================================

* based on if the error is recoverable, camel willl retry, propagate the error to
  the client, fail immediately, or something else.
* recoverable errors are Throwable or Exception and are accessed from the Exchange

  - void setException(Throwable cause);
  - Exception getExceptoin();

* irrecoverable errors set the message as faulted::

    Message message = Exchange.getOut();
    message.setFault(true);
    message.setBody("Invalid customer id");

* Error handling really only occurs in the exhange portion (not the transports)

  - some transports handle there errors in a number of different ways
  - PollingConsumerPollStrategy has a tempalte for handling errors in transport

* Camel supplies a number of error handler strategies (The first three extend
  RedeliveryErrorHandler, the last two don't):

  - DefaultErrorHandler - automatically enabled error handler
  - DeadLetterChanel - Implements the dead letter channel EIP
  - TransactionErrorHandler - transaction aware error handler
  - NoErrorHandler - disables error handling
  - LoggingErrorHandler - sents the errors to the logging handler

* Error handling is performed in the channel that is between each route component

  - error handling, message tracing, interceptors, etc are implemented here
  - by default, errors are not redelivered and exceptions are proagated back to callee

* The dead letter queue can route error messages to any endpoint::

    errorHandler(deadLetterChannel("log:dead?level=ERROR"));
    errorHandler(deadLetterChannel("jms:queue:dead").useOriginalMessage());
    errorHandler(defaultErrorHandler().maximumRedeliveries(5).redeliveryDelay(10000));
    ...
    Exception ex = exchange.getProperty(Exchange.CAUSED_EXCEPTION, Exception.class);

* Error Handler features

  - Redelivery Policies - a number of options to control how to retry
  - can redeliver sync (on same thread) or async (on another thread)
  - Scope
  - Exception Policies
  - Error Handling

* To handle faults, you have to explicitly enable them `chain.handleFault()`
* To handle specific exceptions use `onException` (it walks the chain from
  bottom to top to find the best candidate for processing)::

    chain.onException(ChildException.class).maximumRedliveries(3)
    chain.onException(LowerException.class).maximumRedliveries(5)
    ....
    throw new LowerException(); // would retry 5 times
    // if there are no matches, the default error handler configuration is used
    // if there are many subclasses, the exception with the shortest inheritance
    // gap is used. In case of a match, the first registered handler is used.

    chain.onException(OneException.class, TwoException.class, ThreeException.class)
      .to("log:xml?level=WARN");

* An example of performing error handling at the route scope::

    public void configure() {
        from("mina:tcp://0.0.0.0:4444?textline=true")
            .doTry()
                .process(new ValidateOrderId())
                .to("jms:queue:order.status")
                .process(new GenerateResponse());
            .doCatch(JmsException.class)
                .process(new GenerateFailureResponse())
            .end();
    }

* An example of performing error handling at the global scope::

    public void configure() {
        // handle this exception in this processor,
        // routing is thus not continued
        onException(JmsException.class)
            .handled(true)
            .process(new GenerateFailureResponse());

        // ignore this exception and continue
        onException(ValidationException.class)
            .continue(true);

        // custom retry logic
        onException(RandomException.class)
            .retryWhile(bean(MyRetryRules.class));

        from("mina:tcp://0.0.0.0:4444?textline=true")
            .process(new ValidateOrderId())
            .to("jms:queue:order.status")
            .process(new GenerateResponse());
            .process(new GenerateFailureResponse())
    }

* Other error handling utilities:

  - onWhen - a bean to check a precondition before handling
  - onRedeliver - a processor to operate with before redelivery
  - retryWhile - build customized retry logic for messages

================================================================================
Testing with Camel
================================================================================

* The following are a number of helper test classes:

  - org.apache.camel.test.TestSupport - junit 3 abstraction
  - org.apache.camel.test.CamelTestSupport - junit 3 abstraction
  - org.apache.camel.test.CamelSpringTestSupport - junit 3 abstraction
  - org.apache.camel.test.juni4.TestSupport
  - org.apache.camel.test.juni4.TestSupport
  - org.apache.camel.test.juni4.TestSupport

* Initialize the route in teh test class by implementing the createRouteBuilder::

    /**
     * if you already have a route created in your source tree
     */
    protected RouteBuilder createRouteBuilder() throws Exception {
        return new ExistingRoute();
    }

    /**
     * otherwise, wire it up in the test code
     */
    protected RouteBuilder createRouteBuilder() throws Exception {
        return new RouteBuilder() {
            @Override
            public void configure() throws Exception {
                from("file://target/inbox").to("file://target/outbox");
            }
        }
    }

    /**
     * for spring, use the CamelSpringTestSupport
     */
    protected AbstractXmlApplicationContext createApplicationContext() {
        return new ClassPathXmlApplicationContext("action/existingroute.xml");
        //return new FileSystemXmlApplicationContext("action/existingroute.xml");
    }

* To test in different environments, use the camel properties component::

    <!-- using a spring bean for properties -->
    <bean id="properties"
          class="org.apache.camel.component.properties.PropertiesComponent">
      <property name="location" value="classpath:example.properties" />
    </bean> 
    
    <camelContext id="camel" xmlns="http://camel.apache.org/schema/spring">
      <!-- can also use this instead of the previous spring bean -->
      <propertyPlaceholder id="properties" location="classpath:example.properties" />
      <route>
        <from uri="{{file.inbox}}" />
        <to uri="{{file.outbox}}" />
      </route>
    </camelContext>
    
    /**
     * And the spring properties file
     */
    file.inbox=target/inbox
    file.outbox=target/outbox

    /**
     * And to use the properties in the test
     */
    @EndpointInject(uri = "file:{{file.inbox}}")
    private ProducerTemplate inbox;

    private String inboxDir;
    private String outboxDir;

    public void setUp() throws Exception {
        super.setUp();

        inboxDir  = context.resolvePropertyPlaceholders("{{file.inbox}}");
        outboxDir = context.resolvePropertyPlaceholders("{{file.outbox}}");

        deleteDirectory(inboxDir);
        deleteDirectory(outboxDir);
    }

    @Test
    public void testMoveFile() throws Exception {
        inbox.sendBodyAndHeader("hello world", Exchange.FILE_NAME, "hello.txt");
    }

* To do this without spring, simply use the camel properties directly::

    protected CamelContext createCamelContext() throws Exception {
        CamelContext context = super.createCamelContext();
        PropertiesComponent prop = context.getComponent("properties", PropertiesComponent.class);
        prop.setLocation("classpath:rider-prod.properties");
        return context;
    }


================================================================================
Components
================================================================================

* direct:name - sync direct connect two routes
* seda:name - async direct connect two routes (with blocking queues)
* mock:name - can run asserts on the context (think jmock)
* velocity:name - run the message through the velocity tempalte engine
