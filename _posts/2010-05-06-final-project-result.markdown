---
layout: post
title: Project 4 - Final Project Result
---

{{ page.title }}
============================================================

<p class="meta"/>06 May 2010 - St. Louis</p>


Introduction
------------------------------------------------------------

For the final project [assignment][] I was tasked with reimplementing the algorithm discussed
in the [superpixel][] paper. I attempted to reproduce the results found in the paper
individually in C# with a few helper libraries.

Related Work and References
------------------------------------------------------------

Although I was not attempting to implement any original material, there are a wealth of
papers directly related to subject of image segmentation and graph theory that proved
helpful in this project.  For the sake of brevity, only the most relevant are listed:

*  [Superpixel Lattices](http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf)

   This was the main paper containing the algorithm to implement.

*  [Scene Shape Priors for Superpixel Segmentation](http://web4.cs.ucl.ac.uk/research/vis/pl/publications/SceneShape.pdf)

   This is a continuation of the superpixel lattice paper to allow the algorithm to work
   on videos.

*  [Stereo Matching and Graph Cuts](http://intechweb.org/downloadpdf.php?id=5774)

   This is a helpful introduction to graph theory, network flow, and graph cuts.

*  [A New Approach to the Maximum Flow Problem](http://portal.acm.org/citatation.cfm?id=12144)

   This is an in depth overview of most of the maximum-flow algorithms used to implement
   s.t. min-cuts.

Technical Description
------------------------------------------------------------

Before starting the segmentation algorithm, the user is expected to supply a **boundary
cost map** that contains meaningful boundaries between neighboring pixels. The authors
state that an edge detection output will suffice for the majority of cases. This mapping
is then inverted, normalized, and converted to a directed graph:

{% highlight python %}
    def build_graph(image):
      for y in image.pixels.y:
        for x in image.pixels.x:
          graph.add_node((x,y))
          graph.add_edge((x,y), (x+1,y), edge_weight)
          graph.add_edge((x,y), (x,y+1), edge_weight)
      
    def edge_weight(a,b):
      e ^ abs(a - b) ^ 2 / -normalize
{% endhighlight %}

The edge weight is some form of binary distance function such that pixel differences
above and below a constant threshold become 1 and 0 respectively. In terms of the cost
map, we use 0 to be strong evidence for a natural boundary while 1 indicates no evidence
of a boundary.

After the graph has been initialized with all the relevant nodes and edges, the actual
process of segmenting the image can proceed. Based on the number of superpixels requested
and the amount of overlap allowed, the location of all the guard bands are calculated.
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
path through the boundary map. After each path has been found, the program updates
the weights of those nodes to prevent paths that would cross and destroy the lattice.
Also, to prevent paths from being to close to each other, a band around each path
is given an increased weight:

{% highlight python %}
    def update_path_weight(path):
      for node in path:
        graph.update_weight(node, path_weight)

    def update_band_weight(path):
      for node in path:
        for neighbor in graph.neighbors(node):
          graph.update_weight(neighbor, band_weight)
{% endhighlight %}

This has the added benefit that perpendicular paths will not double back on themselves
as it is simply too expensive to cross an existing path twice (although it is forced
to cross at least once). The program terminates by returning a list of the segmentation
paths successfully found in the specified image.

Experimental Results
------------------------------------------------------------

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

Although the implementation was fairly trivial (in description and implementation),
the major crux of the problem was implementing, providing scaffolding around, and
constraining the maximum flow algorithm. Even when using a packaged implementation
I still had a number of problems, the most of which was actually retrieving the
correct path out of the maximum flow result set.

The major problem with my implementation was the speed of processing.  This is due
to the fact that I am working in a managed environment, constantly modifying the
graph, and dealing with a graph library that may or may not be the most efficient.
As a result, most non-trivial operations took a very long time, especially the
maximum flow algorithm.  As an example, it takes my algorithm about an hour to
segment an 241x161 pixel image into 9 superpixels.

In trying to speed up the process, I simply reduced the size of the input cost maps
by half, however, artifacts resulting from the resizing would be interpreted as possible
edge points and would cause the lattice paths to slightly meander.

As a whole, I was somewhat satisfied with the results of the program as they
did seem to follow the image and create semantic pixels. However in comparing
to the results suggested by the authors, my results appear to be far from ideal.
Furthermore, the speed offered by my implementation is downright abysmal compared
to the speed promised by the authors (2fps to convert a 321x481 image to a 20x20
superpixel lattice).

Future Work
------------------------------------------------------------

There is a great deal of work that could be improved on my current implementation,
most simply involving performance. What follows is a list of possible improvements
to my program:

*   Use a tuned minimum-cuts graph algorithm instead of solving for maximum flow.
    There are a number of algorithms that do not need to solve exhaustively for
    the max flow in order to find the global minimum cut. Also, there are algorithms
    that will quickly find a cut that is *good enough* (guaranteed to be in the upper
    **N** percent of possible cuts).
    
*   Use a lighter representation of the image graph

    * Use a graph wrapper around a sparse array of edges for O(1) access time
    * Only present pieces of the graph to be solved at a time
    
*   Implement a better tortuosity weighting of the paths as mine doesn't appear
    to work all that well.
*   Implement the algorithm in c++ with BGL to increase speed.

External Links
------------------------------------------------------------

*  [QuickGraph](http://quickgraph.codeplex.com)

   This is a port of the boost graph library to C#. It was used to create and work with
   a graph representation of the input image and for the maximum flow algorithm
   implementation.

*  [Aforge.Net](http://code.google.com/p/aforge)

   This is a vision library for C#. It was used to abstract away some of the low level
   unmanaged image pixel operations (although it really could have been excluded).

*  [Intermediary Graphs](http://image-segment.googlecode.com/svn/trunk/Results/)

   These represent four graph segmentation intermediary results that may assist in
   visualizing the algorithm process. The *.dot files are the dot representation of the
   graph and the *.png images are the processed output of graphviz on the associated *.dot file.
   The **h** and **v** represent horizontal and vertical path and **1** and **2** represent
   the first and second path in that direction. The segmentation was run on the
   max-flow-image.bmp located in the same directory.
  
  [superpixel]: http://www.cs.ucl.ac.uk/staff/s.prince/Papers/SuperpixelLattices.pdf "Superpixel Lattice"
  [assignment]: http://research.engineering.wustledu/~pless/559/projects/finalProject.htm "Assignment Details"
  [repository]: http://code.google.com/p/image-segment/ "Master Repository"
  [quickgraph]: http://quickgraph.codeplex.com/ "QuickGraph"
  [log4net]: http://logging.apache.org/log4net/index.html "Log4net"
  [aforge]: http://code.google.com/p/aforge "Aforge Imaging"
  [bsdb]: http://www.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/ "Berkeley Segmentation Dataset and Benchmark"

