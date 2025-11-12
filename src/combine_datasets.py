import pandas as pd
from logger import get_logger
from storage_service import get_customer_data
from requests_service import get_vehicle_data
from database_service import get_purchases_data

logger = get_logger()


def transform_and_combine():
    """
    Transform and combine all datasets
    
    Returns:
        DataFrame: Combined dataset
    """
    logger.info("Starting data transformation and combination...")
    
    # Extract all data
    logger.info("Extracting customers...")
    customers_df = get_customer_data()
    
    logger.info("Extracting vehicles...")
    vehicles_df = get_vehicle_data()
    
    logger.info("Extracting purchases...")
    purchases_df = get_purchases_data()
    
    # Combine datasets
    logger.info("Combining datasets...")
    
    # Drop vehicle_id from customers (we'll use the one from purchases)
    customers_clean = customers_df.drop(columns=['vehicle_id'])
    
    # Join purchases with customers (on customer_id)
    combined_df = purchases_df.merge(
        customers_clean, 
        on='customer_id', 
        how='left'
    )
    logger.info(f"After joining purchases + customers: {len(combined_df)} records")
    
    # Join with vehicles (on vehicle_id)
    combined_df = combined_df.merge(
        vehicles_df, 
        left_on='vehicle_id', 
        right_on='id', 
        how='left'
    )
    logger.info(f"After joining with vehicles: {len(combined_df)} records")
    
    # Show results
    logger.info(f"Final combined dataset: {len(combined_df)} records")
    logger.info(f"Columns: {combined_df.columns.tolist()}")
    logger.info(f"First 5 rows:\n{combined_df.head()}")
    
    return combined_df


if __name__ == "__main__":
    
    final_df = transform_and_combine()