================================================================================
Android Development Guide
================================================================================

--------------------------------------------------------------------------------
Lifecycle Methods
--------------------------------------------------------------------------------

* `onCreate` / `onDestroy` - These states are generally not used for too much as
  the previous states take care of the brunt of the work. These should be as
  quick as possible so the next states can take focus.

* `onStart` / `onStop` - These are the main setup and teardown methods. Perform
  the majority of initialization for you application here.

* `onResume` / `onPause` - These states are for quickly restoring and releasing
  expensive resource handles (radios). These should be relatively quick.

.. note:: Every time the application is rotated, the Activity is destroyed and
   recreated. This is because the configuration may have changed and new
   resources may have to be loaded from the system.

When the `Activity` is destroyed for any reason and recreated, the current
application state is stored in a `Bundle` (which is a collection of key-value
pairs) and then restored the Android without any application intervention.
However, if you need to add extra state, you must overload the following:

* `onSaveInstanceState(Bundle bundle)`
* `onRestoreInstanceState(Bundle bundle)`

.. note:: Always call the superclass methods so the default implementation can
   save and restore the view hierarchy. Call super.save last and super.restore
   first.

--------------------------------------------------------------------------------
Application Components
--------------------------------------------------------------------------------

* `Activities` - These represent a single screen with a user interface. Each
  activity is independent from the others although they may all work together in
  a single application. All activities are subclasses of `Activity`.

* `Services` - These run in the background to perform long running tasks or to
  perform work for remote processes. They have no user interface. These are used
  to say request network resources, play music, etc. All services are subclasses
  of `Service`.

* `Content Providers` - These manage a shared set of application data. These are
  all subclasses of `ContentProvider`.

* `Broadcast Receivers` -
