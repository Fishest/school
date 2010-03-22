'''
'''

import os, time
import numpy as np
from utility import *

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
_log = logging.getLogger("project.pca")

def remove_images_mean(images):
    ''' Given a numpy array of image, this computes the
    mean image and removes it from the collection of images.

    :param images: A numpy array of images
    :returns: The mean image of the input array
    '''
    mean = images.mean(axis=0)
    for id in range(images.shape[0]):
        images[id] -= mean
    return mean

def nipals_algorithm(images):
    ''' Given a numpy array of image, this performs the
    nipals algorithm to retrieve the eigenfaces.

    :param images: A numpy array of images
    :returns: The mean image of the input array
    '''
    imaget = image.T
    covar = np.dot(images, imaget)
    eval, evec = linalg.eigh(covar)
    V = np.dot(imaget, evec).T[::-1] # sorted
    S = sqrt(eval)[::-1] # sorted

    return [V, S]

def compute_distance(a, b):
    ''' Compute the linear distance between the
    two data sets.

    :param a: The first dataset to compare
    :param b: The second dataset to compare
    :returns: The distance between the two datasets
    '''
    # abs(a - b).sum()
    return ((a - b)**2).sum()

def find_distance(vector, n):
    ''' Compute the linear distance between the
    two data sets.

    :param vector: The collection of arrays to compare with
    :param n: The value to compare against the collection
    :returns: The collected distances
    '''
    handle  = [int(compute_distance(v, n)) for v in vector]
    return handle

def _default_labels(count):
    ''' Generate a set of default labels for count number
    of images.

    :param count: The number of labels to generate
    :returns: The collection of labels
    '''
    return ("image #%d" % id for id in xrange(count))

# ----------------------------------------------------------------- # 
# Project Helper Methods
# ----------------------------------------------------------------- # 
class PCA(object):
    '''
    '''

    def __init__(self, **kwargs):
        ''' Initialize a new instance of the PCA class
        '''
        self.images = kwargs.get('images')
        self.labels = kwargs.get('labels', None)
        if self.labels is None:
            self.labels = _default_labels(self.images.shape[0])
        self.initialized = False

    def initialize(self):
        ''' Initializes the values neccessary for performing
        PCA on a set of data.

        :returns: The result of the operation
        '''
        _start = time.time()
        if not self.initialized:
            self.mean = remove_images_mean(self.images)
            self.U, self.S, Vh = LoadWithCache("../images/pca",
                lambda _: np.linalg.svd(self.images))
            self.V = Vh.T # just the way it is
            self.initialized = True
        _log.info("Total time to initialize PCA: %s secs" % (time.time() - _start))
        return self.initialized

    def test_image(self, image):
        ''' Test an image against the underlying pca structures

        :param image: The image to perform pca on
        :returns: The coefficients of the image
        '''
        if self.initialized:
            compare = image - self.mean
            return np.dot(self.V, compare)

    def get_nearest_image(self, image):
        ''' Retrieve the closest image in the set to the
        requested image.

        :param image: The image to find a match for
        :returns: The closest matching image
        '''
        if self.initialized:
            coefs = self.test_image(image)
            import pdb;pdb.set_trace()
            index = np.argmin(find_distance(self.U, coefs))
            return self.images[index]

    def _reconstruct_image(self, index):
        ''' Given an index into the image coefficients,
        try and recreate the image from the svd components.

        :param index: The index into the coefficient table
        :returns: The reconstructed image
        '''
        handle = self.V[index]
        # and some magic occurs here
        return handle

# ------------------------------------------------------------------ #
# Test Code
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    from detector import ImageManager

    _log.setLevel(logging.DEBUG)
    images = ImageManager(valid="../images/faces/faces/",
        invalid="../images/faces/nonfaces/")
    pca = PCA(images = images.valid)
    pca.initialize()
    pca.get_nearest_image(images.valid[0])

