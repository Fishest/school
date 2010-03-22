'''
Haar Feature Generator
----------------------------------------------------------------

The following is a quick implementation of a haar like feature
generator.  it can be used to generate for any given window size
one of the following random feature types:

- 2 box horizontal rectangle
- 2 box vertical rectangle
- 3 box horizontal rectangle
- 3 box vertical rectangle
- 4 box grid rectangle

'''
from random import randint, seed
import numpy as np

# ------------------------------------------------------------------ #
# Logging Setup
# ------------------------------------------------------------------ #
import logging
__log = logging.getLogger("project.feature")

# ------------------------------------------------------------------ #
# Helper Methods
# ------------------------------------------------------------------ #
def __get_random_bounds(size, step=2):
    ''' Given an image size, generate a random window on the
    image. We make sure that we always have a feature that is
    symmetrical.
    
    :param size: A tuple of (x size, y size)
    :param step: The number of regions in the window
    :returns: ((x-min, x-step, x-max), (y-min, y-step, y-max))
    '''
    seed()
    safe   = (size[0] - 1, size[1] - 1)
    xl, yl = randint(0, safe[0]-step),  randint(0, safe[1]-step)
    xp, yp = round((1.0*safe[0]-xl)/step), round((1.0*safe[1]-yl)/step)
    xh, yh = xl + step*randint(1, xp), yl + step*randint(1, yp)
    xs, ys = int((xl*(step-1)+xh)/step)-xl, int((yl*(step-1)+yh)/step)-yl
    return ((xl, xs, xh), (yl, ys, yh))

def __generate_blank_image(size):
    ''' Given an image size, generate a new blank
    image of the same size.
    
    :param size: a tuple of (x-size, y-size)
    :returns: A new blank numpy image array
    '''
    return np.zeros(size, dtype=np.int8)

# ------------------------------------------------------------------ #
# Haar Feature Generators
# ------------------------------------------------------------------ #

def __generate_2_horizontal(size):
    ''' Given an image size, generate a random
    window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: ((xmin, xmid, xmax), (ymin, ymid, ymax))
    '''
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size)
    feat[y[0]:y[2], x[0]:x[1]+x[0]] = -1 # left-box
    feat[y[0]:y[2], x[1]+x[0]:x[2]] =  1 # right-box
    return feat

def __generate_2_vertical(size):
    ''' Given an image size, generate a random
    window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: ((xmin, xmid, xmax), (ymin, ymid, ymax))
    '''
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size)
    feat[y[0]:y[1]+y[0], x[0]:x[2]] = -1 # top-box
    feat[y[1]+y[0]:y[2], x[0]:x[2]] =  1 # bottom-box
    return feat

def __generate_3_horizontal(size):
    ''' Given an image size, generate a random
    window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: ((xmin, xmid, xmax), (ymin, ymid, ymax))
    '''
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size, step=3)
    x1, x2 = (x[0]+x[1]), (x[0]+x[1]*2)
    feat[y[0]:y[2], x[0]:x1] = -1 # left-box
    feat[y[0]:y[2], x1:x2]   =  1 # middle-box
    feat[y[0]:y[2], x2:x[2]] = -1 # right-box
    return feat

def __generate_3_vertical(size):
    ''' Given an image size, generate a random
    window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: ((xmin, xmid, xmax), (ymin, ymid, ymax))
    '''
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size, step=3)
    y1, y2 = (y[0]+y[1]), (y[0]+y[1]*2)
    feat[y[0]:y1, x[0]:x[2]] = -1 # top-box
    feat[y1:y2,   x[0]:x[2]] =  1 # middle_box
    feat[y2:y[2], x[0]:x[2]] = -1 # bottom-box
    return feat

def __generate_4_boxes(size):
    ''' Given an image size, generate a random
    window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: ((xmin, xmid, xmax), (ymin, ymid, ymax))
    '''
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size)
    feat[y[0]:y[1]+y[0], x[0]:x[1]+x[0]] = -1 # upper-box
    feat[y[1]+y[0]:y[2], x[1]+x[0]:x[2]] = -1 # bottom-box
    feat[y[1]+y[0]:y[2], x[0]:x[1]+x[0]] =  1 # upper-box
    feat[y[0]:y[1]+y[0], x[1]+x[0]:x[2]] =  1 # bottom-box
    return feat

__haar_features = (
        __generate_2_vertical, __generate_2_horizontal,
        __generate_3_vertical, __generate_3_horizontal,
        __generate_4_boxes,
  )
__haar_feature_size = len(__haar_features) - 1

# ------------------------------------------------------------------ #
# Haar Integral Feature Generators
# ------------------------------------------------------------------ #

def __generate_integral_2_horizontal(size):
    ''' Given an image size, generate a random
    integral window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: [left, right]
    '''
    x, y = __get_random_bounds(size)
    yw = y[2] - y[0]

    left  = (x[0], y[0], x[1], yw)
    right = (x[1], y[0], x[1], yw)
    return [left, right]

def __generate_integral_2_vertical(size):
    ''' Given an image size, generate a random
    integral window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: [top, bottom]
    '''
    x, y = __get_random_bounds(size)
    xw = x[2] - x[0]

    top    = (x[0], y[0], xw, y[1])
    bottom = (x[0], y[1], xw, y[1])
    return [top, bottom]

def __generate_integral_3_horizontal(size):
    ''' Given an image size, generate a random
    integral window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: [left, middle, right]
    '''
    x, y = __get_random_bounds(size, step=3)
    x1, x2 = (x[0]+x[1]), (x[0]+x[1]*2)
    yw = y[2] - y[0]

    left   = (x[0], y[0], x[1], yw)
    middle = (  x1, y[0], x[1], yw)
    right  = (  x2, y[0], x[1], yw)
    return [left, middle, right]

def __generate_integral_3_vertical(size):
    ''' Given an image size, generate a random
    integral window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: [top, middle, bottom]
    '''
    x, y = __get_random_bounds(size, step=3)
    y1, y2 = (y[0]+y[1]), (y[0]+y[1]*2)
    xw = x[2] - x[0]

    top    = (x[0], y[0], xw, y[1])
    middle = (x[0],   y1, xw, y[1])
    bottom = (x[0],   y2, xw, y[1])
    return [top, middle, bottom]

def __generate_integral_4_boxes(size):
    ''' Given an image size, generate a random
    integral window on the image.
    
    :param size: a tuple of (x size, y size)
    :returns: [ul, ur, bl, br]
    '''
    x, y = __get_random_bounds(size)
    x1, y1 = x[0] + x[1], y[0] + y[1]

    ul = (x[0], y[0], x[1], y[1])
    ur = (  x1, y[0], x[1], y[1])
    bl = (x[0],   y1, x[1], y[1])
    br = (  x1,   y1, x[1], y[1])
    return [ul, ur, bl, br]

__haar_integral_features = (
        __generate_integral_2_vertical, __generate_integral_2_horizontal,
        __generate_integral_3_vertical, __generate_integral_3_horizontal,
        __generate_integral_4_boxes,
  )
__haar_integral_feature_size = len(__haar_integral_features) - 1

# ------------------------------------------------------------------ #
# Public interface
# ------------------------------------------------------------------ #
def GenerateFeature(size=(24,24)):
    ''' Given an image size, generate a random haar
    feature.
    
    :param size: a tuple of (x size, y size)
    :returns: [(x-ul, y-ul, x-width, y-width) ... N]
    '''
    seed()
    index = randint(0, __haar_feature_size)
    feature = __haar_features[index](size)

    # randomize the location of the positive areas
    if randint(0, 1):
        feature *= -1
    return feature.flatten()

def GenerateFeatures(count, size=(24,24)):
    ''' Generates the requested number of haar
    features of the given size.

    :param count: The number of features to generate
    :param size: The requested feature size (default (24,24))
    :returns: A list of the requested features
    '''
    features = [GenerateFeature(size) for _ in xrange(count)]
    return np.array(features, 'f')

def GenerateIntegralFeature(size=(24,24)):
    ''' Given an image size, generate a random haar
    integral feature.
    
    :param size: a tuple of (x size, y size)
    :returns: The random haar feature for the given window size
    '''
    seed()
    index = randint(0, __haar_integral_feature_size)
    feature = __haar_integral_features[index](size)
    return feature

def GenerateIntegralFeatures(count, size=(24,24)):
    ''' Generates the requested number of haar
    integral features of the given size.

    :param count: The number of features to generate
    :param size: The requested feature size (default (24,24))
    :returns: A list of the requested features
    '''
    features = [GenerateIntegralFeature(size) for _ in xrange(count)]
    return features
