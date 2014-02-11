==============================================================
Week 2
==============================================================

--------------------------------------------------------------
Video 1: Application Fundamentals (1)
--------------------------------------------------------------

The main components of an Android application are:

* Activity - Primary class for user interaction

  Usually implements a single focused activity that a user can
  do.

* Service - Run in the background

  These can be used to provide long running serivces in the
  background and to support interacting with remote processes.

* BroadcastReceiver - Components that listens for and responds
  to events.

  This is the subscriber in the publish/subscriber pattern.
  Events are represented by the Intent class and then by the
  Broadcast class. BroadcastReceiver receives and responds to
  Broadcast events.

* ContentProvider - Allows data to be stored and shared across
  applications.

  Uses a database style interface. Also handles IPC for the
  applications.

* Resources - Android resources allow a large number of
  application details to be seperated from the source code to
  be changed dynamically or based on a platform:

  - strings - string, string arrays, and plurals. Stored in
    `res/values/*.xml` as xml string tags:
    `<string name="some_name">String Text</string>`

    Applications can access the string resources by using the
    identifier like `@string/string_name` in layout files. In
    Java code you do `R.string.string_name`.

  - images
  - animations
  - layouts / views
  - media

--------------------------------------------------------------
Video 2: Application Fundamentals (2)
--------------------------------------------------------------

Layouts are defined in layout xml files stored in `res/layout/*.xml`.
Each layout can be accessed in java via `R.layout.layout_name` and
in other layout files as `@layout/layout_name`.

Multiple layout files can be created based on device type, size,
landscape mode, and other factors.

Applications are created by implementing the Activity class.
The main entry point is the `onCreate` method which is generally
responsible for:

* restoring saved state
* setting the content view
* initializing UI elements
* attaching callbacks to UI element actions

`AndroiManifest.xml` contains all the android packaging information
that the build system will use to generate the final apk like:

* permissions
* application name
* latest api level supported

--------------------------------------------------------------
Video 3: The Activity Class (1)
--------------------------------------------------------------

A Task is a set of related activities that are related, but
not neccessarily in the same application. Mosts tasks start at
the home screen.

The Task Backstack works as follows:

* When an activity is created, it is added to the top of the stack
* when an activity is destroyed, it is removed from the stack
 
The application lifecycle is not necessarily in the control of
the application:

* the user can push the back button or navigate away
* the android system can kill a process to regain resources

The activity can be on the following states:

* Running/Resumed - is visible with user interaction
* Paused - is visible, but no user interaction (can be terminated)
* Stopped - not visible, can be terminated

Android announces to your activity what the current lifecycle
state is by calling back the supplied methods (not all need to
be implemented)::

    (activity launched) -> onCreate
    onStop -> onRestart -> onStart
    onPause -> onResume
    onDestroy -> (activity shutdown)
    onCreate -> onStart -> onResume -> (running) -> onPause -> onStop -> onDestroy
                        --- foreground section of activity ---
                ------------ visible section of activity -----------


--------------------------------------------------------------
Video 4: The Activity Class (2)
--------------------------------------------------------------

The lifecycle methods are now explored in more detail:

* `onCreate` - Called when the activity is created and
  sets up the initial state as follows:

  - calls super.onCreate(bundle)
  - sets the activity content view
  - retain references to UI views as necessary
  - configures views as necessary

* `onRestart` - Called when the activity has been stopped
  and is about to be started again. It only needs to be
  implmented if there is logic that needs to be done if
  the application was started and then stopped.

* `onStart` - Called when the activity is about to become
  visible. The typical things done in this callback are:

  - start actions that only occur when visible
  - load persistant application state

* `onResume` - Called when the activity is visible and is
  about to start interacting with the user. The typical
  actions here are:

  - start foreground only behavior

* `onPause` - Called when your activity is about to lose
  focus to another activity. Typical actions here are:

  - shutdown foreground only operations
  - save any persistant state

* `onStop` - Called when the activity is no longer visible
  to the user (may be restarted later). The typical action
  to perform here is to cache the activity state. This may
  not be called if android kills your application (so persist
  data in `onPause`).

* `onDestroy` - Called when the activity is about to be
  destroyed. Typical things to do here are to release
  any activity resources (like background threads). This
  method may not be called if android decides to kill your
  activity.

New activities can be started from other activities by:

* Creating an intent for the activity to start
* Passing that intent to `startActivity` or `startActivityForResult`
