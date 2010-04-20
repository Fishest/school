'''
Papers
-------------------------------------------------------------------------
* http://www.python.org/doc/essays/graphs.html
* http://www.cs.cornell.edu/~dph/papers/seg-ijcv.pdf
* http://cs.gmu.edu/~kosecka/Publications/Micusik-Kosecka-GMUTechRep08.pdf
* http://www.cs.toronto.edu/~kyros/pubs/09.pami.turbopixels.pdf
* http://www.cs.sfu.ca/~mori/research/superpixels/
* http://people.cs.uchicago.edu/~pff/segment/

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

def _load_from_cache(path, callback):
    ''' Helper to load/store the image sets from/to
    a pickle cache to speed-up the initialization process

    :param path: The path to the directory of images
    :param callback: What to do if the cache doesn't exist
    :return: The initialized collection of data
    '''
    pathc = "%s.cache" % os.path.realpath(path)
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

def _open_image(path, flatten=False):
    ''' Open the supplied path as an image
    '''
    from PIL import Image,ImageOps
    if not isinstance(image, str):
        image = path
    else:
        image = Image.open(path)
        image = ImageOps.grayscale(image)
        image = np.array(image)
    if flatten: image = image.flatten()
    return image

#--------------------------------------------------------------------------------#
# Graph Utility Methods 
#--------------------------------------------------------------------------------#
def _add_edges(image, graph, x, y):
    ''' Adds the edges for the specified pixels

    :param image: The image to get the weights from
    :param graph: The graph to add the edges to
    :param x: The x pixel coordinate
    :param y: The y pixel coordinate
    '''
    if x - 1 >= 0:
        w1, w2 = image[x,y], image[x-1,y]
        weight = abs(w1 - w2)
        graph.add_edge(((x,y),(x-1,y)), wt=weight)
    if y - 1 >= 0:
        w1, w2 = image[x,y], image[x,y-1]
        weight = abs(w1 - w2)
        graph.add_edge(((x,y),(x,y-1)), wt=weight)

@method_timer
def build_graph(image):
    ''' Builds a weighted graph from the specified image

    :param image: The image or path to build a graph for
    :returns: The resulting graph
    '''
    image = _open_image(image)
    graph = pygraph()
    ix,iy = image.shape
    for x in xrange(0, ix):
        for y in xrange(0, iy):
            graph.add_node((x, y))
            _add_edges(image, graph, x, y)
    return graph

@method_timer
def build_cache_graph(path):
    ''' Builds a weighted graph from the specified image

    :param image: The image or path to build a graph for
    :returns: The resulting graph
    '''
    return _load_from_cache(path, build_graph)

def _get_direction(source, dest):
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

#--------------------------------------------------------------------------------#
# Main implementation class
#--------------------------------------------------------------------------------#
class GreedyLattice(object):

    _defaults = {
        'pixels'      : (25,25),
        'borderWidth' : 1,
        'tortuosity'  : 80,
        'overlap'     : 0.4,
    }

    def __init__(self, image, **kwargs):
        ''' Initialize a new instance of the GreedyLattice.
        See the defaults for the various tuning parameters for the
        algorithm.

        :param image: The cost map to create a lattice for
        :param kwargs: The tuning parameters of the lattice
        '''
        self.costm = 255 - _open_image(image)
        self.graph = _build_graph(self.costm) 
        self.param = self._defaults.copy()
        self.param.update(kwargs)
        self.hpaths = []
        self.vpaths = []

    def process(self):
        '''
        '''
        pass

    #--------------------------------------------------------------------------------#
    # Private Implementation 
    #--------------------------------------------------------------------------------#
 
    def _add_path(self):
        '''
        '''
        pass

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

