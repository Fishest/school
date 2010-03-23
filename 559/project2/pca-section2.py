'''
'''
import os
import numpy as np
from lib.utility import *
from lib.pca import PCA

# ------------------------------------------------------------------ #
# set up logging
# ------------------------------------------------------------------ #
import logging.handlers

logging.basicConfig(level=logging.DEBUG)
handler = logging.handlers.RotatingFileHandler("pca-final-2.log")
logging.getLogger("project").addHandler(handler)
_log = logging.getLogger("project")

# ------------------------------------------------------------------ #
# set up our image directory paths
# ------------------------------------------------------------------ #
pcs  = None
_size = (45,45)
_win  = (50, 50, 200, 200)
#_win  = None
path = "images/lfwa/lfw2"
dirs = [
    "Gerhard_Schroeder",
    "Donald_Rumsfeld", "Tony_Blair",
    "Colin_Powell", "George_W_Bush",
]

_log.info("\n")
_log.info("-------------------------------------------------------------------")
_log.info("- Test Results With %s pcs" % ("all" if not pcs else pcs))
_log.info("- Window: %s" % ("full" if not _win else str(_win)))
_log.info("- Size:   %s" % ("full" if not _size else str(_size)))
_log.info("-------------------------------------------------------------------")

# ------------------------------------------------------------------ #
# generate all of our test data
# ------------------------------------------------------------------ #
images  = [OpenAlteredImageDirectory(os.path.join(path, face), _size, _win) for face in dirs]
means   = [imageset.mean(axis=0) for imageset in images]
counts  = [imageset.shape[0] for imageset in images]
tests   = [imageset[-1,:] for imageset in images]
dataset = np.concatenate([imageset[:-1,:] for imageset in images])
meanset = np.array(means)
_log.info("index counts %s" % str(counts))

# ------------------------------------------------------------------ #
# start testing our results
# ------------------------------------------------------------------ #
pca = PCA(images = dataset)
pca.initialize(pcs)
tindexes = [pca.get_nearest_image_index(image) for image in tests]
mindexes = [pca.get_nearest_image_index(image) for image in means]

def _check_range(index, value):
    ''' Helper to test if the image is identified correctly
    '''
    b = 0 if index == 0 else sum(counts[:index-1])
    c = counts[index]
    return b <= value <= b + c

# ------------------------------------------------------------------ #
# Record results
# ------------------------------------------------------------------ #
stat = []
for idx in xrange(len(tindexes)):
    r = _check_range(idx, tindexes[idx])
    _log.info("FullTestSet: test image[%d][%d] result[%s]" % (idx, tindexes[idx], r))
    stat.append(r)
stat = 100.0*stat.count(True) / len(stat)
_log.info("FullTestSet: final result[%.2f%%]" % (stat))


stat = []
for idx in xrange(len(mindexes)):
    r = _check_range(idx, mindexes[idx])
    _log.info("FullTestSet: mean image[%d][%d] result[%s]" % (idx, mindexes[idx], r))
    stat.append(r)
stat = 100.0*stat.count(True) / len(stat)
_log.info("FullTestSet: final result[%.2f%%]" % (stat))

# ------------------------------------------------------------------ #
# start testing our results
# ------------------------------------------------------------------ #
pcb = PCA(images = meanset)
pcb.initialize(pcs)
tmindexes = [pcb.get_nearest_image_index(image) for image in tests]

# ------------------------------------------------------------------ #
# Record results
# ------------------------------------------------------------------ #
stat = []
for idx in xrange(len(tmindexes)):
    r = tmindexes[idx] == idx
    _log.info("MeanTestSet: test image[%d][%d] result[%s]" % (idx, tmindexes[idx], r))
    stat.append(r)
stat = 100.0*stat.count(True) / len(stat)
_log.info("MeanTestSet: final result[%.2f%%]" % (stat))
