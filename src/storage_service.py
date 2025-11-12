import boto3
import pandas as pd
import os
from dotenv import load_dotenv
from io import StringIO
from logger import get_logger

logger = get_logger()

load_dotenv()

def get_s3_client():

    profile = os.getenv("AWS_PROFILE")
    session = boto3.Session(profile_name=profile)
    s3 = session.client('s3')
    return s3

def get_customer_data():

    bucket = os.getenv("S3_BUCKET_NAME")
    folder = os.getenv("S3_FOLDER_PREFIX")

    logger.info("Extracting customer data from S3...")

    s3 = get_s3_client()
    s3_key = f"{folder}/raw/customers/project_1_customers.csv"

    logger.info(f"Reading data from s3://{bucket}/{s3_key}")

    response = s3.get_object(Bucket=bucket, Key=s3_key)
    csv_content = response['Body'].read().decode('utf-8')

    customers_df = pd.read_csv(StringIO(csv_content))

    logger.info(f"Loaded {len(customers_df)} customer records")
    logger.info(f"Columns: {customers_df.columns.tolist()}")
    logger.info(f"First 5 rows:\n{customers_df.head()}")
    logger.info(f"Missing values:\n{customers_df.isnull().sum()}")
    
    return customers_df

if __name__ == "__main__":

    customers_df = get_customer_data()