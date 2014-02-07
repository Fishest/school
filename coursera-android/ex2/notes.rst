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

--------------------------------------------------------------
Video 3: The Activity Class (1)
--------------------------------------------------------------

--------------------------------------------------------------
Video 4: The Activity Class (2)
--------------------------------------------------------------
