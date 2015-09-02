================================================================================
Lecture 2: Perceptrons
================================================================================

--------------------------------------------------------------------------------
Architectures
--------------------------------------------------------------------------------

**Feed Forward Neural Network**

  - the first layer is the input and the last layer is the output
  - there can be 1 or more hidden layers between these
  - if there is more than one hidden layer, then we call them deep neural networks
  - they compute a series of transformations between the inputs and outputs
  - these may change the similarities between the various cases (more or less)
  - to achieve this, we need the neurons to model with non-linear functions
  - the activities of the neurons are a non-linear function of the neurons below them

**Recurrent Neural Network**

  - these have directed cycles in their connection graph
  - if a graph is followed, it may be possible to get back to the original neuron
  - they can have very complicated dynamics and are usually hard to train
  - closer to correct biological use cases
  - these can be thought of as deep in terms of time
  - the time connections all have the same weights
  - they can remember information for a long amount of time
  - this ability is really hard to train
  - this can be trained for NL tasks like predicting next characters in a string
  - sample from the distribution of the weights produced from the net

**Symmetrical Neural Network**

  - these are like recurrent nets, but the weights back and forth are the same
  - these are easier to analyze than recurrent nets
  - they are also more restricted in what they do because the respect an energy function
  - symmetrically connected nets without hidden units are called "Hopfield Nets"

--------------------------------------------------------------------------------
Perceptrons
--------------------------------------------------------------------------------

The standard pattern for statistical pattern recognition

1. Convert the raw input vector into a vector of feature activations
1a. Use hand written programs to deduce features based on common sense
2. Learn how to weight each feature activation to get a single scalar quantity
3. If this quantity is above some threshold, decide this is a positive example

The activation is the binary threshold neuron. To learn the bias value, we simply
append it as an extra input with a constant value of 1. We can then learn the
bias for the remaining input.

The following is the perceptron convergence procedure:

1. Use a policy that will keep picking every training case (good sample spread)
2. If the input vector is correctly classified, do nothing
3. If the input vector is incorrectly negative, add its values to the weights
4. If the input vector is incorrectly positive, subtract its values from the weights
5. If a set of weights exists, this will correctly find them

Thus this devolves into finding the correct set of features which is where neural
networks pick up and do for us.

--------------------------------------------------------------------------------
Perceptrons Geometry
--------------------------------------------------------------------------------

The possible weights for a perceptron can be thought of as an N-dimensional
space:

- each space has one dimension per weight
- a point in this space represents a particular setting for all weights
- by eliminating the threshold, each training case is a hyperplane through the origin
- the weights must lie on one side of this hyperplane to correctly classify
- the input vector for that training case is perpendicular to the plane
- the scalar product of the weight vector (with the angle between less than 90 degrees)
  and the input vector will be positive and will classify as (1)
- if the weight vector angle is greater than 90 degress, the scalar product will be
  negative and will classify as (0)
- all the input vectors together will create a constraint cone; any weight vector in
  that space will correctly classify all the training examples
- this has a convex solution

To prove that this will find a solution, we can assume there is a large-margin
feasibility cone for the input set. Every time we make a mistake, the weight
vector is corrected by the mean square error of the feature vector which will
eventually put the weight vector in the feasibility cone.

--------------------------------------------------------------------------------
Why Perceptrons Fail
--------------------------------------------------------------------------------

If you choose features by hand and if you have enough features, a perceptron can
do just about anything. For example, you can have a feature unit for every
instance of a binary input vector. This creates a lookup table that will not
generalize.

The classic example is the XOR problem which no linearly separating hyperplane
can be found (SVM can do this though).


