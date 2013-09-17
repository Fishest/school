
/**
 * Log Viewer
 * - poll and get latest
 * - add new ticket to the bottom
 * - each ticket has a close button that calls clear
 */

<html>
  <head>
    <script src="/js/jquery.min.js"></script>
    <title>Error Queue Logger</title>

    <!-- any javascript you need -->
    <script type="text/javascript">
//
// Given the following REST method:
//   DELETE /api/errors/{id}
//   {
//     status : 'ok'
//   }
//
//   GET    /api/errors ->
//   {
//     errors : [{'id': 1, 'date': '2013-12-01 12:12:12.000Z', 'message' : 'Some error message' }]
//   }
//

    </script>

    <!-- any css you need -->
    <style type="text/css">
    </style>
  </head>

  <!-- any html you need -->
  <body>
  </body>
</html>

/**
 * Active Model
 */

var customer = new Model({
  name: 'Mr. Customer',
  email: 'customer@email.com'
});
customer.subscribe('change', function(event, prop) {
  alert(this.get(prop));
});
customer.set('age', 25);
customer.unsubscribe('change');


function Model(initial) {
  this._props = initial || {};
  this._event = $({});
}

Model.prototype = {
  set = function(key, val) {
  }
  get = function(key) {
  }
  subscribe = function(trigger, callback) {
  }
  unsubscribe = function(trigger) {
  }
  publish = function(trigger, data) {
  }
};

/**
 * Implement setInterval in terms of setTimeout
 */
 function Timer(callback, timeout) {
   this.callback = callback;
   this.timeout  = timeout;
   this.is_running = false;
 }

 Timer.prototype.start = function() {
   var self = this;
   function inner() {
     if (self.is_running) {
       self.callback();
       setTimeout(self.callback, self.timeout);
     }
   }
   this.is_running = true;
   inner();
 };

 Timer.prototype.stop = function() {
   this.is_running = false;
 };

/**
 * Questions
 */

- REST: get / put / post / delete
- templates vs dom construction
- how to use css for interaction (active / disabled)
- difference between == and ===
- why use libraries like jquery / underscore
- favorite parts of CSS3 / HTML5?
- parameters vs arguments vs array
- callbacks vs promise / deferred
- apply vs call
- how can you supply parameters to a parameterless function
- how to call a method in inheritence chain
- prototypical inheritance (inheritance chain)
  if (typeof Object.create !== 'function') {}
    Object.create = function(o) {
      function F() {}
      F.prototype = o;
      return new F();
    }
  }

- this in events, closures, contexts
  function.apply(context, [arguments])

- how do you organize large enterprise projects