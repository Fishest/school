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
