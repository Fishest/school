---
layout: post
title: Project 2 - Viola Jones Face Detector
---

{{ page.title }}
============================================================

<p class="meta"/>11 Feb 2010 - St. Louis</p>

Problem Description
------------------------------------------------------------

For this project we were allowed to form groups to work on one of the two problems
together, however there was a catch.  For each added team member, the team would
have to solve an extra problem.  As such, it really only made sense for each
student to tackle the problem on their own and simply do the one extra problem
that they were on the hook for (which is the option I chose).

We were allowed to chose from two projects (and a number of extra sub-projects),
however this is the one that I decided to implement:

**Face Detection**
*This option considers the Viola Jones Face Detector*

1.  *Base Project, [14 points]*

    The base option is to either start from scratch, or to complete the code that
    we started from class. The extensions are to explore different facets of the
    Viola Jones training process, exploring different features, different
    boosting approaches, or characterizing performce. 

2.  *Extension, Worth [6 points]* 

    Explore the completeness of the feature set. The code from class chose N
    features, and each feature was the best of M randomly generated features.
    The code online uses N=100, and M=20, whereas the original Viola-Jones paper
    exhaustively explored all features and included nearly 200 total features.
    For this extension:

    1. Characterize the performance (on the set aside test data), for classifiers
       trained with different settings for N,M.

    2. Based on your results, discuss which is more important. Is it helpful to
       have more overall features (larger N?) or to try many more possible
       features when figuring out which feature to choose next (much larger M?). 

3.  *Extension, Worth [6 points]*

    For this extension, explore potential ways to speed up execution

    1. Modify your base algorithm to use a cascade of filters (where you can
       mostly reject possible rectangles after just a few features are evaluated).
       Section 4 of the original Viola Jones paper discusses the original approach
       to building the cascade, you are encouraged to use this as a starting point
       to think about how to choose an ordered set of detectors, but are not required
       to exactly follow their model.

    2. Detail pseudo-code of your approach to building the cascade, running time to
       create the cascade, and improvements to the running time when using the
       cascade on sample images (versus not using the cascade). 

4.  *Extension, Worth [6 points]*

    Explore different learning approaches. My example code from class uses a naive
    and partial implementation of boosted learning. In this extension, explore the
    variants of "GentleBoost" and "AdaBoost" (or any other learning algorithm of
    your choice). Present results in terms of training time and classification
    accuracy based on this approach.

5.  *Extension, Worth [6 points]*

    Open ended exploration of features. Viola Jones uses particular features
    defined on a 24 x 24 pixel face. Explore any other set of features for
    face detection.

    1. Give pseudocode for how you generate features

    2. Give running time comparison using your features vs. the rectangular
       features of Viola-Jones.

    3. Give classification accuracy of your features vs. rectangular features of
       Viola-Jones, for a complete classification system using the same number
       of total features. 


Solutions
------------------------------------------------------------

What follows is a pseudo-code description of the various algorithms I used to
generate the random dot autostereograms to complete the first part of the
assignment:

TODO

Classification Accuracy
------------------------------------------------------------

TODO

Performance Results
------------------------------------------------------------

TODO

Discussion
------------------------------------------------------------

For the first implementation, I used the rough algorithm that Dr. Pless
had on the project description and quickly coded up a small script with
a few guessed numbers--it didn't work. After that I decided to rework 
the code into smaller methods and do some investigation on what kind
of separation was needed for my monitor and how that would be calculated
consistently.

After I had all the values pre-calculated, the random dot stereogram just
worked and as such the animated random dot stereogram worked as well
(since it was just creating N random dot stereograms). It did however
take a while to create and a good bit of disk space. The only problem I
faced after this portion was getting the textured stereogram working.

Since I had abstracted the separation point mapping, I was able to reuse
all the existing code and I simply had to worry with pulling the correct
pixel values from the texture.  At first this failed because my texture
was not wide enough to cover the separation needed to provide the correct
depth. After creating some pre-flight code to make sure the texture was
acceptable for the image, this portion worked as well.  The only thing that
remains is a bit of distortion in the resulting stereogram that can only
really be seen when using a texture that isn't abstract enough to hide it.

Demonstration of Successful Detections
------------------------------------------------------------

*What follows are a collection of autostereograms representing the various
required solutions for the problem sets. Open any image in a new window to
see it at full screen. It should be noted that the animated gif is 15 Mb*

**Random Dot Stereogram**

<img width="320" src="http://github.com/bashwork/school/raw/master/559/project1/images/boxes.jpg" />
<img width="320" src="http://github.com/bashwork/school/raw/master/559/project1/images/boxes-rd-sird.jpg" />

**Textured Stereogram**

<img width="320" src="http://github.com/bashwork/school/raw/master/559/project1/images/dino.jpg" />
<img width="320" src="http://github.com/bashwork/school/raw/master/559/project1/images/dino-textured-sird.jpg" />

**Animated Stereogram**

<img width="320" src="http://github.com/bashwork/school/raw/master/559/project1/images/human.gif" />
<img width="320" src="http://students.cec.wustl.edu/~gbc1/human-rd.gif" />


Code Used To Generate The Result Sets
------------------------------------------------------------

*The following is an example of creating a simple random dot stereogram*

    from stereogram import SIRD
    
    sird  = SIRD("images/some-depth-map.jpg")
    image = sird.create_random_dot()
    image.show()

*In order to create a textured stereogram, the user simply needs to supply
the texture to use to hide the depth-map*

    from stereogram import SIRD
    
    sird  = SIRD("images/some-depth-map.jpg")
    image = sird.create_texture("images/some-texture.jpg")
    image.show()

*In order to create an animated SIRD, the user first had to create
an image generator which they would then pass to the animated gif helper
library:*

    from stereogram import SIRD
    import lib
    
    sird  = SIRD("images/some-depth-map.jpg")
    images = sird.create_animated_random_dot()
    lib.CreateAnimatedGif("output.gif", images)

Complete Source Code
------------------------------------------------------------

As already mentioned, this project was implemented in python and the full
code for all the solutions can be found in the following [repository][].
As for support libraries, the following were used throughout the project:

*  [Python Imaging Library(PIL)](http://www.pythonware.com/products/pil/)

   This was used for all the low level image management and manipulation
   like opening and saving image formats and getting and setting pixel
   values

*  [Numpy](http://numpy.scipy.org/)

   This was used to operate on multi-dimensional matrices in python

*  [Scipy](http://www.scipy.org/)

   This was used for all the low level linear algebra functionality.
   Its usage allows a mostly seamless transition from Matlab to python.

Footnotes
------------------------------------------------------------

  [repository]: http://github.com/bashwork/school/tree/master/559/project1/ "Master Repository"
