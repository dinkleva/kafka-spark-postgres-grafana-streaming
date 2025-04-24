def write_to_postgres(df, epoch_id, db_config):
    print(f"🔄 Writing to PostgreSQL at epoch {epoch_id}")
    print("🧪 Config:", db_config)
    if df.rdd.isEmpty():
        print(f"⚠️  Epoch {epoch_id}: Cleaned DataFrame is empty, skipping write.")
        return

    df.printSchema()
    df.show(truncate=False)
    try:
        df.write \
            .format("jdbc") \
            .option("url", db_config["url"]) \
            .option("dbtable", db_config["table"]) \
            .option("user", db_config["user"]) \
            .option("password", db_config["password"]) \
            .option("driver", "org.postgresql.Driver") \
            .mode("append") \
            .save()
    except Exception as e:
        print("Error writing to Postgres:", str(e))
