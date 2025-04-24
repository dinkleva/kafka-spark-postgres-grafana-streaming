from pyspark.sql import DataFrame
from pyspark.sql.functions import regexp_extract, regexp_replace, col, trim, when

def clean_data(df):
    cleaned_df = df

    # Clean ₹ and commas from price fields
    cleaned_df = cleaned_df.withColumn(
        "discounted_price",
        regexp_replace(col("discounted_price"), r"[₹,]", "").cast("double")
    ).withColumn(
        "actual_price",
        regexp_replace(col("actual_price"), r"[₹,]", "").cast("double")
    )

    # Clean '%' sign and cast to double for discount percentage
    cleaned_df = cleaned_df.withColumn(
        "discount_percentage",
        regexp_replace(col("discount_percentage"), r"%", "").cast("double")
    )

    # Clean rating string like "4.5 out of 5" -> just extract the float part
    cleaned_df = cleaned_df.withColumn(
        "rating",
         when(col("rating") == "No rating", 0.0)
        .otherwise(regexp_extract(col("rating"), r"(\d+(\.\d+)?)", 1).cast("double"))
    )

    # Clean rating_count: remove commas, cast to integer
    cleaned_df = cleaned_df.withColumn(
        "rating_count",
        regexp_replace(col("rating_count"), ",", "").cast("int")
    )

    return cleaned_df
