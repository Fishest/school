================================================================================
Python Libraries
================================================================================

--------------------------------------------------------------------------------
Jinja2
--------------------------------------------------------------------------------
http://jinja.pocoo.org/docs/

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Summary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

--------------------------------------------------------------------------------
IPython
--------------------------------------------------------------------------------

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Magic Commands
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* `%edit` - opens an editor and then executes the saved code block
* `%quickref` - prints the ipython quickreference
* `%timeit <command>` - high precision timer of the given command

--------------------------------------------------------------------------------
Pytz
--------------------------------------------------------------------------------

http://pytz.sourceforge.net/

.. code-block::

    from datetime import datetime, timedelta
    from pytz import timezone
    import pytz

    utc_tz        = pytz.utc
    eastern_tz    = timezone('US/Eastern')
    amsterdam_tz  = timezone('Europe/Amsterdam')
    format        = '%Y-%m-%d %H:%M:%S %Z%z'
    local_date    = datetime(2002, 10, 27, 6, 0, 0))
    local_date_es = eastern.localize(local_date)

    print(local_date.strftime(format))
    print(local_date_es.strftime(format))
    print(utc.zone)     # 'UTC'
    print(eastern.zone) # 'US/Eastern'

--------------------------------------------------------------------------------
Profiling
--------------------------------------------------------------------------------

To profile a python application, the best library collection is cProfile and
pstats. These don't out of the box do a good job of showing hot-paths through
a hierarchy, but they have enough ability to show the most used pieces of code
and a simple call hierarchy. To run them, simple do the following:

.. code-block:: bash

    # to instrument script.python
    python -m cProfile -o script.profile script.python
    python -m pstats script.profile

To work with `pstats` there is a help menu that is activated by typing `help` or
`help <command>`.
