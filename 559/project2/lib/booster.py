'''
'''
try: # try for the free speedup
    import psyco
    psyco.full()
except ImportError: pass
try:
    import cPickle as pickle
except ImportError: import pickle

import os
from violajones import *
from haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

__log = logging.getLogger("project2.internal")

# ------------------------------------------------------------------ #
# Helper Utilities
# ------------------------------------------------------------------ #
def _compile_report(desired, actual):
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

    __log.info("--------------------------------------------")
    __log.info("- Feature Detection Report                 -")
    __log.info("--------------------------------------------")
    __log.info(" Correctly detected features:\t\t[%d][%.2f%%]"     % ( p, 100.0* p/l))
    __log.info(" Incorrectly detected features:\t\t[%d][%.2f%%]"   % (fn, 100.0*fn/l))
    __log.info(" Incorrectly detected non-features:\t[%d][%.2f%%]" % (fp, 100.0*fp/l))
    __log.info(" Correctly detected non-features:\t[%d][%.2f%%]"   % ( n, 100.0* n/l))
    __log.info("--------------------------------------------")

def _load_cache(path):
    ''' Helper to load/store the image sets from/to
    a pickle cache to speed-up the initialization process

    :param path: The path to the directory of images
    :return: The initialized image collection
    '''
    cache = "pickle.cache"
    pathc = os.path.join(path, cache)
    result = None

    if os.path.exists(pathc):
        __log.debug("Loading Cache at %s" % pathc)
        with file(pathc, 'r') as handle:
            result = pickle.load(handle)
    else:
        result = OpenImageDirectory(path)
        with file(pathc, 'w') as handle:
            pickle.dump(result, handle)
    return result

def _test_feature(feature, images):
    ''' Given a feature test, run it against the set
    of images and report back the score of the given
    feature test.

    :param feature: The feature to tests
    :param images: The image set to test the feature against
    :returns: The score for the feature test
    '''
    result = np.multiply(images, feature)
    return result.mean()
    #score = 0
    #for image in images:
    #    result = image * feature
    #    score += np.multiply(result,result).sum()
    #return score

def _train_features(images, count=20, rounds=10):
    ''' Given a collection of image features, train
    the specified number of detectors against the set.

    This works by picking the best feature out of the specified
    number of rounds, testing them all, and picking the top
    count feature tests.

    :param images: The collection of images to train with
    :param count: The number of features to generate
    :returns: (features, thresholds)
    '''
    _start = time.time()
    initial = GenerateFeatures(count*rounds)
    features = []
    __log.info("Total time to initialize features: %s secs" % (time.time() - _start))
    _start = time.time()
    for feature in initial:
        score = _test_feature(feature, images)
        features.append((score, feature))
    __log.info("Total time to train features: %s secs" % (time.time() - _start))

    # sort and build our final feature array
    features.sort()
    features = np.array([feature[1] for feature in features])
    thresholds = np.array([feature[0] for feature in features])
    return features, thresholds

# ------------------------------------------------------------------ #
# Class Definitions
# ------------------------------------------------------------------ #
class Booster(object):
    '''
    Helper class to abstract away a great deal of the feature
    boosting logic.
    '''

    def __init__(self, **kwargs):
        ''' Intializes a new instance of the Booster
        '''
        self.feats = _load_cache(kwargs.get('fpath'))
        self.nfeats = _load_cache(kwargs.get('npath'))

    def initialize_features(self, count=20):
        ''' Helper function to generate a trained feature set off
        of the input dataset (positive and negative), report on its
        accurracy, and return the feature detectors that were selected.
    
        :param fpath: The path to the good feature images
        :param npath: The path to the bad feature images
        :returns: The collection of feature detectors
        '''
        self.features, self.thresholds = _train_features(self.feats, count)
        self.features = self.features.reshape((24*24,count)) 

    def analyze_features(self):
        ''' Helper function to generate a trained feature set off
        of the input dataset (positive and negative), report on its
        accurracy, and return the feature detectors that were selected.
        '''
        images  = np.concatenate((self.feats[-100:,:], self.nfeats[-100:,:]), axis=0)
        desired = np.concatenate((np.repeat(True, 100), np.repeat(False, 100)))

        # test the accuracy of the result set
        score = np.dot(self.features.T, images.T);
        actual = (np.sum((score.T - self.thresholds), axis=1) > 0)
        _compile_report(desired, actual)

# ------------------------------------------------------------------ #
# Test Code
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    __log.setLevel(logging.DEBUG)
    boost = Booster(fpath="../images/faces/faces/", npath="../images/faces/nonfaces/")
    boost.initialize_features(20)
    boost.analyze_features()

