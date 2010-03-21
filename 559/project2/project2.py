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

def test_region(features, image, zone):
    ''' Given detector collection and a point for the upper
    left corner of the feature test, check if the feature
    exists in the specified image.
    of images and report back the score of the given
    feature test.

    :param features: The features to test against the image region
    :param image: The image to test the features against
    :param zone: The upper left corner of the feature window
    :returns: True if a feature exists, False otherwise
    '''
    fsize  = 24 - 1
    window = image[zone[0]:zone[0]+fsize,zone[1]:zone[1]+fsize]
    result = np.multiply(features, window)

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
