'''
'''
import pylab
import numpy as np

#--------------------------------------------------------------------------------#
# Missing matlab functions 
#--------------------------------------------------------------------------------#
# Validate these with matlab
#--------------------------------------------------------------------------------#
 
def randperm(value):
    ''' Generates a random permutation based on the input value

    :param value: The number of values to create a permuation for
    :return: The random permutation
    '''
    return np.random.permutation(np.arange(1,value+1))

def ind2sub(shape, path):
    ''' maybe?
    '''
    np.unravel_index(path, shape)

def label2rgb(sp):
    ''' This recreates the following matlab command: 
    label2rgb(sp, 'jet', 'w', 'shuffle')
    cmap=cm.jet
    '''
    pass

def hsv(value=64):
    ''' http://www.math.ufl.edu/help/matlab/hsv.html
    '''
    x = np.double(np.arange(0, value-1)) / value
    r = (    6 * abs(x - (1.0/2) - 1).clip(0,1)
    g = (2 - 6 * abs(x - (1.0/3)    ).clip(0,1)
    b = (2 - 6 * abs(x - (2.0/3)    ).clip(0,1)
    return np.array([r,g,b])

def cmap(value):
    ''' Generate a random colormap with the number of colors

    :param value: The number of colors to generate
    :return: The random colormap
    '''
    from matplotlib.colors import ListedColormap
    return ListedColormap(np.random.rand(256, value))

#--------------------------------------------------------------------------------#
# Port of the visualization code
#--------------------------------------------------------------------------------#

def visual_one(image, sp, paths):
    ''' red boundaries over original image
    '''
    nRows, mCols = image.shape
    pylab.figure; pylab.imshow(image)
    pylab.hold(True)
    for path in paths:
        y, x = ind2sub(image.shape, path)
        pylab.plot(x, y, 'Color', [1 0 0], 'LineWidth', 3)
    pylab.title('Red Superpixel Boundaries - Original Image')
    pylab.show()

def visual_two(image, sp, paths):
    ''' display cost map with randomly coloured greedy regular lattice
    '''
    image = (image - image.min()) / (image.max() - image.min())
    pylab.figure; pylab.imshow(image)
    nRows, mCols = image.shape
    cmap = hsv(len(paths))
    idx = randperm(len(paths))
    pylab.hold(True)
    for path in paths:
        y, x = ind2sub(image.shape, path)
        pylab.plot(x, y, 'Color', cmap(idx(i), :), 'LineWidth', 3)
    pylab.title('Randomly Coloured Greedy Regular Lattice')
    pylab.show()

def visual_three(image, sp, paths):
    ''' stain glass' display mean of each superpixel 'jet' colour map
    with black boundaries.
    '''

    nRows, mCols = image.shape
    pylab.figure; pylab.imshow(label2rgb(sp))
    pylab.hold(True)
    for path in paths:
        y, x = ind2sub(image.shape, path)
        pylab.plot(x, y, 'Color', [0 0 0], 'LineWidth', 3)
    pylab.title('Black Superpixel Boundaries - Random Superpixel Colur')
    pylab.show()

def visual_four(image, sp, paths):
    ''' display mean of each superpixel with black boundaries
    '''
    nRows, mCols = image.shape
    spMean = np.zeros(image.shape)
    for i = 1:sp(end)   
        pixList = sp == i
        meanPix = image[pixList].mean()
        spMean[pixList] = meanPix
    spMean = (spMean - spMean.min()) / (spMean.max() - spMean.min())
    pylab.figure; pylab.imshow(spMean)
    pylab.hold(True)

    for path in paths:
        y, x = ind2sub(image.shape, path)
        pylab.plot(x, y, 'Color', [0 0 1], 'LineWidth', 3)
    pylab.title('Blue Superpixel Boundaries - Mean Superpixel Value')
    pylab.show()

#--------------------------------------------------------------------------------#
# Main tester
#--------------------------------------------------------------------------------#
def main():
    ''' Main test script
    '''
    pass

if __name__ == "__main__":
    main()
