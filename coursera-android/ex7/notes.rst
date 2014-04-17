==============================================================
Week 7: Location
==============================================================

--------------------------------------------------------------
Video 1: Sensors (1)
--------------------------------------------------------------

Sensors are hardware devices that measure the physical
environment including: motion, position, and environment.
The following pieces compose the sensor framework:

* `SensorManager`
  The system service that manages sensors. To work with this,
  simply get a handle to it via: `getSystemService(Context.SENSOR_SERVICE)`.
  To get access to a specific `Sensor`: `SensorManager.getDefaultSensor(int type)`.
  The various types of sensors that you can get access to are:

  - **Motion** - 3-Axis Accelerometer: `Sensor.TYPE_ACCELEROMETER`
  - **Position** - 3-Axis Magnetometer: `Sensor.TYPE_MAGNETIC_FIELD`
  - **Environment** - Pressure Sensor: `Sensor.TYPE_PRESSURE`

* `SensorEventListener`
  To get changes to a `Sensor`, this interface is implemented which
  receives various `SensorEvent` callbacks:

  - `onAccuracyChanged(Sensor sensor, int accuracy)`
  - `onSensorChanged(SensorEvent event)`
  - `registerListener(SensorEventListener listener, Sensor sensor, int rate)`
  - `unregisterListener(SensorEventListener listener, Sensor sensor)`

* `SensorEvent`
  Represents a single `Sensor` event. It includes data that is sensor
  specific as well as: sensor type, time stamp, accuracy, and measurement
  data. In order to make sense of the data, one must understand the sensor
  coordinate system. For example, for a 3-axis sensor lying flat and face
  up on a table: y (top to bottom), x (right to left), z (down to up).
  The coordinate system does not change, even if the device changes
  from portrait to landscape.

.. include:: examples/SensorRawAccelerometerActivity.java
   :code: java

--------------------------------------------------------------
Video 2: Sensors (2)
--------------------------------------------------------------

In order to work with the resulting sensor values, you must
clean the values correctly as they will vary due to natural
movements, environment, and noise. To filter or transform
the resulting values, it may be useful to use one of the
following filters:

* **Low Pass Filter**
  Deemphasizes transient force changes while emphasizing
  constant force components. Used when your application
  needs to pay attention to the constant force and not
  be needing to deal with small fluctuations (say a
  carpenters level).

* **High Pass Filter**
  Emphasizes transient force changes while deemphasizing
  constant force components. Used when your application
  needs to ignore the constant force, but needs to pay
  attention to the small fluctuations (say a musical
  instrument).

.. include:: examples/SensorFilteredValuesActivity.java
   :code: java

.. include:: examples/CompassActivity.java
   :code: java

--------------------------------------------------------------
Video 3: Location and Maps (1)
--------------------------------------------------------------

Mobile applications can benefit from being location aware,
thus android allows applications to retrieve and manipulate
location data.

* **Location**
  This represents a position on the earth. Each instance
  consists of the following: latitude, longitude, timestamp,
  and optionally accuracy, altidue, speed, and bearing.

* **LocationManger**
  This is the system service for accessing location data. It
  is retrieved by calling `getSystemService(Context.LOCATION_SERVICE)`.
  This can then be used determine the last known location,
  register for location updates, and register to receive intents
  when the device moves near or away from a given geographic
  area (GeoFence).

* **LocationListener**
  Defines the callback methods that are called when the
  `Location` or `LocationProvider` status changes. It supplies
  the following callback methods:

  - `onLocationChanged(Location location)`
  - `onProviderEnabled(String provider)`
  - `onProviderDisabled(String provider)`
  - `onStatusChanged(String provider, int status, Bundle extras)`

  To retreive the current location in an android application:

  1. Start listening for updates from the location providers
  2. Maintain a current best estimate of the location
  3. When the estimate is good enough stop listening for updates
  4. Use that best estimate as the current location

  When determining the best location, there are several factors
  to consider:

  - **Measurement Time** - how long should you listen
  - **Accuracy** - can you get away with city instead of street
  - **Power Needs** - how much power can you stand to use

* **LocationProvider**
  This represents a location data source. Android allows many
  forms of location data including: GPS satellites, cell phone
  towers, and WiFi access points. Concretely, the three
  `LocationProvider` types are:
  
  - `Network` - wifi/cell; cheaper, less accurate, faster, less available
  - `GPS` - satellite; expensive, accurate, slower, works outside
  - `Passive` - reuse existing readings; cheapest, fastest, not always available

Each of these providers offer different tradeoffs between cost,
accuracy, availability, and timeliness. To use the various
`LocationProviders` one must specify the following permssions
in the `AndroidManifest.xml`:

.. code-block:: xml

    <uses-permission name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission name="android.permission.ACCESS_FINE_LOCATION" />

.. include:: examples/LocationGetLocationActivity.java
   :code: java

What follows are a collection of battery saving tips for working
with the location providers:

* Always check the last known measurement and use it if you can
* Return updates as infrequently as possible (limit measurement time)
* Use the least accurate measurement necessary
* Turn off the updates on `onPause`

--------------------------------------------------------------
Video 4: Location and Maps (2)
--------------------------------------------------------------

Maps are a visual representations of a given area. Android
supplies mapping support through the Google Maps Android V2
API. It supplies several kinds of maps:

* **Normal** - Traditional road maps
* **Satellite** - Aerial photographs
* **Hybrid** - Combination of Satellite and road maps
* **Terrain** - Topographic details on the maps

Android allows one to customize the maps in a number of ways:

* Change the camera position
* Add markers and ground overlays
* Respond to gestures
* Indicate the user's current locations

In customizing the maps, the following classes may come in handy:

* **GoogleMap**
* **MapFragment**
* **Camera**
* **Marker**

To work with a maps application, the following prerequisites must
be performed:

1. Setup the google play services SDK
2. Obtain an API key
3. Specify settings in the `AndroidManifest.xml`
4. Add the map to the project

The following permissions are needed to work with maps:

.. code-block:: xml

    <!-- to obtain map data from the internet -->
    <uses-permission name="android.permission.INTERNET" />
    <uses-permission name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission name="com.google.android.providers.gsf.permission.READ_GSERVICES" />

    <!-- to save data from the internet -->
    <uses-permission name="android.permission.WRITE_EXTERNAL_STORAGE" />

    <!-- to obtain location data -->
    <uses-permission name="android.permission.ACCESS_COARSE_LOCATION" />
    <uses-permission name="android.permission.ACCESS_FINE_LOCATION" />
