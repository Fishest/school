'''
'''
#try: # try for the free speedup
#    import psyco
#    psyco.full()
#except ImportError: pass

import time, operator
import numpy as np
import numpy.matlib as M

from haar import GenerateFeatures

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
logging.basicConfig()

_log = logging.getLogger("project.boosting")

# ------------------------------------------------------------------ #
# Internal Training Logic
# ------------------------------------------------------------------ #
class Booster(object):
    ''' A helper class to abstract away all the logic for boosting
    a set of feature detectors and the data they will be trained on.
    '''

    def __init__(self, **kwargs):
        ''' Initialize a new instance of the Booster class
        '''
        self.valid = kwargs.get('valid')
        self.invalid = kwargs.get('invalid')
        self.weights = None

    def _find_threshold(self, feature, scores, space=25):
        ''' Given a feature test result, find the best threshold
        for future feature tests.

        :param feature: The feature to find a good threshold for
        :param scores: The score data to search for the threshold
        :returns: The best computed threshold
        '''
        cs, ct = 0, 0
        thresholds = M.linspace(scores.min(), scores.max(), space)
        for thresh in thresholds:
            _log.debug("Testing next threshold...")
            classifier = (scores - thresh).T
            result = classifier * self.alldesired * self.weights
            result = result.sum()
            if result > cs:
                cs,ct = result,thresh
                self.classifier = classifier
        return cs,ct

    def _test_feature(self, feature):
        ''' Given a feature test, run it against the set
        of images and report back the score of the given
        feature test.

        :param feature: The feature to tests
        :param images: The image set to test the feature against
        :returns: The score for the feature test
        '''
        score = np.multiply(self.allimages, feature)
        return self._find_threshold(feature, score)

    def train_features(self, count=20, rounds=10):
        ''' Given a collection of image features, train
        the specified number of detectors against the set.
    
        This works by picking the best feature out of the specified
        number of rounds, testing them all, and picking the top
        count feature tests.
    
        :param images: The collection of images to train with
        :param count: The number of features to generate
        :returns: (features, thresholds)
        '''
        self.initialize_training()
        initial = GenerateFeatures(count*rounds)
        features = []
        for feature in initial:
            _start = time.time()
            score, threshold = self._test_feature(feature)
            features.append((score, threshold, feature))
            self._normalize_weights() # re-normalize our data
            _log.debug("Generating next feature...%f" % (time.time() - _start))
    
        # sort and build our final feature array
        features.sort(key=operator.itemgetter(0))
        features = np.array([feature[2] for feature in features[:count]])
        thresholds = np.array([feature[1] for feature in features[:count]])
        return features, thresholds

    # ------------------------------------------------------------------------ #
    # Traning Initialization
    # ------------------------------------------------------------------------ #
    def initialize_training(self):
        ''' Helper method to hold all the initialization steps
        for generating the neccessary training information.
        '''
        _log.debug("Initializing boosted feature training")
        self._normalize_weights()
        self._setup_dataset()

    def _normalize_weights(self):
        ''' Normalize the local training weight data
        '''
        if self.weights is None: # initial setup
            sv,sn = self.valid.shape[0], self.invalid.shape[0]
            self.weights = np.concatenate((sn*np.ones(sv), sv*np.ones(sn)))
        else:
            exponential  = M.exp(-self.alldesired * self.classifier)
            self.weights = self.weights * exponential
        self.weights = self.weights / self.weights.sum()

    def _setup_dataset(self):
        ''' This initializes the datasets that the trainer will be
        operating against
        '''
        sv,sn = self.valid.shape[0], self.invalid.shape[0]
        self.allimages = np.concatenate((self.valid, self.invalid), axis=0)
        self.alldesired = np.concatenate((np.repeat(True, sv), np.repeat(False, sn)))

# ------------------------------------------------------------------------ #
# Testing
# ------------------------------------------------------------------------ #
def _main():
    import pickle
    from detector import ImageManager
    _log.setLevel(logging.DEBUG)
    images = ImageManager(valid="../images/faces/faces/", invalid="../images/faces/nonfaces/")
    booster = Booster(valid=images.valid, invalid=images.invalid)
    out = booster.train_features(count=200, rounds=10)
    with file('final-features', 'w') as f:
        pickle.dump(out, f)

if __name__ == "__main__":
    _main()
