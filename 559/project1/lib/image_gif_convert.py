""" MODULE images2gif

Provides a function (writeGif) to write animated gif from a series
of PIL images or numpy arrays.

This code is provided as is, and is free to use for all.

Almar Klein (June 2009)

- based on gifmaker (in the scripts folder of the source distribution of PIL)
- based on gif file structure as provided by wikipedia

"""
from struct import pack
import PIL
from PIL import Image, ImageChops
from PIL.GifImagePlugin import getheader, getdata
import numpy

# getheader gives a 87a header and a color palette (two elements in a list).
# getdata()[0] gives the Image Descriptor up to (including) "LZW min code size".
# getdatas()[1:] is the image data itself in chuncks of 256 bytes (well
# technically the first byte says how many bytes follow, after which that
# amount (max 255) follows).

#--------------------------------------------------------------------- # 
# Private Helper Functions
#--------------------------------------------------------------------- # 

def CreateAnimationHeader(image):
    ''' Returns the GIF89a image header for the requested image

    :param image: The image to create a header for
    :returns: The animated gif header for the specified image
    '''
    bb  = "GIF89a"                      # Magic header
    bb += pack('H', image.size[0])      # canvas width in pixels
    bb += pack('H', image.size[1])      # canvas height in pixels
    bb += "\x87\x00\x00"
    return bb

def CreateApplicationExtension(loops=0):
    ''' Returns the application extension that specifies how
    many times to loop

    :param loops: The number of times to loop, or 0 to loop forever
    :returns: The animated gif application extension.
    '''
    bb  = "\x21\xFF\x0B"                # application extension
    bb += "NETSCAPE2.0"                 # I dunno
    bb += "\x03\x01"                    # Indicates data follows
    bb += pack('H', (loops or 2**16-1)) # how many times to loop
    bb += '\x00'                        # end
    return bb

def CreateGraphicsControlExtension(duration=0.1):
    ''' Returns the Graphics Control Extension which is a header
    for each image in the set that specifies the transparency and
    the duration.

    :param duration: How long the specified image should be shown
    :returns: The animated gif graphics control extension.
    '''
    bb  = '\x21\xF9\x04'                # i dunno
    bb += '\x08'                        # no transparancy
    bb += pack('H', int(duration*100))  # in 100th of seconds
    bb += '\x00'                        # no transparant color
    bb += '\x00'                        # end
    return bb

def _writeGifToFile(fp, images, durations, loops):
    """ Given a set of images writes the bytes to the specified stream.
    """
    
    # init
    frames = 0
    previous = None
    
    for im in images:
        
        if not previous:
            # first image
            
            # gather data
            palette = getheader(im)[1]
            data = getdata(im)
            imdes, data = data[0], data[1:]            
            header = CreateAnimationHeader(im)
            appext = CreateApplicationExtension(loops)
            graphext = CreateGraphicsControlExtension(durations[0])
            
            # write global header
            fp.write(header)
            fp.write(palette)
            fp.write(appext)
            
            # write image
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)
            
        else:
            # gather info (compress difference)              
            data = getdata(im) 
            imdes, data = data[0], data[1:]       
            graphext = CreateGraphicsControlExtension(durations[frames])
            
            # write image
            fp.write(graphext)
            fp.write(imdes)
            for d in data:
                fp.write(d)
        
        # prepare for next round
        previous = im.copy()        
        frames = frames + 1

    fp.write(";")  # end gif
    return frames

#--------------------------------------------------------------------- # 
# Public Functions
#--------------------------------------------------------------------- # 

def CreateAnimatedGif(filename, images, duration=0.1, loops=0, dither=1):
    """ writeGif(filename, images, duration=0.1, loops=0, dither=1)
    Write an animated gif from the specified images. 
    images should be a list of numpy arrays of PIL images.
    Numpy images of type float should have pixels between 0 and 1.
    Numpy images of other types are expected to have values between 0 and 255.
    """
    
    if PIL is None:
        raise RuntimeError("Need PIL to write animated gif files.")
    
    images2 = []
    
    # convert to PIL
    for im in images:
        
        if isinstance(im,Image.Image):
            images2.append( im.convert('P',dither=dither) )
            
        elif numpy and isinstance(im, numpy.ndarray):
            if im.dtype == numpy.uint8:
                pass
            elif im.dtype in [numpy.float32, numpy.float64]:
                im = (im*255).astype(numpy.uint8)
            else:
                im = im.astype(numpy.uint8)
            # convert
            if len(im.shape)==3 and im.shape[2]==3:
                im = Image.fromarray(im,'RGB').convert('P',dither=dither)
            elif len(im.shape)==2:
                im = Image.fromarray(im,'L').convert('P',dither=dither)
            else:
                raise ValueError("Array has invalid shape to be an image.")
            images2.append(im)
            
        else:
            raise ValueError("Unknown image type.")
    
    # check duration
    if hasattr(duration, '__len__'):
        if len(duration) == len(images2):
            durations = [d for d in duration]
        else:
            raise ValueError("len(duration) doesn't match amount of images.")
    else: durations = [duration]*len(images2)
    
    with open(filename, 'wb') as fp:
        n = _writeGifToFile(fp, images2, durations, loops)
    
if __name__ == '__main__':
    im = numpy.zeros((200,200), dtype=numpy.uint8)
    im[10:30,:] = 100
    im[:,80:120] = 255
    im[-50:-40,:] = 50
    images = [im*1.0, im*0.8, im*0.6, im*0.4, im*0]
    CreateAnimatedGif('lala3.gif',images, duration=0.2, dither=0)
    
