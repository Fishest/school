---
layout: post
title: Project 4 - Final Project Status
---

{{ page.title }}
============================================================

<p class="meta"/>06 Apr 2010 - St. Louis</p>


Description
------------------------------------------------------------

For the final project I will be reimplementing the algorithm discussed in the [superpix][] paper
in [python][]. I will be working alone on the project, so as per the project specification, a
re-implementation should meet the requirements for this task. As far as I am able, I will be
implementing the algorithm from scratch while using [numpy][] and [pylab][] to provide equivalent
base Matlab functionality.

description of algorithm

The final goal for this project will be to create a library that can be called with any image
type and return a processed super pixel image. In order to evaluate the result of the library,
a simple command line (or GUI driven) application will be created around the library that will
take in an image and show a side-by-side before and after screen. The application will also
provide the ability to tune the various parameters of the system and see the results reflected;
these include: the super pixel resolution, the path tortuosity, and the path width constraint.
I will also use the human labeled images along with a simple distance function to produce
quantitative accuracy results of my implementation.

In order to test the algorithm, I will use a collection of images ranging in their degree
of complexity (i.e. a simple object on a constant background to a city scene with a large
number of features). Using the test applications I will write, I will examine the resulting
super pixel images and observe the result of the tuning on the result of the images.

I will be obtaining all my image data from the [bsdb][] which has a large collection of images
that have been hand segmented by a collection of users. As such I will have no need for any
special photography equipment.

External Links
------------------------------------------------------------

*  [Project Paper](http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf)

   This is the paper that was presented at the CVPR 2008 conference. It will be the main reference
   for this project.
  
*  [Project Page](http://web4.cs.ucl.ac.uk/research/vis/pvl/index.php?option=com_content&view=article&id=78%3Asuperpixel-lattices&Itemid=60)

   This page contains a brief project description as well as the projects implementation in Matalab.
   Although the code will not be used in my re-implementation (which will be in python), it may be used
   as a guide.

  [superpix]: http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf "Superpixel Lattice"
  [python]: http://www.python.org "Python Programming Language"
  [repository]: http://github.com/bashwork/school/tree/master/559/project2/ "Master Repository"
  [numpy]: http://numpy.scipy.org/ "Numpy"
  [pylab]: http://www.scipy.org/PyLab "Pylab"
  [bsdb]: http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/ "Berkeley Segmentation Dataset and Benchmark"

