=================================================
Homework 1
=================================================

:Author: Galen Collins bashwork at gmail dot com
:Date:   Sun Jan 24 17:00:50 CST 2010

*In the language of your choice, create a program that reads in an image,
finds the eyes, and outputs the image with the eye location marked.*

Solution
-------------------------------------------------

I chose to detect eyes by using red-eye detection and removal. The solution
was obtained by the following steps:

* read the image into Matlab
* run the image through three predetermined color thresholds (RGB)
  * these were created with inspection using impixel on the image
* combine the three color logic vectors into a single logic vector of pixel locations
* remove the original image's red component where the pixel is true in the logic vector
