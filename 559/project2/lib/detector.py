'''
'''
#try: # try for the free speedup
#    import psyco
#    psyco.full()
#except ImportError: pass
try:
    import cPickle as pickle
except ImportError: import pickle

import os
from violajones import *
from boosting import TrainFeatures
from haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

_log = logging.getLogger("project2.internal")

# ------------------------------------------------------------------ #
# Helper Utilities
# ------------------------------------------------------------------ #
def load_with_cache(path, callback):
    ''' Helper to load/store the image sets from/to
    a pickle cache to speed-up the initialization process

    :param path: The path to the directory of images
    :param callback: What to do if the cache doesn't exist
    :return: The initialized collection of data
    '''
    cache = "pickle.cache"
    pathc = os.path.join(path, cache)
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

def compile_report(desired, actual):
    ''' Given the desired classification results and
    the actual classification results, this generates
    a report of how well the detector performed

    :param desired: The desired logic array
    :param actual: The resulting logic array
    :returns: (positive, negative, false-positive, false-negative)
    '''
    l  = len(desired)
    p  = sum((desired == True) & (actual == True))
    n  = sum((desired == False) & (actual == False))
    fp = sum((desired == False) & (actual == True))
    fn = sum((desired == True) & (actual == False))

    _log.info("\n\n")
    _log.info("----------------------------------------------------------------------")
    _log.info("- Feature Detection Report                                           -")
    _log.info("----------------------------------------------------------------------")
    _log.info(" Correctly detected features:\t\t[%4d][%3.2f%%]"     % ( p, 100.0* p/l))
    _log.info(" Incorrectly detected features:\t\t[%4d][%3.2f%%]"   % (fn, 100.0*fn/l))
    _log.info(" Incorrectly detected non-features:\t[%4d][%3.2f%%]" % (fp, 100.0*fp/l))
    _log.info(" Correctly detected non-features:\t[%4d][%3.2f%%]"   % ( n, 100.0* n/l))
    _log.info("----------------------------------------------------------------------")
    _log.info("\n\n")

    return (p,n,fp,fn)

# ------------------------------------------------------------------ #
# Class Definitions
# ------------------------------------------------------------------ #
class ImageManager(object):
    '''
    '''

    def __init__(self, **kwargs):
        ''' Intializes a new instance of the ImageManager
        '''
        callback = lambda path: OpenImageDirectory(path)
        self.valid = load_with_cache(kwargs.get('valid'), callback)
        self.invalid  = load_with_cache(kwargs.get('invalid'), callback)

    def get_training_set(self, count):
        ''' Retrieves a training set of valid and invalid
        feature images to be used to train a detector.

        :param count: The number of each type of image to return
        :returns: ([valid, invalid], [identifiers])
        '''
        images  = np.concatenate((self.valid[-count:,:], self.invalid[-count:,:]), axis=0)
        desired = np.concatenate((np.repeat(True, count), np.repeat(False, count)))
        return (images, desired)

class Detector(object):
    '''
    Helper class to abstract away a great deal of the feature
    boosting logic.
    '''

    def __init__(self, **kwargs):
        ''' Intializes a new instance of the Booster
        '''
        self.size = (24,24)
        self.initialized = False

    def train(self, data, count=20):
        ''' Helper function to generate a trained feature set off
        of the input dataset (positive and negative), report on its
        accurracy, and return the feature detectors that were selected.
    
        :param data: The dataset to train with
        :param count: The number of detectors to generate
        '''
        self.initialized = False
        self.features, self.thresholds = TrainFeatures(data, count)
        self.features = self.features.reshape((24*24, count)) 
        self.initialized = True

    def test_image(self, image):
        ''' This tests if a single image is of a matching
        feature.
    
        :param image: The images to test as features
        :returns: True if the image is a feature, False otherwise
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        _start = time.time()
        score  = np.dot(self.features.T, image.T);
        actual = np.sum((score.T - self.thresholds), axis=1) > 0
        _log.debug("Total time to scan single feature: %s secs" % (time.time() - _start))
        return actual

    def test_image_collection(self, images):
        ''' This tests if a collection of images are matching
        features.
    
        :param images: The images to test as features
        :returns: A logical list of the test results
        '''
        return [test_image(image) for image in images]

    def test_image_zone(self, image, zone):
        ''' Helper function to generate a trained feature set off
        of the input dataset (positive and negative), report on its
        accurracy, and return the feature detectors that were selected.
    
        :param image: The image to test a certain zone in
        :param zone: The zone of the image to test
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        _start = time.time()
        fsize  = self.size[0] - 1
        window = image[zone[0]:zone[0]+fsize, zone[1]:zone[1]+fsize]
        result = test_image(window)
        _log.debug("Total time to scan single feature: %s secs" % (time.time() - _start))
        return result

    def test_full_image(self, image):
        ''' This tests all possible windows of a given image for
        the requested feature type and returns all matching
        locations.

        Return result is [(x,y), ...]
    
        :param image: The image to test for features
        :returns: A list of the possible feature locations
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        _start = time.time()
        results = []
        for x in xrange(0,image.shape[0] - self.size[0]):
            for y in xrange(0,image.shape[1] - self.size[1]):
                zone = (x,y)
                if test_image_zone(image, zone):
                    results.append(zone)
        _log.info("Total time to scan full image: %s secs" % (time.time() - _start))
        return results

    def test_full_image_collection(self, images):
        ''' This tests all possible windows of a given image
        in a collection of images for the requested feature
        type and returns all matching locations.

        Return result is [(image, [results]), ...]
    
        :param image: The image to test for features
        :returns: A list of the possible feature locations
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        return [(image, test_full_image(image)) for image in images]

    def test_accuracy(self, images, desired):
        ''' Test the accuracy of the current detector set

        :param images: A collection of images to analyze
        :param desired: The expected result of the detector
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        _start = time.time()
        score = np.dot(self.features.T, images.T);
        actual = (np.sum((score.T - self.thresholds), axis=1) > 0)
        _log.info("Total time to test detector accuracy: %s secs" % (time.time() - _start))
        return compile_report(desired, actual)

# ------------------------------------------------------------------ #
# Test Code
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    _log.setLevel(logging.DEBUG)
    images = ImageManager(valid="../images/faces/faces/", invalid="../images/faces/nonfaces/")
    classify = Detector()
    classify.train(images.valid, 20)

    im, de = images.get_training_set(100)
    classify.test_accuracy(im, de)

