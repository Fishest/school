================================================================================
Angular.js
================================================================================

--------------------------------------------------------------------------------
Code School Chapter 1: Directives
--------------------------------------------------------------------------------

To create an application in Angular, it is first neccessary to create a module
for your application. This can be combined with directives to create a reactive
application:

.. code-block:: html

    <!DOCTYPE html>
    <html ng-app="application">
    <head>
      <link rel="stylesheet" type="text/css" href="bootstrap.min.css" />
    </head>
    <body>
      <p>Here is a simple expression: {{ 4 + 6 }}</p>

      <script type="text/javascript" href="angular.min.js"></script>
      <script type="text/javascript" href="app.js"></script>
    </body>
    </html>

.. code-block:: javascript

    (function() {
      // defines the base application module and its dependencies
      var app = angular.module('application', []);

    })();

To add behavior, it is neccessary to create controllers. Controller names
must be in capital-case and must include the "Controller" suffix:

.. code-block:: html

    <div ng-controller="StoreController as store">
      <h1>{{store.product.name}}</h2>
      <h2>{{store.product.cost}}</h2>
      <p>{{store.product.data}}</p>
    </div>

.. code-block:: javascript

    (function() {
      // ...
      var gem = { 
        name: "Topaz",
        cost: 12.35,
        data: "This is a topaz gem"
      };

      // a simple controller for our behavior
      app.controller('StoreController', function() {
        this.product = gem;
      });
    })();

There are many directives in angular, for example to show a button based on a
condition. It should be noted, that if a property or expression does not exist
for an object, angular interprets it as false:

.. code-block:: html

    <div ng-controller="StoreController as store">
      <div ng-hide="store.product.soldOut">  <!-- hide directive or ng-show="!expression" -->
        <h1>{{store.product.name}}</h2>
        <h2>{{store.product.cost}}</h2>
        <p>{{store.product.data}}</p>
        <button ng-show="store.product.canPurchase">Add To Cart</button>
      </div>
    </div>

.. code-block:: javascript

    (function() {

      var gem = { 
        name: "Topaz",
        cost: 12.35,
        data: "This is a topaz gem",
        canPurchase: false,
        soldOut: True
      };

    })();

To work with multiple items, we can use the `ng-repeat` directive:

.. code-block:: html

    <div ng-controller="StoreController as store">
      <div ng-repeat="product in store.products">
        <h1>{{product.name}}</h2>
        <h2>{{product.cost}}</h2>
        <p>{{product.data}}</p>
        <button ng-show="product.canPurchase">Add To Cart</button>
      </div>
    </div>

.. code-block:: javascript

    (function() {

      var gems = [
        { 
          name: "Topaz",
          cost: 12.35,
          data: "This is a topaz gem",
          canPurchase: false,
        },
        { 
          name: "Opal",
          cost: 5.12,
          data: "This is a opal gem",
          canPurchase: true,
        }
      ];

      app.controller('StoreController', function() {
        this.products = gems;
      });

    })();

--------------------------------------------------------------------------------
Code School Chapter 2: Filters and Custom Directives
--------------------------------------------------------------------------------

If you need to modify data in a view, don't modify it in a controller, instead
create a filter that the data can be applied to in the view using the `|`
operator:

.. code-block:: html

    <div ng-controller="StoreController as store">
      <div ng-repeat="product in store.products">
        <h1>{{product.name}}</h2>
        <h2>{{product.cost | currency}}</h2>
        <p>{{product.data}}</p>
      </div>
    </div>

Filters generally work with the following scheme:

.. code-block:: javascript

  {{ data* | filter:options* }}
  {{ '123412512341311234' | date:'MM/dd/yyyy @ hh:mma' }}
  {{ 'lowercase' | uppercase }}
  {{ 'some very long string' | limitTo:8 }}

They can also be used in directives, for example:

.. code-block:: html

  <li ng-repeat="product in store.products | limitTo:3">
  <li ng-repeat="product in store.products | orderBy:'-cost'">

A quick gotcha is it you need to use the result of an expression as a `src` value;
you need to actually use the `ng-src` directive otherwise the browser tries to load
the raw expression:

.. code-block:: html

  <img ng-src="{{product.images[0].full}}" />

To add more interation to the page, we can use the `ng-click` directive to create
dynamic tabs (using twitter-bootstrap framework for styling):

.. code-block:: html

    <!-- to set an initial value for an expression -->
    <section ng-init="tab = 1">
      <ul class="nav nav-pills">
        <!-- to set a class based on an expression -->
        <li ng-class="{ active:tab === 1 }">
          <a href ng-click="tab = 1">Description</a>
        </li>
        <li ng-class="{ active:tab === 2 }">
          <a href ng-click="tab = 2">Specification</a>
        </li>
        <li ng-class="{ active:tab === 3 }">
          <a href ng-click="tab = 3">Reviews</a>
        </li>
      </ul>

      <!-- show an element based on an expression -->
      <div class="panel" ng-show="tab === 1">
        <h4>Description</h4>
        <p>{{product.description}}</p>
      </div>

      <div class="panel" ng-show="tab === 2">
        <h4>Specification</h4>
        <p>{{product.specfication}</p>
      </div>

      <div class="panel" ng-show="tab === 3">
        <h4>reviews</h4>
        <p ng-repeat"review in product.reviews">{{review}}</p>
      </div>

    </section>

At this point it may be a good idea to move this logic to its own controller
so that it isn't completely embedded in our view:

.. code-block:: html

    <section ng-controller="PanelController as panel">
      <ul class="nav nav-pills">
        <!-- to set a class based on an expression -->
        <li ng-class="{ active:panel.isSelected(1) }">
          <a href ng-click="panel.selectTab(1)">Description</a>
        </li>
        <li ng-class="{ active:panel.isSelected(2) }">
          <a href ng-click="panel.selectTab(2)">Specification</a>
        </li>
        <li ng-class="{ active:panel.isSelected(3) }">
          <a href ng-click="panel.selectTab(3)">Reviews</a>
        </li>
      </ul>

      <!-- show an element based on an expression -->
      <div class="panel" ng-show="panel.isSelected(1)">
        <h4>Description</h4>
        <p>{{product.description}}</p>
      </div>

      <div class="panel" ng-show="panel.isSelected(2)">
        <h4>Specification</h4>
        <p>{{product.specfication}</p>
      </div>

      <div class="panel" ng-show="panel.isSelected(3)">
        <h4>reviews</h4>
        <p ng-repeat"review in product.reviews">{{review}}</p>
      </div>

    </section>

.. code-block:: javascript

    app.controller('PanelController', function() {
      this.tab = 1;
      this.selectTab  = function(tab) { this.tab = tab || 1; };
      this.isSelected = function(tab) { return this.tab === tab; };
    });

--------------------------------------------------------------------------------
Code School Chapter 3: Forms and Models
--------------------------------------------------------------------------------

If we want to start working with forms, we need to introduce models. This gives
us live bindings to and from the view and controllers:

.. code-block:: html

    <div class="panel" ng-show="panel.isSelected(3)">
      <h4>reviews</h4>
      <blockquote ng-repeat"review in product.reviews">
        <b>Stars: {{review.stars</b>
        {{review.body}}
        <cite>by: {{review.author}}</cite>
      </blockquote>

      <form name="reviewForm">

        <!-- live preview model below -->
        <blockquote ng-repeat"review in product.reviews">
          <b>Stars: {{review.stars</b>
          {{review.body}}
          <cite>by: {{review.author}}</cite>
        </blockquote>

        <!-- form to drive the live preview -->
        <select ng-model="review.stars">
          <option value="1">1 Star</option>
          <option value="2">2 Star</option>
          <option value="3">3 Star</option>
          <option value="4">4 Star</option>
          <option value="5">5 Star</option>
        </select>
        <textarea ng-model="review.body">
        </textarea>
        <label>by:</label>
        <input type="email" ng-model="review.author" />
        <input type="submit" value="Submit" />
      </form>
    </div>

This gets us the live preview of the model, but we are not able to add the
reviews to our controller yet.  To do that, let's create a controller and
initialize the review:

.. code-block:: javascript

    (function() {

      app.controller('ReviewController', function() {
        this.review = {}:
        this.addReview = function(product) {
          product.reviews.push(this.review);
          this.review = {}; // reset live preview
        };
      });

    })();

.. code-block:: html

    <!-- the xCtrl is a convention used by angular programmers -->
    <form name="reviewForm" ng-controller="ReviewController as reviewCtrl"
     ng-submit="reviewCtrl.addReview(product)">

      <!-- live preview model below -->
      <blockquote ng-repeat"review in product.reviews">
        <b>Stars: {{reviewCtrl.review.stars</b>
        {{reviewCtrl.review.body}}
        <cite>by: {{reviewCtrl.review.author}}</cite>
      </blockquote>

      <!-- form to drive the live preview -->
      <select ng-model="reviewCtrl.review.stars">
        <option value="1">1 Star</option>
        <option value="2">2 Star</option>
        <option value="3">3 Star</option>
        <option value="4">4 Star</option>
        <option value="5">5 Star</option>
      </select>
      <textarea ng-model="reviewCtrl.review.body">
      </textarea>
      <label>by:</label>
      <input type="email" ng-model="reviewCtrl.review.author" />
      <input type="submit" value="Submit" />
    </form>

If we want to validate the input to the data model, angular supplies a few
simple primitives:

* form element classes ng-dirty, ng-valid, ng-invalid
* validation of types: email, url, number

.. code-block:: html

    <!-- disable default browser validation -->
    <form name="reviewForm" novalidate
      ng-controller="ReviewController as reviewCtrl"
      ng-submit="reviewForm.$valid && reviewCtrl.addReview(product)">

      <!-- add required fields to the inputs -->
      <select ng-model="reviewCtrl.review.stars" required>
        <option value="1">1 Star</option>
      </select>
      <textarea ng-model="reviewCtrl.review.body" required>
      </textarea>
      <label>by:</label>
      <input type="email" ng-model="reviewCtrl.review.author" required />
      <input type="submit" value="Submit" />

      <!-- to help debugging the validation -->
      <div>review form is {{reviewForm.$valid}}</div>
    </form>

--------------------------------------------------------------------------------
Code School Chapter 4: Custom Directives
--------------------------------------------------------------------------------

If you want to reuse templates throughout the application, simply pull that part
of the HTML out into a separate file and then use the `ng-include` directive:

.. code-block:: html

    <ul class="list-group">
      <li class="list-group-item" ng-repeat="product in store.products">
        <h3 ng-include="'product-title.html'">
        </h3>
      </li>
    </ul>

.. code-block:: html

    {{product.name}}
    <em class="pull-right">{{product.price | currency}}</em>

In this case, instead of including a partial template file, we can create a
custom directive. Angular allows us to create the directives that can:

* expand the templates (custom tag or attribute)
* model complex UI
* register for events or callbacks
* reusing common components and controller logic

.. code-block:: javascript

    // This creates a new custom directive that returns a directive
    // configuration describing how this directive works. We can then
    // use the directive in HTML like <product-title></product-title>
    // note that product-title in html === productTitle in js
    app.directive("productTitle", function() {
      return {
        restrict: 'E',                    // the type of directive (element)
        templateUrl: 'product-title.html' // url of template
      };
    });


The directives can be used as elements or attributes. The general guide is
to use element directives for UI widgets and attribute directives for
mixin behaviours like tooltips:

.. code-block:: html

    <!-- don't use self closing for custom elements -->
    <product-title></product-title> <!-- 'E': element -->
    <h3 product-title></h3>         <!-- 'A': attribute -->

We can also use custom directives to contain controllers as well:

.. code-block:: javascript

    app.directive("productPanels", function() {
      return {
        restrict: 'E',
        templateUrl: 'product-panels.html',
        controller: function() {
        },
        controllerAs: 'panels'
      };
    });

.. code-block:: html

    <product-panels>
    ...
    </product-panels>

--------------------------------------------------------------------------------
Code School Chapter 5: Dependencies
--------------------------------------------------------------------------------

To separate out common functionality, move common code to its own module:

.. code-block:: javascript

    // in file app.js
    (function() {
      var app = angular.module('store', ['store-products']);
      app.controller('StoreController', function() { });
    });

    // in file products.js
    (function() {
      var app = angular.module('store-products', []);
      app.controller('productTitle', function() { });
      app.controller('productGallery', function() { });
      app.controller('productPanels', function() { });
    });

.. code-block:: html

    <!DOCTYPE html>
    <html ng-app="application">
    <head>
      <link rel="stylesheet" type="text/css" href="bootstrap.min.css" />
    </head>
    <body>

      <script type="text/javascript" href="angular.min.js"></script>
      <script type="text/javascript" href="app.js"></script>
      <script type="text/javascript" href="products.js"></script>
    </body>
    </html>

To add additional functionality to our application, we need to use services
which model dependencies. Angular has a number already defined to perform:

* `$http` - to perform JSON http requests
* `$log` - to log debug messages to the console 
* `$filter` - to filter out elements from an array

.. code-block:: javascript

    // both return a promise object with a .success and .error method
    $http({ method: 'GET', url: '/products.json' });
    $http.get('/products.json', { apiKey: 'password' });
    $http.post('/products/id', { data: 'value' });
    $http.put('/products/id', { data: 'value' });
    $http.delete('/products/id');

    // to specify service dependencies to the controllers, do the following
    app.controller('StoreController', [ '$http', function($http) {
      var store = this;
      store.products = [];
      $http.get('/products.json').success(function(data) {
        store.products = data;
      });
    }]);

    // to specify more dependencies, just list them
    app.controller('StoreController', [ '$http', '$log', function($http, $log) {
    }]);

--------------------------------------------------------------------------------
Developer Guide
--------------------------------------------------------------------------------

https://docs.angularjs.org/guide/controller

Angular can be described as a framework consisting of the following pieces:

* **template**
  
  In angular, the templates are actually HTML that is marked with various
  directives. The root directive `ng-app` marks the start of the application
  that is scanned and compiled when the page is loaded. The rest of the
  magic is achieved through angular's data binding.

* **directive**

  Angular allows basic HTML to be extended with custom attributes and elements.
  Although angular provides a number of attributes out of the box, it makes it
  easy to create your own to add additional functionality to HTML. Bascially,
  think of these as the template expressions that should be parsed and then
  bound to the controller models achieving the two way data binding.

* **model**

  This is the source of truth for an angular application. Models in angular
  are actually just properties of the controller, however angular has another
  way of achieving models that is equivalent to the environment in compilers.
  This is achieved with the `$scope` utility which uses prototypical inheritence
  to have model hierachry.

* **scope**

  This is the context where the model is stored and the controllers are run.
  All directives and expressions have access to it and use it in their operation.
  Scopes also include a number of utilities that make them a bit more useful then
  a simple javascript object:

  * `$watch` - to register pubsub for model changes
  * `$emit` - to manually send an event to parents
  * `$broadcast` - to manually send an event to children
  * `$digest` - run after an `$apply` to check for dirty changes to `$emit`
  * `$apply` - to manually apply changes to the model

  The lifecycle of scopes is as follows:

  * **create** - the root scope is created by the injector during bootstrap
  * **watch**  - when compiling templates, watchers are registered on scopes
  * **mutate** - model mutations are performed in `$scope.$apply`
  * **observe** - `$digest` looks for changes and alerts all affected `$watch`
  * **destroy** - when the scope is no longer in use, call `$scope.$destroy()`

  Watches can be by reference, by collection, or by value (in increasing order
  of performance cost). Use the cheapest one that makes sense, but make sure
  that you use the correct one that will reflect your changes.

* **expression**

  These are simply javascript expressions that are evaled against the current
  `$scope` with the `$eval` method. There is no flow control support (except
  for ternary) and common errors result in `null` and `undefined` instead of
  throwing errors. Furthermore, the result of expressions can be chained to
  filters.

  These expressions are actually safer to run than traditional expressions sent
  to `eval` because they use the `$parse` service which blocks access to globals.
  In order to use things like `window`, the expression must rely upon a service,
  for example `$window`.

  If the expression is run from the result of an event, the event data will be
  passed into the expression as `$event` (either jqlite or jquery object).

  Another useful feature is a one time binding that will only be evaluated
  once `{{::binding}}`. For expressions: `{{ item in ::items }}`.

* **compiler**

  Parses the template and instantiates directives and expressions.

* **filter**

  These simply format the value of an expression for display to the user.
  They can be chained in the expression using `|`. Filters can also be
  injected into controllers by declaring a dependency on `filterXXX`.

  To create your own filter, simply provide a pure idempotent function
  to the `filter` method on the module.

.. code-block::

    {{ expression | filter }}
    {{ expression | filter1 | filter2 }}
    {{ expression | filter:arg1:arg2 }}

    // define our own filter
    app.filter('reverse', function(value) {
      return value.split('').reverse().join('');
    });

* **view**

  The view in angular is actually HTML that is marked up with custom template
  code. Not only can one use templates to parse expressions, angular lets one
  create custom HTML elements as proposed by the upcoming shadow-dom construct.

* **controller**

  All the business logic for an angular application is stored in a controller.
  The documentation gives a succint definition as "a javascript constructor
  function that is used to augment a scope." So, the controller can set the
  initial values of the `$scope` and add behavior to the `$scope` that can
  in turn modify it based on user input. Controllers should be very slim and
  as much code as possible should be moved to services and shared. Some general
  rules for when not to use angular controllers are:

  * manipulating the DOM - use databinding instead
  * format input - use angular form controls instead
  * filter output - use angular filters instead
  * share code or state across - use angular services instead
  * manage component life-cycle - let the injector do its job

* **injector**
  
  Angular has its own built in IOC container to perform dependency injection.
  It works via an idoiomatic DSL where modules or controllers define the
  dependencies they need (imports) and utilities define themselves as available
  for usage (exports). This is generally the same as require.js.

* **module**

  This is simply a container for the different parts of an application including
  controllers, services, filters, and directives. It includes the ability to
  configure itself and a run method (both essentially main methods) and to
  require other modules which can configure themselves.

* **service**

  Services are a little misleading, in fact they are just reusable units
  of business logic that work independent of the view. It should be noted that
  angular services are lazyily initialized and are singletons! The convention
  for built in services is to prefix them with `$`. Services are created with 
  the `factory` method of the module or by the injected `$provide` service.
  The latter is used to perform mock injection during testing.

.. code-block:: javascript

    angular
    .module('myModule', [])
    .factory('myService', ['$log', function($log) {
      var service = {}; // build something to return
      $log.log("I have created a new service instance");
      return service;
    }]);
