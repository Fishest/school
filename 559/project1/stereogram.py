'''
AutoStereogram Creator
----------------------------------------

As of now this supports the following sirds:

- random dot
- auto-stereogram random dot
- auto-stereogram texture

For more information about the algorithm or of stereograms, visit the
following links:

- `Techmind <http://www.techmind.org/stereo/stech.html>`_
- `Wikipedia <http://en.wikipedia.org/wiki/Autostereogram>`_

Example Useage
----------------------------------------
from stereogram import SIRD

v = SIRD("Boxes.jpg")
j = v.create_random_dot()
j.show()
'''
#try: # try for the free speedup
#    import psyco
#    psyco.full()
#except ImportError: pass

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

def create_text_depthmap(message="Hello", width=1024, height=768):
    ''' Build a depth map with the supplied text which can be
    used to create a sird.

    TODO work with a collection of messages and position to fit all

    :param message: The message to build a deptmap for
    :param width: The width of the resulting texture map
    :param height: The height of the resulting texture map
    :returns: The resulting random texture map
    '''
    from PIL import ImageDraw, ImageFont

    path     = "/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf"
    padding  = 20
    size     = int((1.65 * (width - 2*padding)) / len(message))
    position = (padding, int((height/2) - (size / 2)))

    output   = Image.new('RGB', (width, height))
    font     = ImageFont.truetype(path, size)
    draw     = ImageDraw.Draw(output)
    draw.text(position, message, font=font, fill="#808080")

    return output

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
    an appropriate depthmap.
    '''
    dpi        = 81
    yshift     = dpi / 16
    distance   = dpi * 14
    separation = dpi * 2.5
    factor     = 0.55
    maximum    = dpi * 12
    minimum    = int((factor * maximum * distance) / ((1 - factor) * maximum + distance))
    pattern    = (separation * maximum) / (maximum + distance)

    def __init__(self, depthmap):
        ''' Initialize a new instance of the SIRD generator

        Depthmap can be an image path, uri, or a PIL image. If an image is passed
        in it can be RGB or grayscale, regardless it will be successfully converted
        to grayscale.

        :throws IOError: This will throw an IOError if the file does not exist
        :param depthmap: The depthmap to hide in a sird
        '''
        if isinstance(depthmap, str):
           self.depth = Image.open(depthmap)
        else: self.depth = depthmap
        self.depth = ImageOps.grayscale(self.depth)

    # ------------------------------------------------------------------------- #
    # Private Interface
    # ------------------------------------------------------------------------- #
    def _correct_texture(self, texture):
        ''' Makes sure that the supplied texture will be wide enough to
        correctly cover the supplied seperation. If not, we resize it in
        a scaled manner so that it will cover the max seperation.

        :param texture: The texture to correct
        :returns: The correct resized texture
        '''
        size = texture.size
        if size[0] < self.pattern:
            height = (size[1] * self.pattern) / size[0]
            size = (int(self.pattern), int(height))
        return texture.resize(size)

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
        depth = self.maximum - (color * (self.maximum - self.minimum) / 255)
        return (self.separation * depth) / (depth + self.distance)

    def _validate(self, points, width, links):
        ''' This validates that the point is valid from the left
        and right viewpoint. Based on the validation, the left and
        right mappings will be updated.

        :param points: The left and right points to validate
        :param width: The width to validate
        :param links: The left and right link mappings to update
        :returns: void
        '''
        visible = true;
        left, right = points

        if (left <= 0) or (right > width):
            return
        
        if links[0][right] != right:
            if links[0][right] < left:
                links[1][links[0][right]] = links[0][right];
                links[0][right] = right;
            else: visible = false

        if links[1][left] != left:
            if links[1][left] > right:
                links[0][links[1][left]] = links[1][left];
                links[1][left] = left;
            else: visible = false;
    
        if visible:
            links[0][right] = left;
            links[1][left]  = right;

    def _create_lookup(self, depth, row):
        ''' Build a lookup table for the specified row
    
        :param depth: The depthmap image to create a lookup for
        :param row: The row to return a lookup table for
        :returns: The resulting sird
        '''
        row    = depth[row]
        width  = len(row)
        result = range(0, width) # initialize with no links

        for k,v in enumerate(row):
            d = int(self._get_displacement(v) / 2)
            left, right = k-d, k+d
            # self._validate((left,right), width, (linkl,linkr))
            if (left >= 0) and (right < width):
                result[right] = left
        return result

    def _create(self, depth):
        ''' Build a sird image using random dots to hide the depthmap.
    
        :param depth: The depthmap to create a sird for
        :returns: The resulting sird
        '''
        output = Image.new('RGB', depth.size)
        (dw, dh) = output.size
        mapping = numpy.asarray(depth)

        for h in xrange(dh):
            lookup = self._create_lookup(mapping, h)
            for w in xrange(dw):
                if lookup[w] == w: # if the point isn't mapped
                    output.putpixel((w,h), get_random_color())
                else:
                    output.putpixel((w,h), output.getpixel((lookup[w],h)))
        return output

    def _create_textured(self, depth, texture):
        ''' Build a sird image using a supplied texture file
        to hide the depthmap.
    
        :param depth: The depthmap to create a sird for
        :param texture: The texture map to use
        :returns: The resulting sird
        '''
        output = Image.new('RGB', depth.size)
        (dw, dh) = output.size
        (tw, th) = texture.size
        mapping = numpy.asarray(depth)
        lastlink = -10

        for h in xrange(dh):
            lookup = self._create_lookup(mapping, h)
            for w in xrange(dw):
                if lookup[w] == w: # if the point isn't mapped
                    if lastlink == (w - 1):
                        output.putpixel((w,h), output.getpixel((w - 1, h)))
                    else:
                        height = (h + ((w / self.pattern) * self.yshift)) % th
                        output.putpixel((w,h), texture.getpixel(
                            (w % self.pattern, height)))
                else:
                    output.putpixel((w,h), output.getpixel((lookup[w],h)))
                    lastlink = w
        return output

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
        overlay = self._correct_texture(Image.open(texture))
        return self._create_textured(self.depth, overlay)

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
        overlay = self._correct_texture(Image.open(texture))
        return (self._create_textured(self.depth.rotate(i*10), overlay)
            for i in xrange(frames))

# ------------------------------------------------------------------------- #
# Exposed Interface
# ------------------------------------------------------------------------- #
__all__ = [
    'SIRD',
    'get_random_gray', 'get_random_color',
    'get_random_depthmap', 'get_random_texture',
]
