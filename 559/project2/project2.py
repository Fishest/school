'''
'''
import time
from optparse import OptionParser
#import numpy as np

from lib.violajones import *
from lib.haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

__log = logging.getLogger("project2")
__log.setLevel(logging.DEBUG)

# ------------------------------------------------------------------ #
# Helper Utilities
# ------------------------------------------------------------------ #
def test_feature(feature, images):
    ''' Given a feature test, run it against the set
    of images and report back the score of the given
    feature test.

    :param feature: The feature to tests
    :param images: The image set to test the feature against
    :returns: The score for the feature test
    '''
    score = 0
    for image in images:
        pass
    return score

def test_ii_feature(feature, images):
    ''' Given a feature test, run it against the set
    of integral images and report back the score of
    the given feature test.

    :param feature: The feature to tests
    :param images: The image set to test the feature against
    :returns: The score for the feature test
    '''
    score = 0
    for image in images:
        pass
    return score

def train_features(path, count=20):
    ''' Given a path to a collection of image features, train
    the specified number of detectors against the set.

    :param path: The path to the directory of images
    :param count: The number of features to generate
    :returns: The collection of trained detectors
    '''
    _start = time.time()
    images = OpenImageDirectory(path)
    initial = GenerateFeatures(count*10)
    features = []
    for feature in initial:
        score = test_feature(feature, images)):
        features.add((score, feature))
    __log.debug("Total time to train features: %s ticks" % (time.time() - _start))
    return [feature[1] for feature in features]

def train_ii_features(path, count=200):
    ''' Given a path to a collection of image features, train
    the specified number of detectors against the set.

    :param path: The path to the directory of images
    :param count: The number of features to generate
    :returns: The collection of trained detectors
    '''
    _start = time.time()
    images = OpenImageDirectory(path)
    initial = GenerateFeatures(count*10)
    features = []
    for feature in initial:
        score = test_ii_feature(feature, images)):
        features.add((score, feature))
    __log.debug("Total time to train ii-features: %s ticks" % (time.time() - _start))
    return [feature[1] for feature in features]

def process_image(image, features):
    ''' Given an image and a set of haar-features, we
    apply the features against image and return the resulting
    feature locations.

    :param image: The image path to test
    :param features: The rectangle features to test for features
    :returns: The locations of each face in the image.
    '''
    _start = time.time()
    if isinstance(image, str): image = OpenImage(image)
    pyramid = CreateImagePyramid(image, scale=1.25)
    __log.debug("Total time to process and image: %s ticks" % (time.time() - _start))

def process_ii_image(image, features):
    ''' Given an image and a set of haar-features, we
    apply the features against image and return the resulting
    feature locations.

    :param image: The image path to test
    :param features: The rectangle features to test for features
    :returns: The locations of each face in the image.
    '''
    _start = time.time()
    if isinstance(image, str): image = OpenImage(image)
    pyramid = CreateIntegralImagePyramid(image, scale=1.25)
    __log.debug("Total time to process and ii-image: %s ticks" % (time.time() - _start))

# ------------------------------------------------------------------ #
# Main Entry Point
# ------------------------------------------------------------------ #
def main():
    '''
    '''
    pass

# ------------------------------------------------------------------ #
# Main Jumper
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    _start = time.time()
    main()
    __log.debug("Total application run time: %s ticks" % (time.time() - _start))
