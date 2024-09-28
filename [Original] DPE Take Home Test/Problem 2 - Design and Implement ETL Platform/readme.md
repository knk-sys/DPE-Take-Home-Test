# ETL Design
![alt text](<ETL Design.png>)

## Amazon S3 (Input Data Source):
This is the starting point where the raw data is stored.
The dataset "High Volume For-Hire Vehicle Trip Records" is uploaded to an S3 bucket, serving as the input source for the ETL pipelines.


## AWS Glue Crawlers
Crawlers are used to scan the data stored in S3 and automatically create metadata tables in the AWS Glue Data Catalog.
The crawlers will infer the schema (columns, types) of the raw data stored in S3, which allows it to be processed by the ETL jobs.


## AWS Glue Jobs (ETL Processing)
There are two Glue jobs (ETL processes) shown in the design, each with its specific transformation logic:
#### ETL Job 1 (Top Box)
Extracts data from S3, transforms it (for example, calculating daily total transactions), and then loads the results into Amazon RDS.

#### ETL Job 2 (Bottom Box)
Similar to the first job, it extracts data from S3, performs a different transformation (such as calculating the top 5 TLC Taxi Zones), and loads the results into Amazon RDS.


## Amazon RDS (Target Storage for Processed Data)
The output from the Glue jobs, after transformation, is loaded into an Amazon RDS instance.
Two tables are stored in RDS:
1. daily_transaction for daily transaction totals.
2. daily_topfive_taxi_zone for the top 5 taxi zones based on the trip data.

## Amazon CloudWatch
CloudWatch can be used to schedule and monitor the AWS Glue jobs.
AWS Glue jobs can be triggered as cron jobs for regular data pipeline execution and error tracking.



# Preparation
## Setup AWS S3:
Create an S3 bucket.
Upload the dataset fhvhv_tripdata_2022_to_2023 to an appropriate folder in S3.
s3 path: s3://my-glue-etl-dataset/fhvhv_tripdata_2022_to_2023-001/


## Create a Relational Database in RDS:
I will use a MySQL instance in AWS RDS.
Configure security groups to allow access from Glue. (IAM roles)
Note database’s connection details (endpoint, port, username, and password).

## AWS Glue ETL Pipelines
## Step 1: Setup AWS Glue Crawler to Catalog Data
### Create a Glue Database:
 Navigate to AWS Glue.
 Click on Databases under the Data Catalog section.
 Click on Add Database, and name it to fhvhv_tripdata_db.

### Create a Crawler:
 Go to Crawlers in AWS Glue.
 Click on Add Crawler:
 Data Source: Choose the S3 bucket where dataset is located. s3://my-glue-etl-dataset/fhvhv_tripdata_2022_to_2023-001/
 IAM Role: Ensure role has proper permissions for S3 and Glue. (AmazonRDSDataFullAccess, AmazonS3FullAccess, AWSGlueServiceRole, CloudWatchLogsFullAccess)
 Schedule: set a schedule (e.g., daily) or leave it for manual runs.
 Target: Choose the database created earlier. 
 Run the Crawler to create the table metadata in Glue Catalog.

 
## Step 2: Create AWS Glue Jobs for the Data Pipelines
### Pipeline 1: Daily Total Transactions Calculation
Create a Glue Job:
Navigate to Jobs in AWS Glue.
Click on Add Job and configure:
Name: naming to the jobs daily_total_transactions_job.
IAM Role: Select a role with permissions for Glue, S3, and RDS.
Script: Select the option to write your own script.
Source: Select the table created by your Glue Crawler (fhvhv_tripdata).
Output: Set S3 as your temporary storage.
Script for Pipeline:
Ref to daily_tran.py

### Pipeline 2: Top 5 Taxi Zones Calculation
Create a Second Glue Job:
Navigate to Jobs and add another job, e.g., top5_taxi_zones_job.
Select the same IAM Role and set S3 as temporary storage.
Script for Pipeline:
Ref to top_5_taxi.py

## Step 3: Schedule Jobs Using AWS Glue Triggers
Create Triggers:
Navigate to Triggers in AWS Glue.
Add a new Trigger for each pipeline:
Trigger 1: Schedule daily to run the daily_total_transactions_job.
Trigger 2: Schedule daily to run the top5_taxi_zones_job.
Configure Trigger Settings:
Set the frequency (e.g., every 24 hours at a specific time).
Add dependencies if needed.
Testing and Monitoring
Run the Jobs:
Test both Glue jobs manually to ensure they complete without errors.
Check the results in RDS tables: daily_transaction and daily_topfive_taxi_zone.

## Set Up CloudWatch Monitoring:
Use AWS CloudWatch to monitor Glue job logs and set up alarms for job failures.

## Query the result 
SELECT * FROM daily_transaction ORDER BY calculated_at DESC LIMIT 100;
SELECT * FROM daily_topfive_taxi_zone ORDER BY calculated_at DESC LIMIT 100;


The following steps are for reference purposes only, as I could not perform them on AWS due to insufficient balance to run services such as RDS, Glue, and Crawlers. This cost includes setting up the relational database in RDS, running the Glue jobs, and storing data in S3. 