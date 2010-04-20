---
layout: post
title: Project 4 - Final Project Status
---

{{ page.title }}
============================================================

<p class="meta"/>20 Apr 2010 - St. Louis</p>


Description
------------------------------------------------------------

For the final project I will be reimplementing the algorithm discussed in the [superpix][] paper
in [python][]. I will be working alone on the project, so as per the project specification, a
re-implementation should meet the requirements for this task. As far as I am able, I will be
implementing the algorithm from scratch while using [numpy][] and [pylab][] to provide equivalent
base Matlab functionality.

Current Status
------------------------------------------------------------

As of now, I have traversed the paper as well, a majority of the referenced literature,
and a collection of related material to get a better understanding of the problem to solve.
Furthermore, I have reproduced the test runner in python, created code to generate the boundary
cost maps from input images, and created a graph framework to use for determining the
separation paths across the image.

The problems that I have run into is are as follows:

*   I do not have a full grasp on the s-t min cuts algorithm to be used in creating paths
*   The paper doesn't decently explain how the algorithm uses the constraining weights
    for crossing a path, moving perpendicular to the source/sink, and distancing neighboring
    paths.
*   The paper doesn't make clear exactly how the authors choose each path and boundary grid
    aside from the fact that they are added incrementally. 

Finally, the test data that I will be using to test my implementation will be drawn from
the processed images presented in the paper (which were found in the [bsdb][]) as these
are the only results of their algorithm I could find:

* http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/gray/42049.html
* http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/gray/54082.html
* http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/gray/271035.html
* http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/gray/208001.html
* http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/dataset/images/color/295087.html

External Links
------------------------------------------------------------

*  [Project Paper](http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf)

   This is the paper that was presented at the CVPR 2008 conference. It will be the main reference
   for this project.
  
  [superpix]: http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf "Superpixel Lattice"
  [python]: http://www.python.org "Python Programming Language"
  [repository]: http://github.com/bashwork/school/tree/master/559/project2/ "Master Repository"
  [numpy]: http://numpy.scipy.org/ "Numpy"
  [pylab]: http://www.scipy.org/PyLab "Pylab"
  [bsdb]: http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/ "Berkeley Segmentation Dataset and Benchmark"

