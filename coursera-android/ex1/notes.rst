==============================================================
Week 1
==============================================================

--------------------------------------------------------------
Video 1: The Android Platform
--------------------------------------------------------------

The lowest level is the linux kernel:

* security layer
* memory and process management
* network and file IO
* device drivers

The kernel is patched to add some android specific services:

* custom power management
* android shared memory
* low memory killer
* interprocess communication (binder)

At the native layer, android supplies:

* customer libc implementation (bionic)
* surface manager (display management)
* media framework (audio/video)
* webkit (web browser)
* opengl (graphics engine)
* sqlite (relational database engine)

Android runtime is composed of:

* The dalvik virtual machine (dalvik vm internals by dan bornstein)
* The core java libraries

The android application framework is composed of the following:

* Package Manager: database about packages installed on the
  android device.
* Window Mangaer: manages the many windows that comprise an
  android application.
* View System: includes common user interface widgets.
* Resource Manager: manages the non compiled resources of an
  application (strings, layouts, graphics).
* Activity Manager: manages application lifecycle and the
  navigation stack.
* Content Provider: inter-application data sharing.
* Location Manager: provides location and movement information
* Notification Manager: allows applications place notifications
  in the notification bar.

The android application layer supplies some stock base applications
that can easily be replaced in the system: dialer, gallery, sms, etc.

--------------------------------------------------------------
Video 2
--------------------------------------------------------------

How to set up the ADK, IDE, and emulater. Also how to work with
the debugger.

--------------------------------------------------------------
Video 3
--------------------------------------------------------------

Dalvik Debug Monitor Service (DDMS) includes a number of helpful
tools that can make debugging your programming easiser. They
include:

* file explorer: can explore the device file system
* logcat: can view the logs by the system and application
* traceview: can view trace logs of the system while debugging
* hierarchyview: can view the hierarchy of the various UI elements
