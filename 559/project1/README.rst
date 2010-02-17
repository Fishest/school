=================================================
Project 1
=================================================

:Author: Galen Collins bashwork at gmail dot com
:Date:   Sun Feb 11 17:00:50 CST 2010

**Autostereogram Generator**
*(Not recommended if you can't see autostereograms)*

1.  *Base Project, [14 points]*

    Write a program that makes an autostereogram. This program must be automatic,
    and take in a depth map, and (perhaps a texture source, or you can generate
    the texture randomly). You turn in a web page, with your favorite (2 or 3)
    example outputs (and the depth map they came from). 

2.  *Extension, Worth [6 points]* 

    Moving autostereograms (good java choice). The idea here is to create a depth
    map that changes through time, and then show the autostereogram images through
    time (so that you see a moving depth map). This might entail creating a depth
    map that is a mathematical function that depends on time (or frame number t):

        d(x,y) = 4 + sin((x+t) / 150)

    Now, continually update the autostereograms as the depth map changes. This
    would be a nice java applet, or you could save the results as a movie
    (mpeg or avi). 

3.  *Extension, Worth [6 points]* 

    Making "pretty" autostereograms. Random dot pictures are less compelling than
    many magic eye pictures. Create and detail how you created several images that
    are more compelling than random dot stereograms. 

Solution
-------------------------------------------------

