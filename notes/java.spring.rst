================================================================================
Java Spring Reference Manual
================================================================================

http://www.springsource.org/projects
http://static.springsource.org/spring/docs/3.2.x/spring-framework-reference/html/

--------------------------------------------------------------------------------
Spring Modules
--------------------------------------------------------------------------------

**Core Container**

The Core Container consists of the Core, Beans, Context, and Expression Language
modules.

The Core and Beans modules provide the fundamental parts of the framework,
including the IoC and Dependency Injection features. The BeanFactory is a
sophisticated implementation of the factory pattern. It removes the need for
programmatic singletons and allows you to decouple the configuration and
specification of dependencies from your actual program logic.

The Context module builds on the solid base provided by the Core and Beans
modules: it is a means to access objects in a framework-style manner that is
similar to a JNDI registry. The Context module inherits its features from the
Beans module and adds support for internationalization (using, for example,
resource bundles), event-propagation, resource-loading, and the transparent
creation of contexts by, for example, a servlet container. The Context module
also supports Java EE features such as EJB, JMX ,and basic remoting. The
ApplicationContext interface is the focal point of the Context module.

The Expression Language module provides a powerful expression language for
querying and manipulating an object graph at runtime. The language supports
setting and getting property values, property assignment, method invocation,
accessing the context of arrays, collections and indexers, logical and
arithmetic operators, named variables, and retrieval of objects by name from
Spring's IoC container. It also supports list projection and selection as well
as common list aggregations.

**Data Access/Integration**

The Data Access/Integration layer consists of the JDBC, ORM, OXM, JMS and Transaction modules.
The JDBC module provides a JDBC-abstraction layer that removes the need to do
tedious JDBC coding and parsing of database-vendor specific error codes.

The ORM module provides integration layers for popular object-relational mapping APIs,
including JPA, JDO, Hibernate, and iBatis. Using the ORM package you can use all of
these O/R-mapping frameworks in combination with all of the other features Spring offers,
such as the simple declarative transaction management feature mentioned previously.

The OXM module provides an abstraction layer that supports Object/XML mapping
implementations for JAXB, Castor, XMLBeans, JiBX and XStream.

The Java Messaging Service (JMS) module contains features for producing and
consuming messages.

The Transaction module supports programmatic and declarative transaction management
for classes that implement special interfaces and for all your POJOs (plain olds
 Java objects).

**Web**

The Web layer consists of the Web, Web-Servlet, Web-Struts, and Web-Portlet modules.
Spring's Web module provides basic web-oriented integration features such as
multipart file-upload functionality and the initialization of the IoC container
using servlet listeners and a web-oriented application context. It also contains
the web-related parts of Spring's remoting support.

The Web-Servlet module contains Spring's model-view-controller (MVC) implementation
for web applications.

The Web-Struts module contains the support classes for integrating a classic Struts
web tier within a Spring application.

The Web-Portlet module provides the MVC implementation to be used in a portlet
environment and mirrors the functionality of Web-Servlet module.

**AOP and Instrumentation**

Spring's AOP module provides an  aspect-oriented programming implementation
allowing you to define, for example, method-interceptors and
pointcuts. The separate Aspects module provides integration with AspectJ.

The Instrumentation module provides class instrumentation support and
classloader implementations to be used in certain application servers.

**Test**

The Test module supports the testing of Spring components with JUnit or TestNG.
It provides consistent loading of Spring ApplicationContexts and caching of
those contexts. It also provides mock objects that you can use to test your code
in isolation.

--------------------------------------------------------------------------------
Setting up Logging
--------------------------------------------------------------------------------

Sprint has a hard requirement on some logging framework being available (some
implementation of the JCL). Out of the box, Spring can work with: commons-logging,
slf4j, and log4j (with log4j being the easiest to configure and use).

Here is a simple log4j maven configuration::

    <dependencies>
       <dependency>
          <groupId>org.springframework</groupId>
          <artifactId>spring-context</artifactId>
          <version>3.0.0.RELEASE</version>
          <scope>runtime</scope>
       </dependency>
       <dependency>
          <groupId>log4j</groupId>
          <artifactId>log4j</artifactId>
          <version>1.2.14</version>
          <scope>runtime</scope>
       </dependency>
    </dependencies> 


Here is a simple log4j.properties configuration file which needs to be present
somewhere in the classpath::

    log4j.rootCategory=INFO, stdout
    
    log4j.appender.stdout=org.apache.log4j.ConsoleAppender
    log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
    log4j.appender.stdout.layout.ConversionPattern=%d{ABSOLUTE} %5p %t %c{2}:%L - %m%n
    
    log4j.category.org.springframework.beans.factory=DEBUG


--------------------------------------------------------------------------------
Spring MVC
--------------------------------------------------------------------------------

http://docs.spring.io/spring/docs/current/spring-framework-reference/html/mvc.html

--------------------------------------------------------------------------------
Spring Testing
--------------------------------------------------------------------------------

http://docs.spring.io/spring/docs/current/spring-framework-reference/html/testing.html

--------------------------------------------------------------------------------
Spring Scheduling
--------------------------------------------------------------------------------

http://docs.spring.io/spring/docs/current/spring-framework-reference/html/scheduling.html

Spring abstracts its operations behind the `TaskExecutor` interface which is
simply a way to abstract the various implementations:

* `SimpleAsyncTaskExecutor` - thread per task
* `SyncTaskExecutor` - run on the calling thread
* `ConcurrentTaskExecutor` - explicitly configured java executor
* `ThreadPoolTaskExecutor` - simply java executor implementation
* `SimpleThreadPoolTaskExecutor` - based on Quartz's threadpool implementation
* `WorkManagerTaskExecutor` - CommonJ thread pool implementation

What follows is a simple example of using the `TaskExecutor` interface and
configuring an explicit instance:

.. code-block:: java

    import org.springframework.core.task.TaskExecutor;
    
    public class TaskExecutorExample {
    
        private class MessagePrinterTask implements Runnable {
    
            private String message;
    
            public MessagePrinterTask(String message) {
                this.message = message;
            }
    
            public void run() {
                System.out.println(message);
            }
    
        }
    
        private TaskExecutor taskExecutor;
   
        public TaskExecutorExample(TaskExecutor taskExecutor) {
            this.taskExecutor = taskExecutor;
        }
    
        public void printMessages() {
            for(int i = 0; i < 25; i++) {
                taskExecutor.execute(new MessagePrinterTask("Message" + i));
            }
        }
    }

.. code-block:: xml

    <bean id="taskExecutor"
      class="org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor">
      <property name="corePoolSize" value="5" />
      <property name="maxPoolSize" value="10" />
      <property name="queueCapacity" value="25" />
    </bean>
    
    <bean id="taskExecutorExample" class="TaskExecutorExample">
      <constructor-arg ref="taskExecutor" />
    </bean>

There is also the `TaskScheduler` abstraction which can be used to schedule
repeated tasks at some interval. There is also the `Trigger` interface which
can be used to schedule the next task based on the results of the current
one. There are a few implementations of the following interface:

* `CronTrigger` - for complex cron based schedules
* `PeriodicTrigger` - that accecpts a fixed period and delay

.. code-block:: java

    public interface Trigger {
        Date nextExecutionTime(TriggerContext triggerContext);
    }

    public interface TriggerContext {
        Date lastScheduledExecutionTime();
        Date lastActualExecutionTime();
        Date lastCompletionTime();
    }

There are implementations of the `TaskScheduler` that back up to the current
`ScheduledExecutorService` implementation as well as a few third party
implementations.

To make use of `Scheduled` or `Async` annotations, enable them on your
configuration classes:

.. code-block:: java

    @Configuration
    @EnableAsync
    @EnableScheduling
    public class TaskConfig {

        // scheduled methods must return void and not accept any arguments
        // if this is needed, they should be configured classes
        @Scheduled(fixedRate=5000)
        public void doSomething() { }

        @Scheduled(cron="\*/5 * * * * MON-FRI")
        public void doSomethingElse() { }

        // Async methods can take and return values, but they must be wrapped
        // in Future. The Async annotation can take a value to specify what
        // executor it should be run in. To catch exceptions from Async methods
        // implement the `AsyncUncaughtExceptionHandler` interface
        @Async
        public Future<String> doSomethingLater(String input) { }
    }

These interfaces also wrap `Quartz` pretty thinly, but allow one to drive
quartz code with a little less configuration.
