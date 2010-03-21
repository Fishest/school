'''
'''
from random import randint, seed
import numpy as np

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
    print "Generating 2-H"
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
    print "Generating 2-V"
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
    print "Generating 3-H"
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
    print "Generating 3-V"
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
    print "Generating 4-B"
    feat = __generate_blank_image(size)
    x, y = __get_random_bounds(size)
    feat[y[0]:y[1]+y[0], x[0]:x[1]+x[0]] = -1 # upper-box
    feat[y[1]+y[0]:y[2], x[1]+x[0]:x[2]] = -1 # bottom-box
    feat[y[1]+y[0]:y[2], x[0]:x[1]+x[0]] =  1 # upper-box
    feat[y[0]:y[1]+y[0], x[1]+x[0]:x[2]] =  1 # bottom-box
    return feat

# ------------------------------------------------------------------ #
# Public interface
# ------------------------------------------------------------------ #
__haar_features = (
        __generate_2_vertical, __generate_2_horizontal,
        __generate_3_vertical, __generate_3_horizontal,
        __generate_4_boxes,
  )
__haar_feature_size = len(__haar_features) - 1

def generate_haar_feature(size=(24,24)):
    ''' Given an image size, generate a random haar
    feature.
    
    :param size: a tuple of (x size, y size)
    :returns: The random haar feature for the given window size
    '''
    seed()
    index = randint(0, __haar_feature_size)
    feat  = __haar_features[index](size)

    # randomize the location of the positive areas
    if randint(0, 1): feat *= -1
    return feat


