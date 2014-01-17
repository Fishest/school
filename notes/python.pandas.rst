================================================================================
Python Pandas
================================================================================

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

There are two types in pandas:

* `Series` - This is a 1-dimensional type
* `TimeSeries` - Series with index containing datetime
* `DataFrame` - This is a 2-dimensional type (container for `Series`)
* `Panel` - This is a 3-dimensional type (container for `DateFrame`)

--------------------------------------------------------------------------------
Chapter 2: Ipython
--------------------------------------------------------------------------------

An external script can be run with `%run input.py` and the resulting global
variables will be set in the ipython interpreter.

A piece of code can be run piecewise by copying it and using `%paste` to run
what is in the clipboard in its own block. To examine the code before running
it, you can run `%cpaste`.

There are a number of extra magic commands such as:

* `%time code` - to time a python function a single time
* `%timeit code` - to time a python function multiple times
* `%reset` - to reset the current namespace
* `%magic` - lists the available magic commands
* `%pdb` - to drop into pdb after an exception
* `%debug` - to enable the debugger to start after an exception
* `%logstart` - to start logging the entire python session
* `var = !cmd` - run the unix command and store the result
* `%bookmark alias path` - to make alias to common directories
* `%prun <flags> function()` - to profile the supplied function
* `%run -p <flags> file.py` - to profile the supplied file from ipython
* `%lprun -f <function> statement` - to line by line profile a function


Here are some useful utilities that can be useful:

.. code-block:: python

    def set_trace():
        from IPython.core.debugger import Pdb
        Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)

    def debug(f, *args, **kwargs):
        from IPython.core.debugger import Pdb
        pdb = Pdb(color_scheme='Linux')
        return pdb.runcall(f, *args, **kwargs) // sigh**

You can profile an application using the command line profiler as follows:
`python -m cProfile application.py`. Or you can do this from the ipyhton
shell. If you need to reload a module, just `reload(module)`. If you need
to perform a deep reload (recursive), just `dreload(module)`.

--------------------------------------------------------------------------------
Chapter 4: Numoy
--------------------------------------------------------------------------------

Numpy provides a number of utilities to make operation on large data sets much
easier:

* Fast and space-efficient multidimensional array with vectorized arithmetic
  operations and sophisticated broadcasting capabilities
* Mathematical functions for fast operations on entire arrays of data without loops
* Tools for reading / writing array data to disk and working with memory-mapped files
* Linear algebra, random number generation, and Fourier transform capabilities
* Tools for integrating code written in C, C++, and Fortran

Here are some common operations with numpy:

.. code-block:: python

    data = [1,2,3,4,5,6,7,8]
    arry = np.array(data)     # create an array from supplied data
    arry.astype('int')        # convert the array to the specified type
    arry.shape                # a tuple of the matrix shape
    arry.dtype                # the underlying datatype of the array
    arry.ndim                 # the number of dimensions of the array
    np.ones(10)               # create an array of ones (single dimension)
    np.zeros((10, 10))        # create an array of zeros (two dimension)
    np.empty((2, 2, 2))       # create an array without initialization (three dimensions)
    np.arange(10)             # create an array like range(10)
    np.ones_like(arry)        # create a one array with the provided shape
    np.zeros_like(arry)       # create a zero array with the provided shape
    np.empty_like(arry)       # create an empty array with the provided shape
    np.asarray(arry)          # if already an ndarray, do not copy
    np.identity(10)           # create NxN identity matrix
    np.eye(10)                # create NxN identity matrix

    arr1 * arr2               # multiply the two matricies, or +,-
    arr1 + 10                 # perform the scalar operation on all elements
                              # in the array: +,-,/,*,**
    arr1[10]                  # gets the supplied value from the array
    arr1[1:5] = 5             # broadcast the value 5 to each element

    slce = arry[1:5]          # creates a view of the array (not a copy)
    slce[:] = 64              # the values in arry and slce are now 64
    arry[1:5].copy()          # creates a shallow copy of the view

    arr[0][2]                 # accesses an element in a 2d array
    arr[0, 2]                 # tuple accesses an element in a 2d array
    arr[:, :2]                # can create sophisticated slices
    arry[data == 1, :4]       # advanced boolean array selection and slicing
    arry[(data == 1) || (data == 2)]
    arry[[4,3,0,6]]           # retrieve the slices of matrix
    arry[[-1,-5,-3]]          # retrieve the slices of matrix, negatively

page 87 (more stuff to document)


Example of using numpy random methods to perform a random walk:

.. code-block:: python

    import numpy as np
    steps = 100
    draws = np.random.randint(0, 2, size=steps)
    steps = np.where(draws > 0, 1, -1)
    walk  = steps.cumsum()
    walk.min()                 # the minimum walk along a trajectory
    walk.max()                 # the maximum walk along a trajectory
    (np.abs(walk) >= 10).argmax()

    # to make this perform many walks, only the following needs to change
    # also, you can change the distribution below to use normal, gaussian, etc
    # instead of using the randint (coin toss)
    walks = 100
    draws = np.random.randint(0, 2, size=(walks, steps))
    steps = np.where(draws > 0, 1, -1)
    walks = steps.cumsum(1)
    hits  = (np.abs(walks) >= 30).any(1)    # the walks that passed 30
    hits.sum()                              # the number of walks that passed 30
    xing  = (np.abs(walks[hits])).argmax(1) # the largest crossing points

--------------------------------------------------------------------------------
Chapter 5: Getting started with pandas
--------------------------------------------------------------------------------

What follows is a good preamble to any pandas script:

.. code-block:: python

    from pandas import Series, DataFrame # the main pandas data structures
    import pandas as pd                  # the main pandas prefix
    import numpy as np                   # optional to include numpy support

There are two important data structures that are used in pandas, the first
is the `Series`. This is a one dimensional array of data with an associated
array of index lables (defaulted to 0..N-1):

.. code-block:: python

    s = Series({'a': 1, 'b': 2, 'c': 3, 'd': 4})
    s = Series([1,2,3,4], index=['a', 'b', 'c', 'd'])
    s[0] == s['a']  # True
    s[['b', 'c']]   # [2, 3]
    s[s % 2 == 0]   # [2, 4]

    # values can be checked for existance or not, also performing
    # operations with two mismatched Series collections will align
    # correctly.
    s.isnull()
    s.notnull()

    # properties of the series can be changed
    s.name = "letters"
    s.index.name = "count"
    s.index = ['c', 'd', 'e', 'f']

The next object is the `DataFrame`. It is a tabular spreadsheet like structure
that can be though of as a dict of `Series` all sharing the same indexes. With
it you can perform column level and row level operations:

.. code-block:: python

    # a frame can be created in a number of ways and columns can be overriden
    # or set from existing data. By setting a dict of dict, the outer dict becomes
    # the columns and the inner dict becomes the index.
    data = {
        'state': ['AL', 'MO', 'WA', 'CO'],
        'year':  [1996, 2003, 2012, 2015],
        'date':  [True, True, True, False]
    }
    frame = DataFrame(data)
    frame = DataFrame(data, columns=['state', 'year', 'date', 'dept'], index=[1,2,3,4])

    # The various properties can be explored
    frame.values      # the current entries in the data frame as a 2d array
    frame.index       # to see the current index
    frame.columns     # to see all the columns
    frame.T           # to transpose the index and columns

    # the columns can be accessed by dict or property accessors, both of which
    # return series data. If you assign a list to a column, it must match the length
    # exactly. If you assign a Series, the DataFrame will adapt to align missing fields.
    frame['state']               # This returns a Series as a view (modifications are reflected)
    frame.state
    frame['dept'] = 'eng'        # set the value for all entries (say missing)
    frame['age']  = np.arange(4) # set a series for all values, will create a new column
    del frame['age']             # will remove an existing column


    # rows can be retrieved in a number of ways
    frame.ix[2]

Index objects are immutable sets that can be safely shared between code. There 
are a few specialized indexes in pandas for specific datatypes or hierarchies.
The index type has a number of methods that make it useful as a set datatype.

What follows is the essential functionality of working with data in Series or
DataFrames using pandas:

.. code-block:: python

    # reindexing creates a new object indexed with the new index
    # missing values can be supplied with a single fill value, forward fill(ffill),
    # backwards fill(bfill), or do it yourself after reindexing. DataFrames are
    # the same except you can reindex the columns or the indexes.
    s1 = Series([1,2,3,4], index=['a', 'b', 'c', 'd'])
    s2 = s1.reindex([0, 1, 2, 3, 4], fill_value=0)
    s3 = s1.reindex([0, 1, 2, 3, 4], method='ffill')

    # axis can be dropped using the drop command, these return a new instance
    series.drop('a')
    series.drop(['a', 'b'])
    frame.drop('a')
    frame.drop('state', axis=1)

    # indexing works similar to numpy, except you use the index
    series[[0,1,2]]             # multiselect
    series[series > 2]          # boolean indexing
    series[0:2]                 # slice with a range
    series[0:2] = 0             # slice assignment single value
    series[0:2] = np.arange(3)  # slice assignment list value
    frame['a']                  # select single column
    frame['a':'c']              # slices based on labels (inclusive)
    frame[:5]                   # rows by integer slicing
    frame[frame.year > 2000]]   # boolean extraction
    frame[frame < 5] = 0        # mass setting of non-mixed types
    frame.ix[[0:2], 'year']     # row selection with slice
    frame.ix[frame.date < 2005] # boolean selection of rows
    frame.xs                    # select row or column as series with label
    frame.icol                  # select column by integer index
    frame.irow                  # select row by integer index

When merging data sets, pandas creates the union of the indexes, aligns and pads
data as neccessary before returing the new object:

.. code-block:: python

    # If the data doesn't overlap, pandas will set the result as NaN
    # The same methods exist for Series and DataFrame types:
    # add, sub, div, mul.
    s = Series([1,2,3,4], index=['a', 'b', 'c', 'd'])
    r = Series([5,6,7,8], index=['b', 'c', 'e', 'f'])
    s + r                  # [NaN, 7, 9, NaN, NaN, NaN]
    s.add(r, fill_value=0) # [1, 7, 9, 4, 7, 8]

    # Operations between Series and DataFrame broadcast simlilar to
    # traditional numpy arrays
    na = np.arange(12).reshape(3,4)
    na - na[0]

    index = ['MO', 'AL', 'TX', 'WA']
    frame = DataFrame(np.arange(12).reshape(4, 3), columns=list('bde'), index=index)
    series = frame.ix[0]
    frame - series                # to broadcast over rows
    frame.sub(frame['b'], axis=0) # to broadcast over columns

Many types of functions can be applied to `DataFrame` or `Series`:

.. code-block:: python

    def double(x): return x * 2
    def single(x): return x.max() - x.min()
    def multi(x):  return Series([x.min(), x.max()], index=['min', 'max'])
    frame.apply(single axis=1) # reduce a row or column to single value
    frame.apply(multi)         # can return a series of data as well
    frame.applymap(double)     # can apply a method to each value in a DataFrame
    frame['a'].map(double)     # can apply a method to each value in a Series
    frame.sum()                # also mean, max, min, etc
    np.abs(frame)              # can apply numpy unary functions

Data can be sorted and ranked on both data types:

.. code-block:: python

    s = Series([1,2,3,4], index=['a', 'b', 'c', 'd'])
    s.sort_index()                         # to sort by the indexes
    s.order()                              # to sort by the values
    s.rank()                               # ranks values with ties broken by average
    s.rank(method='first')                 # use the first, max, min, average

    f = DataFrame(np.arange(12).reshape(4, 3), columns=list('efg'), index=list('abcd'))
    f.sort_index(axis=1)                   # to sort by the column labels
    f.sort_index(axis=0, ascending=False)  # to sort in descending order
    f.sort_index(by='a')                   # to sort by the values of a column
    f.sort_index(by=['a', 'b'])            # to sort by the values of many columns
    f.rank(axis=1)                         # rank based on the supplied axis

page 132
