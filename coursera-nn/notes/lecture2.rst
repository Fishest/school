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
