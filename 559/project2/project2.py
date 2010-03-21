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

def decode_matches(matches, size):
    ''' Given a collection of matches and the image size
    they were found at, convert all the matches to operate
    on the scale of the original image.

    :param matches: collection of [[size, pos]...]
    :param size: The original size of the image
    :returns: The match collection with the pixel locations scaled
    '''
    final = []
    for match, msize in matches:
        scale = size[0] / msize[0]
        final.add([(match[0]*scale, match[1]*scale), msize])
    return final

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
        result = image * feature
        score += np.multiply(result,result).sum()
    return score

def train_features(images, count=20, rounds=10):
    ''' Given a collection of image features, train
    the specified number of detectors against the set.

    This works by picking the best feature out of the specified
    number of rounds, testing them all, and picking the top
    count feature tests.

    :param images: The collection of images to train with
    :param count: The number of features to generate
    :returns: The collection of trained detectors
    '''
    _start = time.time()
    initial = GenerateFeatures(count*rounds)
    features = []
    __log.debug("Total time to initialize features: %s ticks" % (time.time() - _start))
    _start = time.time()
    for feature in initial:
        score = test_feature(feature, images)):
        features.add((score, feature))
    __log.debug("Total time to train features: %s ticks" % (time.time() - _start))
    features.sort()
    return features[:count]

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

# ------------------------------------------------------------------ #
# Project Logic
# ------------------------------------------------------------------ #

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
