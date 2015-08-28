================================================================================
Computer Vision
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* Normalized Cut (Shi & Malik)
* Spatial Pyramid Matching (Ponce)
* Histogram of Gradients (Dalal and Triggs)
* Deformable Part Model

--------------------------------------------------------------------------------
Image Kernels
--------------------------------------------------------------------------------

.. todo:: summary, edge error, normalization

Applying the kernels is basically the following process:

.. code-block:: python

    def apply_kernel(image, kernel):
        ''' Apply the supplied kernel to the supplied image.

        :param image: The image to apply the kernel to (row x col)
        :param kernel: The kernel matrix to apply to the image (row x col)
        :returns: The image after the kernel has been applied
        '''
        Iy, Ix = len(image),  len(image[0])  # the images sizes
        Ky, Kx = len(kernel), len(kernel[0]) # the kernel sizes
        result = image.clone()               # the resulting image

        for row in range(0, Iy - Ky):        # the rows bound by kernel size
            for col in range(0, Ix - Kx):    # the cols bound by kernel size
                result[row][col] = sum(kernel[r][c] * image[row + r][ col + c]
                  for r in range(0, Ky) for c in range(0, Kx))
        return result

* *sobel*

  Sobel kernels are Used to show only the differences in adjacent pixel values
  in a particular direction. It can be used for edge detection

.. code-block:: clojure

     bottom      right        left        top
   [-1 -2 -1]  [-1  0  1]  [ 1  0 -1]  [ 1  2  1]
   [ 0  0  0]  [-2  0  2]  [ 2  0 -2]  [ 0  0  0]
   [ 1  2  1]  [-1  0  1]  [ 1  0 -1]  [-1 -2 -1]

* *emboss*

  Emboss kernels give the illusion of depth by emphasizing the differences of
  pixels in a given direction.

.. code-block:: clojure

     tl->br      br->tl      tr->bl      bl->tr
   [-2 -1  0]  [ 2  1  0]  [ 0 -1 -2]  [ 0  1  2]
   [-1  1  1]  [ 1  1 -1]  [ 1  1 -1]  [-1  1  1]
   [ 0  1  2]  [ 0 -1 -2]  [ 2  1  0]  [-2 -2  0]

* *identity*

  Identity kernel simply returns the original image unchanged.

.. code-block:: clojure

   [ 0  0  0]
   [ 0  1  0]
   [ 0  0  0]

* *outline*

  Outline kernel is used to highlight large differences in pixel values. A pixel
  next to neighbor pixels with close to the same intensity will appear black in
  the new image while one next to neighbor pixels that differ strongly will appear
  white. It can be used for edge detection.

.. code-block:: clojure

   [-1 -1 -1]
   [-1  8 -1]
   [-1 -1 -1]

* *sharpen*

  Sharpen kernel is used to emphasize differences in adjacent pixels, making the
  image look more vivid.

.. code-block:: clojure

   [ 0 -1  0]
   [-1  5 -1]
   [ 0 -1  0]

* *blur*

  Blur kernel is used to de-emphasize differences in adjacent pixels, making the
  image look more blurry.

.. code-block:: clojure

          gaussian             box
         [ 1  2  1]        [ 1  1  1] 
  (1/16) [ 2  4  2]  (1/9) [ 1  1  1]
         [ 1  2  1]        [ 1  1  1]

* *edge detect*

  Used to detect edges in an image.

.. code-block:: clojure

   [ 0  1  0]  [  1  0 -1]
   [ 1 -4  1]  [  0  0  0]
   [ 0  1  0]  [ -1  0  1]
