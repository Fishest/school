'''
'''
import time
from optparse import OptionParser
import pylab

from lib.utility import *
from lib.detector import ImageManager, Detector

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

__log = logging.getLogger("project")

# ------------------------------------------------------------------ #
# Project Logic
# ------------------------------------------------------------------ #
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

def overlay_results(image, results):
    ''' Given an image and a collection of results,
    put a box at every given match location.

    :param image: The image to mark the matches
    :param results: A list of matched features
    :returns: The image with the features boxed
    '''
    final = image.copy()
    for result in results:
        pass
    return final

def process_image(path, classify):
    ''' Given an image and a set of haar-features, we
    apply the features against image and return the resulting
    feature locations.

    :param path: The path to the image to test
    :param classify: The feature detector
    :returns: The locations of each face in the image.
    '''
    _start = time.time()
    image = OpenImage("images/example.jpg", flat=False)
    results = classify.test_full_image(image)
    __log.debug("MAIN detection run time: %s secs" % (time.time() - _start))

    # Mark the result locations and display the image
    import pdb; pdb.set_trace()
    #final = overlay_results(image, results)
    final = results
    pylab.imshow(final, pylab.cm.gist_gray)
    pylab.show()

# ------------------------------------------------------------------ #
# Main Entry Point
# ------------------------------------------------------------------ #
def build_options():
    ''' Helper to centralize the option parsing logic
    '''
    parser = OptionParser()

    parser.add_option("-c", "--conf",
        help="The configuration file to load",
        dest="file")

    parser.add_option("-v", "--debug",
        help="Turn on to enable tracing",
        action="store_true", dest="debug", default=False)
    (opt, arg) = parser.parse_args()

    # enable debugging information
    if opt.debug:
        try:
            __log.setLevel(logging.DEBUG)
        except Exception, e:
    	    print "Logging is not supported on this system"
    return arg

def main():
    ''' The following is the actual implementation of the project.
    We simply take an image, classify it, and show the results.
    '''
    args = build_options()

    # Setup and train our detector
    _start = time.time()
    images = ImageManager(valid="images/faces/faces/", invalid="images/faces/nonfaces/")
    classify = Detector()
    classify.train(images, 20)
    __log.debug("MAIN training run time: %s secs" % (time.time() - _start))

    process_image("images/example.jpg")

# ------------------------------------------------------------------ #
# Main Jumper
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    main()
