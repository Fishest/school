'''
Papers
-------------------------------------------------------------------------
* http://www.python.org/doc/essays/graphs.html
* http://www.cs.cornell.edu/~dph/papers/seg-ijcv.pdf
* http://cs.gmu.edu/~kosecka/Publications/Micusik-Kosecka-GMUTechRep08.pdf
* http://www.cs.toronto.edu/~kyros/pubs/09.pami.turbopixels.pdf
* http://www.cs.sfu.ca/~mori/research/superpixels/
* http://people.cs.uchicago.edu/~pff/segment/

Modules to remember
-------------------------------------------------------------------------
scipy.spatial.distance
'''
import scipy
import numpy as np
from pygraph.classes.graph import graph as pygraph

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
_log = logging.getLogger("project.utility")
logging.basicConfig(filename="%s.log" % __file__, level=logging.DEBUG)

#--------------------------------------------------------------------------------#
# Helper Utility Methods 
#--------------------------------------------------------------------------------#
import os, time
try:
    import cPickle as pickle
except ImportError: import pickle

def method_timer(func):
    '''
    The following is a simple decorator to time how long
    it takes the decorated function to run.
    '''
    def _call(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        finish = time.time() - start
        name = "%s" % (func.__name__)
        _log.debug("Total Time[%.4f secs] for action[%s]" % (finish, name))
        return result
    _call.__name__ = func.__name__
    return _call

class Cache(object):
    ''' A helper cache abstraction using pickle as its
    storage mechanism.
    '''

    @staticmethod
    def load(path):
        ''' Load an object from the specified location
        '''
        _log.debug("loading cache from %s" % path)
        with file(path, 'r') as handle:
            return pickle.load(handle)

    @staticmethod
    def store(value, path):
        ''' Store an object at the specified location
        '''
        _log.debug("storing cache at %s" % path)
        with file(path, 'w') as handle:
            pickle.dump(value, handle)

    @staticmethod
    def try_load_from_cache(path, callback):
        ''' Helper to load/store the image sets from/to
        a pickle cache to speed-up the initialization process
    
        :param path: The path to the directory of images
        :param callback: What to do if the cache doesn't exist
        :return: The initialized collection of data
        '''
        pathc = "%s.cache" % os.path.realpath(path)
        result = None
    
        if os.path.exists(pathc):
            result = Cache.load(pathc)
        else:
            result = callback(path)
            Cache.store(result)
        return result

def open_image(path, flatten=False, size=None):
    ''' Open the supplied path as an image
    '''
    from PIL import Image,ImageOps
    if not isinstance(path, str):
        image = path
    else:
        image = Image.open(path)
        image = ImageOps.grayscale(image)
        image = np.array(image)
    if flatten: image = image.flatten()
    if size: image = image.resize(size)
    return image

#--------------------------------------------------------------------------------#
# Helper Classes
#--------------------------------------------------------------------------------#
class Compass(object):
    ''' An enumeration for the different directions of
    pixel movements.  This is used to calculate the tortuosity
    '''
    NORTH      = 1
    NORTHEAST  = 2
    EAST       = 3
    SOUTHEAST  = 4
    SOUTH      = 5
    SOUTHWEST  = 6
    WEST       = 7
    NORTHWEST  = 8

    @staticmethod
    def get_direction(source, dest):
        ''' Get the direction of the move between two points
    
        :param source: The source point
        :param dest: The destination point
        :returns: The resulting direction of the move
        '''
        ax, ay = source
        bx, by = dest
    
        if ax == bx and ay == by + 1:
            return Compass.SOUTH
        elif ax == bx and ay + 1 == by:
            return Compass.NORTH
        elif ax == bx + 1 and ay == by:
            return Compass.EAST
        elif ax + 1 == bx and ay == by:
            return Compass.WEST
        # the following are not used in this application
        elif ax + 1 == bx and ay + 1 == by:
            return Compass.NORTHWEST
        elif ax + 1 == bx and ay == by + 1:
            return Compass.SOUTHWEST
        elif ax == bx + 1 and ay == by + 1:
            return Compass.SOUTHEAST
        elif ax == bx + 1 and ay + 1 == by:
            return Compass.NORTHEAST

#--------------------------------------------------------------------------------#
# Main tester
#--------------------------------------------------------------------------------#
def main():
    ''' Main test script
    '''
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass

if __name__ == "__main__":
    main()

