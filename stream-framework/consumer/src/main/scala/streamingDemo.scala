package com.datastax.demo

import java.sql.Timestamp
import java.text.SimpleDateFormat

import com.datastax.spark.connector._
import com.datastax.spark.connector.writer.{TTLOption, WriteConf}
import com.datastax.driver.core.{Session, Cluster, Host, Metadata}

import scala.collection.JavaConversions._
import kafka.serializer.StringDecoder
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{SQLContext, SaveMode}
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Milliseconds, Seconds, StreamingContext, Time}
import org.apache.spark.{SparkConf, SparkContext}

case class UserStats(user: String, ts: String, arg1: Int, arg2: Int, arg3: Int)

object SparkKafkaConsumer extends App {

  val appName = "test"
  val topicName = "test"
  val cassandra_host = "10.255.0.120"

  val conf = new SparkConf().setAppName(appName)
  val sc = SparkContext.getOrCreate(conf)

  val sqlContext = SQLContext.getOrCreate(sc)
  import sqlContext.implicits._


    val cluster = Cluster.builder().addContactPoint(cassandra_host).build()
    val session = cluster.connect()
    session.execute("DROP KEYSPACE IF EXISTS demo")
    session.execute("CREATE KEYSPACE demo WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 1 }")
    session.execute(
      """CREATE TABLE demo.user_stats (
        |user TEXT,
        |ts TEXT,
        |arg1 INT,
        |arg2 INT,
        |arg3 INT,
        |PRIMARY KEY (user,ts)
        )""".stripMargin)
    session.close()

  val ssc = new StreamingContext(sc, Milliseconds(10000))
  ssc.checkpoint(appName)

  //val kafkaTopics = Set[String] (topicName)
  val kafkaTopics = Set(topicName)
  val kafkaParams = Map[String, String]("metadata.broker.list" -> "kafka:9092", "auto.offset.reset" -> "smallest" )

  val kafkaStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, kafkaTopics)

  // kafkaStream.print
  kafkaStream
    .foreachRDD {
      (message: RDD[(String, String)], batchTime: Time) => {
        val df = message.map {
          case (k, v) => v.split(",")
        }.map(payload => {
          val ts = System.currentTimeMillis().toString
          UserStats(payload(0), ts,  payload(1).toInt, payload(2).toInt, payload(3).toInt)
        }).toDF("user", "ts", "arg1", "arg2","arg3")
        df
          .write
          .format("org.apache.spark.sql.cassandra")
          .mode(SaveMode.Append)
          .options(Map("keyspace" -> "demo", "table" -> "user_stats"))
          .save()
      }
    }

  //val json = sc.parallelize(Seq(kafkaStream)) //.saveToCassandra("demo", "user_stats")
  //json.foreach { x => print(x) }

  //sqlContext.jsonRDD(json).map(MonthlyCommits(_)).saveToCassandra("githubstats","monthly_commits")

  ssc.start()
  ssc.awaitTermination()

}
