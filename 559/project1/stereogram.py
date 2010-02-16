'''
AutoStereogram Creator
----------------------------------------
- random dot
- auto-stereogram random dot
- auto-stereogram texture
- auto-stereogram ascii


Information obtained from `Techmind <http://www.techmind.org/stereo/stech.html>`_
'''
try: # try for the free speedup
    import psyco
    psyco.full()
except ImportError: pass

from random import randint
from PIL import Image, ImageOps
import numpy

# ------------------------------------------------------------------------- #
# Helper Methods
# ------------------------------------------------------------------------- #

def get_random_gray():
    ''' Return a random grey value

    :returns: A random gray value
    '''
    return randint(0,255)

def get_random_color():
    ''' Return a random color tuple for each call

    :returns: A random RGB tuple
    '''
    return (randint(0,255), randint(0,255), randint(0,255))

def get_random_depthmap():
    ''' Return a random PIL Image depthmap from the
    site http://www.3d-eye.info

    :returns: A random initialized PIL Image depthmap
    '''
    import urllib2
    import cStringIO
    import re

    url   = 'http://www.3d-eye.info/depht-image-pattern-stereogram-gallery/data/media/2/'
    files = re.findall('<A HREF="(.*\.jpg)">', urllib2.urlopen(url).read())
    file  = files[randint(0,len(files))]
    data  = urllib2.urlopen(url+file).read()
    return Image.open(cStringIO.StringIO(data))

def get_random_texture():
    ''' Return a random PIL Image texture from the
    site http://www.easystereogrambuilder.com

    TODO The url stuff is not right as they id is random.
    I will have to use beautiful soup or find another source.

    :returns: A random initialized PIL Image depthmap
    '''
    import urllib2
    import cStringIO
    import re

    url  = 'http://www.easystereogrambuilder.com/Patterns/FullSize/%d.jpg' % randint(1,177)
    data = urllib2.urlopen(url).read()
    return Image.open(cStringIO.StringIO(data))

def create_random_texture(width, height):
    ''' Build a random texture map to use for mapping depth
    map points when creating a sird.

    :param width: The width of the resulting texture map
    :param height: The height of the resulting texture map
    :returns: The resulting random texture map
    '''
    output = Image.new('RGB', (width, height))
    for w in xrange(width):
        for h in xrange(height):
            output.putpixel((w,h), get_random_color())
    return output

# ------------------------------------------------------------------------- #
# Classes
# ------------------------------------------------------------------------- #
class SIRD(object):
    '''
    This class helps create various SIRD images given
    an appropriate depthmap
    '''

    def __init__(self, depthmap, separation=100):
        ''' Initialize a new instance of the SIRD generator

        Depthmap can be an image path, uri, or a PIL image. If an image is passed
        in it can be RGB or grayscale, regardless it will be successfully converted
        to grayscale.

        :throws IOError: This will throw an IOError if the file does not exist
        :param depthmap: The depthmap to hide in a sird
        :param separation: The eye separation in pixels
        '''
        self.separation = separation
        if isinstance(depthmap, str):
           self.depth = Image.open(depthmap)
        else: self.depth = depthmap
        self.depth = ImageOps.grayscale(self.depth)

    # ------------------------------------------------------------------------- #
    # Static Private Helper Methods
    # ------------------------------------------------------------------------- #

    def _create_lookup(self, depth, row):
        ''' Build a lookup table for the specified row
    
        :param depth: The depthmap image to create a lookup for
        :param row: The row to return a lookup table for
        :returns: The resulting sird
        '''
        row = numpy.asarray(depth)[row]
        result = range(0, len(row)) # + 1?

        for k,v in enumerate(row):
            d = self._get_displacement(v)
            if (d + k) < len(row):
                result[d + k] = k
        return result

    def _create(self, depth, texture=None):
        ''' Build a sird image using random dots to hide the depthmap.
    
        :param depth: The depthmap to create a sird for
        :param texture: The texture map to use or None to use a random one
        :returns: The resulting sird
        '''
        output = Image.new('RGB', depth.size)
        (dw, dh) = output.size

        # TODO
        #if not texture:
        #    texture = create_random_texture(40, 40)

        for h in xrange(dh):
            lookup = self._create_lookup(depth, h)
            for w in xrange(dw):
                if lookup[w] == w: # if the point isn't mapped
                    output.putpixel((w,h), get_random_color())
                else: output.putpixel((w,h), output.getpixel((w,h)))
        return output

    # ------------------------------------------------------------------------- #
    # Private Interface
    # ------------------------------------------------------------------------- #

    def _get_displacement(self, color):
        ''' Return the displacement for the given depth color

        The depth map is usually a grayscale picture, and you need to map
        the color (probably from 0-256) to a distance (how far apart the
        next pixel should be over).  Often mapping depths of 0-256 into the
        range of disparities of 100-250 pixels is about right, but it
        depends on your monitor/printer.

        :param color: The gray color to get the displacement for
        :returns: The displacement for the specified color
        '''
        # max-depth  = max(colors, 0)
        # pixels     = inches * monitor-ppi
        # depth      = max - (color * (max - min) / 255)
        # separation = (eye-sep * depth) / (depth * distance)

        return self.separation + (color / 2)

    # ------------------------------------------------------------------------- #
    # Public Interface
    # ------------------------------------------------------------------------- #

    def create_random_dot(self):
        ''' Build a sird image using random dots to hide the depthmap.
    
        :returns: The resulting sird
        '''
        return self._create(self.depth)
    
    def create_textured(self, texture):
        ''' Build a sird image using the specified texture
        to hide the depthmap.
    
        :param texture: The texture filename to hide the depthmap
        :returns: The resulting sird
        '''
        return self._create(self.depth, Image.open(texture))

    def create_animated_random_dot(self, frames=37):
        ''' Build a sird image that rotates using random dots
        to hide the depthmap.
    
        :param frames: The number of frames to create
        :returns: The resulting sird
        '''
        return (self._create(self.depth.rotate(i*10))
            for i in xrange(frames))
    
    def create_animated_textured(self, texture, frames=37):
        ''' Build a sird image that rotates using the specified
        texture to hide the depthmap.
    
        :param texture: The texture filename to hide the depthmap
        :param frames: The number of frames to create
        :returns: The resulting sird
        '''
        overlay = Image.open(texture)
        return (self._create(self.depth.rotate(i*10), overlay)
            for i in xrange(frames))

# ------------------------------------------------------------------------- #
# Exposed Interface
# ------------------------------------------------------------------------- #
__all__ = [
    'SIRD',
    'get_random_gray', 'get_random_color',
    'get_random_depthmap', 'get_random_texture',
]
