================================================================================
FFMPEG Guide
================================================================================

--------------------------------------------------------------------------------
Formats
--------------------------------------------------------------------------------

The muxer / demuxers for ffmpeg are supplied by the libavformat library which
inlcudes 

--------------------------------------------------------------------------------
Command Line Application
--------------------------------------------------------------------------------

What follows are the most common parameters to the `ffmpeg` command line program:

.. code-block:: bash

    -formats   print the list of supported file formats
    -codecs    print the list of supported codecs (E=encode,D=decode)
    -i         set the input file. Multiple -i switchs can be used
    -f         set video format (for the input if before of -i, for output otherwise)
    -fs N      set the max file size of the output file
    -an        ignore audio
    -vn        ignore video
    -ar        set audio rate (in Hz)
    -ac        set the number of channels
    -ab        set audio bitrate
    -acodec    choose audio codec or use “copy” to bypass audio encoding
    -vcodec    choose video codec or use “copy” to bypass video encoding
    -r         video fps. You can also use fractional values like 30000/1001 instead of 29.97
    -s         frame size (w x h, ie: 320x240)
    -aspect    set the aspect ratio i.e: 4:3 or 16:9
    -sameq     ffmpeg tries to keep the visual quality of the input
    -t N       encode only N seconds of video (you can use also the hh:mm:ss.ddd format)
    -to N      encode only to position N in the video
    -croptop, -cropleft, -cropright, -cropbottom   crop input video frame on each side
    -y         automatic overwrite of the output file
    -ss        select the starting time in the source file
    -vol       change the volume of the audio
    -g         Gop size (distance between keyframes)
    -b         Video bitrate
    -bt        Video bitrate tolerance
    -metadata  add a key=value metadata

The configuration options have now changed to work as follows:

.. code-block:: bash

    -b:a            == -ab
    -b:v            == -b
    -codec:a / -c:a == -acodec
    -codec:v / -c:v == -vcodec

--------------------------------------------------------------------------------
Cookbook
--------------------------------------------------------------------------------

What follows are a collection of common operations that can be performed using
the stock ffmpeg command line utilites.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extract Information About a File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg -i <file>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Convert some stream into an HLS stream:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg             /
      -i <stream>      / # use the following input stream
      -an              / # no audio
      -c:v libx264     / # use x264 codec (-c:v copy)
      -f hls           / # use hls format
      -hls_time 9      / # use max size 9 second hls chunks
      -hls_list_size 9 / # use max 9 entries in playlist
      -hls_wrap 9      / # wrap the files so only 9 exist
      -s 480x270       / # set the frame size of the video
      stream.m3u8        # write to the following playlist

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Screencast from the X server (linux only):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg -f x11grab -video_size cif -framerate 25 -i :0.0 screencast.mpg

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Mux Audio + Video
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you need to merge video and audio, you can do so by supplying multiple inputs
and then an output format:

.. code-block:: bash

    ffmpeg          /
      -i audio.mp4  / # the audio file to mux
      -i video.mp4  / # the video file to mux
      output.mp4      # the resulting muxed file


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Change The Media Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg       /
      -i <file>  / # use the supplied input 
      -c:a copy  / # keep the same audio codec
      -c:v copy  / # keep the same video codec
      copy.flv     # output to the new container format

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Slice From Video
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg         /
      -i video.flv / # the input file to slice from
      -ss 00:10:00 / # where to start slicing from
      -t  00:01:00 / # the amount of time to extract
      -c:a copy    / # keep the same audio codec
      -c:v copy    / # keep the same video codec
      slice.flv      # output the newly sliced file

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extract Audio From Video
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are some other options that are useful for this action:

* `-c:a libaac` to use the *AAC* format

.. code-block:: bash

    ffmpeg            /
      -i video.avi    / # the input video to extract from
      -vn             / # no video output
      -ar 44100       / # with the supplied auto rate
      -ac 2           / # which channel to extract
      -ab 128k        / # audio bit rate
      -f mp3          / # using the mp3 container
      music.mp3         # the final output file

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Extract Images From Video
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This will write an image every second from a video. Other useful options are:

* `-ss 01:22:13`  start at a certain point
* `-t 10` write only `N` seconds of images
* `-vframes 1` write only `N` frames of images

.. code-block:: bash

    ffmpeg              /
      -i input.avi      / # use the following video as input
      -r 1              / # get an image every second; 0.1 every 10 seconds
      -s 1024x720       / # convert the image to this size
      -f image2         / # extract to jpeg
      frame-%03d.jpeg     # write to the following files

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create Video From Images
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg                 /
      -framerate 10        / # specify the framerate of the video
      -i 'image-%03d.jpeg' / # specify the input images glob
      out.mkv                # specify the output format

If you want to create a video from a single image, you can loop over that image
for the supplied amount of time:

.. code-block:: bash

    ffmpeg              /
      -loop 1           / # loop over the supplied image
      -i image.jpg      / # use a single image as the video
      -t 00:00:05       / # loop for 5 seconds
      -an               / # use no audio
      -c:v libx264      / # output using x264
      out.mp4             # output to the supplied file

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Read From The Webcam
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    
    ffmpeg                  / # for OSX
      -f qtkit              / # uses the qtkit to read from the webcam
      -video_device_index 0 / # uses device 0 or the first webcam
      -i ""                 / # empty input file
      stream.flv              # output to the mpeg file

    ffmpeg                  / # on linux
      -f oss
      -i /dev/dsp
      -f video4linux2
      -i /dev/video0
      stream.flv

    ffmpeg                  / # on windows
      -f dshow
      -i video=”video source name”:audio=”audio source name” 
      stream.flv

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Stream a File To An FMS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg             /
      -re              / # read file in real time
      -i local.mp4     / # the input file to stream
      -c copy          / # copy video and audio codec
      -f flv           / # convert to flv container
      rtmp://server/live/streamName # send to the following server

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Save a Stream to File
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg                             /
      -i rtmp://server/live/streamName / # the input stream to read
      -c copy                          / # copy video / audio codec
      dump.flv                           # the file to save to

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Write Stream to a Rolling Window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    ffmpeg                          /
      -i rtmp://INPUT               / # the infinite input stream
      -codec copy                   / # copy the video / audio codec
      -f segment                    / # segment the file
      -segment_list segments.list   / # store the segments here
      -segment_time 3600            / # each segment is one hour
      -segment_wrap 24              / # store a buffer of 24 segments
      out%03d.mp4                     # store to the following buffer

--------------------------------------------------------------------------------
Filters
--------------------------------------------------------------------------------

https://www.ffmpeg.org/ffmpeg-filters.html#Video-Filters
