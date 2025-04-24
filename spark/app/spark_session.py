from pyspark.sql import SparkSession

def create_spark_session():
    return SparkSession.builder \
        .appName("KafkaSparkStreaming") \
        .master("spark://spark-master:7077") \
        .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
        .getOrCreate()
