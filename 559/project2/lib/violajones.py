'''
'''
try: # try for the free speedup
    import psyco
    psyco.full()
except ImportError: pass

import os
import numpy as np
from PIL import Image, ImageOps

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
__log = logging.getLogger("project2.internal")

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
    def next(si, sc):
        while min(si) >= 24:
            yield si
            si = map(lambda n: int(n/sc), si)
    return [image.resize(size) for size in next(image.size, scale)]

def CreateIntegralImagePyramid(image, scale=1.25):
    ''' Given a pil image, this returns an integral image
    image pyramid with each image reduced by the scale factor
    from the previous image.

    :param image: The image to create an image pyramid for
    :param scale: The scale factor to reduce the image at each stage
    :returns: The image pyramid for the specified image
    '''
    def next(si, sc):
        while min(si) >= 24:
            yield si
            si = map(lambda n: int(n/sc), si)
    return [CreateIntegralImage(image.resize(size)) for size in next(image.size, scale)]

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
    :returns: (v, s, mean-image)
    '''
    mean = RemoveMeanFromImages(images)
    u,s,v = np.linalg.svd(images)
    v = v[:images.shape[0]]
    return v,s,mean

def OpenImage(file):
    ''' Given an image path, open it as a flat numpy array.

    :param file: The path to the image to open
    :returns: The image as a grayscale numpy array
    '''
    image = ImageOps.grayscale(Image.open(file))
    return np.array(image).flatten()

def OpenImageDirectory(path):
    ''' Given a path, open all the images in the directory
    and create an array of PIL images.

    :param path: The directory path to open
    :returns: A collection of PIL Images
    '''
    files  = (os.path.join(path, file) for file in os.listdir(path))
    images = [OpenImage(file) for file in files]
    return np.array(images, 'f')

