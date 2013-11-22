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


Here are some useful utilities that can be useful:

.. code-block:: python

    def set_trace():
        from IPython.core.debugger import Pdb
        Pdb(color_scheme='Linux').set_trace(sys._getframe().f_back)

    def debug(f, *args, **kwargs):
        from IPython.core.debugger import Pdb
        pdb = Pdb(color_scheme='Linux')
        return pdb.runcall(f, *args, **kwargs) // sigh**

page 65
