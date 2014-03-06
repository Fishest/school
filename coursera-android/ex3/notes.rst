==============================================================
Week 3
==============================================================

--------------------------------------------------------------
Video 1: The Intent Class (1)
--------------------------------------------------------------

The `Intent` class is a data structure that represents:

* An operation to be performed
* An event that has occurred

Intent can be composed of multiple fields:

* Action: the action requested to be performed,
  `ACTION_DIAL`, `ACTION_SYNC`, `ACTION_EDIT`, `ACTION_MAIN`
* Data: data to be passed to the action modeled as a URI
* Category: the categories that can handle the supplied action
  `CATEGORY_BROWSABLE`, `CATEGORY_LAUNCHER`
* Type: the mimetype of the supplied data (if not supplied, this will be inferred)
* Component: the singular activity that should recieve the intent
  `setCompontent`, `setClass`, `setClassName`
* Extras: extra information stored with the intent (map of key value pairs)
  `Intent.EXTRA_EMAIL`
* Flags: specify how an intent should be handled
  `FLAG_ACTIVITY_NO_HISTORY`, `FLAG_DEBUG_LOG_RESOLUTION`

Calling an `Intent`:


.. code-block:: java
    
    Intent intent = new Intent(Intent.ACTION_DIAL, Uri.parse("tel:+11231231234"));
    // or
    Intent intent = new Intent();
    intent.setAction(Intent.ACTION_DIAL);
    intent.setData(Uri.parse("tel:+11231231234"));
    intent.putExtra(Intent.EXTRA_EMAIL, "email@address.com");
    startActivity(intent);

--------------------------------------------------------------
Video 2: The Intent Class (2)
--------------------------------------------------------------

The target activity can be started based on:

* The specific activity named to be started
* The implicit activity to be started based on the supplied data

The second option is intent resolution. This is specified by an
intent filter which describes which operations an activity can
handle (specified in AndroidManifest.xml or programatically).
This resolutions uses: Action, Data (Uri and Type), and Category::

    <activity ...>
      <intent-filter ...>
        <action android:name="android.intent.action.DIAL" />
      </intent-filter>
    </activity>

To recieve implicit intents, an activity should specify an
intent category with::

  <category android:name="android.intent.category.DEFAULT" />

Android intent handlers can also specify a priority flag that can
be used to break ties between intent handlers.

To debug intent filters, use the command `adb shell dumpsys package`
command.

--------------------------------------------------------------
Video 3: Permissions
--------------------------------------------------------------

Android protects resources and data with permissions. They are
used to limit access to:

* user information (contacts)
* cost-sensitive apis (sms/mms)
* system resources (camera)

Permissions are represented as strings in the `AndroidManifest.xml`.
They can declare permissions that they use themselves or that they
require of other components:

.. code-block:: xml

    <manifest>
      ...
      <uses-permission android:name="android.permission.CAMERA" />
      <uses-permission android:name="android.permission.INTERNET" />
      <uses-permission android:name="android.permission.ACCESS_FINE_LOCATIONS" />
      ...
    </manifest>

You can define and enforce your own permissions that other
applications must acquire before operating:

.. code-block:: xml

    <manifest>
      ...
      <permission
        android:name="com.bashwork.permission.SECURE"
        android:label="@string/app_name"
        android:description="@string/secure_perm_string">
      </permission>

      <application
        android:permission="com.bashwork.permission.SECURE">
        ...
      </application>
      ...
    </manifest>

Android allows developers to set permissions on a component
basis (A `SecurityException` is thrown if the needed permissions
are not supplied):

* **Activity** - restrict who can call `startActivity()`
  and `startActivityForResult()`.
* **Service** - restricts which components can start
  and bind to services. This limits access to `Context.startService()`,
  `Context.stopService()`, and `Context.bindService()`.
* **BroadcastReciever** - restricts which components can send
  and recieve broadcasts.
* **ContentProvider** - restrict which components can read
  and write data to a content provider.

--------------------------------------------------------------
Video 4: The Fragment Class (1)
--------------------------------------------------------------

Fragments were added to android to support larger displays like
tablets. The one activity and one screen may not work for displays
where we can have multiple screen frames at once.

Fragments represent a portion of a UI within an Activity. Multiple
fragments can be used in a single activity and the same fragment
can be used in multiple activities.

The fragment lifecycle is coordinated with the lifecycle of
the hosting activity. Fragments can be in the following states:

* Resumed - fragment is visibile in the running activity
* Paused - another activity is in the foreground and has focus
* Stopped - the fragment is not visible
 
A fragment also recieves lifecycle callback methods from the
parent activity:

* `onAttach` - when the fragment is attached to the parent activity
* `onCreate` - when the fragment is being created
* `onCreateView` - setup and return the UI fragment view
* `onActivityCreated` - after the parent activity is created
* `onStart` - routed from the parent activity
* `onResume` - routed from the parent activity
* `onPause` - routed from the parent activity
* `onStop` - routed from the parent activity
* `onDestroyView` - called before the fragment view is destroyed
* `onDestroy` - called before the fragment is destroyed
* `onDetach` - fragment is detached from the parent

--------------------------------------------------------------
Video 5: The Fragment Class (2)
--------------------------------------------------------------

Fragments can be statically added to a layout by using the
activity's layout file. They can also be added programatically
by using the `FragmentManager`. Regardless, the layout can then
be inflated or implemented in the `onCreateView` method. Afterwards
`onCreateView` returns a view that is then embedded into the
parent `Activity`.

To add a fragment to an activity dynamically, one must do the
following four steps:

1. Get a reference to the `FragmentManager`
2. Begin a `FragmentTransaction`
3. Add the fragment
4. Commit the `FragmentTransaction`

`FragmentTransaction` allow one to dynamically change the UI
to adapt to changing screen conditions on demand instead of
simply filling existing static layouts.

If you set `setRetainInstance(true)`, when the activity is
destroyed, the fragment is simply detached and re-attached
when the activity is started again; it is not destroyed!
