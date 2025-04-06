from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from pyspark.sql.functions import from_json
# Define Schema Based on the Data Format in Kafka
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_name", StringType(), True),
    StructField("category", StringType(), True),
    StructField("discounted_price", StringType(), True),
    StructField("actual_price", StringType(), True),
    StructField("discount_percentage", StringType(), True),
    StructField("rating", DoubleType(), True),
    StructField("rating_count", IntegerType(), True),
    StructField("about_product", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("user_name", StringType(), True),
    StructField("review_id", StringType(), True),
    StructField("review_title", StringType(), True),
    StructField("review_content", StringType(), True),
    StructField("img_link", StringType(), True),
    StructField("product_link", StringType(), True)
])

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .master("spark://spark-master:7077") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0") \
    .getOrCreate()

# Read stream from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "amazon_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert Kafka message to string
# df_transformed = df.selectExpr("CAST(value AS STRING) as message")

# # Print messages to console
# # query = df_transformed.writeStream \
# #     .outputMode("append") \
# #     .format("console") \
# #     .start()

# # query.awaitTermination()

df_transformed = df.selectExpr("CAST(value AS STRING) as json_string") \
    .withColumn("data", from_json(col("json_string"), schema)) \
    .select("data.*")  # Extract fields

# Print messages to console for debugging
df_transformed.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

df = df_transformed.drop("key")



# Write Stream to PostgreSQL
def write_to_postgres(df, epoch_id):
    df.write \
      .format("jdbc") \
      .option("url", "jdbc:postgresql://postgres:5432/kafka_streaming") \
      .option("dbtable", "amazon_products") \
      .option("user", "postgres") \
      .option("password", "postpass") \
      .option("driver", "org.postgresql.Driver") \
      .mode("append") \
      .save()

df.writeStream \
    .foreachBatch(write_to_postgres) \
    .start() \
    .awaitTermination()
