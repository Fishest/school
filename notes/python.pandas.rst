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

Pandas indexes have a number of methods based on set logic (all of these
methods produce new index instances if they are mutators):

.. code-block:: python

    index.append        # concatenate another index
    index.diff          # compute the index set difference
    index.intersection  # compute the index set intersection
    index.union         # compute the index set union
    index.isin          # compute boolean array of left in right
    index.delete        # compute index with supplied row deleted (axis=0,1)
    index.drop          # compute new index with supplied row dropped (axis=0,1)
    index.insert        # compute new index with new additional rows
    index.is_monotonic  # True if the index is monotonically increasing
    index.is_unique     # True if the index has no duplicates
    index.unique        # compute the array of unique values in the index

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

Operations on pandas values are designed to deal with missing rows,
this can be controlled through:

.. code-block:: python

    frame = DataFrame([1.4, np.nan], [7.1, -4.5], [np.nan, np.nan], columns=['one', 'two'], index=['a', 'b', 'c'])
    frame.sum()                     # [8.5, -4.5]
    frame.sum(skipna=False)         # [np.nan, np.nan]
    frame.sum(axis=1, skipna=False) # [np.nan, 2.6, np.nan]


Pandas provides a number of functions involving statistics on a 
dataset out of the box:

.. code-block:: python

    frame.count                    # number of non-NA values
    frame.describe                 # summary of statistics of series or frame
    frame.min, frame.max           # the max, min values of each column
    frame.argmin, frame.argmax     # the indexes of max, min values
    frame.idxmin, frame.idxmax     # the indexes of max, min values
    frame.quantile                 # compute the sample quantile range
    frame.sum                      # sum of the values per axis
    frame.mean                     # mean of values per axis
    frame.median                   # median of values per axis
    frame.mad                      # mean absolute deviation from mean value of values per axis
    frame.var                      # variance of values per axis
    frame.std                      # standard deviation of values per axis
    frame.skew                     # skewnewss (3rd moment) of values per axis
    frame.kurt                     # kurtosis (4th moment) of values per axis
    frame.cumsum                   # cumulative sum of values per axis
    frame.cummin, frame.cummax     # cumulative min, max of values per axis
    frame.cumprod                  # cummulative product of values
    frame.diff                     # 1st arithmetic difference between values
    frame.pct_change               # percent change between values

.. todo:: Page 136 yahoo stock data

Pandas is designed to correctly handle missing data in frames and
series instances as well as a number of methods for working with
missing values:

.. code-block:: python

    frame.dropna()                  # drop all rows with NA values
    frame.dropna(axis=1, how='all') # drop all cols with _all_ NA values
    frame.dropna(thresh=3)          # drop all rows with at least 3 NA values
    frame.isnull()                  # boolean array of where NA values
    frame[frame.notnull()]          # boolean array of where not NA values:w
    frame.fillna(value)             # replace all NA with value
    frame.fillna({ 1:, 0.1 })       # replace all NA values in row 1 with value
    frame.fillna(inplace=True)      # modify the existing instance and do not make a copy
    frame.fillna(frame.mean())      # replace NA values with each rows mean

Pandas allows for higher dimensional indexes with `MultiIndex`. There is
also the `Panel` datatype that allows for N dimensional frames:

.. code-block:: python

    series = Series(np.random.randn(10), index=[
        ['a', 'a', 'a', 'b', 'b', 'b', 'c', 'c', 'd', 'd'],
        [1,2,3,1,2,3,1,2,2,3]])
    series.index                       # view the multi-index
    frame = series.unstack()           # creates a dataframe
    frame.stack()                      # converts a dataframe to a multi-series
    frame.swaplevel('key1', 'key2')    # swap the index level
    frame.sortlevel(1)                 # sort the frame by the specified level
    frame.swaplevel(0, 1).sortlevel(0) # sort by the new level
    frame.sum(level=1)                 # all methods can operate on arbitrary levels

There is abiguity about whether to use position or index indexing
if the index is numeric. Therefore, if you are going to use positional
based indexing (series[-1]), use `Series.iget_value(idx)`, `Frame.irow(idx)`,
or `Frame.icol(idx)`. Use the index for all other methods.

--------------------------------------------------------------------------------
Chapter 6: Data Loading, Storage, and File Formats
--------------------------------------------------------------------------------

Pandas has a number of methods for easily reading data in various formats. All
of the following handle the various issues:

* indexing on one or more columns and setting column names
* type detection and conversion including custom types
* datetime parsing including aggregating values over many columns
* iterating over chunks of large files
* unclean data issues like skipping bad rows

.. code-block:: python

    read_csv         # read from a delimited file, url, or stream (, delim)
    read_table       # read from a delimited file, url, or stream (\t delim)
    read_fwf         # read data in fixed width columns (no delim)
    read_clipboard   # read table from the current clipboard

    read_csv('file.csv', header=None)           # if you want pandas to assign column names
    read_csv('file.csv', names=['a', 'b', 'c']) # for setting your own column names
    read_csv('file.csv', index_col='c')         # for setting the index
    read_csv('file.csv', sep='\s+')             # for columns seperated by variable spacing
    read_csv('file.csv', skiprows=[0,1,2])      # for skipping bad rows or comments
    read_csv('file.csv', na_values=['Nil'])     # specify what values should be skipped
    read_csv('file.csv', na_values={'a':'Nil'}) # specify skip values per column
    read_csv('file.csv', nrows=5)               # only read N rows from the dataset
    read_csv('file.csv', chunksize=1000)        # read and parse the file in chunks
    Series.from_csv('file.csv')                 # to read into a Series

Reading in chunks can be used to efficiently aggregate statistics from a file:

.. code-block:: python

    chunks = read_csv('file.csv', chunksize=1000)
    totals = Series([])
    for chunk in chunks:
        totals = totals.add(chunk['key'].value_counts(), fill_value=0)
    totals = totals.order(ascending=False)

Data can also be written out from a data frame:

.. code-block:: python

    frame.to_csv(sys.stdout, sep='|')           # write the frame to stdout
    frame.to_csv('file.cvs', na_rep='NULL')     # define how missing values should be displayed
    frame.to_csv('file.cvs', index=0, header=0) # disable printing of column and row headers
    frame.to_csv('file.cvs', cols=['a', 'b'])   # print only a subset of columns in specified order

.. note:: For more complicated schemes, use the built in python csv
   module and define your own cvs.Dialect.

.. todo:: Explore hdf5 with pytables and h5py. These should be used for
   write once and read many applications.

What follows is an example of using pandas with the twitter web api:

.. code-block:: python

    import requests
    import json

    query  = 'http://search.twitter.com/search.json?q=python%20pandas'
    result = requests.get(query)
    data   = json.loads(result.text)
    fields = ['created_at', 'from_user', 'id', 'text']
    frame  = DataFrame(data['results'], columns=fields)

What follows is an example of using pandas with the beautifulsoup:

.. code-block:: python

    from pandas.io.parsers import TextParser
    from BeautifulSoup import BeautifulSoup
    from urllib2 import urlopen

    def _unpack(row, kind='td'):
        return [val.text for val in row.findAll(kind)]

    def parse_options_data(table):
        rows = table.findAll('tr')
        header = _unpack(rows[0], kind='th')
        data = [_unpack(r) for r in rows[1:]]
        return TextParser(data, names=header).get_chunk()

    buffer = urlopen('http://finance.yahoo.com/q/op?s=AAPL+Options')
    soup   = BeautifulSoup(buffer)
    urls   = [link.get('href') for link in soap.body.findAll('a')]
    tables = soap.body.findAll('table')
    calls  = parse_options_data(tables[9])
    puts   = parse_options_data(tables[13])

What follows is an example of using pandas with a database:

.. code-block:: python

    import sqlite3

    table = """
    CREATE TABLE test
    (a VARCHAR(20), b VARCHAR(20),
    c REAL, d INTEGER
    );"""

    con = sqlite3.connect(':memory:')
    con.execute(table)
    con.commit()

    data = [('Atlanta', 'Georgia', 1.25, 6),
        ('Tallahassee', 'Florida', 2.6, 3),
        ('Sacramento', 'California', 1.7, 5)]
    stmt = "INSERT INTO test VALUES(?, ?, ?, ?)"
    con.executemany(stmt, data)
    con.commit()

    cursor = con.execute('select * from test')
    rows   = cursor.fetchall()
    frame  = DataFrame(rows, columns=zip(cursor.description)[0])

--------------------------------------------------------------------------------
Chapter 7: Data Wrangling
--------------------------------------------------------------------------------

Pandas has a few methods for combining and merging various datasets, say from a
normalized database. The common methods are as follows:

.. code-block:: python

    pd.merge(f1, f2)                              # merge the two datasets with an implicit key
    pd.merge(f1, f2, on='key')                    # merge the two datasets on the specified key
    pd.merge(f1, f2, on=['key1', 'key2'])         # merge the two datasets on many keys
    pd.merge(f1, f2, left_on='k1', right_on='k2') # merge with different key names
    pd.merge(f1, f2, how='outer')                 # inner by default; options are { left, right, outer }

    f1 = DataFrame({'key': ['a', 'b', 'c'], 'data2':range(3) })
    f2 = DataFrame({'key': ['b', 'b', 'a', 'c', 'a', 'a', 'b'], 'data2':range(7) })
    pd.merge(f1, f2)                              # a many to one merge, many to many is the cartesian product
    pd.merge(f1, f2, suffixes=['_l', '_r'])       # break merging ties with column suffixes
    pd.merge(f1, f2, right_index=True)            # to merge with the left, right, or both indexes
    f1.join(f2)                                   # shorthand method if you are joining on indexes

Pandas also extends the numpy concat operations to handle a number of issues:

.. code-block:: python

    s1 = Series([0, 1], index=['a', 'b'])
    s2 = Series([2, 3, 4], index=['c', 'd', 'e'])
    s3 = Series([5, 6], index=['f', 'g'])
    pd.concat([s1, s2, s3])                       # no index overlap simply glues the values
    pd.concat([s1, s2, s3], axis=1)               # concat on the columns and return a DataFrame

    f1.combine_first(f2)                          # can be though of patching values in f1 with f2

Pandas allows you to stack and unstack `DataFrames` and `Series`:

.. code-block:: python

    series = frame.stack('column')                # stack a frame onto a series
    series.unstack('column')                      # unstack the series back to a dataframe
    frame.stack()                                 # by default the leftmost column is used

Pandas allows you to clean your `DataFrames` with a number of operations:

.. code-block:: python

    frame.duplicates()                            # returns a bool array of duplicated values
    frame.drop_duplicates()                       # returns a new frame with duplicates removed
    frame.drop_duplicates(['k1', 'k2'])           # drop duplicates on the following columns
    frame.drop_duplicates(take_last=True)         # default takes the first duplicate, this takes the last

Here is an example of cleaning existing data

.. code-block:: python

    meat_to_animal = {
        'bacon': 'pig',
        'pulled pork': 'pig',
        'pastrami': 'cow',
        'corned beef': 'cow',
        'honey ham': 'pig',
        'nova lox': 'salmon'
    }
    frame = DataFrame({'food': ['bacon', 'pulled pork', 'bacon', 'Pastrami',
        'corned beef', 'Bacon', 'pastrami', 'honey ham', 'nova lox'],
        'ounces': [4, 3, 12, 6, 7.5, 8, 3, 5, 6]})
    frame['animal'] = frame['food'].map(str.lower).map(meat_to_animal)

    frame.index = frame.index.map(str.upper)         # we can modify the index with a map operation
    frame.rename(index=str.title, columns=str.upper) # helper that does the same; also takes dict mapping

.. todo:: page 197 binning
