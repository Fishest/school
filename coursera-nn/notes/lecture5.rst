================================================================================
Lecture 5: Object Recognition
================================================================================

--------------------------------------------------------------------------------
Why Object Recognition is Difficult
--------------------------------------------------------------------------------

* **Segmentation**

  Viewpoints are cluttered with other objects. This makes it hard to tell if
  objects are pieces of the same object. Futhermore, objects are also occluded
  behind other objects.

* **Lighting**

  The intensity of a pixel is determined as much by the lighting conditions as
  it is the color of the object.

* **Deformation**

  Objects can be deformed in a large number of ways, for example cursive vs
  normal script.

* **Affordance**

  Object classes are determined by how they are used. So many chairs may have
  various structures as long as they are used for sitting.

* **Viewpoint**

  Changes in viewpoint can cause changes in the image that most models cannot
  deal with. This moves the information around in the pixels (affine). We need
  to eliminate the dimension hopping.

--------------------------------------------------------------------------------
Achieving Viewpoint Invariance
--------------------------------------------------------------------------------

As humans, we are so good at viewpoint invariance that we do not appreicate how
hard it is to do. There are several techniques to deal with this:

* use redundant invariant features (under transformations)

  - with a big enough bag of features, there is only one way to make an object
  - the higher level features will learn how to construct them
  - we need to avoid contributing features for different objects

* put a box around the image and use normalized pixels

  - if this box is labeled correctly, this solves the dimension hopping problem
  - this can solve many of the affine transformation problems
  - however segmenting to the box is hard (occlusion, errors, orientations)
  - can train with well segmented images and test a number of coarse boxes

* use replicated features with pooling (convolutional nets)
* use a hierarchy of parts that have explicit poses relative to the camera

--------------------------------------------------------------------------------
Convolutional Neural Network for Recognizing Digits
--------------------------------------------------------------------------------

The idea is to use many different copies of the same feature detector with many
different positions. This is because if it is useful in one place, it must be
useful somewhere else. The connections between features will have the same weights
during training. This training reduces the number of free parameters to be learned.
Futhermore, we will have many features maps (say each patch of the image) to learn
different feature sets with the same input weights.

We can train using the same back-propigation algorithm, but now we add constraints
such that a collection of weights are equal befor and after a training sample.

Replicating the features does not achieve invariance, it achieves equivariance.
the neural activities are not invariant to transformation (if the image is
translated, the neural response will also be translated). What is invariant is
the knowledge. So if you know how to detect an image in one part of the scene,
we can learn how to detect it in another part of the scene.

To achieve invariance, we can pool the outputs of replicated feature detectors.
We can average (or take the max) of four neighboring replicated detectors to
give a single output to the next level. This reduces the number of inputs to
the next layer allowing us to have more different features maps. The problem
with this is that after a few layers, we lose the information about position.
If we only care to recognize that there is say a face in an image, this will
not matter.

Yann LeCun (Le Net) uses a number of techniques to tuen the model (pooling,
weight sharing, and local connectivity). This is a form of introducing bias
into the model. Another way to achieve this is to use a much more dumb model,
but using a great deal more data (possibly synthetic).

--------------------------------------------------------------------------------
Convolutional Neural Network for Recognizing Objects
--------------------------------------------------------------------------------

It is harder to make the leap from recognizing hand written digits to objects,
this is because:

* there are hundreds of more classes (1000 vs 10)
* there are hundreds of more pixel (256x256 color vs 28x28 gray)
* two dimensional image of a three dimensional scene
* cluttered scenes require segmentation
* multiple objects in each scene

The current winner for vision-net is a convnet:

* 7 hidden layers (not including pooling)
* first 2 layers are convolutional
* last two layers are globally connected
* trained with patches and reflections
* trained with dropout

  - prevents overfitting
  - prevents neurons from relying on neighbors to fix up errors
  - each neuron will learn more useful feature

* test with four corner patches, central patch, and reflections

  - vote on the highest match
  - train on two Nvidia GPUs (1000 cores)
