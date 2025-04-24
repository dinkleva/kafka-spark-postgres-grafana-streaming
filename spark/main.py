import yaml
from pyspark.sql.functions import col, from_json
from app.spark_session import create_spark_session
from app.schema import schema
from app.cleaner import clean_data
from app.writer import write_to_postgres

with open("config/spark-config.yml", "r") as f:
    config = yaml.safe_load(f)

spark = create_spark_session()

kafka_config = config["kafka"]
postgres_config = config["postgres"]

raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_config["servers"]) \
    .option("subscribe", kafka_config["topic"]) \
    .option("startingOffsets", kafka_config["startingOffsets"]) \
    .load()

#debugging
# raw_df.selectExpr("CAST(value AS STRING)").show(truncate=False)

json_df = raw_df.selectExpr("CAST(value AS STRING) as json_string") \
                .withColumn("data", from_json(col("json_string"), schema)) \
                .select("data.*")

# json_df = json_df.drop("key")
clean_df = clean_data(json_df)

# clean_df.writeStream\
#         .format("console")\
#         .outputMode("append")\
#         .start()

clean_df.writeStream \
    .foreachBatch(lambda df, epoch_id: write_to_postgres(df, epoch_id, postgres_config)) \
    .start() \
    .awaitTermination()
