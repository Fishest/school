==============================================================
Week 6: Graphics
==============================================================

--------------------------------------------------------------
Video 1: Graphics and Animation (1)
--------------------------------------------------------------

In order to draw 2d graphics in android, one can:

* **Draw to a View**
  when one needs to draw simple graphics with little or no
  updates after the initial draw.

* **Draw to a Canvas**
  when the graphics are more complex and when they may
  recieve regular updates.

Graphics are drawn using `Drawables` which are something that
can be drawn. Examples of `Drawables` are:

* `ShapeDrawable`
  These are used to draw specific primitive shapes. Subclasses
  include: `PathShape` for lines, `RectShape` for rectangles,
  and `OvalShape` for ovals and rings.

* `BitmapDrawable`
* `ColorDrawable`

.. TODO:: Add examples of these drawables statically and
   dynamically.

These drawables can be set in views using static XML layout
files or done dynamically and programatically.

.. TODO:: Add examples of both of these

--------------------------------------------------------------
Video 2: Graphics and Animation (2)
--------------------------------------------------------------

SurfaceView operations and SurfaceHolder callbacks.

.. TODO:: Add example of working with a SurfaceView and its
   callbacks

--------------------------------------------------------------
Video 3: Graphics and Animation (3)
--------------------------------------------------------------

Changing the properties of a view over a period of time for
the purpose of animating it is generally a method of chaning
one or more of its:

* size
* position
* transparency
* orientation

To help in this regard, android supports the following View
Animation classes:

* `TransitionDrawable`
  This specifies a 2-layer drawable such that the 1st and 2nd
  layers can be faded between.

* `AnimationDrawable`
  Animates a seris of `Drawables`, showing each `Drawable`
  for a certain amount of time. This can be performed entirely
  in an XML file.

* `Animation`
  A series of transformations are applied to the contents of a
  view. The program can manipulate the animation timings to
  give effects of sequential or simultaneos changes. These
  transformations are referred to as Tweens.

.. TODO:: Add examples of these

The Property Animation architecture contains the following
tools to help animate properties:

* `ValueAnimator` - The timing engine for animations
* `TimeInterpolator` - Defines how much values should change w.r.t time
* `AnimatorUpdateListener` - called everytime a new frame is created
* `TypeEvaluator` - Calculates a properties value at a given point at time
* `AnimatorSet` - Combines individual animations to create more complex ones

.. TODO:: Add examples of these

--------------------------------------------------------------
Video 4: Touch and Gestures (1)
--------------------------------------------------------------

Android uses `MotionEvent` to represent an event from an
input device like a touch screen. It contains things like:

* **Action Code** - This represents the state change that occurred
* **Action Values** - Position and movement properties like time,
  source, location, pressure, and more depending on the input
  device.

In Android, Multitouch screens emit one movement trace per
touch source. Individual touch sources are called pointers.
Each pointer has a uniqueID as soon as it is created and as
long as it is active. `MotionEvents` can refer to multiple
pointers. Finally, each pointer may have an index in the event,
but that index is not stable over time (the pointer id is).

`MotionEvents` have action codes that desribe the state of the
event; some of these are:

* ACTION_DOWN
* ACTION_POINTER_DOWN
* ACTION_POINTER_UP
* ACTION_MOVE
* ACTION_UP
* ACTION_CANCEL

Android touch events attempt to gurantee the following
consistency gurantees:

1. Pointers will go down one at a time
2. The will move as a group
3. The will come up one at a time or be cancelled

The MotionEvent has the following methods that can be used
to operate with the pointer events:

* `getActionMasked()`
* `getActionIndex()`
* `getPointerId(int pointerIndex)`
* `getPointerCount()`
* `getX(int pointerIndex)`
* `getY(int pointerIndex)`
* `findPointerIndex(int pointerId)`

When a touch event has occurred, android attemps to deliver
the event to a hierarchy of subscribers. The current view
first receives the event via the `View.onTouchEvent(MotionEvent event)`
method. This should return `true` if the event was consumed,
else `false` so that another handler can consume the event.
Other parts of the system can register to receive touch events
by attaching a `View.onTouchListener` to the
`View.setOnTouchListener` callback handler. The `onTouch`
method of the listener will then be called when a touch event
happens. The attached listener is called before the view
receives the event.

To handle multiple touches as complex gestures, you must
follow the events that correspond to the complete gesture.

.. include:: examples/IndicateTouchLocationActivity.java
   :code: java

--------------------------------------------------------------
Video 5: Touch and Gestures (2)
--------------------------------------------------------------

For complex gestures, Android supplies the `GestureDetector`
which can recognize some of the more common gestures including
single tap, double tap, and fling.

To use this, the `Activity` creates a `GestreDetector` that
implements the `OnGestureListener` interface.

.. include:: examples/ViewFlipperTestActivity.java
   :code: java

To create custom gestures, use the `GestureBuilder`. When
you finish performing gestures in the capture application,
copy the file `/sdcard/gestures` to your `/res/raw` directory.

.. include:: examples/GesturesActivity.java
   :code: java

--------------------------------------------------------------
Video 6: Multimedia (1)
--------------------------------------------------------------

Android provides support for encoding and decoding a variety
of common media formats allowing one to play and record audio,
still images, and video:

* **AudioManager**
  Manages volume, system sound effects, and ringer mode control.
  After acquiring an instance of the manager, one can load and play
  sound effects, manage the system volume, and manage peripherals.
  To work with the `AudioManager`, one needs to get a handle by:
  `Context.getSystemService(Context.AUDIO_SERVICE)`

.. include:: examples/AudioVideoAudioManagerActivity.java
   :code: java

* **SoundPool**
  Represents a collection of audio samples (streams) and allows one
  to play a number of them together.

* **RingTone**
* **RingtonManager**
  Provides access to audio clips used for incoming phone calls,
  notifications, alarms, etc. This allows applications to get
  and set ringtones and to play and stop playing them.

.. include:: examples/AudioVideoRingtoneManagerActivity.java
   :code: java

--------------------------------------------------------------
Video 7: Multimedia (2)
--------------------------------------------------------------

* **MediaPlayer**
  Controls playback of audio and video streams and files. It
  also allows applications to control the playback of these
  files. The operation of the playback is governed by a somewhat
  complex state machine. The media player is governed by the
  following methods:

  - `setDataSource` - set the data source to play
  - `prepare` - initialize the underlying video for playing (sync)
  - `start` - start the media in the playing state
  - `stop` - stop the media from playing
  - `pause` - pause the media from playing
  - `seekTo` - seek to a particular spot in the media
  - `release` - release the underlying handles to the media

  There exists the `VideoView` which is a `SurfaceView` that
  wraps the `MediaPlayer` making it easy to incorporate the
  `MediaPlayer` into one's application.

.. todo:: Add the state machine logic for the media player
.. include:: examples/AudioVideoVideoPlayActivity.java
   :code: java

* **MediaRecorder**
  This is used to record audio and video and operates with a
  state machine just like the `MediaPlayer`. This is controlled
  with the following methods:

  - `setAudioSource` - Sets the source for the incoming audio (microphone) 
  - `setVideoSource` - Sets the source for the incoming video (camera)
  - `setOutputFormat` - Sets the output format for the media
  - `prepare` - Initializes the underlying recorder
  - `start` - Starts recording
  - `stop` - Stops recording
  - `release` - Releases all the underlying recorder resources

.. include:: examples/AudioRecordingActivity.java
   :code: java

* **Camera**
  This is a client for working with the underlying camera hardware.
  It manages camera settings, starting and stoping camera previews,
  and capturing images and videos. In order to use the camera, perform
  the following steps:
  
  1. Get a `Camera` instance
  2. Set the `Camera` parameters as neccessary
  3. Setup the preview display
  4. Start the preview
  5. Take a picture and process the data
  6. Release the camera when not in use

  To use the camera, you will need to add a few flags to your android
  resource file:

.. code-block:: xml

    <uses-permission android:name="android.permission.CAMERA" />
    <uses-feature android:name="android.hardware.camera" />
    <uses-feature android:name="android.hardware.camera.autofocus" />

.. include:: examples/AudioVideoCameraActivity.java
   :code: java
