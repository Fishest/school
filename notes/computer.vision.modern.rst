================================================================================
Computer Vision a Modern Approach
================================================================================

--------------------------------------------------------------------------------
Chapter 1: Introduction
--------------------------------------------------------------------------------

--------------------------------------------------------------------------------
Chapter 2: Image Formation
--------------------------------------------------------------------------------

* pinhole camera model
http://en.wikipedia.org/wiki/Pinhole_camera_model

* blur spot
* focal length
* aperture / f-number

large aperture / small f-number:

  - bright image / short exposure time
  - shallow depth of field

small aperture / large f-number:

  - dark image / long exposure time
  - large depth of field

.. image:: images/camera-aperture.jpg
   :target: http://en.wikipedia.org/wiki/Aperture
   :align: center

vignetting (lenses in series)

  - layers of lenses reduce total light

chromatic abboration (parts of light have different wavelength)

  - corrected with lens materials / layers

.. image:: images/chromatic-aberration.jpg
   :target: http://en.wikipedia.org/wiki/Chromatic_aberration
   :align: center

geometric distortion
  - barrel / shear

--------------------------------------------------------------------------------
Chapter 3: Digital Image Sensing
--------------------------------------------------------------------------------

* photon shot noise
* read (thermal) noise
* quantization noise
* dark current noise
* fixed pattern noise

.. image:: digital camera pipeline
