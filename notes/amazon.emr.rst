================================================================================
Amazon EMR Framework
================================================================================

--------------------------------------------------------------------------------
Accessing Hadoop Resources
--------------------------------------------------------------------------------

* *ResourceManager*  : lynx http://ip-172-31-8-102.ec2.internal:9026
* *NameNode*         : lynx http://ip-172-31-8-102.ec2.internal:9101
* *Spark Jobs*       : lynx http://ip-172-31-8-102.ec2.internal:4040
* *Spark History*    : lynx http://ip-172-31-8-102.ec2.internal:18080

--------------------------------------------------------------------------------
Creating Spark Applications
--------------------------------------------------------------------------------

What follows is a simple example of a scala spark application on EMR. Here is
a runner that will grab and run `sbt` used to build scala projects:

.. code-block:: bash

    #!/bin/bash
    
    root=$(
      cd $(dirname $(readlink $0 || echo $0))/..
      /bin/pwd
    )
    
    sbtjar=sbt-launch.jar
    
    if [ ! -f $sbtjar ]; then
      echo 'downloading '$sbtjar 1>&2
      curl -O http://typesafe.artifactoryonline.com/typesafe/ivy-releases/org.scala-sbt/sbt-launch/0.12.1/$sbtjar
    fi
    
    test -f $sbtjar || exit 1
    test -f ~/.sbtconfig && . ~/.sbtconfig
    java -jar $sbtjar "$@"

Here is a simple `scala` build file that can build a scala project:

.. code-block:: sbt

    name := "Simple Project"
    
    version := "1.0"
    
    scalaVersion := "2.10.4"
    
    libraryDependencies += "org.apache.spark" %% "spark-core" % "1.3.1"

Here is a simple scala project that performs a word count:

.. code-block:: scala

    import org.apache.spark.SparkContext
    import org.apache.spark.SparkContext._
    import org.apache.spark.SparkConf
    
    object SimpleApp {
      def main(args: Array[String]) {
        val logFile = "/home/hadoop/spark/README.md"
        val conf = new SparkConf().setAppName("Simple Application")
        val sc = new SparkContext(conf)
        val logData = sc.textFile(logFile, 2).cache()
        val numAs = logData.filter(line => line.contains("a")).count()
        val numBs = logData.filter(line => line.contains("b")).count()
        println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
      }
    }

--------------------------------------------------------------------------------
Creating Spark Cluster
--------------------------------------------------------------------------------

To create a new spark cluster and have all the relevant dependencies installed,
simply run the following command (assuming that you have previously setup the
following dependencies):

.. code-block:: bash

    aws emr create-cluster \
      --name SparkCluster --ami-version 3.6.0 \
      --instance-type m3.xlarge --instance-count 3 \
      --ec2-attributes KeyName=aws-spark,InstanceProfile=EMR-EC2-DefaultRole \
      --bootstrap-actions Path=s3://support.elasticmapreduce/spark/install-spark \
      --service-role EMR-DefaultRole

To get information about the currently running cluster, simply use the `aws`
shell command to query about its state:

.. code-block:: bash

    aws emr list-clusters
    aws emr list-clusters --active
    aws emr describe-cluster --cluster-id ${cluster-id}
    aws emr list-steps --cluster-id ${cluster-id}
    aws emr describe-step --cluster-id ${cluster-id} --step-id ${step-id}

To connect to the cluster and open a spark shell to operate in, run the
following command. Note that `spark-shell` can be replaced with `pyspark`
or any other shell that you would like to connect to:

.. code-block:: bash

    aws emr ssh --key-pair-file ~/.ssh/aws-spark.pem \
      --command "MASTER=yarn-client /home/hadoop/spark/bin/spark-shell" \
      --cluster-id j-XXXXXXXXXXX

To terminate the cluster and shutdown the resources, simply run the following
with the cluster identifier that you obtained earlier:

.. code-block:: bash

    aws emr terminate-clusters --cluster-id ${1}

--------------------------------------------------------------------------------
Running Custom Spark Jobs
--------------------------------------------------------------------------------

To run a custom application on the spark cluster, do the following:

.. code-block:: bash

    sbt compile && sbt package  # produces target/scala-2.10/yourapp_2.10-1.0.0.jar
    aws emr describe-cluster --cluster-id ${cluster-id} # get the MasterPublicDnsName

    scp -i ~/.ssh/aws-spark.pem \
      target/scala-2.10/yourapp_2.10-1.0.0.jar \
      hadoop@ec2-xxx-xxx-xxx-xxx.region.compute.amazonaws.com:/home/hadoop/share/hadoop/common/lib/

    # submit the job to the cluster
    MASTER=yarn-client /home/hadoop/spark/bin/spark-submit \
      --class com.amazon.YourApp /home/hadoop/share/hadoop/common/lib/yourapp_2.10-1.0.0.jar
      <app arguments>

To test the application out locally (usually before you load it on the cluster),
do the following:

.. code-block:: bash

    sbt assembly # produces target/scala-2.10/YourApp-assembly-1.0.0.jar

    java -Dspark.master=local \
      -classpath target/scala-2.10/YourApp-assembly-1.0.0.jar \
      com.amazon.YourApp <app arguments>

--------------------------------------------------------------------------------
Ipython Notebooks
--------------------------------------------------------------------------------

To work with `ipython` notebooks, do the following from the remote machine:

.. code-block:: bash

    ssh -i ~/.ssh/aws-spark.pem -N -D 9999 hadoop@ec2-52-6-2-65.compute-1.amazonaws.com

--------------------------------------------------------------------------------
Example Hadoop Runs
--------------------------------------------------------------------------------

What follows is an example of running a spark shell job:

.. code-block:: scala

    // start with MASTER=yarn-client /home/hadoop/spark/bin/spark-shell
    val file = sc.textFile("s3://support.elasticmapreduce/bigdatademo/sample/wiki")
    val reducedList = file.map(l => l.split(" ")).map(l => (l(1), l(2).toInt)).reduceByKey(_+_, 3)
    reducedList.cache
    val sortedList = reducedList.map(x => (x._2, x._1)).sortByKey(false).take(50)

What follows is an exmample of a hadoop `hive` job:

.. code-block:: sql

    // start with MASTER=yarn-client /home/hadoop/spark/bin/spark-sql --executor-memory 4G
    SET spark.sql.shuffle.partitions=10;
    create external table wikistat
      (projectcode string, pagename string, pageviews int, pagesize int) ROW FORMAT DELIMITED FIELDS TERMINATED BY ' '
      location 's3://support.elasticmapreduce/bigdatademo/sample/wiki';
    CACHE TABLE wikistat;
    select pagename, sum(pageviews) c from wikistat group by pagename order by c desc limit 10;
