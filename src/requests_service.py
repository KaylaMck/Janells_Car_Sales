import requests
import pandas as pd
import os
from dotenv import load_dotenv
from logger import get_logger

logger = get_logger()

load_dotenv()

def get_vehicle_data():
    
    api_url = os.getenv("API_BASE_URL")
    
    logger.info("Extracting vehicle data from API...")
    logger.info(f"API URL: {api_url}")
    
    # Start with page 1
    page = 1
    page_size = 100  # Get 100 records at a time
    all_vehicles = []
    
    while True:
        # Make API request
        params = {
            "page": page,
            "page_size": page_size
        }
        
        logger.info(f"Fetching page {page}...")
        response = requests.get(api_url, params=params)
        
        if response.status_code != 200:
            logger.error(f"API request failed: {response.status_code}")
            break
        
        data = response.json()
        vehicles = data.get("vehicles", [])
        
        # Add vehicles to our list
        all_vehicles.extend(vehicles)
        
        logger.info(f"Got {len(vehicles)} vehicles from page {page}")
        
        # Check if we got all the data
        total = data.get("total", 0)
        if len(all_vehicles) >= total:
            logger.info(f"Reached total of {total} vehicles")
            break
        
        page += 1
    
    # Convert to DataFrame
    df = pd.DataFrame(all_vehicles)
    
    logger.info(f"Loaded {len(df)} vehicle records")
    logger.info(f"Columns: {df.columns.tolist()}")
    logger.info(f"First 5 rows:\n{df.head()}")
    
    return df

if __name__ == "__main__":
    vehicles_df = get_vehicle_data()
