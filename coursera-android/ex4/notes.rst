==============================================================
Week 4
==============================================================

--------------------------------------------------------------
Video 1: User Interfaces (1)
--------------------------------------------------------------

`View` is a key building block in the android UI. They occupy
a rectangular space on the screen and are responsible for
drawing themselves and handling events. Android includes a
number of predefined views:

* `Button` - a view that can be clicked on to perform an action
* `ToggleButton` - a two-state button that displays its state
* `CheckBox` - a two-state button modeled with checked/unchecked
* `RatingBar` - a view comprising a row of stars used to rate
* `AutoCompleteTextView` - a text field that autocompletes input

Views have a number of common operations such as:

* setting visibility (show or hide)
* set checked state
* set listeners that should run on specific events
* set various properties (opactity, background, rotation)
* manage input focus and allow text input

Views handle various events that are handled by attaching event
listeners to operations like:

* touch user interaction (`OnClickListener.onClick()`)
* keyboard input (`OnKeyListener.onKey()`)
* focus changed (`OnFocusChangeListener.onFocusChange()`)
* lifecycle events from Android

Views are organized as a tree of views. To process the view
hierarchy, android walks the tree three times:

1. measure and get the dimensions of all the views (`onMeasure`)
2. layout and position each view (`onLayout`)
3. draw each view (`onDraw`)

Custom views can override portions of this process to do 
different things:

1. `onMeasure` - determine the size of this view and its children
2. `onLayout`  - assign a size and position to all its children
3. `onDraw`    - view should render its content

Other custom events that can be handled are:

* `onFocusChanged` - for handling when the view focus state has changed
* `onKeyUp` / `onKeyDown` - for handling key input events
* `onWindowVisibilityChanged` - when the parent view has changed its visibility

--------------------------------------------------------------
Video 2: User Interfaces (2)
--------------------------------------------------------------

In order to make a compound view, we use `ViewGroup`. These
are invisible views that contain other views. There are a number
of predefined ViewGroups:

* `RadioGroup` - a group of radio / check boxes displaying option
* `TimePicker` - allows the user to select a given time
* `DatePicker` - allows the user to select a given date
* `WebView` - displays a selected web page
* `MapView` - displays a map and allows user interaction
* `Spinner` - a scrollable selectable list of items (`SpinnerAdapter`)
* `Gallery` - a horizontally scrolling list (`SpinnerAdapter`)

`AdapterViews` are views whose children are managed by the
backing data in an `Adapter`. So the `AdapterView` displays
the data view, and the `Adapter` manages and provides the
data to the `AdapterView`.

An example of this is the `ListView`. This is a scrollable list
of selectable items. These items are managed by a `ListAdapter`.
The `ListView` can filter the input items based on text input.

.. TODO::
   Copy some source code for interacting with adapters here.

--------------------------------------------------------------
Video 3: User Interfaces (3)
--------------------------------------------------------------

`Layout` is a generic `ViewGroup` that defines a structure for
the `Views` and `ViewGroups` it contains. Examples of predefined
layouts in Android are:

* `LinearLayout` - arranges child views in a horizontal/vertical linear layout
* `RelativeLayout` - arranges child views relative to each other
* `TableLayout` - arranges child views into rows and columns.
* `GridView` - arranges children into a 2-D scrollable grid

.. TODO::
   Copy some various layout examples xml

Activities support menus for user operations. The Activities can
add elements to the menu and handle clicks to menu items. There
are three types of menus:

1. `Options` - shown when user presses the menu button
2. `Context` - view-specific when user press and holds the view
3. `Submenu` - menu activiated when a user touches a menu item

In order to create menus:

1. Define the menu resources in `res/menu/filename.xml`
2. Inflate the menu items in `onCreateOptionsMenu` using menu inflater
3. Handle item selection in appropriate `on...ItemsSelected` methods
 
.. code-block:: java

   // To add a custom menu, first inflate it using the
   // supplied menu resource
   @Override
   public boolean onCreateOptionsMenu(Menu menu) {
       MenuInflater inflater = getMenuInflater()
       inflater.inflate(R.menu.top_menu, menu);
       return true;
   }

   // Then handle the callback for the selected menu
   // option and existing menu items.
   @Override
   public boolean onOptionsItemSelected(MenuItem item) {
       switch(item.getItemId()) {
           case R.id.help:
               Toast.makeText(getApplicationContext(), "you have been helped", Toast.LENGTH_SHORT).show();
               return true;
           default
               return super.onOptionsItemSelected(item);
       }
   }

.. TODO::
   Copy some menu xml code

--------------------------------------------------------------
Video 4: User Interfaces (4)
--------------------------------------------------------------

Menus support a number of other features like:

* grouping related menu items
* binding shortcut keys to common menu items
* binding intents to menu items

The `ActionBar` allows for quick access to common operations and
functions very much like the application bar in many desktop
applications. Each fragment can add a new entry into this bar
as they are installed.

`ActionBar.Tab` allows tabbed layouts to be realized such that
only the currently viewed tab is active. Each tab is connected
to a single fragment.

`Dialogs` are independent subwindows used by `Activities` to 
communicate with users. There are a number of `Dialog` subclasses
that android provides for specific purposes:

* `AlertDialog` 
* `ProgressDialog` 
* `DatePickerDialog` 
* `TimePickerDialog` 
