---
layout: post
title: Project 4 - Final Project Result
---

{{ page.title }}
============================================================

<p class="meta"/>06 May 2010 - St. Louis</p>


Introduction
------------------------------------------------------------

For the final project [assignment][] I was tasked with re-implementing the algorithm
discussed in the [superpixel][] paper. In this paper the authors propose a novel system
for segmenting an image given only a feature map of the image. Their implementation
differs from traditional image segmentation techniques in that they attempt to preserve
a regular lattice structure of the final superpixels which can be processed by existing
image algorithms without them having to be specialized for the purpose. The details
of their algorithm as well as a description of how I implemented are discussed in the
remainder of this presentation.

**Note:** *I worked on this project individually using C# and a small set of helper libraries.*

Related Work and References
------------------------------------------------------------

There were a wealth of papers that I read about image segmentation and graph theory
that proved helpful in this project. For the sake of brevity, only the most relevant
are listed below:

*  [Superpixel Lattices](http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf)

   *This was the main paper that I based most of my implementation on. It is also the
   location of the author's results which can be used as a comparison against mine.*

*  [Scene Shape Priors for Superpixel Segmentation](http://web4.cs.ucl.ac.uk/research/vis/pl/publications/SceneShape.pdf)

   *This is a continuation of the superpixel lattice paper extended to allow the algorithm
   to work on video input data. It helped answer some questions I had about the original
   implementation.*

*  [Stereo Matching and Graph Cuts](http://intechweb.org/downloadpdf.php?id=5774)

   *This is a helpful introduction to graph theory, network flow, and graph cuts
   that proved invaluable in understanding the algorithms used in the author's paper
   including s.t. min-cuts.*

*  [A New Approach to the Maximum Flow Problem](http://portal.acm.org/citatation.cfm?id=12144)

   *This is an in depth overview of most of the maximum-flow algorithms approaches as well
   as a comparison to their performance and trade-offs.*

Technical Description
------------------------------------------------------------

Before starting the segmentation algorithm, the user was expected to supply a *boundary
cost map* that contains meaningful boundaries between neighboring pixels. The authors
state that an edge detection output will suffice for the majority of cases. This mapping
is then inverted, normalized, and converted to a directed graph where each pixel was
represented by a node in the graph. To facilitate the s.t. min-cuts algorithm, I only
supplied edges to nodes below and to the right (which followed the direction from source
to sink).

**Note**: *In order to keep my results consistent with the authors, I simply used the
training edge maps from the [bsdb][] database that matched the input the author's used.*

{% highlight python %}
    def build_graph(image):
      for y in image.pixels.y:
        for x in image.pixels.x:
          graph.add_node((x,y))
          graph.add_edge((x,y), (x+1,y), edge_weight)
          graph.add_edge((x,y), (x,y+1), edge_weight)
{% endhighlight %}

The edge weight function could be any form of binary distance function such that
differences between neighboring pixels above and below a constant threshold become 1
and 0 respectively. Relating this to the cost map, 0 indicates that there was strong
evidence for a natural boundary while 1 indicates no such evidence.

{% highlight python %}
    def edge_weight(a,b):
      weight = e ^ abs(a - b) ^ 2 / -normalize
      weight > threshold ? true : false
{% endhighlight %}

After the graph has been initialized with all the relevant nodes and edges, the actual
process of segmenting the image can proceed. Based on the number of superpixels requested
and the amount of overlap allowed, the locations of all the guard bands are calculated
such that a regular array of equal size bands exist in the horizontal and vertical
direction.

{% highlight python %}
    # math replaced with general idea for brevity
    def generate_bands(image, pixels):
      xsize  = image.size.x / pixels.x
      ysize  = image.size.y / pixels.y
      xbands = [0:xsize:image.size.x]
      ybands = [0:ysize:image.size.y]
      return alternate_bands(xbands, ybands)
{% endhighlight %}

These are used to constrain the segmentation paths to a semi-regular lattice shape. The
program then iterates through each band attaching the source and sink to each side of
the guard band:

{% highlight python %}
    def setup_guard_band(band):
      source, sink = (-1,-1), (-2,-2)
      graph.add_nodes(source, sink)
      for node in band.source.start..band.source.end:
        graph.add_edge(source, node, guard_weight)
      for node in band.sink.start..band.sink.end:
        graph.add_edge(node, sink, guard_weight)

    def cleanup_guard_band(band):
      source, sink = (-1,-1), (-2,-2)
      graph.remove_nodes(source, sink)
{% endhighlight %}

The program then solves for the maximum flow between the source and sink nodes and
then uses the duality between maximum flow and minimum cut to solve for the cheapest
path through the specified graph band. After each path has been found, the program updates
the weights of the nodes in the discovered path to prevent other paths moving in the same
direction from crossing and destroying the lattice:

{% highlight python %}
    def update_path_weight(path):
      for node in path:
        graph.update_weight(node, path_weight)
{% endhighlight %}

It should be noted that the algorithm takes turns between finding a vertical and horizontal
path to hopefully add additional constraints to the winding of the paths. Furthermore, to
prevent paths from being too close to each other (and producing useless superpixels), a band
around the discovered path was given additional weight. The size of the band was based on a
tunable input parameter:

{% highlight python %}
    def update_band_weight(path):
      for node in path:
        for neighbor in graph.neighbors(node, width):
          graph.update_weight(neighbor, band_weight)
{% endhighlight %}

This has the added benefit that perpendicular paths will not double back on themselves
as it was simply too expensive to cross an existing path twice (although it was forced
to cross at least once). The program terminates by returning a list of the segmentation
paths successfully found in the specified image which can then be used to generate any
number of overlays on the final result image.

Experimental Results
------------------------------------------------------------

What follows is a collection of the result sets from running my program.
The first image in each set was the input gray-scale image, followed by the input
boundary cost map, and finally the segmented output of running the cost map
through my program and post-processing the resulting path output:

In the processed images, the blue lines indicate vertical paths while red lines
indicate horizontal paths. For a comparative purposes, two images have been
segmented into 3x3 superpixels while the remaining images have been segmented
into 9x9 superpixels:

** Example 1 **

<img width="320" src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/42049.jpg" />
<img width="320" src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/bench/gray/gPb_gray/42049.bmp" />
<img width="320" src="http://image-segment.googlecode.com/svn/trunk/Images/output-42049.jpg" />

** Example 2 **

<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/54082.jpg" />
<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/bench/gray/gPb_gray/54082.bmp" />
<img width="320" src="http://image-segment.googlecode.com/svn/trunk/Images/output-54082.jpg" />

** Example 3 **

<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/271035.jpg" />
<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/bench/gray/gPb_gray/271035.bmp" />
<img width="320" src="http://image-segment.googlecode.com/svn/trunk/Images/output-271035.jpg" />

** Example 4 **

<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/208001.jpg" />
<img src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/bench/gray/gPb_gray/208001.bmp" />
<img width="320" src="http://image-segment.googlecode.com/svn/trunk/Images/output-208001.jpg" />

** Example 5 **

<img width="320" src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300/html/images/plain/normal/gray/295087.jpg" />
<img width="320" src="http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/bench/gray/gPb_gray/295087.bmp" />
<img width="320" src="http://image-segment.googlecode.com/svn/trunk/Images/output-295087.jpg" />

Discussion of Results
------------------------------------------------------------

Although the overall algorithm was fairly trivial (in description and implementation),
the major work was in providing the scaffolding around working with an image in
graph format and implementing the s.t. min-cuts algorithm. Even when using a
a third-party max-flow algorithm, I was still faced with the task of finding the
correct minimum path from the residual edge result set.

The major problem with my implementation was the speed of processing. This was due
to the fact that I am working in a managed environment, constantly modifying the
graph, and dealing with a graph library that may or may not be the most efficient
for the number of nodes and edges I am dealing with (~40k nodes and ~100k edges).

As a result, most non-trivial operations took a very long time, especially the
maximum flow algorithm.  As an example, it takes my algorithm about an hour to
segment an 241x161 pixel image into 9 superpixels and roughly 3 hours to segment
the same image into 81 superpixels!  Comparing this to the speed promised by the
authors (2fps to convert a 321x481 image to a 20x20 superpixel lattice) shows
that they spent a great deal of time tuning their implementation.

In trying to speed up the process, I simply reduced the size of the input cost maps
by half, however, artifacts resulting from the resizing were sometimes interpreted
as possible edge points and would cause the lattice paths to slightly meander.

As a whole, I was satisfied with the results of the program as they did seem to
follow the image and create semantic pixels. Furthermore, when comparing to the
output of the authors' implementation, my program appeared to produce similar
results.

Future Work
------------------------------------------------------------

There is a great deal of work that could be improved on my current implementation,
mainly involving performance. What follows is a list of possible improvements
to my program:

*   Use a tuned minimum-cuts graph algorithm instead of solving for maximum flow.

    * Maybe substitute the current maximum flow implementation with the push-relabel
      method of Goldberg and Tarjan.
    * There are a number of algorithms that do not need to solve exhaustively for
      the max flow in order to find the global minimum cut ([stoer-wagner][]).
    * Maybe find algorithms that will quickly find a cut that is *good enough*
      (guaranteed to be in the upper **N** percent of possible cuts).
    
*   Use a lighter representation of the image graph

    * Use a graph wrapper around a sparse array of edges for O(1) access time
    * Break the graph into pieces to be solved one at a time
    
*   Implement the algorithm in C++ with BGL, or at least the main portions and
    call down from a higher level language.

External Links
------------------------------------------------------------

*   [Berkeley Segmentation Dataset and Benchmark](http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/)
    
    This is the image database that the authors pulled their image data from.  In order
    to compare results, I collected all the gray example images from their paper
    from this site as well as the edge cost maps associated with them.

*   [Code Repository](http://code.google.com/p/image-segment/)
    
    This is the repository that all the code for this project resides at as well
    as the test data and output results.
 
*   [QuickGraph](http://quickgraph.codeplex.com)

    This is a port of the boost graph library to C#. It was used to create and work with
    a graph representation of the input image and for the maximum flow algorithm
    implementation.

*   [Aforge.Net](http://code.google.com/p/aforge)

    This is a vision library for C#. It was used to abstract away some of the low level
    unmanaged image pixel operations (although it really could have been excluded).

*   [Intermediary Results](http://image-segment.googlecode.com/svn/trunk/Results/)

    The following represents a few intermediary representations of the program process
    that were recorded in debug sessions that may assist in understanding the workflow:

    *  The *dot* files are the graphviz serialization format of the image graph
    *  The *dot.png* files are the processed graphviz files to produce examples of the graph
       minimum cut at various bands.
    *  The *max-flow-image.bmp* file was the example processed image that the previous two
       formats were generated from.
    *  The *xml* files are the serialized output paths that were generated from the program
       for the specified images. They were processed to create the path overlays on the final
       result images.
    *  The *log* files are the processing logs that show about how long each step in the process
       took for my implementation.
  
  [stoer-wagner]: http://www.cs.dartmouth.edu/~ac/Teach/CS105-Winter05/Handouts/stoerwagner-mincut.pdf "Stoer Wagner"
  [superpixel]: http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf "Superpixel Lattice"
  [assignment]: http://research.engineering.wustledu/~pless/559/projects/finalProject.htm "Assignment Details"
  [repository]: http://code.google.com/p/image-segment/ "Master Repository"
  [quickgraph]: http://quickgraph.codeplex.com/ "QuickGraph"
  [log4net]: http://logging.apache.org/log4net/index.html "Log4net"
  [aforge]: http://code.google.com/p/aforge "Aforge Imaging"
  [bsdb]: http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/ "Berkeley Segmentation Dataset and Benchmark"

