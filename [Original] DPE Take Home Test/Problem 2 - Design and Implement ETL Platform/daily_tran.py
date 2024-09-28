import sys
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.sql.functions import col, count

# Create GlueContext and Spark session
spark = SparkSession.builder.appName('daily_total_transactions').getOrCreate()
glueContext = GlueContext(spark.sparkContext)

# Load data from Glue catalog
datasource = glueContext.create_dynamic_frame.from_catalog(database="fhvhv_tripdata_db", table_name="fhvhv_tripdata")

# Convert to Spark DataFrame
df = datasource.toDF()

# Filter data for the previous day
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
filtered_df = df.filter(df['pickup_date'] == yesterday)

# Calculate total transactions
total_transactions = filtered_df.count()

# Save result back to relational database (e.g., MySQL or PostgreSQL)
result_df = spark.createDataFrame([(yesterday, total_transactions, datetime.now())], ["transaction_date", "total_transactions", "calculated_at"])

result_df.write \
    .format("jdbc") \
    .option("url", "jdbc:mysql://your-db-endpoint:3306/yourdbname") \
    .option("dbtable", "daily_transaction") \
    .option("user", "username") \
    .option("password", "password") \
    .save()
