from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count
from datetime import datetime, timedelta

# Create Spark session
spark = SparkSession.builder.appName('top5_taxi_zones').getOrCreate()

# Load data from Glue catalog
datasource = glueContext.create_dynamic_frame.from_catalog(database="fhvhv_tripdata_db", table_name="fhvhv_tripdata")

# Convert to Spark DataFrame
df = datasource.toDF()

# Filter data up to the previous day
today = datetime.now().strftime('%Y-%m-%d')
filtered_df = df.filter(df['pickup_date'] < today)

# Group by taxi zone and calculate counts
zone_counts = filtered_df.groupBy("taxi_zone_id").count()

# Get top 5 taxi zones
top_5_zones = zone_counts.orderBy(col("count").desc()).limit(5)

# Save result back to relational database
top_5_zones.withColumn("calculated_at", datetime.now()).write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://your-db-endpoint:3306/yourdbname") \
    .option("dbtable", "daily_topfive_taxi_zone") \
    .option("user", "username") \
    .option("password", "password") \
    .save()
