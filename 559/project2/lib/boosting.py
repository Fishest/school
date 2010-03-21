'''
'''
#try: # try for the free speedup
#    import psyco
#    psyco.full()
#except ImportError: pass
try:
    import cPickle as pickle
except ImportError: import pickle

import time
import numpy as np
from haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

_log = logging.getLogger("project2.internal")

# ------------------------------------------------------------------ #
# Internal Training Logic
# ------------------------------------------------------------------ #
def TestFeature(feature, images):
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

def TrainFeatures(images, count=20, rounds=10):
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
    _log.info("Total time to generate features: %s secs" % (time.time() - _start))
    _start = time.time()
    for feature in initial:
        score = TestFeature(feature, images)
        features.append((score, feature))
    _log.info("Total time to train features: %s secs" % (time.time() - _start))

    # sort and build our final feature array
    # features.sort()
    features = np.array([feature[1] for feature in features[:count]])
    thresholds = np.array([feature[0] for feature in features[:count]])
    return features, thresholds

