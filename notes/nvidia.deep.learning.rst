================================================================================
Nvidia Deep Learning
================================================================================

https://developer.nvidia.com/digits
https://developer.nvidia.com/cudnn
https://developer.nvidia.com/deep-learning
https://developer.nvidia.com/deep-learning-courses

--------------------------------------------------------------------------------
Chapter 1: Introduction
--------------------------------------------------------------------------------

A neural network is composed of neurons which operate as follows:

.. code-block:: math

    y = F(w_1 x_1 + w_2 x_2 + w_3 x_3)
    F(x) = max(0, x)

    F = simple activation function
    y = value of neuron

Deep Neural Networks (Genral Approach)

* No need to design features ahead of time / extracted automatically
* learned features are optimal for the task at hand
* robust to natual variations in the data learned
* the same NN approach can be generalized for many different applications
* many different data types can be used as input data
* performance improves with more data
* method of training is massively parrallelizeable

Convolutional Neural Networks (Images)

* modeled after the human visual cortex
* learns a hierarchy of visual features
* local pixel level features are scale and translation invariant
* learns the "essence" of visual objects and generalizes well
* each neuron feeds to every lower level neuron

Recurrent Neural Networks (Natual Langauge)

* very good at learning sequences of input
* works by feeding back from a hidden layer to itself 
* essentially allows loops that form a sort of HMM

--------------------------------------------------------------------------------
Chapter 1: GPU Computation
--------------------------------------------------------------------------------

Typical GPU DNN application hierarchy:

* Application: digit recognition
* GPU Accelerated Libraries: Caffee, Theano, Torch, Kaldi
* Performance Libraries: cuDNN, cuBLAS
* CUDA
* GPU

--------------------------------------------------------------------------------
Chapter 1: Questions
--------------------------------------------------------------------------------

* Networks should be made bigger and then overfitting controlled with regularization
  methods instead of being restricted to a smaller network. Also, previously trained
  networks can be used and then tuned for a specific purpose.
* A DNN can be run in reverse back projecting the features that were most
  salient in the classification. Deconvolution networks can be used to find
  the optimal images that would trigger higher level neurons.
* DNN are better than traditional approaches when using strictly raw data. If
  the data is structured or abstracted away, ensemble methods prove better.
* A DNN can be trained using un-classified data by changing the objective of the
  training process. Say to compress the dimensionality of the training set or 
  represent sparse clusters of the set.
* A pre-trained network can be fine tuned by replacing the last layer with a new
  layer and training on new specific data. This is because the lower level neurons
  are generic enough to be reusable.
