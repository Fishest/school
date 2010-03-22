'''
'''

import os, time
import numpy as np
from PIL import Image, ImageOps

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
__log = logging.getLogger("project.utility")

# ----------------------------------------------------------------- # 
# Project Helper Methods
# ----------------------------------------------------------------- # 
def CreateImagePyramid(image, scale=1.25):
    ''' Given a pil image, this returns an image pyramid with
    each image reduced by the scale factor from the previous image.

    :param image: The image to create an image pyramid for
    :param scale: The scale factor to reduce the image at each stage
    :returns: The image pyramid for the specified image
    '''
    def next(si):
        while min(si) >= 24:
            yield si
            si = map(lambda n: int(n/scale), si)
    return [image.resize(size) for size in next(image.size)]

def CreateIntegralImagePyramid(image, scale=1.25):
    ''' Given a pil image, this returns an integral image
    image pyramid with each image reduced by the scale factor
    from the previous image.

    :param image: The image to create an image pyramid for
    :param scale: The scale factor to reduce the image at each stage
    :returns: The image pyramid for the specified image
    '''
    def next(si):
        while min(si) >= 24:
            yield si
            si = map(lambda n: int(n/scale), si)
    return [CreateIntegralImage(image.resize(size)) for size in next(image.size)]

def CreateFeaturePyramid(feature, size, scale=1.25):
    ''' Given a numpy array, this returns an feature pyramid with
    each feature increased by the scale factor from the previous feature.

    :param image: The feature to create an image pyramid for
    :param size: The image size to peak at
    :param scale: The scale factor to reduce the image at each stage
    :returns: The feature pyramid for the specified feature
    '''
    def _nx(si):
        _mul = lambda n: int(n*scale)
        while max(si) <= max(size):
            yield si
            si = map(_mul, si)

    def _im(ft, sz):
        im = Image.fromarray(ft).resize(sz)
        return np.asarray(im)

    return [_im(feature, size) for size in _nx(feature.shape)]

def CreateIntegralImage(image):
    ''' Given a PIL image, this computes the integral
    image and returns as a numpy array.

    :param image: The image to create an integral image for
    :returns: The integral image for the specified image
    '''
    result = np.asarray(image).astype("double")
    return np.cumsum(np.cumsum(result, axis=1), axis=0)

def RemoveMeanFromImages(images):
    ''' Given a numpy array of image, this computes the
    mean image and removes it from the collection of images.

    :param images: A numpy array of images
    :returns: The mean image of the input array
    '''
    mean = images.mean(axis=0)
    for id in range(images.shape[0]):
        images[id] -= mean
    return mean

def PerformPCA(images):
    ''' Given a numpy array of image, this performs PCA
    on the input and returns the relevant parameters.

    :param images: A numpy array of images
    :returns: (u,s,v, mean-image)
    '''
    mean = RemoveMeanFromImages(images)
    u,s,v = np.linalg.svd(images)
    v = v[:images.shape[0]]
    return u,s,v,mean

def OpenImage(file, flat=True):
    ''' Given an image path, open it as a flat numpy array.

    :param file: The path to the image to open
    :returns: The image as a grayscale numpy array
    '''
    image = ImageOps.grayscale(Image.open(file))
    return np.array(image).flatten() if flat else np.array(image)

def OpenImageDirectory(path):
    ''' Given a path, open all the images in the directory
    and create an array of PIL images.

    :param path: The directory path to open
    :returns: A collection of PIL Images
    '''
    files  = (os.path.join(path, file) for file in os.listdir(path))
    images = [OpenImage(file) for file in files]
    return np.array(images, 'f')

def ComputeIntegralFeature(feature, image):
    ''' Given a feature and an integral image, compute the
    value of the given box on the image.

    :param feature: The feature array to calculate
    :param image: The integral image to apply the feature against
    :returns: The total value of that feature
    '''
    x,y = image.shape
    fx, fy, fw, fh, fc = feature
   
    # ---------------------------------------------------------------
    # To compute the integral image sum of a box, we simply do
    # the following:
    # sum = br - bl - ur + ul
    # ---------------------------------------------------------------
    total  = image[fx+fw, fy+fh] + image[fx, fy]
    total -= image[fx, fy+fh] + image[fx+fw, fy]
    return fc * total

def ComputeIntegralFeatures(features, image):
    ''' Given a set of features and an integral image,
    compute the value of the given boxes on the image.

    :param features: The colllection of features to calculate
    :param image: The integral image to apply the features against
    :returns: The total value of the features
    '''
    total = [ComputeIntegralFeature(feature, image) for feature in features]
    return sum(total)
