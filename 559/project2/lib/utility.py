'''
'''
try:
    import cPickle as pickle
except ImportError: import pickle

import os, time
import numpy as np
from PIL import Image, ImageOps

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
_log = logging.getLogger("project.utility")

# ----------------------------------------------------------------- # 
# Project Helper Methods
# ----------------------------------------------------------------- # 
def LoadWithCache(path, callback):
    ''' Helper to load/store the image sets from/to
    a pickle cache to speed-up the initialization process

    :param path: The path to the directory of images
    :param callback: What to do if the cache doesn't exist
    :return: The initialized collection of data
    '''
    pathc = "%s.cache" % os.path.realpath(path)
    result = None

    if os.path.exists(pathc):
        _log.debug("Loading Cache from %s" % pathc)
        with file(pathc, 'r') as handle:
            result = pickle.load(handle)
    else:
        result = callback(path)
        _log.debug("Storing Cache at %s" % pathc)
        with file(pathc, 'w') as handle:
            pickle.dump(result, handle)
    return result

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
