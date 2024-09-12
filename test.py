from pyspark.sql.functions import regexp_extract, col, when, current_timestamp, unix_timestamp

# Define the regular expressions to extract threatId and threatType
threatId_pattern = '"threatId":"([A-Za-z0-9]+)"'
threatType_pattern = '"threatType":"([A-Za-z0-9]+)"'

# Extract the threatId and threatType using regex
df_with_threats = df.withColumn("threatId", regexp_extract(col("event_details"), threatId_pattern, 1)) \
                    .withColumn("threatType", regexp_extract(col("event_details"), threatType_pattern, 1))

# Filter rows where threatType is "url" and the timestamp is less than a day old
df_filtered = df_with_threats.withColumn("threatId", when(
    (col("threatType") == "url") & 
    (unix_timestamp(current_timestamp()) - unix_timestamp(col("timestamp")) <= 86400),  # 86400 seconds = 1 day
    col("threatId")
))

# Filter out rows where threatId is null
df_filtered = df_filtered.filter(col("threatId").isNotNull())

# Show only the threatId
df_filtered.select("threatId").show()