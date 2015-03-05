================================================================================
Performance Profiling
================================================================================

http://www.slideshare.net/brendangregg/scale2015-linux-perfprofiling

--------------------------------------------------------------------------------
Summary
--------------------------------------------------------------------------------

* **who** - `top`, `htop`
* **why** - `perf record -g`, flame graphs
* **what** - `perf stat -a -d`
* **how** - application monitoring

--------------------------------------------------------------------------------
Linux Kernel Profiling
--------------------------------------------------------------------------------

This is the main linux profiler. Users interact with the system with the
userland `perf` command (linux-tools-common). It allows users to profile or
trace the following:

* CPU performance monitoring counters (PMC)
* Statically defined tracepoints
* User and kernel dynamic tracing
* kernel line and local variable tracing
* Efficient in-kernal counts and filters
* Stack tracing with `libunwind`
* Code annotation

.. code-block:: bash

    usage: perf [--version] [--help] COMMAND [ARGS]
    
    The most commonly used perf commands are:
      annotate        Read perf.data (created by perf record) and display annotated code
      archive         Create archive with object files with build-ids found in perf.data file
      bench           General framework for benchmark suites
      buildid-cache   Manage build-id cache.
      buildid-list    List the buildids in a perf.data file
      diff            Read perf.data files and display the differential profile
      evlist          List the event names in a perf.data file
      inject          Filter to augment the events stream with additional information
      kmem            Tool to trace/measure kernel memory(slab) properties
      kvm             Tool to trace/measure kvm guest os
      list            List all symbolic event types
      lock            Analyze lock events
      mem             Profile memory accesses
      record          Run a command and record its profile into perf.data
      report          Read perf.data (created by perf record) and display the profile
      sched           Tool to trace/measure scheduler properties (latencies)
      script          Read perf.data (created by perf record) and display trace output
      stat            Run a command and gather performance counter statistics
      test            Runs sanity tests.
      timechart       Tool to visualize total system behavior during a workload
      top             System profiling tool.
      trace           strace inspired tool
      probe           Define new dynamic tracepoints
    
    See 'perf help COMMAND' for more information on a specific command.

The `perf` command intstruments using `stat` or `record`. Each command has three
main parts: action, event, scope. For example, the following command records
stack traces at 99Hz on all cpus: `perf record -F 99 -a -g -- sleep 10`. The
perf command can be run at a number of scopes:

* system wide (all cpus) `-a`
* target pid  `-p <pid>`
* target command `<command>`
* specific CPU `-c <cpu>`
* user-level only `<event>:u`
* kernel-level only `<event>:k`
* custom filter `--filter <filter>`

--------------------------------------------------------------------------------
Common Commands
--------------------------------------------------------------------------------

.. code-block:: bash

   perf list               # list all currently known events
   perf list | grep sched  # searching for sched tracepoints
   perf list "sched:\*"    # listing sched tracepoints
   perf stat <command>     # cpu counter statistics for command
   perf stat -d <command>  # detailed cpu counter statistics
   perf stat -p <pid>      # cpu counter statistics for pid
   perf stat -a sleep 5    # cpu counter statistics for the whole system

--------------------------------------------------------------------------------
Probes
--------------------------------------------------------------------------------

Probes can be inserted into the kernel with the following utilities:

* `uprobes` - userspace probes
* `kprobes` - for in kernel
