================================================================================
Lecture 1: Introduction
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

Neural networks will perform well at things the brain performs well at and V.V:

* good at identifying items in an image
* bad at performing large calculations

We model the neurons in a NN after the neurons in a brain:

* they are generic and can learn any function
* they can adapt by + / - the weight of the connection
* they can have a large fan out to learn complex functions

--------------------------------------------------------------------------------
Types of Neurons
--------------------------------------------------------------------------------

**Linear Neuron**

.. code-block:: math

    y = b + \sum_i x_i * w_i
    y = output
    b = bias
    i = index over connections
    x = output i
    w = weight on input i

**Binary Threshold Neuron**

1. Compute a weighted sum over the inputs
2. Send out a fixed size spike of activity if the weight is over a threshold
3. Each spike is a proposition and each neuron composes each truth
a. works on the idea of logic which isn't a great model of brains

.. code-block:: math

    z = \sum_i x_i * w_i
    z = output sum
    y = { 1 if z >= \theta else 0 } 

This can also be represented as:

.. code-block:: math

    z = b + \sum_i x_i * w_i
    b = -\theta
    y = { 1 if z >= 0 else 0 } 

**Rectified Linear Neuron**

1. They compute a linear weighted sum of inputs
2. The output is a non-linear function of the total input

.. code-block:: math

    z = b + \sum_i x_i * w_i
    y = { z if z > 0 else 0 } 

**Sigmoid Neuron**

These give a real value output that is a smooth and bounded function of
their input. Typically these use a logistic function which is easy to
perform derivates on.

.. code-block:: math

    z = b + \sum_i x_i * w_i
    y = 1 / (1 + \e ^ -z)
    y = 1 if isLarge(z) else 0 if isSmall(z)

**Stochastic Binary Neuron**

These are the same as the Sigmoid neuron, however instead of outputting the
value of the logistic function, they use that to generate a probability of
producing 1 / 0 and sample from that.

.. code-block:: math

    z = b + \sum_i x_i * w_i
    s = 1 / (1 + \e ^ -z)
    y = p(s = 1)

This idea can be used for the Rectified neuron by treating the output as the
rate of a poisson distribution.

--------------------------------------------------------------------------------
Simple Learning
--------------------------------------------------------------------------------

For the MNIST dataset, think about the bottom layer being the layer checking the
individual pixel intensities. If that pixel is on, it gets to cast a vote to one
or more output shapes (numbers). The output class with the most votes wins.

To train, increment the active pixels for correct output classes and decrement
active pixels for incorrect classes. We start with random initial weights. A
single layer is equivalent to learning a template for the inputs (memorizing
the inputs). The output is the one with the biggest template overlap.

To do better we need to extract general featurest of output classes and match
on those.

--------------------------------------------------------------------------------
Types of Learning
--------------------------------------------------------------------------------

1. Supervised Learning

   * learn to predict an output when given an input vector
   * regression and classification are the two types
   * regression is given a stream of numbers, try and predict the correct number
   * classification is choose a class label given a feature set (0 / 1)
   * given `y = f(x, W)` mutate `W` to the training set to `y` is the correct label
   * validate by squared error `e - 0.5 * (y - t) ^ 2` (`t` = expected label)

2. Unsupervised Learning

   * learn a good internal representation of an input
   * clustering was the general use for this approach for a long time
   * provide compact low dimensional representation of the input
   * can find economical representations of features (binary)

3. Reinforcement Learning

   * learn to select an action to maximize a payoff
