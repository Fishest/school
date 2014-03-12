==============================================================
Week 5: Notifications
==============================================================

--------------------------------------------------------------
Video 1: User Notifications (1)
--------------------------------------------------------------

There are two types of notifications that can be made:

* Toast - popups that take the view focus
* Notifcation Area - appears in the upper system bar

Toast messages are used to present quick information to the
user and they automatically fade in and fade out. Custom toast
messages can be created by specifying a custom view to apply
to the toast. An example of using various toast messages:

.. code-block:: java

    // to make a simple toast
    Toast.makeText(context, text, duration).show()

    // to make a custom toast
    Toast toast = Toast.makeText(getApplicationContext());
    toast.setView(getLayoutInflater().inflate(R.layout.custom, null));
    toast.setDuration(Toast.LENGTH_LONG);
    toast.setGravity(Gravity.CENTER_VERTICAL, 0, 0);
    toast.show();

-.-------------------------------------------------------------
Video 2: User Notifications (2)
--------------------------------------------------------------

Android provides the Notification area for alerting users about
various events. It also provides the notification drawer so
users can pull it down and see more information about said
events.

In order to send a notification to the notification bar:

1. Decide on the title, detail, and a small icon for your event
2. Decide on the ticker text and a small icon for the notify area
3. Decide on the view for the drawer and the onClick action

In order to update the notification, Android supplies the
`NotificatinManager`.

.. TODO::
   Add notification bar example code

--------------------------------------------------------------
Video 3: Broadcast Receiver (1)
--------------------------------------------------------------

`BroadcastReceiver` is a base class for components that receive
and react to various events. In order to work, they register
to receive events that they are interested in. Events that
occur are represented as `Intents` that are then broadcasted
to the system. Android then routes these intents to the registered
parties' `onReceive(Intent intent)` method (JMS topics).

`BroadcastReceivers` can register in two ways:

1. Statically via the AndroidManifest.xml
2. Dynamically by calling the `registerReceiver` method

.. code-block:: xml

    <receiver
      android:enabled=["true" | "false"]
      android:exported=["true" | "false"]
      android:icon="drawable resource"
      android:label="string resource"
      android:name="string"
      android:permission="string">
      <intent-filter>
    </receiver>

.. code-block:: java

    Receiver receiver = new Receiver();
    String filter = "com.some.intent.filter";

    // This only captures broadcasts from the current application. To
    // Get system level events, use Context.registerReceiver
    LocalBroadcastManager manager = LocalBroadcastManager.getInstance(getApplicationContext());
    manager.registerReceiver(receiver, new IntentFilter(filter));
    
    // Then to send messages to the receiver, perhaps have an action
    // callback on some part of the UI
    button.setOnClickListener(view => manager.sendBroadcast(new Intent(filter)));
    
    // Before the application is destroyed, be sure to cleanup
    manager.unRegisterReceiver(receiver);

There are a few special broadcast methods that are supported:

* Normal vs Ordered

  - normal processing has the order undefined
  - orderd processes intents in a sequential priority based order

* Stick vs Non-Sticky

  - sticky will persist so future registers will see the event (battery level)
  - non-sticky will be discarded after the notification (current area)

* With special permissions (only allow if receivers have needed permission)

To debug notifications, there are a number of helpful tools:

* `Intent.setFlag(FLAG_DEBUG_LOG_RESOLUTION)` to log the notification
* `adb shell dumpsys Activity name` for dynamically registered recievers
* `adb shell dumpsys package` for statically registered recievers

--------------------------------------------------------------
Video 4: Broadcast Receiver (2)
--------------------------------------------------------------

Intents are delivered by calling `onReceive` and passing in:

1. The context in which the receiver is running
2. The intent that was received

The intent handler is run as a high priority task on the main
thread, so anything it does should be short lived. If your
handler has a lot of work to do, push the bottom half to a
service to be completed.

As the `Receiver` is no longer considered valid after the
`onReceive` returns, no asynchronous operations can be started
(showing a dialog, starting an activity with result, etc).

To order the broadcasts specifically, use the following methods:

.. code-block:: java

    void sendOrderedBroadcast(Intent intent, String permission);
    void sendOrderedBroadcast(Intent intent, String permission,
        BroadcastReceiver receiver, Handler scheduler, int initialCode,
        String initialData, Bundle initialExtras);

Sticky intents work by caching the received intents in the anroid
system. Newer intents simply overwrite the older ones. When a new
dynamically registered `BroadcastReceiver` is registered, any cached
intents that match the intent filter are broadcasted. This means that
one sticky intent is returned for each sticky intent registered for.

.. code-block:: java
   
    // In order to send these, the broadcaster must have the
    // BROADCAST_STICKY permission
    void sendStickyBroadcast(Intent intent);
    void sendStickyBroadcast(Intent intent, BroadcastReceiver receiver,
        Handler scheduler, int initialCode, String initialData,
        Bundle initialExtras);

    if (isInitialStickyBroadcast()) {
        // check if this is the cached value or a fresh value
    }

--------------------------------------------------------------
Video 5: Threads, AsyncTasks, and Handlers (1)
--------------------------------------------------------------

This was basically a review of Java threads. It also made clear
the common advice to not run long running tasks on the main UI
thread. Furthermore, UI update cannot be performed on a non-UI
thread:

.. code-block:: java

    // both of the following methods can be used to run code
    // on the UI thread of a view or activity.
    boolean View.post(Runnable action);
    void Activity.runOnUiThread(Runnable action);

    // to perform a long activity with a result on a given
    // view, run a thread and then post to the UI thread
    new Thread(new Runnable() {
        public void run() {
            Bitmap bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.background);
            view.post(new Runnable() {
                public void run() {
                    view.setImageBitmap(bitmap)
                }
            });
    ).start();

--------------------------------------------------------------
Video 6: Threads, AsyncTasks, and Handlers (2)
--------------------------------------------------------------

`AsyncTask` is supplied by Android to provide a structured way
to manage work involving background and UI threads. The
background thread performs work and indicates its progress in some
way. The UI thread performs task setup, publishing intermediate
progress, and using the final result:

.. code-block:: java

    // simply implement this generic task worker
    class AsyncTask<Params, Progress, Result> {   // specify the parameter types
        void onPreExecute();                      // run on UI thread before background work
        void doInBackground(Params... params);    // runs on background thread
        void publishProgress(Progress... values); // called from background
        void onProgressUpdate(Progress... values) // invoked on UI thread
        void onPostExecute(Result result);        // run on UI thread after doInBackground
    }

`Handler` is used to hand off work between two tasks (between
any two threads, not just UI). Each `Handler` is associated with
a thread. One thread can hand off work to another by sending
messages and posting `Runnables` to a `Handler` associated with
the other thread:

.. code-block:: java

    // the following can post runnables to the work queue
    boolean post(Runnable runnable);
    boolean postAtTime(Runnable runnable, long uptimeMillis);
    boolean postDelayed(Runnable runnable, long delayedMillis);

    // To work with messages, create a message and set its contents
    // The overridden handler will then handle these messages on the
    // UI thread.
    Message message = handler.obtainMessage(int code, Object param);
    handler.sendMessage(message);
    handler.sendMessageAtFrontOfQueue(message);
    handler.sendMessageAtTime(message, long uptimeMillis);
    handler.sendMessageDelayed(message, long delayedMillis);

Each android threada is associated with a MessageQueue and a
Looper. The message queue holds messages and runnables to be
dispatched by the looper. When a message or runnable is posted
to a thread, it is added to that thread's message queue to be
processed when it is dequeue by the looper. If the object in
the queue is a Runnable, the thread simply calls `run()` on it.
If it is a `Message`, the `handleMessage()` method is called.

--------------------------------------------------------------
Video 7: Alarms
--------------------------------------------------------------

`Alarms` are a mechanism for sending `Intents` at some point in
the future. This allows one application to make code execute,
even when that application is no longer running. Once registered,
`Alarms` remain active even if the device is asleep. The alarm
can then be configured to wake the sleeping device or retain
the alarm event until the next time the device is woken up.
Alarms continue to run until the device is shut down, at which
point all the alarms are cancelled. Examples of using alarms:

* MMS for the retry scheduler
* Settings for the bluetooth discoverable timeout
* Phone for user information cache (timeout reprime)

`Alarms` are created and managed by interacting with the
`AlarmManager`:

.. code-block:: java

    // to create alarms, use one of the supplied methods
    // the last method allows android to optimize or batch the
    // events to prevent waking up the device too many times.
    AlarmManager manager = (AlarmManager)getSystemService(Context.ALARM_SERVICE);
    manager.set(int type, long triggerAtTime, PendingIntent operation);
    manager.setRepeating(int type, long triggerAtTime, long interval, PendingIntent operation);
    manager.setInexactRepeating(int type, long triggerAtTime, long interval, PendingIntent operation);
    manager.cancel(intent);

    // If you use the last method, you must use one of the following
    // interval options, otherwise the method devolves to setRepeating
    INTERVAL_FIFTEEN_MINUTES
    INTERVAL_HALF_HOUR
    INTERVAL_HOUR
    INTERVAL_HALF_DAY
    INTERVAL_DAY

There are a number of configurability options involving the
alarms. The first of which is how time is interpreted:

* Realtime - relative to system clock
* Elapsed - relative to system uptime

Next, the choice needs to be made what to do when the
alarm goes off when the device is sleeping:

* Wake up device and deliver intent
* Wait to deliver intent until device wakes up

All of these options are reflected in the following type
constants:

* RTC_WAKEUP
* RTC
* ELAPSED_REALTIME
* ELAPSED_REALTIME_WAKEUP

To create a `PendingIntent`, there are a few methods:

.. code-block:: java

    PendingIntent getActivity(Context context, int requestCode,
        Intent intent, int flags, Bundle options);

    PendingIntent getBroadcast(Context context, int requestCode,
        Intent intent, int flags);

    PendingIntent getService(Context context, int requestCode,
        Intent intent, int flags);

--------------------------------------------------------------
Video 8: Networking (1)
--------------------------------------------------------------

Basically a recap of sockets, HTTP, JSON, and XML. Android
supplies a collection of utilities alongside the java BCL to
help perform networking:

* `Socket`
* `HttpURLConnection`
* `AndroidHttpClient`

.. TODO::
   Copy implementation code

--------------------------------------------------------------
Video 9: Networking (2)
--------------------------------------------------------------

Basically a recap of JsonParser.

.. TODO::
   Copy implementation code
