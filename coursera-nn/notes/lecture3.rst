================================================================================
Lecture 3: Learning Weights
================================================================================

--------------------------------------------------------------------------------
The Linear Neuron Learning
--------------------------------------------------------------------------------

In a perceptron, the weights are getting closer to a good set of weights.  In a
linear neuron the outputs are getting closer to the target outputs. The percepton
learning algorithm cannot be used on a linear neuron as it averages the training
sets to find a weight vector. In more complex networks, the average of two good
networks may produce a bad network. Thus multi-network, the perceptron algorithm
isn't used.

Linear neurons have a real value output which is the weighted sum of its inputs.
The learning works by reducing the error summed over all the training cases. The
error is the squared difference between the output and the actual output.

.. code-block:: math

    y = \sum_i x_i * w_i
    y = w^t * x

When we encounter an error in our model, we use the delta rule to update the weights
to account for the error:

.. code-block:: match

    \delta w_i = \epsilon * x_i * (t - y)
    \delta w_i = change in weight for w_i
    \epsilon   = the learning rate
    t          = the target output
    y          = the current output
    t - y      = the residual error

    \delta w_i = -\epsilon * \frac{\partial E}{\partial w_i}
               = \sum_n \epsilon * x_i^n * (t^n - y^n)

This may produce worse weights, but it will produce a better overall weight set
for the target output. There may not be a perfect answer given a training set.
If we set the learning rate small enough, we can get close enough to the correct
values. Also, if two inputs are highly correlated, it may make the learning rule
very slow (as we cannot tell which weight to correctly modify). So the major
pain point is choosing the correct learning rate.

--------------------------------------------------------------------------------
The Error Surface of a Linear Neuron
--------------------------------------------------------------------------------

The error space can be represented as a quadratic bowl with the horizontal axis
representing the weight space and the vertical axis representing the error. So
a vertical cross section will be a parabola and a horizontal cross section will
be an ellipse.

The simplest kind of batch learning does a steepest descent on the error surface
(gradient descent perpendicular to the contour lines). The simplest kind of
online learning will zig-zag along the contour lines (as each training set will
pull us in possibly less than ideal directions). However, the training sets will
create a constraint plane that will guide a path to the ideal weights.

Learning can be slow if the ellipse is elongated as the deepest descent will be
following the "parabolic ravine" for a long time.

--------------------------------------------------------------------------------
Training a Logistic Neuron
--------------------------------------------------------------------------------

The derivative of the logic function:

.. code-block:: math

    z = b + \sum_i x_i * w_i

    \frac{\partial z}{\partial w_i} = x_i
    \frac{\partial z}{\partial x_i} = w_i

The derivative of the output function:

.. code-block:: math

    y = \frac{1}{1 + e^-z}

    \frac{\partial y}{\partial z} = y * (y - 1)
      = ... a proof follows

The learning rule is the derivative of the output with respect to each weight:

.. code-block:: math

    \frac{\partial y}{\partial w_i}
      = \frac{\partial z}{\partial w_i} * \frac{\partial z}{\partial z}
      = x_i * y * (1 - y)

    \frac{\partial E}{\partial w_i}
      = \sum_n \frac{\partial y^n}{\partial w_i} \frac{\partial E}{\partial y^n}
      = -\sum_n x_i^n * (t^n - y^n) * y^n * (1 - y^n)
      = ....... (delta rule) * (slope of logistic function)

--------------------------------------------------------------------------------
The Backpropagation Algorithm
--------------------------------------------------------------------------------

There are a few ideas that could be used to train hidden units:

1. Randomly perturb each hidden unit and check if it gets better
1a. This take a very long time
1b. Late in training, perturbing a single weight will usually always be bad

2. Randomly perturb each hidden unit in parallel
2a. This will generally always be detrimental to the network

3. Finite difference approximation (approximate the gradient)

.. code-block:: math

    \frac{\partial E}{\partial z_j}
      = \frac{\partial y_j}{\partial z_j} * \frac{\partial E}{\partial y_j}
      = y_j * (1 - y_j) * \frac{\partial E}{\partial y_j}

    \frac{\partial E}{\partial y_i}
      = \sum_j \frac{\partial z_j}{\partial y_i} * \frac{\partial E}{\partial z_j}
      = \sum_j w_ij * \frac{\partial E}{\partial z_j}

    \frac{\partial E}{\partial w_ij}
      = \frac{\partial z_j}{\partial w_ij} * \frac{\partial E}{\partial z_jj}
      = y_i * \frac{\partial E}{\partial z_j}

   y = activity leading into neuron
   E = error for that output
   z = total value going into neuron
   j = current layer
   i = previous layer

--------------------------------------------------------------------------------
Using Backpropagation
--------------------------------------------------------------------------------

There are a few questions about using backpropagation to train a network, namely:

1. how often to updated the weights (optimization)
2. how to prevent overfitting

For the first case, there are a number of learningtechniques:

* **online**
  This update the weights as new samples come in. The problem with this is that
  the updates spend a great deal of time zig-zagging around in the weight space.

* **full-batch**
  This updates the weights with the entire batch of samples. The problem with
  this is that we may have a bad set of weights and would rather not go through
  the entire set of samples to move the weights just in the right direction.

* **mini-batch**
  This updates the weights with a small batch of samples. This will zig-zag a
  little bit, but will spend most of the time going towards the correct goal.
  This is typically used with large datasets.

Now, how much should the weights be updated. We can choose a fixed learning
weight and use that throughout the training. Otherwise we can have an adaptive
learning weight that can check if the error rate is oscilating around. If so,
it can lower the learning rate. If we are making good progress, we can increase
the learning rate. We can even change the learning rate for each connection
individually. We can change from using steepest descent to another heuristic
near the end of learning.

A learning algorithm doesn't know anything about the data. What we want to do
is learn good trends of the data. However, by sampling a dataset, we may
introduce trends by having gaps in the data or a prevalence of specific
samples. The model will thus learn correct and incorrect trends. To prevent
this we can use some of the following techniques:

* **Weight Decay**
  Try to keep many of the weights small or zero to make the model simpler

* **Weight Sharing**
  Try to keep many of the weights the same to keep the model simpler

* **Early Stopping**
  Have a test dataset that we occasionally peek at to validate our values.
  Once that set starts to get worse, we stop training.

* **Model Averaging**
  Train a number of models and average them

* **Bayesian Fitting of neural nets**
  Fancy model averaging
 
* **Dropout**
  Attempt to remove redundant or unuseful hidden units

* **Generative Pre-training**
  ???
