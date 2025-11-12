import pymssql
import pandas as pd
import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger()

load_dotenv()


def get_purchases_data():
    """
    Extract purchases data from Azure SQL Server
    
    Returns:
        DataFrame: Purchases data
    """
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    
    logger.info("Extracting purchases data from Azure SQL Server...")
    logger.info(f"Server: {server}")
    logger.info(f"Database: {database}")
    
    # Connect to Azure SQL
    conn = pymssql.connect(
        server=server,
        user=username,
        password=password,
        database=database
    )
    
    # Query the purchases table
    query = "SELECT * FROM purchases"
    logger.info(f"Running query: {query}")
    
    # Read into DataFrame
    df = pd.read_sql(query, conn)
    
    # Close connection
    conn.close()
    
    logger.info(f"Loaded {len(df)} purchase records")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"First 5 rows:\n{df.head()}")
    logger.info(f"Missing values:\n{df.isnull().sum()}")
    
    return df


if __name__ == "__main__":
    purchases_df = get_purchases_data()