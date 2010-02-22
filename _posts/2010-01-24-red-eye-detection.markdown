---
layout: post
title: Homework 1 - Red Eye Detection
category: school
---

{{ page.title }}
============================================================

<p class="meta"/>24 Jan 2010 - St. Louis</p>

Problem and Solution
------------------------------------------------------------

> _In the language of your choice, create a program that reads in an image(s),
> finds the eyes, and outputs the image with the eye location marked._

As this was supposed to be a warm up assignment, I chose to simply
search for eyes suffering from the
[red eye effect](http://en.wikipedia.org/wiki/Red-eye_effect).
The following is a summary of the solution I implemented:

* Read the image into Matlab (imread).
* Find the highest occurrences of red (255) in the image
* Chose the single highest row and the highest and lowest columns
* Draw a cross-hair on each of those points ([r, cl] [r, ch])

As already mentioned, this was implemented in Matlab and the code can be found in the following
[repository](http://github.com/bashwork/school/tree/master/559/homework1/homework1.m).

Successful Image Conversion
------------------------------------------------------------

Since the following image contains a pretty consistent red eye color that
maxes out the red spectrum, we can simply search for those points. After
that, we only need two points, one for each eye, so we just choose the
max and min of the columns. Next, since we only need to place two points,
we only need one row. The result can be seen below:

<img width="640" src="http://github.com/bashwork/school/raw/master/559/homework1/working-input-result.jpg" />

...Less Than Successful Image Conversion
------------------------------------------------------------

Since the following image does not contain red eyes (especially red eyes that are
in the same range as the previous image), we not only do not detect the subject's
eyes, but we accidental detect random parts of the tunic instead:

<img width="640" src="http://github.com/bashwork/school/raw/master/559/homework1/failing-input-result.jpg" />

