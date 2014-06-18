============================================================
Chapter 1
============================================================

* move the program to the data and not vice versa
* two phases: map and reduce

  - map - filter and transform
  - reduce - aggregate over the results

* other common operations are implemented by default
  - shuffle, partitioning, etc

* datatypes used by mapreduce: key/value pairs and lists
  - key/values are usually int/string, but can also be dummy ignored values

* input to the application is list of key/value pairs
  - for files list(<string file_name, string file_data>)
  - for large file list(<int line_number, string log_event>)

* map function takes each element of the list and processes it
  - list(<k1, v1>) -> map(<k1, v1>) -> list(<k2, v2>)
  - counting words: map(<filename, content>) -> list(<word, count>)

* reduce function aggregates result into final result
  - list(<k2, list(v2)>) -> list(<k3, v3>)
  - counting words: reduce(<word, list(1, 2, 3)>) -> list(<word, 6>)

* mapreduce handles the pipeline between methods (collection and iteration)
  and output final results to files.

Example:

.. code-block:: java

    map(String filename, String document) {
        List<String> T = tokenize(document);
        for each token in T {
        	emit((String)token, (Integer)1);
        }
    }

    reduce(String token, List<Integer> values) {
        Integer sum = 0;
        for each value in values {
            sum = sum + value;
        }
        emit((String)token, (Integer)sum);
    }

* lucene -> nutch -> hadoop


============================================================
Chapter 2
============================================================

------------------------------------------------------------
Node Types
------------------------------------------------------------

* NameNode

  The master of the HDFS that directs the data node slave daemons.
  Basically the bookkeeperof HDFS for the cluster. This is the only
  service run by this machine (point of failure).

* DataNode

  Run by each slave node in the cluster to handle reading/writing
  files from HDFS. Communicates with the other DataNodes to find
  and work with files in question. Also backs up and replicates
  DateNode data.

* Secondary NameNode

  Single service run on its own machine. Basically a hot backup of
  the NameNode (to prevent failure). Needs to be set as primary in
  case of NameNode failure. For small networks, can be run on a
  slave node.

* JobTracker

  Takes job submissions and determines the execution plan to run
  ontop of Hadoop. Handles distributing tasks to files and nodes.
  Run one daemon per cluster on a server master node. For small
  networks run this and the NameNode on the same machine.

* TaskTracker

  Run on each slave node to run receive tasks from the JobTracker.
  Can spawn many JVM instances to run many map/reduce jobs in
  parallel. Heartbeats to JobTracker to determine availability.
  If heartbeat isn't heard, the JobTracker will assume this
  TaskTracker is crashed and will resubmit the job to anothero one.

------------------------------------------------------------
Hadoop Configuration Types
------------------------------------------------------------

* Local (standalone) mode

  The default mode for hadoop when initially uncompressed.
  All configuration files are simply empty. Communicates
  entirely locally and doesn't use HDFS and doesn't launch
  any daemons.

* Pseduo (distributed) mode

  This is basically a cluster of one.  You simply run all
  the daemons on one box. Ususally as a proof of concept
  for debugging.

* Full (distributed) mode

  Any number of fully distributed hadoop clusters.  Generally
  follows: master, backup master, hadoop1..hadoopN slaves

Can rapidly switch between the various modes using simlinked
configuration folders.

* The NamedNode generates a web interface on port 50070 with
  an overview of the cluster and nodes.
* The JobTracker generates a web interface on port 50030 with
  an overview of the current working jobs.
* These can be replaced or supplimented by using Hue.


============================================================
Chapter 3
============================================================

* HDFS is the persistance layer for map/reduce data. You don't
  have to programatically deal with this, the framework does that
  for you (files are read from HDFS and written back).
* There is the hdfs fuse bridge which emulates this.
* Standard file utilities don't work on HDFS, but there are utilities
  that implement the common operations. You generally only work on HDFS
  to import data into HDFS and export out

Example commands::

    # default working directory of /user/$USER
    hadoop fs -cmd args             # generic method command
    hadoop fs -ls                   # ls /user/$USER
    hadoop fs -lsr /                # basically dirtree /
    hadoop fs -mkdir /user/chuck    # makes parent directories if needed

    # path hdfs://localhost:9000/user/chuck/example.txt
    # equal to example.txt if logged in as chuck
    hadoop fs -cat example.txt
    hadoop fs -put example.txt .    # cp example.txt /user/$USER/example.txt
    hadoop fs -get example.txt .    # cp /user/$USER/example.txt example.txt
    hadoop fs -cat example.txt | head
    hadoop fs -tail example.txt
    hadoop fs -rm example.txt
    hadoop fs -rmr /user/chuck

    # example result of ls
    $ hadoop fs -ls
    Found 1 items
    -rw-r--r--  1 chuck supergroup 264 2009-01-14 11:02 /user/chuck/example.txt
                ^ replication factor

------------------------------------------------------------
MR Types
------------------------------------------------------------

* classes must implement the Writable interface to be mr values
* classes must implement the WritableComparable<T> to be mr keys or values

The following are the predefined prmitives:

* BooleanWritable - boolean primitive wrapper
* ByteWritable - byte primitive wrapper
* DoubleWritable - double primitive wrapper
* FloatWritable - float primitive wrapper
* IntWritable - int primitive wrapper
* LongWritable - long primitive wrapper
* NullWritable - placeholder when key/value isn't needed
* Text - wrapper for UTF8 text

Example custom graph edge type::

    public class Edge implements WritableComparable<Edge> {
        public String sourceNode;
        public String sinkNode;

        @Override
        public void readFields(DataInput in) throws IOException {
            sourceNode = in.readUTF();
            sinkNode = in.readUTF();
        }

        @Override
        public void write(DataOutput out) throws IOException {
            out.writeUTF(sourceNode);
            out.writeUTF(sinkNode);
        }

        @Override
        public int compareTo(Edge o) {
            return (sourceNode.compareTo(o.sourceNode) != 0)
                ? sourceNode.compareTo(o.sourceNode)
                : sinkNode.compareTo(o.sinkNode);
        }
    }

------------------------------------------------------------
MR Mapper
------------------------------------------------------------

* To be a mapper, implement the Mapper interface and inherit
  from the MapReduceBase class.

There are a number of default mapper implementations:

* IdentityMapper<K, V> -> Mapper<K, V, K, V> -> maps input to output
* InverseMapper<K, V> -> Mapper<K, V, V, K> -> reverses key and value
* RegexMapper<K, V> -> Mapper<K, Text, Text, LongWritable> -> (match, 1)
* TokenCountMapper<K> -> Mapper<K, Text, Text, LongWritable> -> (token, 1)

Interface for Mapper<K1, V1, K2, V2>::

    void map(K1 key, V1 value, OutputCollector<K2, V2> output,
        Reporter reporter) throws IOException { ... }

------------------------------------------------------------
MR Reducer
------------------------------------------------------------

* To be a reducer, implement the Reducer interface and inherit
  from the MapReduceBase class.

There are a number of default reducer implementations:

* IdentityReducer<K,V> -> Reducer<K,V,K,V> -> maps input to output
* LongSumReducer<K> -> Reducer<K, LongWritable, K, LongWritable> -> sum of keys

Interface for Redcuer<K2, V2, K3, V3>::

    void reduce(K2 key, Iterator<V2> values, OutputCollector<K3, V3> output,
        Reporter reporter) throws IOException { ... }

------------------------------------------------------------
MR Partitioner
------------------------------------------------------------

* This step is run between map and reduce stages to efficiently
  shuffle and distribute the data sets.
* By default hadoop uses the HashPartitioner to distribute work
  to the various reducers. This can be customized though by
  implementing the Partitioner<T, Writable> interface.

An example of partitioning the Edge class is as follows::

    public class EdgePartitioner implements Partitioner<Edge, Writable> {
        @Override
        public int getPartition(Edge key, Writable value, int numPartitions) {
            return key.sourceNode.hashCode() % numPartitions;
        }

        @Override
        public void configure(JobConf conf) {}
    }

------------------------------------------------------------
Processing
------------------------------------------------------------

* hadoop splits input data into chunks (input splits) to
  effectively process the data in parallel. The hadoop
  file processing and HDFS are designed around this.

* The type of input is specified by the InputFormat interface.
* The default implementation is the TextInputFormat, this uses
  the line of the file as the value and the byte offset of the
  line as the key.

There are a number of default implementations:

* TextInputFormat -> (byte offset, file line)
* KeyValueTextInputFormat -> key\tvalue -> (key, value)
* SequenceFileInputFormat<K,V> -> efficient key value format
  - usually used between mapreduce jobs
* NLineInputFormat -> TextInputFormat with exactly N lines

* When implementing your own InputFormat, inherit from the
  FileInputFormat to handle the file splitting details. Then
  you only have to return an implementation of RecordReader<K, V>
* Can overload to make specifically typed key-value records.

There are some RecordReaders already implemented for your (you can
usually use the existing ones and just perform your custom logic in
the next() method):

* LineRecordReader -> <LongWritable, Text>
* KeyValueLineRecordReader

Here is an example custom FileReader::

    public class TimeUrlTextInputFormat extends
        FileInputFormat<Text, URLWritable> {

        public RecordReader<Text, URLWritable> getRecordReader(
            InputSplit input, JobConf job, Reporter reporter) throws IOException {
            return new TimeUrlLineRecordReader(job, (FileSplit)input);
        }
    }

    public class URLWritable implements Writable {
        protected URL url;
        public URLWritable() {}
        public URLWritable(URL url) { this.url = url; }

        public void write(DataOutput out) throws IOException {
            out.writeUTR(url.toString());
        }

        public void readFields(DataInput in) throws IOException {
            url = new URL(in.readUTF());
        }

        public void set(String in) throws MalformedURLException {
            url = new URL(s);
        }
    }

    public class TimeUrlLineRecordReader implements RecordReader<Text, URLWritable> {
        private KeyValueLineRecordReader lineReader;
        private Text lineKey, lineValue;

        public TimeUrlLineRecordReader(JobConf job, FileSplit split) throws IOException {
            lineReader = new KeyValueLineRecordReader(job, split);
            lineKey = lineReader.createKey();
            lineValue = lineReader.createValue();
        }
        
        public boolean next(Text key, URLWritable value) throws IOException {
            if (!lineReader.next(lineKey, lineValue) {
                return false;
            }
            key.set(lineKey);
            value.set(lineValue.toString());

            return true;
        }

        public Text createKey() {
            return new Text("");
        }

        pubilc URLWritable createValue {
            return new URLWritable();
        }

        public long getPos() throws IOException {
            return lineReader.getPos();
        }

        public float getProgress() throws IOException {
            return linReader.getProgress();
        }

        public void close() throws IOException {
            lineReader.close();
        }
    }

------------------------------------------------------------
Output Format
------------------------------------------------------------

* Controls the final result output (usually to part-nnnnn that
  references the partition).
* specify by setting the setOutputFormat() on the JobConf object.

Can implement your own by inheriting from the FileOutputFormat
abstract class:

* TextOutputFormat<K,V>
* SequenceFileOutputFormat<K,V>
* NullOutputFormat<K,V>

============================================================
Part 4
============================================================

Can use the java interface or the scripting interface::

    $> bin/hadoop jar contrib/streaming/hadoop-streaming-1.0.1.jar
    	-input xae
    	-output stream-output
    	-mapper 'cut -f 2 -d,'
    	-reducer 'uniq'

    $> bin/hadoop jar contrib/streaming/hadoop-streaming-1.0.1.jar
    	-input xae
    	-output count-output
    	-mapper 'wc -l'
    	-D mapred.reduce.tasks=0

    $> bin/hadoop jar contrib/streaming/hadoop-streaming-1.0.1.jar
    	-input xae
    	-output count-output
    	-mapper 'RandomSample.py 10'
    	-D mapred.reduce.tasks=1    # uses identity reducer(sorts)
        #-mapper 'cat'                identity mapper

Can simplify statistics with the aggregate package.  Just need to
supply a mapper to convert to the following format `function:key\tvalue`.
The following functions are supplied:

* DoubleValueSum
* LongValueSum
* LongValueMin
* LongValueMax
* StringValueMax
* StringValueMin
* UniqValueCount
* ValueHistogram

Then just issue a command like::

    $> bin/hadoop jar contrib/streaming/hadoop-streaming-1.0.1.jar
    	-input xae
    	-output count-output
    	-mapper 'AttributeCount.py'
    	-file 'AttributeCount.py'
        -reducer aggregate

============================================================
Part 5 - Advanced Hadoop
============================================================

------------------------------------------------------------
Chaining MapReduce Jobs
------------------------------------------------------------

* Can manually create many Job objects and chain results
* Can do ChainMapper and ChainReducer to incrementally run
  small map/reduce jobs (record wise chain, not total job chain)

  - These use less I/O which is generally faster

* datajoin to perform joins at reduce step (repartitioned join,
  repartitioned sort-merge join).

  - each record is tagged with its data source (to preserve schema)
  - group key is added a the join key
  - combine stage determines what type of join to use (inner, outer)

* Implemented by implementing abstract classes:
 
  - DataJoinMapperBase
  - DataJoinReducerBase
  - TaggedMapOutput

* Can send a file to all nodes for efficiency (say a cache or a 
  result that may fit all in memory)

  - DistributedCache.addCacheFile()
  - DistributedCache.getLocalCacheFiles()
  - Set files in job configure
  - Load files in map/reduce configure method
  - Both methods defualt to using HDFS unless specified

------------------------------------------------------------
Semijoin
------------------------------------------------------------

============================================================
Cookbook / Recipies
============================================================

* passing job specific parameters to your tasks
  - the configuation is available to all the map/reduce tasks
  - using the tool interface allows easy definitions
* probing for task specific information
  - mapred.job.id
  - mapred.jar
  - job.local.dir
  - mapred.tip.id
  - mapred.task.id
  - mapred.task.is.map
  - mapred.task.partition
  - map.input.file
  - map.input.start
  - map.input.length
  - mapred.work.output.dir
  - the same can be performed from the streaming code::

    import os
    filename = os.environ["map_input_file"]
    localdir = os.environ["job_local_dir"]

* Partition into multiple output files (MultipleOutputFormat)::

    public static class PartitionByCountryMTOF
        extends MultipleTextOutputFormat<NullWritable,Text>
    {
        protected String generateFileNameForKeyValue(NullWritable key,
            Text value, String filename)
        {
            String[] arr = value.toString().split(",", -1);
            String country = arr[4].substring(1,3);
            return country + "/" + filename;
        }
    }

* More versitle class is MultipleOutputs
  - allows multiple output collectors
* Input/Output to database
  - DBInputFormat
  - DBOutputFormat, DBWritable interface
* Keep output in sorted order

============================================================
Managing Hadoop
============================================================

------------------------------------------------------------
Configuring Hadoop
------------------------------------------------------------

* dfs.name.dir - /home/hadoop/dfs/name
* dfs.data.dir - /home/hadoop/dfs/data
  - if you have multiple drives, specify comma seperated list
  - hadoop can use each drive in parallel
* mapred.local.dir - /hadoop/mapred/system
  - if you have multiple drives, specify comma seperated list
  - hadoop can use each drive in parallel
* hadoop.tmp.dir - /home/hadoop/tmp
* mapred.child.java.opts - -Xmx512m
* dfs.datanode.du.reserved - 1073741824
* mapred.tasktracker.map.tasks.maximum
  - 2 per core (minus 2 total for task tracker and data node)
* mapred.tasktracker.map.reduce.maximum
* mapred.reduce.tasks

------------------------------------------------------------
Monitoring Hadoop
------------------------------------------------------------

* bin/hadoop fsck /
* bin/hadoop dfsadmin -report
* bin/hadoop dfsadmin -metasave <logfile>
* bin/hadoop dfsadmin -refreshNodes (on removing a node)
* bin/start-balancer.sh (on adding a node)

* file permissions (basic, not really secure)
* file system quotas per user
* trash backup feature (accidental deletion revert)
  - fs.trash.interval - <time> or 0
* use Reporter.incCounter() (can make your own)
  - Reporter.incCounter(String group, String counter, long value)
  - Reporter.incCounter(Enum key, long value)
* for streaming
  - sys.stderr.write("reporter:counter:ClaimsCounter,Missing,1\n")
  - sys.stderr.write("reporter:status:<message>\n")
* enable record skipping
  - setMapperMaxSkipRecords
  - setMapperMaxSkipGroups
  - bin/hadoop fs -text <file>
* bin/hadoop org.apache.hadoop.mapred.IsolationRunner ../job.xml
  - export HADOOP_OPTS="-agentlib:jdwp=transport=dt_socket,server=y,address=8000"
  - jdb -attach 8000

============================================================
Best Practices
============================================================

------------------------------------------------------------
Increase Hadoop Performance
------------------------------------------------------------

* reduce network traffic with a combiner
* reduce the amount of input data
* compress data going over the wire
  - mapred.compress.map.output
  - mapred.map.output.compression.codec
  - DefaultCodec, GzipCodec, BZip2Codec
  - Use sequence files if you can (they support splitting)::

    conf.setOutputFormat(SequenceFileOutputFormat.class);
    SequenceFileOutputFormat.setOutputCompressionType(conf, CompressionType.BLOCK);
    FileOutputFormat.setCompressOutput(conf, true);
    FileOutputFormat.setOutputCompressorClass(conf, GzipCodec.class);

* mapred.job.reuse.jvm.num.tasks
* mapred.map.tasks.speculative.execution
* mapred.reduce.tasks.speculative.execution
* don't use streaming tasks (use hadoop jobs)

============================================================
Part Extra
============================================================

------------------------------------------------------------
Hadoop Cloud
------------------------------------------------------------

* amazon web service hadoop
* amazon web service s3
* amazon web service emr (elastic map reduce)

------------------------------------------------------------
Pig
------------------------------------------------------------

* unlike sql, pig is a data processing language used to 
  specify a series of data processing steps.
* All commands are lazy until a dump/store is requested
* Can run programs locally or through hadoop
* An example of a pig program::

	log  = LOAD 'excite-small.log' AS (user, time, query);
	# can also force schema => AS (user:chararray, time:long, query:chararray);
	grpd = GROUP log BY user;
	# can also use position => BY $0
	cntd = FOREACH grpd GENERATE group, COUNT(log);
	lmt  = limit cntd 10;
	DUMP lmt;

* if you specify schema, all unmatched lines are casted to null.
* Three way to run programs: 

  - grunt shell
  - pig scripts
  - embedded into java program

* There are a number of debugging commands::

	grunt> set debug on
	grunt> set job.name 'my job name'
	grunt> exec			# run in background
	grunt> run			# run in foreground
	grunt> dump alias;	# prints to screen
	grunt> store alias;	# stores to file
	# basic file manipulation commands
	ls, pwd, cd, cat, mkdir, rm, rmf, mv
	# to limit the number of results printed::
	grunt> lmt = limit alias 5;
	grunt> dump lmt;
	grunt> describe alias;		# view alias schema
	grunt> illustrate alias;	# describe alias process
	grunt> explain alias;		# produce AST

* The types of pig are the following:

  - int
  - long
  - float
  - double
  - chararray
  - bytearray
  - Tuple - an ordered set of fields (struct)
  - Bag - an unordered set of tuples (schema not required to be the same)
  - Map - key value pairs (keys are chararray)

* Index tuples by position or name
* Index bags by `.`, `log.query`
* Index maps by `#`, `key#value`
* Pig supports basic arithmetic and logic operators
* Pig supports a number of basic built in functions
* The following relational operators are supported::

	grunt> c = union a, b;	# join two sets
	grunt> split c into d if $0 == 0, e if $0 == 1;
	grunt> distinct c
	grunt> f = filter c by $1 > 3;
	grunt> h = group log by DayOfWeek(time);	# can group by function
	grunt> d = group log by all;				# one big group map
	grunt> j = cogroup a by $2, b by $2;		# outer join
	grunt> j = cogroup a by $2, b by $2 inner;	# inner join, ignore missing matches

------------------------------------------------------------
Pig User Defined Functions (UDF)
------------------------------------------------------------

* many already defined: https://cwiki.apache.org/confluence/display/PIG/PiggyBank
* two kinds: eval and load/store
* example usage::

	register piggybank/java/piggybank.jar;
	define Upper org.apache.pig.piggybank.evaluation.string.UPPER();
	b = foreach a generate Upper($0);

* custom eval example (minus the outputSchema and getArgToFuncMapping)::

	public class UPPER extends EvalFunc<String>
	{
		public String exec(Tuple input) throws IOException {
			if (input == null || input.size() == 0)
				return null;
			try {
				String str = (String)input.get(0);
				return str.toUpperCase();
			} catch(Exception e){
				System.err.println("Failed to process input; error - " + e.getMessage());
				return null;
			}
		}
	}

* can parameterize the script as follows::

	/*
	 * @file script.pig
	 * run this script with the following command:
	 * pig -param input=file.log -param size=4 script.pig
	 * pig -param_file parameters script.pig
	 * debug with -dryrun and -debug
	 */
	log = load '$input' as (user, time, query);
	lmt = limit log $size
	dump lmt;

------------------------------------------------------------
Hive
------------------------------------------------------------

* data warehousing package on top of hadoop
* query with a sql like language (hiveql)
* works on structured data and adds an additional metadata layer
* metadata needs to be persisted into a relational database
  - by default uses derby, but can use and jdbc database
* can query with web gui, jdbc, or cli
* can use hdfs data, or can manage data for you and add optimizations

============================================================
To Research
============================================================

* jets3t - java s3 library
* itext - work with pdfs in java
