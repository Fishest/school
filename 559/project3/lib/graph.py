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
from utility import *
from pygraph.classes.graph import graph as pygraph
from pygraph.algorithms import minmax

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
_log = logging.getLogger("project.graph")
logging.basicConfig(filename="%s.log" % __file__, level=logging.DEBUG)

#--------------------------------------------------------------------------------#
# Graph Utility Methods 
#--------------------------------------------------------------------------------#
import math
class GraphUtility(object):
    ''' Graph helper utility methods
    '''

    @staticmethod
    def add_edges(image, graph, x, y):
        ''' Adds the edges for the specified pixels
    
        :param image: The image to get the weights from
        :param graph: The graph to add the edges to
        :param x: The x pixel coordinate
        :param y: The y pixel coordinate
        '''
        def get_weight(ln, rn):
            base = abs(ln - rn)**2 / -600.0
            return math.e**base
        if x - 1 >= 0:
            weight = get_weight(image[x,y], image[x-1,y])
            graph.add_edge(((x,y),(x-1,y)), wt=weight)
        if y - 1 >= 0:
            weight = get_weight(image[x,y], image[x,y-1])
            graph.add_edge(((x,y),(x,y-1)), wt=weight)
    
    @staticmethod
    def image_to_graph(path):
        ''' Builds a weighted graph from the specified image
    
        :param path: The image or path to build a graph for
        :returns: The resulting graph
        '''
        image = open_image(path)
        graph = pygraph()
        ix,iy = image.shape
        for x in xrange(0, ix):
            for y in xrange(0, iy):
                graph.add_node((x, y))
                GraphUtility.add_edges(image, graph, x, y)
        return graph
    
    @staticmethod
    def cache_image_to_graph(path):
        ''' Builds a weighted graph from the specified image
    
        :param image: The image or path to build a graph for
        :returns: The resulting graph
        '''
        return try_load_from_cache(path, GraphUtility.image_to_graph)

#--------------------------------------------------------------------------------#
# Helper Classes
#--------------------------------------------------------------------------------#

class Weight(object):
    ''' A constant class representing the different weights
    for each constraint.

    :param PATH: The weight to be added for a segmentation path
    :param BAND: The weight to be added as a path buffer
    :param TURN: The weight to be added for moving against the flow
    :param FLOW: The weight to be added for a flow from sink/source to node
    :param STRIP: The weight to be added for a boundary strip
    :param BOUNDARY: The weight to be added for an image edge boundary
    '''
    PATH     = 80
    BAND     = 40
    TURN     = 40
    FLOW     = 500
    STRIP    = 65000
    BOUNDARY = 255

#--------------------------------------------------------------------------------#
# Graph abstraction class
#--------------------------------------------------------------------------------#
class ImageGraph(object):
    '''
    :param h_source_node: A unique node representing the source node
    :param h_sink_node: A unique node representing the sink node
    '''
    source   = (-1,-1)
    sink     = (-2,-2)
    band_width = 5

    def __init__(self, image):
        ''' Initializes a new instance of the image graph
        '''
        self.shape = image.shape
        self.graph = GraphUtility.image_to_graph(image)

    # ----------------------------------------------------------------------- # 
    # Methods dealing with the source/sink and band
    # ----------------------------------------------------------------------- # 

    @method_timer
    def add_source_and_sink(self, band, direction):
        ''' Add the source and sink nodes and connect them across the
        image to simulate a band region.

        :param band: ((sx,sy),(ex,ey))
        :param direction: The compass direction the bad should be applied
        '''
        x,y = self.shape
        (sx,sy),(ex,ey) = band
        self.graph.add_node(self.source)
        self.graph.add_node(self.sink)

        if direction == Compass.EAST:
            for xs in xrange(0,x):
                hp,lp = (xs,ey), (xs,sy)
                self.graph.add_edge((self.source, lp), wt=Weight.FLOW)
                self.graph.add_edge((self.sink, hp), wt=Weight.FLOW)
        elif direction == Compass.SOUTH:
            for ys in xrange(0,y):
                hp,lp = (ex,ys), (sx,ys)
                self.graph.add_edge((self.source, lp), wt=Weight.FLOW)
                self.graph.add_edge((self.sink, hp), wt=Weight.FLOW)

    @method_timer
    def remove_source_and_sink(self):
        ''' Remove the previously added source and sink.
        '''
        self.graph.del_node(self.source)
        self.graph.del_node(self.sink)

    #--------------------------------------------------------------------------#
    # Methods dealing with finding paths
    #--------------------------------------------------------------------------#

    @method_timer
    def perform_min_cut(self):
        ''' Remove the source and sink from their current location
        in the graph.
        '''
        self.add_source_and_sink(((0,0),(0,100)), Compass.EAST)
        o = minmax.maximum_flow(self.graph, self.source, self.sink)
        self.remove_source_and_sink()
        return o;

    #-------------------------------------------------------------------------# 
    # Methods dealing with managing path weights / flow
    #-------------------------------------------------------------------------# 

    def update_edge_weight(self, edge, value):
        ''' Update the weights for the newly found path
        in the graph.
        '''
        weight = self.graph.edge_weight(edge) + value
        self.graph.set_edge_weight(point, wt=weight)

    @method_timer
    def update_edges_weights(self, edges, value):
        ''' Update the weights for the newly found path
        in the graph.
        '''
        for edge in edges:
            self.update_edge_weight(edge, value)

    #--------------------------------------------------------------------------#
    # Methods dealing with the band path
    #--------------------------------------------------------------------------#

    def get_neighbors(self, node, count):
        ''' Get all the neighbors of a given node count steps
        away as a unique set.

        :param node: The node to get the neighbors for
        :param count: How many steps away to search
        :returns: The neighbors of the given node
        '''
        # TODO this should return verticies not nodes
        if count <= 0: return [node]
        neighbors = self.graph.neighbors(node)
        result = set(neighbors)
        for neighbor in neighbors:
            result.update(get_neighbors(neighbor, count - 1))
        return result

    @method_timer
    def get_path_band(self, path):
        ''' Given a path of nodes, return the set of neighbors at
        the predefined band width step away.

        :param path: The path to get the neighbor band for
        :returns: The neighbors on the path band
        '''
        neighbors = set()
        for node in path:
            neighbors.update(self.get_neighbors(node, self.band_width))
        return neighbors

#------------------------------------------------------------------------------#
# Main implementation class
#------------------------------------------------------------------------------#
class GreedyLattice(object):
    '''
    '''

    _defaults = {
        'pixels'      : (11,11),
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
        self.costm = 255 - open_image(image)
        self.param = self._defaults.copy()
        self.param.update(kwargs)
        self.hpaths = []
        self.vpaths = []

    @method_timer
    def initialize_cost_map(self):
        ''' Performs all the neccessary initialization
        and creation of the cost map graph.
        '''
        self.params['stripWidth'] = np.uint(np.double(self.costm.shape) \
            / self.params['pixels'])
        #self._add_image_strips()
        self.graph = build_graph(self.costm)

    #--------------------------------------------------------------------------#
    # Private Implementation 
    #--------------------------------------------------------------------------#
 
    def _add_path(self):
        '''
        '''
        pass

    def _add_image_strips(self):
        ''' Add the constant image strip barriers evenly
        throughout the cost map. The number of strips is based
        on the number of pixels requested in the final image.
        '''
        x,y   = self.costm.shape
        xw,yw = self.param['stripWidth']
        self.costm[0:x:xw,:] = Weight.STRIP
        self.costm[:,0:y:yw] = Weight.STRIP

    #--------------------------------------------------------------------------#
    # Update weight values
    #--------------------------------------------------------------------------#
    def _update_path_weight(self, path):
        '''
        '''
        self.graph.update_edges_weights(path, Weight.PATH)
        nodes = self.graph.get_path_band(path)
        self.graph.update_edges_weights(path, Weight.BAND)


#------------------------------------------------------------------------------#
# Main tester
#------------------------------------------------------------------------------#
def main():
    ''' Main test script
    '''
    try:
        import psyco
        psyco.full()
    except ImportError:
        pass
    costm = 255 - open_image("../images/42049.bmp")
    graph = ImageGraph(costm);
    print graph.perform_min_cut()

if __name__ == "__main__":
    main()

