---
layout: post
title: Project 2 - PCA Face Recognition
---

{{ page.title }}
============================================================

<p class="meta"/>11 Feb 2010 - St. Louis</p>


Problem Description
------------------------------------------------------------

We were allowed to chose from two projects (and a number of extra sub-projects),
however this is the one that I decided to implement:

**Face Recognition**
*This option explores the use of PCA for recognition*

1.  *Base Project, [14 points]*

    1. Acquire and make sure that you can read in the images from: the AT&T face
       database.

    2. Create the PCA decomposition of this set of images (you may shrink the
       images so that this process all fits into memory), leaving out one image per
       person (for later testing).

    3. For each test image, project it onto the PCA basis and compute its coefficients.

    4. Find the training image with the most similar coefficients, and record if
       this is an image of the same person.

    5. Report recognition accuracy results for a) recognition by computing the mean
       image for each person in the database, and (for each test image) finding
       the closest mean face, and (b,c,d,e) when using 2 4 6 and 9 principle components. 

2.  *Extension, Worth [6 points]* 

    1. (This is probably *not* as easy as it seems). There are a large number of
       data sets of labeled faces. My favorite is the "aligned labeled faces in
       the wild" which is drawn from faces in AP news photos, and the faces are
       then warped and aligned into a common coordinate system.

    2. Make reasonable choices for, and then report on (a) your choice of test
       and training data set -- which is not as clear because there are different
       numbers of faces for different people, (b) whether you get better performance
       when using the entire 256 x 256 image, or by using just the "central" face
       portion. Discuss your results, which results are better? Why?

    3. Discuss your results on this data set versus the data set in the base option.
       Which results are better? Why? 


Solutions
------------------------------------------------------------

As [numpy][] already had the svd operation defined (like Matlab),
most of the code I had to write was simply scaffolding around it
and helpers to get data into it. The following is the actual
implementation of svd that I used (*note the T method is transpose*):

    def svds(images):
        U, S, Vh = numpy.linalg.svd(images, full_matrices=False)
        return (U, (Vh.T * S)) 

The hardest coding part was in computing the eigenface for a new
image and finding which training image it looked the most like:

    def get_eigenface(self, image):
        compare = image - self.mean
        return numpy.dot(self.U.T, compare)
 
    def get_nearest_image(self, image):
        index = self.get_nearest_image_index(image)
        return self.images[index]
 
    def get_nearest_image_index(self, image):
        coefs = self.get_eigenface(image)
        # argmin returns the index of the min element
        return numpy.argmin(find_distance(coefs, self.V))

To find the distance between a new image's coefficients and
the coefficients of the training set, I simply used the
following functions:

    def compute_distance(n, v):
        return ((n - v)**2).sum()
         
    def find_distance(n, vector):
        return [int(compute_distance(n, v)) for v in vector]

The vast majority of code was created in the test runner scripts
which are discussed later in this posting.


AT&T Dataset Classification Accuracy
------------------------------------------------------------

In the first section, it is quite evident that increasing the
number of principal components generated assists in accurate
facial recognition. Except for one case at ten components
(which I cannot really explain) every result went up for the
AT&T dataset:

*   **400 Images with 2 Principal Components**

    * test image against full image set: 57.50%
    * mean image against full image set: 45.00%
    * test image against mean image set: 32.50%

*   **400 Images with 4 Principal Components**

    * test image against full image set: 80.00%
    * mean image against full image set: 75.00%
    * test image against mean image set: 60.00%

*   **400 Images with 6 Principal Components**

    * test image against full image set: 87.50%
    * mean image against full image set: 85.00%
    * test image against mean image set: 85.00%

*   **400 Images with 9 Principal Components**

    * test image against full image set: 95.00%
    * mean image against full image set: 97.50%
    * test image against mean image set: 90.00%

*   **400 Images with 10 Principal Components**

    * test image against full image set:  92.50%
    * mean image against full image set: 100.00%
    * test image against mean image set: 100.00%


Labeled Faces in the Wild Dataset Discussion
------------------------------------------------------------

This was the real test of the ability of the face recognition
as it roughly simulates a realistic situation where this process
would come into play. After downloading the dataset, I
generated an list ordered by the number of images per person
and decided to simply work with the five largest sets. I looked
through a few of the images and thought the remainder would be
*good enough* (lesson learned).

There were a number of procedures I tried in order to boost the
accuracy of the recognition (and many variations and combined
permutations of those as well). The first thing I did was try
and change the size of the images. This did not affect the
accuracy until I got down to 45x45 sized images. As a result I
settled on 80x80 image sizes simply to increase my speed.

Next, I decided to crop the relevant portions of the image.
I determined my threshold via guess and check with [pylab][]
and a number of pictures of ex-president Bush. I found a pretty
consistent window with an upper-left point of 50,50 and
bottom-right point of 200,200. This increase my accuracy and
got two tests images to be correctly identified (with a two
person training set of 766 images).

I then decided to increase the training sets to five people
with a total of 1140 images. All my detections immediately
failed except for Bush and the test images against the mean images.
I decided to reduce my image sizes back down to 45,45 so I
could try a few things faster, namely removing bad images from
the dataset.

After removing 33 images from the Bush set, I tried the detector
with no face window filter and all the the detectors failed. When
I added it back, I was able to detect Mr. Bush again. While looking
at some of the images included in the set, it was immediately clear
(after using the AT&T set) that the real problem was with the
training data.  After removing only 33 from the set of 530, I was
able to detect Bush in a collection of 5 other people.


Performance Results
------------------------------------------------------------

For this project I used the numpy package which is a high level
wrapper around the atlas linear algebra library (it tries to
tune performance of BLAS and Lapack to your machine). This allows
for a marked performance increase in a number of python operations,
however, not all of the library is implemented in c/c++. Continuing,
even when the library drops into pure c, it cannot turn a single
core laptop into a supercomputer.

For both sections of the assignment, the main bottleneck was performing
the svd on the training data. The following examples show some of the
timing results for different data sets:

*   **400 images at (92x112)**

    * 0.0773 seconds to load images and take mean
    * 9.7361 seconds for svd 
    * 0.0783 slicing primary components

*   **40 images at (92x112)**

    * 0.0098 seconds to load images and take mean
    * 0.2367 seconds for svd 
    * 0.0108 slicing primary components

*   **766 images at (80x80)**

    *  0.1596 seconds to load images and take mean
    * 33.5918 seconds for svd 
    *  0.1606 slicing primary components
    
*   **1140 images at (80x80)**

    *  0.2156 seconds to load images and take mean
    * 58.6586 seconds for svd 
    *  0.1895 slicing primary components

The clearly shows the performance hit taken by using an interpreted
language.  However, since the only operation that is taking a significant
portion of time is the svd, a solution would be to call down to a c library
or possibly run on a better tuned interpreter (pysco, pypy, unladen, etc).
It should also be noted that projecting the new image to test and comparing
its resulting vector took milliseconds across the board.


Example Result Sets
------------------------------------------------------------

*Although including the vast amount of testing data would be prohibitive
I will link to the datasets that I used and have provided the result
logs from my testing*

**Aligned Labeled Faces in the Wild**

*  [link](http://www.openu.ac.il/home/hassner/data/lfwa/)
*  [results](http://github.com/bashwork/school/blob/master/559/project2/examples/pca-section2.log)

   This is a collection taken from the labeled faces in the wild, cropped,
   warped, and center aligned. It is a large collection of labeled faces, however,
   only a few personalities have a large collection of images (most have less than
   10). Continuing, the quality of the images **greatly** varies.

**AT&T Database of Faces**

*  [link](http://www.cl.cam.ac.uk/research/dtg/attarchive/facedatabase.html)
*  [results](http://github.com/bashwork/school/blob/master/559/project2/examples/pca-section1.log)

   This is a collection built internally at AT&T for a research project. There
   are 40 sets of people with ten images each of slightly different orientation
   (looking straight, looking up, etc). It is a high quality set that made it
   easy for your tests to run well.


Code Used To Generate The Result Sets
------------------------------------------------------------

The following is an example of creating a system that can recognize
a face from the trained data set. It then displays the two images
side by side so the user can evaluate the results:

    import pylab
    from lib.pca import PCA
    from lib.utility import *

    images = OpenImageDirectory("images/faces")
    pca = PCA(images = images)
    pca.initialize()
    result = pca.get_nearest_image(images[0])

    pylab.subplot(1,2,1)
    pylab.imshow(images[0].reshape((112,92)))
    pylab.subplot(1,2,2)
    pylab.imshow(result.reshape((112,92)))
    pylab.gray()
    pylab.show()

*For more complex examples of image testing with this code,
examine the following test runners*

*  [runner 1](http://github.com/bashwork/school/blob/master/559/project2/pca-section1.py)
*  [runner 2](http://github.com/bashwork/school/blob/master/559/project2/pca-section2.py)


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
   as well as a front-end for a number of linear algebra operations
   (matrix multiply, dot product, svd, etc).

*  [Scipy](http://www.scipy.org/)

   This is the umbrella project for the python science libraries.
   I didn't actually use any of its functionality in this project.

*  [Pylab](http://www.scipy.org/PyLab)

   The goal of pylab is to make switching from Matlab to python
   as easy as possible. It clones most of the functionality directly.
   I used its graphing capabilities (wrappers around Matplotlib and
   a number of GUI tool-kits).


  [repository]: http://github.com/bashwork/school/tree/master/559/project2/ "Master Repository"
  [numpy]: http://numpy.scipy.org/ "Numpy"
  [pylab]: http://www.scipy.org/PyLab "Pylab"
