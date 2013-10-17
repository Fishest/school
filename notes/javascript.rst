=================================================
Javascript
=================================================

In javascript, there is no difference between classes and instances (
although it is fine to informally speack of objects being an instance
of a given type):

* there are only objects
* any object can be used as a prototype to create a new object (template)
* there is no class definition with a constructor function
* any function can be a constructor and can set the initial values
* new properties can be added and removed dynamically at run time
* no multiple inheritance
* inheritance is done with prototypes

.. code-block:: javascript

    function Worker(fields) {
        this.name = fields.name || "";
        this.age  = fields.age  ||  0;
    }

    function Teacher(fields) {
        Worker.call(this, fields);
        this.job = "'"teacher";
    }
    Teacher.prototype = new Worker;

    var bob = new Person({name: 'Bob Rodgers', age: 25});
    var helen = new Teacher();

-------------------------------------------------
Class Creation
-------------------------------------------------

When `new` is called with a constructor function:

1. a generic object is created and passed as `this` to the constructor
2. the constructor sets all the properties that it wants
3. the `__proto__` property is set to the Type.prototype value
4. this constructed object is finally returned

It should be noted that the parent values are not stored in the immediate
child. Instead, when a value is looked up, say `name`, the runtime first
checks the current object. If the value is not found there, it walks the
prototype chain to the parent and checks if it contains that field. This
continues up the chain until the field is found or it reaches the top most
parent and returns `undefined`.

To test if an instance of a type of class, the following work:

.. code-block:: javascript

    var teacher = new Teacher

    // all of the following return true
    teacher instanceof Teacher;
    teacher instanceof Worker;
    teacher.__proto__ == Teacher.prototype;
    teacher.__proto__.__proto__ == Worker.prototype;;
    teacher.__proto__.__proto__.__proto__ == Object.prototype
    teacher.__proto__.__proto__.__proto__.__proto__ == null;

    // a quick reimplementation of instanceof
    function instanceOf(object, class) {
        while (object != null) {
            if (object.__proto__ == class.prototype) {
                return true;
            }
            object = object.__proto__;
        }
        return false;
    }

Although javascript does not support multiple inheritance, you can
simulate it by simply calling multiple constructors in the child
constructor function.  It should be noted that this will be added
to the constructed instance, but any changes to the parent prototype
after construction will not be reflected in the child.

-------------------------------------------------
Dynamic Properties and Functions
-------------------------------------------------

If you directly add a property to an instance, it will be set for that
instance only.  If you want to add it to all the instances, add it to
the prototype class:

.. code-block:: javascript

    bob.salary = 10000;                  // this just applies to bob 
    helen.salary;                        // this is undefined
    Teacher.prototype.salary = 30000.00; // this applies to all instances
    helen.salary;                        // this returns 30000

Continuing, if you want to change a field at runtime and have the value
propigated down the inheritance chain, the field cannot be set in the 
constructor function, it must be a prototype on the type:

.. code-block:: javascript

    function Food(type) {
        this.type = type;
    }
    Food.prototype.cost = "unknown";  // this cannot be set in constructor

    function Apple() {
        Food.call(this, 'fruit');
    }
    var a = new Apple();          // the value of a.cost == "unknown"
    Food.prototype.cost = "free"; // the value of a.cost == "free"

-------------------------------------------------
Mixins
-------------------------------------------------

This can be done using a mixin extend function
which can be used to add a mixin to an existing class:

.. code-block:: javascript

    var RoundButton = function(radius, label, action) {
      this.radius = radius;
      this.label  = label;
      this.action = action;
    }
    
    // using a mixin extend function
    function extend(object, mixin) {
      for (var fn in mixin) {
        if (object.hasOwnProperty(fn)) {
          object[fn] = mixin[fn];
        }
      }
      return object;
    }
    
    var circleMixin = {
      area: function() { return Math.PI * this.radius * this.radius; },
      grow: function() { this.radius++; },
      shrink: function() { this.radius--; }
    };
    var buttonMixin {
      hover = function(flag) { flag ? $.appendClass('hover')   : $.removeClass('hover'); },
      press = function(flag) { flag ? $.appendClass('pressed') : $.removeClass('pressed'); },
      fire = function() { return this.action(); }
    };
    
    extend(RoundButton.prototype, circleMixin);
    extend(RoundButton.prototype, buttonMixin);

We can also allow the mixin to directly inject itself into
another class:

.. code-block:: javascript

    // allowing the mixin to extend the type
    var asCircle = function() {
      this.area: function() { return Math.PI * this.radius * this.radius; };
      this.grow: function() { this.radius++; };
      this.shrink: function() { this.radius-- };
      return this;
    };
    
    var asButton = function() {
      this.hover = function(bool) {
        bool ? $.appendClass('hover') : $.removeClass('hover');
      };
      this.press = function(bool) {
        bool ? $.appendClass('pressed') : $.removeClass('pressed');
      };
      this.fire = function() { return this.action(); };
      return this;
    };
    
    asCircle.call(RoundButton.prototype);
    asButton.call(RoundButton.prototype);

Options can be added to the mixins as well:

.. code-block:: javascript

    // adding options to the mixin
    var asOval = function(options) {
      this.grow = function() {
        this.shortRadius += (options.growBy/this.ratio());
        this.longRadius  += options.growBy;
      };
      this.shrink = function() {
        this.shortRadius += (options.shrinkBy/this.ratio());
        this.longRadius  += options.shrinkBy;
      };
      return this;
    };
    
    var OvalButton = function(longRadius, shortRadius, label, action) {
      this.longRadius = longRadius;
      this.shortRadius = shortRadius;
      this.label = label;
      this.action = action;
    };
    
    asOval.call(OvalButton.prototype, { growBy: 2, shrinkBy: 2 });
    asButton.call(OvalButton.prototype);

Finally we can cache function creation to increase performance.
In this case we need to curry the option application to the
mixins:

.. code-block:: javascript

    // with cached closure to prevent recreating functions
    var asRectange = (function() {
      function area() { return this.length * this.width; }
      function grow() { this.length++, this.width++; }
      function shrink() { this.length--, this.width--; }
      return function() {
        this.area = area;
        this.grow = grow;
        this.shrink = shrink;
      };
    })();
    
    // currying to store options
    Function.prototype.curry = function() {
      var fn = this;
      var args = [].slice.call(arguments, 0);
      return function() {
        return fn.apply(this. args.concat([].slice.call(arguments, 0));
      }
    };
    
    var asRectange = (function() {
      function area() { return this.length * this.width; }
      function grow(rate) { this.length += rate, this.width += rate; }
      function shrink(rate) { this.length -= rate, this.width -= rate; }
      return function(options) {
        this.area = area;
        this.grow = grow.curry(options['growBy']);
        this.shrink = shrink.curry(options['shrinkBy']);
      };
    })();
