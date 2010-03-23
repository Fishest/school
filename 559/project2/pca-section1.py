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
handler = logging.handlers.RotatingFileHandler("pca-final.log")
logging.getLogger("project").addHandler(handler)
_log = logging.getLogger("project")

# ------------------------------------------------------------------ #
# set up our image directory paths
# ------------------------------------------------------------------ #
pcs  = None
path = "images/att-faces"
dirs = os.listdir(path)
dirs.remove('README')

_log.info("\n\n")
_log.info("-------------------------------------------------------------------")
_log.info("- Test Results With %s pcs" % ("all" if not pcs else pcs))
_log.info("-------------------------------------------------------------------")

# ------------------------------------------------------------------ #
# generate all of our test data
# ------------------------------------------------------------------ #
images  = [OpenImageDirectory(os.path.join(path, face)) for face in dirs]
means   = [imageset.mean(axis=0) for imageset in images]
tests   = [imageset[-1,:] for imageset in images]
dataset = np.concatenate([imageset[:-1,:] for imageset in images])
meanset = np.array(means)

# ------------------------------------------------------------------ #
# start testing our results
# ------------------------------------------------------------------ #
pca = PCA(images = dataset)
pca.initialize(pcs)
tindexes = [pca.get_nearest_image_index(image) for image in tests]
mindexes = [pca.get_nearest_image_index(image) for image in means]

# ------------------------------------------------------------------ #
# Record results
# ------------------------------------------------------------------ #
stat = []
for idx in xrange(len(tindexes)):
    r = (9*idx) <= tindexes[idx] <= (((idx+1) * 9) - 1)
    _log.info("FullTestSet: test image[%d][%d] result[%s]" % (idx, tindexes[idx], r))
    stat.append(r)
stat = 100.0*stat.count(True) / len(stat)
_log.info("FullTestSet: final result[%.2f%%]" % (stat))


stat = []
for idx in xrange(len(mindexes)):
    r = (9*idx) <= mindexes[idx] <= (((idx+1) * 9) - 1)
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
