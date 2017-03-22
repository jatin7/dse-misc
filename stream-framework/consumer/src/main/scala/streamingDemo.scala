package com.datastax.demo
/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements.  See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License.  You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/**
 * Created by carybourgeois on 10/30/15.
  *  Modified by jasonhaugland on 10/20/16.
 */

import java.sql.Timestamp
import java.text.SimpleDateFormat

import com.datastax.spark.connector._
import com.datastax.spark.connector.writer.{TTLOption, WriteConf}
import kafka.serializer.StringDecoder
import org.apache.spark.rdd.RDD
import org.apache.spark.sql.{SQLContext, SaveMode}
import org.apache.spark.streaming.kafka.KafkaUtils
import org.apache.spark.streaming.{Milliseconds, Seconds, StreamingContext, Time}
import org.apache.spark.{SparkConf, SparkContext}

object SparkKafkaConsumer extends App {

  val appName = "test"
  val topicName = "test"

  val conf = new SparkConf().setAppName(appName)
  val sc = SparkContext.getOrCreate(conf)

  val sqlContext = SQLContext.getOrCreate(sc)
  import sqlContext.implicits._

  val ssc = new StreamingContext(sc, Milliseconds(10000))
  ssc.checkpoint(appName)

  //val kafkaTopics = Set[String] (topicName)
  val kafkaTopics = Set(topicName)
  val kafkaParams = Map[String, String]("metadata.broker.list" -> "kafka:9092", "auto.offset.reset" -> "smallest" )

  val kafkaStream = KafkaUtils.createDirectStream[String, String, StringDecoder, StringDecoder](ssc, kafkaParams, kafkaTopics)

  kafkaStream.print

  ssc.start()
  ssc.awaitTermination()

}
