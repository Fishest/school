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

--------------------------------------------------------------
Video 6: Threads, AsyncTasks, and Handlers (2)
--------------------------------------------------------------

--------------------------------------------------------------
Video 7: Alarms
--------------------------------------------------------------

--------------------------------------------------------------
Video 8: Networking (1)
--------------------------------------------------------------

--------------------------------------------------------------
Video 9: Networking (2)
--------------------------------------------------------------
