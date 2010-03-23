'''
'''
import os
from utility import *
from boosting import Booster
from haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

_log = logging.getLogger("project.detector")

# ------------------------------------------------------------------ #
# Helper Utilities
# ------------------------------------------------------------------ #
def get_trained_set(images, count):
    ''' Given the desired classification results and
    the actual classification results, this generates
    a report of how well the detector performed

    :param desired: The desired logic array
    :param actual: The resulting logic array
    :returns: (positive, negative, false-positive, false-negative)
    '''
    base = 400
    def _gen(_):
        # as our implementation is ungodly slow, we are
        # loading features generated from a much beefier
        # box in matlab :D
        booster = Booster(valid=images.valid, invalid=images.invalid)
        return booster.train_features(count=200, rounds=10)
    f,t = LoadWithCache("../images/features", _gen)
    return f[:,:,base:count+base], t[:,base:count+base]

def compile_report(desired, actual):
    ''' Given the desired classification results and
    the actual classification results, this generates
    a report of how well the detector performed

    :param desired: The desired logic array
    :param actual: The resulting logic array
    :returns: (positive, negative, false-positive, false-negative)
    '''
    l  = len(desired) / 2 # half good half bad
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
    _log.info(" Correctly detected non-features:\t\t[%4d][%3.2f%%]" % ( n, 100.0* n/l))
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
        self.valid = LoadWithCache(kwargs.get('valid'), callback)
        self.invalid  = LoadWithCache(kwargs.get('invalid'), callback)

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
        self.features, self.thresholds = get_trained_set(data, count)
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
        score  = np.dot(self.features.T, image.T);
        actual = np.sum((score.T - self.thresholds), axis=1) > 0
        return actual

    def test_image_collection(self, images):
        ''' This tests if a collection of images are matching
        features.
    
        :param images: The images to test as features
        :returns: A logical list of the test results
        '''
        return [self.test_image(image) for image in images]

    def test_image_zone(self, image, zone):
        ''' Helper function to generate a trained feature set off
        of the input dataset (positive and negative), report on its
        accurracy, and return the feature detectors that were selected.
    
        :param image: The image to test a certain zone in
        :param zone: The zone of the image to test
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        fsize  = self.size[0]
        window = image[zone[0]:zone[0]+fsize, zone[1]:zone[1]+fsize].reshape(fsize*fsize)
        result = self.test_image(window)
        return result

    @method_timer
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
        results = []
        for x in xrange(0, image.shape[0] - self.size[0]):
            for y in xrange(0, image.shape[1] - self.size[1]):
                zone = (x,y)
                if self.test_image_zone(image, zone):
                    results.append(zone)
            print "\033[2J Current image scanning status: %s%% done" % (100*x/image.shape[0])
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
        return [(image, self.test_full_image(image)) for image in images]

    @method_timer
    def test_accuracy(self, images, desired):
        ''' Test the accuracy of the current detector set

        :param images: A collection of images to analyze
        :param desired: The expected result of the detector
        '''
        if not self.initialized:
            raise Exception("The detector must be initialized first!")
        score  = np.dot(self.features.T, images.T);
        import pdb; pdb.set_trace()
        actual = (np.sum((score.T - self.thresholds), axis=1) > 0)
        return compile_report(desired, actual)

# ------------------------------------------------------------------ #
# Test Code
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    _log.setLevel(logging.DEBUG)
    images = ImageManager(valid="../images/faces/faces/",
        invalid="../images/faces/nonfaces/")
    classify = Detector()
    classify.train(images.valid, 100)

    im, de = images.get_training_set(200)
    classify.test_accuracy(im, de)

