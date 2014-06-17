================================================================================
Amazon Simple Workflow Service Flow Framework
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

The flow framework relies upon four core technologies:

* `Promise<T>`
  Represents the future result of an activity or asynchronous method. The primary
  use of these objects is to manage data flow between asynchronous components.
  Flow handles this by deferring execution of the next activity until the passed
  in promise object is ready.

* `Settable<T>`
  This is a subtype of the promise type and functions exactly the same. In this
  case though, one needs to manually set the resulting value of the operation
  instead of the framework doing it for them.

* `Activity`
  These are mechanisms for distributing tasks across multiple processes and
  perhaps across multiple systems. Although the code is called like an
  imperitive method, they are called asynchronously and SWF mediates
  communication between a workflow and the other activies. These work by
  returning a promise when they are executed allowing the remaining code
  to operate with them.

* `@Asynchronous`
  This decoration allows a method to operate very much like another activity.
  If the decorated method receives a promise type, it will delay being called
  until the promise is ready so that the code can simply call the promise `get`
  method and not have to bother dealing with the asynchronous nature of flow.
  Calling the method thus returns immediately and is scheduled along side the 
  supplied promise.

--------------------------------------------------------------------------------
Repeatedly Execute An Activity
--------------------------------------------------------------------------------

If one wants to call a method `N` times, they cannot simply call it in a loop
like the following java code. This is because the methods are asynchronous and
will all be scheduled at the same time and possibly run in parallel:

.. code-block:: java

    for (int i = 0; i < N; ++i) {  // the next operation will not block for the previous
        client.doSomething();      // these will all be run concurrently
    }

One way to handle this is to chain the next call on the previous call's promise:

.. code-block:: java

    @Override
    public void loop(int N) {
        if (n > 0) {
            Promise<Void> hasRun = Promise.Void();   // so the first iteration will run
            for (int i = 0, i < n; ++i) {            // loop through each activity
                hasRun = client.doSomething(hasRun); // chain the next run to the previous
            }
        }
    }

Another way is to use a recursive asynchronous method to iterate. This differs
from the previous implemenation in that only one execution is pending at a given
time while the for loop puts `N` tasks in a pending state waiting for the previous
task to be completed:

.. code-block:: java

    @Override
    public void startWorkflow() {
        Promise<Integer> count = client.getRecordCount();
        processRecords(count);
    }

    @Asynchronous
    public void processRecords(Promise<Integer> count) {
        processRecords(count.get());
    }

    @Asynchronous
    public void processRecords(int count, Promise<?>... waitFor) {
        if (count >= 1) {
            Promise<Void> nextWaitFor = client.processRecords();
            processRecords(count - 1, nextWaitFor);
        }
    }

Finally, the equivalent of a do-while loop can be implemented using the
same implementation of the recursive loop, but this time only recursing
while the sentinal is still valid:

.. code-block:: java

    @Override
    public void doWhile() {
        doBody();
    }

    @Asynchronous
    private void doBody() {
        Promise<Integer> result = client.getRandomNumber();
        whileNext(result);
    }

    @Asynchronous
    private void whlieNext(Promise<Integer> result) {
        if (result.get() >= 1) {
            doBody();
        }
    }

--------------------------------------------------------------------------------
Execute Multiple Activities Concurrently
--------------------------------------------------------------------------------

If one needs to run multiple workflows concurrently and then combine their results
(like a map reduce), a simple solution like the following can be used:

.. code-block:: java

    @Override
    public void runFixed() {
        Promise<Integer> result1 = client.generateRandom();
        Promise<Integer> result2 = client.generateRandom();
        reduceResults(result1, result2);
    }

    @Asynchronous
    public void reduceResults(Promise<Integer> result1, Promise<Integer> result2) {
        if (result1.get() + results2.get() > 5) {
            client.generateRandom();
        }
    }

If there are a a dynamic number of results to generate and then reduce,
simply use a list to accumulate the results:

.. code-block:: java

    @Override
    public Promise<Integer> runDynamic(int count) {
        List<Promise<Integer>> results = new ArrayList<Promise<Integer>>();
        for (int i = 0; i < count; ++i) {
            Promise<Integer> result = client.generateRandom();
            results.add(result);
        }
        Promise<Integer> sum = reduceResults(results);
        return client.reportResults(sum);
    }

    //
    // The @Wait below is to instruct flow to wait for all the promises to
    // finish since they are wrapped in a list.
    //
    @Asynchronous
    public Promise<Integer> reduceResults(@Wait List<Promise<Integer>> results) {
        int sum = 0;
        for (Promise<Integer> result : results) {
            sum += result.get();
        }
        return Promise.asPromise(sum);
    }

If multiple activities need to be executed concurrently, but only the
first one to finish used (say to hedge requests), one can use the try-catch
blocks and cancel the others from the first to finish. Although the try-catch
block isn't needed, it allows for the other executions to be cancelled:

.. code-block:: java

    public class PickFirstBranchWorkflow {

        private TryCatch branch1;
        private TryCatch branch2;

        //
        // The OrPromise completes when one of the promises is complete.
        // There is also the AndPromise which completes when both of the
        // supplied promises complete.
        //
        @Override
        public Promise<List<String>> search(final String query) {
            Promise<List<String>> result1 = searchOnCluster1(query);
            Promise<List<String>> result2 = searchOnCluster2(query);
            OrPromise branch = new OrPromise(result1, result2);
            return processResults(branch);
        }

        //
        // And similar for the searchOnCluster2. The chain operation allows
        // another part of the operation to use the original promise.
        //
        private Promise<List<String>> searchOnCluster1(final String query) {
            final Settable<List<String>> result = new Settable<List<String>>();
            branch1 = new TryCatch() {
                @Override
                protected void doTry() throws Throwable {
                    Promise<List<String>> response = client1.search(query);
                    result.chain(response);
                }

                @Override
                protected void doCatch(Throwable ex) throws Throwable {
                    if (!(ex instanceof CancellationException)) {
                        throw ex;
                    }
                }
            };
            return result;
        }

        //
        // Need to make sure the order is correct and matches which branch
        // is which so we can cancel the right branch.
        //
        private Promise<List<String>> processResults(OrPromise result) {
            Promise<List<String>> output  = null;
            Promise<List<String>> result1 = (Promise<List<String>>)result.getValues()[0];
            Promise<List<String>> result2 = (Promise<List<String>>)result.getValues()[1];

            if (result1.isReady()) {
                output = result1;
                if (!result2.isReady()) {
                    result2.cancel(null);
                }
            } else {
                output = result2;
                result1.cancel(null);
            }

            return output;
        }
    }

--------------------------------------------------------------------------------
Execute Workflow Logic Conditionally
--------------------------------------------------------------------------------

If your workflow logic needs to choose an activity to perform based on a computed
value, simply pass that value to a new asynchronous method to choose:

.. code-block:: java

    @Override
    public void processOrders() {
        Promise<OrderChoice> choice = client.getItemOrder();
        Promise<Void> waitFor = processItemOrder(choice);
        client.finishOrder(waitFor);
    }

    @Asynchronous
    private Promise<Void> processItemOrder(Promise<OrderChoice> choice) {
        switch (choice.get()) {
            case APPLE:   return client.getApple();
            case ORANGE:  return client.getOrange();
            case CABBAGE: return client.getCabbage();
        }
    }

If one needs to execute multiple activities based on conditional
logic, figure out which ones to run, perform them in parallel,
then merge the results as the final response:

.. code-block:: java

    @Override
    public void processOrders() {
        Promise<List<OrderChoice>> choices = client.getBasketOrder();
        Promise<List<Void>> waitFor = processBasketOrder(choices);
        client.finishOrder(waitFor);
    }

    @Asynchronous
    public Promise<List<Void>> processBasketOrder(Promise<List<OrderChoice>> basket) {
        List<Promise<Void>> results = new ArrayList<Promise<Void>>();
        for (OrderChoice choice : basket.get()) {
            Promise<Void> result = processSingleOrder(choice);
            results.add(result);
        }

        return Promises.listOfPromisesToPromise(results);
    }

    @Asynchronous
    public Promise<Void> processSingleChoice(OrderChoice choice) { ... }

--------------------------------------------------------------------------------
Complete An Activity Task Manually
--------------------------------------------------------------------------------

If you need some form of manual intervention to complete an activity task (say
have an employee verify a step), you can use the `@ManualActiviyCompletion`
decorator. This allows the activity to return immediately and then be completed
later:

.. code-block:: java

    @Override
    public void startWorkflow() {
        Promise<Void> autoResult = client.automaticActivity();
        Promise<String> humanResult = client.humanActivity(autoResult);
        client.sendNotification(humanResult);
    }

    //
    // As this is a manual activity completion, the return from the
    // activity (null) is simply ignored and the resulting Promise<String>
    // remains unready. The unique supplied task token can be used to later
    // finish the workflow.
    //
    @Override
    @ManualActivityCompletion
    public String humanActivity() {
        ActivityExecutionContext context = contextProvider.getActivityExecutionContext();
        String token = context.getTaskToken();
        System.out.println("Task received, completion token: " + token);
        return null;
    }

The human task can be completed by any external program using the supplied
token. What follows is a simple console application that does just this.
Other approaches are to say store the token in a database and have a polling
program go through every so often and complete the waiting tasks:

.. code-block:: java

    public class HumanTaskConsole {
        public static void main(String[] args) throws IOException {
            String token  = getTaskToken(); // from some user input
            String result = getResult();    // from some user input

            AmazonSimpleWorkflow service = createSWFClient();
            ManualActivityCompletionClientFactory factory =
                new ManualActivityCompletionClientFactoryImpl(service);
            ManualActivityCompletionClient client = factory.getClient(token);
            client.complete(result);
        }
    }

--------------------------------------------------------------------------------
Handling Errors Thrown Asynchronously
--------------------------------------------------------------------------------

If errors are thrown asynchronously, the standard java mechanisms for handling
errors (try-catch) will not work. Instead, the flow framework provides a number
of helper utilities, formally: `TryCatch`, `TryFinally`, and `TryCatchFinally`:

.. code-block:: java

    @Override
    public void startWorkflow() {
        final Promise<Integer> resourceId = client.allocateResource();

        //
        // This actually executes concurrently with the allocateResource
        // call as either could start or finish first. If allocateResource
        // throws however:
        // 1. if doTry hasn't started yet, the whole TryCatchFinally is cancelled
        // 2. if doTry has started, all of its pending tasks are cancelled
        // 2a. after that doCatch is called with a CancellationException
        // 2b. after that doFinally is called
        //
        new TryCatchFinally() {
            @Override
            protected void doTry() throws Throwable {
                client.useResource(resourceId);
            }

            //
            // Activities performed in the doCatch or doFinally
            // cannot be cancelled, only activities performed in
            // the doTry.
            //
            @Override
            protected void doCatch(Throwable ex) throws Throwable {
                client.rollbackChanges(resourceId);
            }

            //
            // The finally method will always be called regardless
            // if an exception was thrown or not.
            //
            @Override
            protected void doFinally() throws Throwable {
                if (resourceId.isReady()) {
                    client.cleanUpResource(resourceId);
                }
            }
        }
    }

If one needs to handle exceptions asynchronously, simple store the throwable
in a `Settable` and then call the asynchronous method:

.. code-block:: java

    @Override
    public void startWorkflow() throws Throwable {
        final Settable<Throwable> exception = new Settable<Throwable>();
        final Promise<Integer> resourceId = client.allocateResource();

        new TryCatch() {
          //
          // If the useResource call throws, the waitFor will never be
          // set and thus the call to setState here will never proceed.
          //
          @Override
          protected void doTry() throws Throwable {
              Promise<Void> waitFor = client.useResource(resourceId);
              setState(exception, null, waitFor);
          }

          //
          // The setState uses a void promise to allow setState to
          // proceed immeidately.
          //
          @Override
          protected void doCatch(Throwable ex) throws Throwable {
              setState(exception, ex, Promise.Void());
          }
        };
        handleException(exception, resourceId);
    }

    //
    // This will block until the exception and resourceId are set.
    //
    @Asynchronous
    private void handleException(Promise<Throwable> exception, Promise<Integer> resourceId) {
        Throwable ex = exception.get();
        if (ex != null) {
            if (ex instanceof ActivityTaskFailedException) {
                Throwable inner = ex.getCause();
                if (inner instanceof ResourceNoResponseException) {
                    client.reportBadResource(resourceId.get());
                } else if (inner instance of ResourceNotAvailableException) {
                    client.refreshResourceCatalog(resourceId.get());
                } else {
                    throw ex;
                }
            } else {
                throw ex;
            }
        }
    }

    //
    // The no wait tells flow to not block the workflow on waiting
    // for the supplied parameter to become ready. However, it will
    // wait on the result of the waitFor which was supplied.
    //
    @Asynchronous
    private void setState(@NoWait Settable<Throwable> exception,
        Throwable ex, Promise<Void> waitFor) {

        exception.set(ex);
    }

--------------------------------------------------------------------------------
Retry Failed Asynchronous Code
--------------------------------------------------------------------------------

If a failure occurs in asynchronous code, it may be ephemeral in which case it
may be prudent to try the execution one or more times based on some strategy.
One such strategy is to simply keep retrying the code until it succeeds or a
certain number of attempts have failed:

.. code-block:: java

    public class RetryableWorkflow {
        private final int maxRetries = 10;
        private int retryCount = 0;

        @Override
        public void process() {
            final Settable<Boolean> shouldRetry = new Settable<Boolean>();
            new TryCatchFinally() {
                @Override
                protected void doTry() throws Throwable {
                    client.unreliableActivity();
                }
                @Override
                protected void doCatch(Throwable ex) throws Throwable {
                    if (++retryCount <= maxRetries) {
                        shouldRetry.set(true);
                    } else {
                        throw ex;
                    }
                }
                @Override
                protected void doFinally() throws Throwable {
                    if (!shouldRetry.isReady()) {
                        shouldRetry.set(false);
                    }
                }
            };
            retryUntilSuccess(shouldRetry);
        }
    }

    //
    // The retry is performed here instead of in the doCatch as
    // in the doCatch we cannot perform any cancellation, while
    // here we can.
    //
    @Asynchronous
    private void retryUntilSuccess(Promise<Boolean> shouldRetry) {
        if (shouldRetry.get()) {
            process();
        }
    }

Instead of calling back to back after a failure, it is usually prudent to
wait a little while as the resource might still be unavailable. The Flow
framework provides an exponential retry strategy for this purpose which
supplies the following tuning parameters:

* the initial retry wait time
* the back off coefficient (default of 2.0)
* the maximum number of retry attempts (default unlimited)
* the maximum retry interval (default unlimited)
* the expiration time after which the process will fail (default unlimited)
* the exceptions that will trigger the retry process (default all throwables)
* the exceptions that will not trigger a retry (default none)

.. code-block:: java

    //
    // The time calculation for the delay is as follows:
    // retryInterval = initialInterval * Math.pow(backoffCoeff, numberOfTries - 2)
    //
    @Activities(version = "1.0")
    @ActivityRegistrationOptions(
        defaultTaskScheduleToStartTimeoutSeconds = 30,
        defaultTaskStartToCloseTimeoutSeconds = 30)
    public interface ExponentialRetryAnnotationActivities {

        //
        // After applying this decorator, the framework will automatically
        // handle applying the retry policy.
        //
        @ExponentialRetry(
            initialRetryIntervalSeconds = 5,
            maximumAttempts = 5,
            exceptionsToRetry = IllegalStateException.class)
        public void unreliableActivity();
    }

If you don't want to statically compile the retry policy and would instead
like runtime control, you can simply apply the decorator at run time:

.. code-block:: java

    public class DecoratorRetryWorkflowImpl implements RetryWorkflow {
        private RetryActivitiesClient client = new RetryActivitiesClientImpl();

        public void process() {
            long initialRetrySeconds = 5;
            ExponentialRetryPolicy retryPolicy = new ExponentialRetryPolicy(initialRetrySeconds)
                .withMaximumAttempts(5);
            Decorator decorator = new RetryDecorator(retryPolicy);
            client = decorator.decorate(RetryActivitiesClient.class, client);
            handleUnreliableActivity();
        }

        public void handleUnreliableActivity() {
            client.unreliableActivity();
        }
    }

The most flexible approach is to simply implement the retry logic yourself:

.. code-block:: java

    public class CustomLogicRetryWorkflowImpl implements RetryWorkflow {

        @Override
        public void process() {
            callActivityWithRetry();
        }

        @Asynchronous
        public void callActivityWithRetry() {
            final Settable<Throwable> failure = new Settable<Throwable>();
            new TryCatchFinally() {
                protected void doTry() throws Throwable {
                    client.unreliableActivity();
                }
                protected void doCatch(Throwable e) {
                    failure.set(e);
                }
                protected void doFinally() throws Throwable {
                    if (!failure.isReady()) {
                        failure.set(null);
                    }
                }
            };
            retryOnFailure(failure);
        }

        @Asynchronous
        private void retryOnFailure(Promise<Throwable> exception) {
            Throwable failure = exception.get();
            if (failure != null && shouldRetry(failure)) {
                callActivityWithRetry();
            }
        }

        protected Boolean shouldRetry(Throwable e) {
            //custom logic to decide to retry the activity or not
            return true;
        }
    }

--------------------------------------------------------------------------------
Wait For A Signal
--------------------------------------------------------------------------------

The flow framework includes the ability to define your own signal using the
`@Signal` decorator in the activity interface. This combined with the workflow
timer can be used to signal tasks and deciding when a task has waited long enough:

.. code-block:: java

    @Workflow
    @WorkflowRegistrationOptions(defaultExecutionStartToCloseTimeoutSeconds = 300)
    public interface WaitForSignalWorkflow {

        @Execute(version = "1.0")
        public void placeOrder(int amount);

        @Signal
        public void changeOrder(int amount);
    }


    public class WaitForSignalWorkflowImpl implements WaitForSignalWorkflow {
        private Settable<Integer> signalReceived = new Settable<Integer>();
        private final int changeOrderPeriod = 30;


        public WaitForSignalWorkflowImpl() {
            DecisionContextProvider provider = new DecisionContextProviderImpl();
            DecisionContext context = provider.getDecisionContext();
            clock = context.getWorkflowClock();
        }

        @Override
        public void placeOrder(int amount) {
            Promise<Void> timer = startDaemonTimer(changeOrderPeriod);
            OrPromise signalOrTimer = new OrPromise(timer, signalReceived);
            processOrder(amount, signalOrTimer);
        }

        @Asynchronous
        private void processOrder(int originalAmount, Promise<?> waitFor) {
            int amount = originalAmount;
            if (signalReceived.isReady())
                amount = signalReceived.get();
                client.processOrder(amount);
        }

        //
        // If this is called, the order will be processed using
        // the newly supplied value and the timer will be ignored.
        //
        @Override
        public void changeOrder(int amount) {
            if(!signalReceived.isReady()){
                signalReceived.set(amount);
            }
        }

        //
        // If this timer goes off, then the original order
        // will be used. The returned promise becomes valid when
        // the timer expires. The daemon flag tells the flow framework
        // to automatically cancel this task when the workflow completes.
        //
        @Asynchronous(daemon = true)
        private Promise<Void> startDaemonTimer(int seconds) {
            Promise<Void> timer = clock.createTimer(seconds);
            return timer;
        }
    }
