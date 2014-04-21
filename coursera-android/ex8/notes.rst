==============================================================
Week 8: Data Management
==============================================================

--------------------------------------------------------------
Video 1: Data Management (1)
--------------------------------------------------------------

There are a number of mechanisms that can be used to store
data. The following represents the generally available mechanisms
and when they should be used:

* **Shared Preferences** - small amount of primitive data
* **Internal Storage**   - small amounts of private data
* **External Storage**   - large amounts of public data
* **SQLite Databases**   - small to large amounts of private structured data

`SharedPreferences` can be thought of as a persistent map that
holds key-value pairs of simple data types. The values stored
here are automatically persisted across application sessions.
They are often used for long term storage of customizable
application data such as: account name, wifi networks, and user
customizations. Here is how you use it:

.. code-block:: java

    // To associate the preferences with an activity or custom name
    SharedPreferences prefs = Activity.getPreferences(MODE_PRIVATE);
    SharedPreferences prefs = Context.getPreferences("custom", MODE_PRIVATE);

    // To write to a preference database
    SharedPreferences.Editor editor = prefs.edit();
    editor.putInt("int-name", 4);
    editor.putString("string-name", "value");
    editor.remove("int-name");
    editor.commit(); // to persist the changes

    // To read from a preference database
    Map values = prefs.getAll()
    Boolean value = prefs.getBoolean("bool-name", false);
    String value  = prefs.getString("string-name", "default");

`PreferenceFragment` is a simple fragment that android supplies
to manage and update the user preferences.

.. include:: examples/ViewAndUpdatePreferencesActivity.java
   :code: java

Android also supports `File` classes which represent a file
system entity identified by a path name. In Android the file
system is represented as one of the two classes:

* **Internal** - used for smaller application private data sets
* **External** - used for larger, non-private data sets

The `File` API includes the following methods (as well as many more):

* `openFileOutput(String name, int mode)` - opens a private file for writing
* `openFileInput(String name)` - opens a private file for reading

--------------------------------------------------------------
Video 2: Data Management (2)
--------------------------------------------------------------

To write to external memory files, one needs to realize that
the external memory can be removed so it can exist or maybe
not. So before working with it, one must check the current
state by using `Environment.getExternalStorageState()`:

* `MEDIA_MOUNTED` - present with read/write access.
* `MEDIA_MOUNTED_READ_ONLY` - present, but only read-only
* `MEDIA_REMOVED` - the media is not present

To work with external storage, the proper permissions must be
specified:

.. code-block:: xml

    <uses-permission android:name="android.permssion.WRITE_EXTERNAL_STORAGE" />

.. include:: examples/ExternalFileWriteReadActivity.java
   :code: java

If one needs temporary storage, they may use `Cache Files` which
android provides. These are special as they will be deleted by
the android system when storage is low. These files are also
removed when the application is uninstalled.

.. code-block:: java

    // The following return application specific cache directories
    File cache = Context.getCacheDir();         // internal storage
    File cache = Context.getExternalCacheDir(); // external storage

Finally, for structured data a database might be more useful. For
this android includes an implementation of `SQLite`. To work with
`SQLite`, android provides the following helpers:

1. Subclass the `SQLiteOpenHelper`
2. Call `super` from the subclass constructor to initialize the db
3. Override `onCreate` and `onUpgrade` ot execute `Create Table` commands
4. Use `SQLiteOpenHelper` methods to open and return a database
5. Execute operations on the underlying database

.. include:: examples/DatabaseOpenHelper.java
   :code: java

If you need to debug your database, the underlying files are
stored in the `/data/data/<package name>/databases/` directory.
You can then debug the databases using the `sqlite3` command
which drops you into a SQL repl.

--------------------------------------------------------------
Video 3: The ContentProvider Class (1)
--------------------------------------------------------------

`ContentProvider` represents a repository of structured data.
It encapsulates total data sets and enfoces data access
permssions on those data sets. These were designed to enable
sharing of data between applications. To do this, the clients
access `ContentProviders` through a `ContentResolver`. These
present a database style interface for reading and writing
data: query, insert, update, delete, triggers (update
notifications).

The `ContentProvider` data model is represented logically as
a collection of database tables (ex `_ID`, `artist`, `name`).
The different content providers are referrenced by unique
`URI` the format of which maps to specific providers. The
format is `content://<authority>/<path>/<id>`:

* `content` - scheme indicating a content provider
* `authority` - id for the client provider
* `path` - segments indicating the type of data to be accessed
* `id` - a specific record to request in the data set (optional)

What follows is an example of using a content provider:

.. code-block:: java

    String columns[] = new String[] { Contacts._ID,
        Contacts.DISPLAY_NAME, Contacts.PHOTO_THUMBNAIL_URI };
    String whereClause = "((" + Contacts.DISPLAY_NAME + " NOTNULL) AND ("
        + Contacts.DISPLAY_NAME + " != '' ) AND (" + Contacts.STARRED
        + "== 1))";
    String sortOrder = Contacts._ID + " ASC";

    ContentResolver contentResolver = getContentResolver();
    Cursor cursor = contentResolver.query(Contacts.CONTENT_URI,
        columnsToExtract, whereClause, null, sortOrder);

Android provides a number of default `ContentProvider`:

* **Browser** - for bookmarks and history
* **Call Log** - for telephone usage
* **Contacts** - for contact data
* **Media** - for the media database (photos, videos, etc)
* **UserDictionary** - Database for predictave spelling

Performing a query on the main thread can affect the application
responsiveness, so android provides `CursorLoader` which uses
and `AsyncTask` to perform queries on a background `Thread`:

.. include:: examples/ContactsListExample.java
   :code: java

--------------------------------------------------------------
Video 4: The ContentProvider Class (2)
--------------------------------------------------------------

.. code-block:: java

    Cursor content.query(       // returns a cursor to the result set
        Uri uri,                // the content provider URI
        String[] projection,    // the columns to retrieve
        String selection,       // the sql selection pattern 
        String[] selectionArgs, // the selection arguments
        String sortOrder        // the data set sort order
    );

    int content.delete(         // returns the number of rows deleted
        Uri uri,                // the content provider URI
        String where,           // the sql selection pattern 
        String[] whereArgs      // the selection arguments
    );

    Uri content.insert(         // returns Uri to new data element
        Uri uri,                // the content provider URI
        ContentValues values    // the values to insert
    );

    int content.update(         // returns the number of rows updated
        Uri uri,                // the content provider URI
        ContentValues values,   // the new field values
        String selection,       // the sql selection pattern 
        String[] selectionArgs  // the selection arguments
    );

To create one's own `ContentProvider` do the following:

1. Implement a storage system for the data (usually a sqlite database)
2. Define a contact class to support users of the provider
3. Implement a `ContentProvider` subclass (query, delete, insert, update)
4. Declare and configure the content provider in `AndroidManifest.xml`:

.. code-block:: xml

    <application>
      ...
      <provider
          android:name="content.provider.name"
          android:authorities="content.provider.authority"
          android:exported="true" >
      </provider>
      ...
    </application>

.. include:: examples/StringsContentProvider.java
   :code: java

--------------------------------------------------------------
Video 5: The Service Class (1)
--------------------------------------------------------------

The `Service` class in android does not provide a user
interface. It instead serves two main purposes: performing
background processing and supporting remote method execution.
Once started, the service can run in the background indefinitely,
however, the android system does reserve the right to terminate
the service if it needs its resources.

Started services usually perform a single operation and then
terminate themselves. By default, services run in the main
thread of their hosting application. If the service needs to
perform a great deal of work, it may be neccessary to start
the service in another thread.

Components that need to work directly with a service can do
so by binding to the service. Binding to a service allows a
component to send requests to and receive responses from a
local or remote service. A binding time, if the service is not
already started, it will be if necessary. The service will
then remain running as long as at least one client is bound
to it. The service can also start in the foreground (say if
it is playing media) so that it is less likely to be killed
by the android system.

.. code-block:: java

    Context.startService(Intent intent);
    Context.bindService(Intent intent, ServiceConnection conn, int flags);

--------------------------------------------------------------
Video 6: The Service Class (2)
--------------------------------------------------------------

There are a few ways of binding to remote services, namely
using messenger services and the AIDL tools. The Messenger
Managers allows messages to be sent from one component to
another across process boundaries. These messages are then
queued and processed sequantially by the recipient. To create
this system:

1. The service creates a handler for processing specific messages
2. The service creates a messanger that provides a binder to clients 
3. The client uses the binder to create its own messenger
4. The client uses that messenger to send messages to the service

.. include:: examples/LoggingService.java
   :code: java

.. include:: examples/LoggingServiceClient.java
   :code: java

To implement a messenger service with AIDL:

1. Define the remote interface in `AIDL`. To do this, create a
   service interface in an `.aidl` file. This defines the methods
   that components can use to interact with your service.

2. Implement the remote interface
3. Implement the service methods
4. Implement the client methods

AIDL has the following syntax:

- Similar to java interface syntax to declare methods
- cannot declare static methods 
- non primitive parameters require a directional tag
- in (to server), out (to client), inout (in both directions)
- the AIDL data types are limited to the java primitive types
- can also use other AIDL generated interfaces
- and finally any classes that implement the `Parcelable` protocol
- the collections can be lists (generic) and maps (raw)

The following is an example of an aidl file:

.. code-block:: java

    // saved in keygenerator.aidl
    interface KeyGenerator {
        String getKey();
    }
