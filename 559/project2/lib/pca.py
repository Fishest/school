'''
'''

import numpy as np
from utility import *

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
_log = logging.getLogger("project")

# ------------------------------------------------------------------ #
# Helper Functions
# ------------------------------------------------------------------ #

@method_timer
def nipals_algorithm(images):
    ''' Given a numpy array of image, this performs the
    nipals algorithm to retrieve the eigenfaces.

    :param images: A numpy array of images
    :returns: The mean image of the input array
    '''
    vcovar = np.dot(images, images.T)
    #ucovar = np.dot(images.T, images)
    veval, vevec = np.linalg.eigh(vcovar)
    #ueval, uevec = np.linalg.eigh(ucovar)

    V = np.dot(image.T, vevec).T[::-1] # sorted
    S = np.sqrt(veval)[::-1] # sorted

@method_timer
def svds(images):
    ''' Computes the sparse svd of the given image
    collection

    :param images: The input images to perform the svd on
    :returns: [U, S, V]
    '''
    Uh, S, Vh = np.linalg.svd(images, full_matrices=False)
    return (Uh, (Vh.T * S))

def compute_distance(n, v):
    ''' Compute the linear distance between the
    two data sets.

    :param n: The first dataset to compare
    :param v: The second dataset to compare
    :returns: The distance between the two datasets
    '''
    return ((n - v)**2).sum()

def find_distance(n, vector):
    ''' Compute the linear distance between the
    two data sets.

    :param n: The value to compare against the collection
    :param vector: The collection of arrays to compare with
    :returns: The collected distances
    '''
    handle = [int(compute_distance(n, v)) for v in vector]
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
    ''' Facade around working with PCA
    '''

    def __init__(self, **kwargs):
        ''' Initialize a new instance of the PCA class
        '''
        self.images = kwargs.get('images')
        self.labels = kwargs.get('labels', None)
        if self.labels is None:
            self.labels = _default_labels(self.images.shape[0])
        self.initialized = False

    @method_timer
    def initialize(self, pcs=None):
        ''' Initializes the values neccessary for performing
        PCA on a set of data.

        :param pcs: The number of principal components to use
        '''
        self.initialized = False
        self.intialize_mean_images()
        self.U, self.V = svds(self.mimages.T)

        if pcs: # if we want to limit the number of components
            self.U, self.V = self.U[:pcs], self.V[:pcs]

        self.initialized = True

    @method_timer
    def intialize_mean_images(self):
        ''' Create the mean image of the class and
        create the mean images array.
        '''
        self.mean = self.images.mean(axis=0)
        self.mimages = self.images - self.mean

    def get_eigenface(self, image):
        ''' Test an image against the underlying pca structures

        :param image: The image to perform pca on
        :returns: The coefficients of the image
        '''
        if self.initialized:
            compare = image - self.mean
            return np.dot(self.U.T, compare)

    def get_nearest_image(self, image):
        ''' Retrieve the closest image in the set to the
        requested image.

        :param image: The image to find a match for
        :returns: The closest matching image
        '''
        if self.initialized:
            index = self.get_nearest_image_index(image)
            return self.images[index]

    def get_nearest_image_index(self, image):
        ''' Retrieve the closest image in the set to the
        requested image.

        :param image: The image to find a match for
        :returns: The closest matching image
        '''
        if self.initialized:
            coefs = self.get_eigenface(image)
            return np.argmin(find_distance(coefs, self.V))

    def _reconstruct_image(self, index):
        ''' Given an index into the image coefficients,
        try and recreate the image from the svd components.

        :param index: The index into the coefficient table
        :returns: The reconstructed image
        '''
        handle = np.dot(self.U, self.V)
        handle = self.mean + handle
        return handle[index, :]

# ------------------------------------------------------------------ #
# Test Code
# ------------------------------------------------------------------ #
def _main():
    import pylab, time, pickle
    import logging.handlers

    logging.basicConfig(level=logging.DEBUG)
    handler = logging.handlers.RotatingFileHandler("pca-report.log")
    logging.getLogger("project").addHandler(handler)

    id = 9
    with file("../images/att-image-set.pickle", 'r') as f:
        images = pickle.load(f)
    #images = OpenImageDirectory("../images/att-faces/s1")
    pca = PCA(images = images)
    pca.initialize()
    result = pca.get_nearest_image(images[id])

    pylab.gray()
    pylab.subplot(1,2,1);pylab.imshow(images[id].reshape((112,92)))
    pylab.subplot(1,2,2);pylab.imshow(result.reshape((112,92)))
    pylab.show()

if __name__ == "__main__":
    _main()

