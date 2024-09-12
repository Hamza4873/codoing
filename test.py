from pyspark.sql import functions as F
from pyspark.sql import SparkSession
from datetime import datetime, timedelta

# Initialize Spark session
spark = SparkSession.builder.getOrCreate()

# Example DataFrame with a timestamp column
data = [
    ("2024-09-11 10:00:00",),
    ("2024-09-12 08:00:00",),
    ("2024-09-12 14:00:00",),
    ("2024-09-10 15:00:00",),
]
df = spark.createDataFrame(data, ["timestamp"]).withColumn("timestamp", F.col("timestamp").cast("timestamp"))

# Get the current timestamp and 24 hours before
current_time = datetime.now()
start_time = current_time - timedelta(hours=24)

# Directly using .filter to filter the DataFrame
filtered_df = df.filter((F.col("timestamp") >= F.lit(start_time)) & (F.col("timestamp") <= F.lit(current_time)))

# Show the filtered DataFrame
filtered_df.show(truncate=False)