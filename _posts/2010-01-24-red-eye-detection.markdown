---
layout: post
title: Homework 1 - Red Eye Detection
---

{{ page.title }}
============================================================

<p class="meta"/>24 Jan 2010 - St. Louis</p>

Problem and Solution
------------------------------------------------------------

> _In the language of your choice, create a program that reads in an image,s
> finds the eyes, and outputs the image with the eye location marked._

I chose to detect eyes by using red-eye detection and removal.
The solution was obtained by the following steps:

* Read the image into Matlab.
* Pass the image through three per-color(RGB) static thresholds to create
  three color location logic vectors (these were created by manually inspecting
  pixels of interest).
* Logically *AND* the three color logic vectors into a single logic vector.
* Remove the original image's red component where the pixel is *TRUE* in the logic vector.

As already mentioned, this was implemented in Matlab. The code can be found in the following
[repository](http://github.com/bashwork/school/tree/master/559/homework1/homework1.m).

Successful Image Conversion
------------------------------------------------------------

Since the following image contains a pretty consistent red eye color, we can just
create a static threshold of the colors and send the image through it.  We then have
a logic vector that we can apply against the original image to perform any alteration
on the pixels that matched that color range.

<img width="640" src="http://github.com/bashwork/school/raw/master/559/homework1/working-input-result.jpg" />

...Less Than Successful Image Conversion
------------------------------------------------------------

Since the following image does not contain red eyes (especially red eyes that are
in the same range as the previous image), we not only do not detect the subject's
eyes, but we accidently detect random parts of the tunic instead.

<img width="640" src="http://github.com/bashwork/school/raw/master/559/homework1/failing-input-result.jpg" />

