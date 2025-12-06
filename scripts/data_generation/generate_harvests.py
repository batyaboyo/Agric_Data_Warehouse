"""
Generate Harvests Data
Creates synthetic harvest records linked to farmers and products
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(43) # Different seed
np.random.seed(43)
random.seed(43)

QUALITY_GRADES = ['A', 'B', 'C']
STORAGE_METHODS = ['Silo', 'Warehouse', 'Traditional Granary', 'Hermetic Bags', 'Open Air']
SEASONS = ['2023-A', '2023-B', '2024-A']

def generate_harvests(farmers_df, products_df, output_dir="../../data"):
    """
    Generate synthetic harvest data
    
    Args:
        farmers_df: DataFrame of farmers
        products_df: DataFrame of products
        output_dir: Output directory
    """
    print(f"Generating harvest records for {len(farmers_df)} farmers...")
    
    if farmers_df is None or products_df is None:
        print("Error: farmers_df and products_df are required")
        return pd.DataFrame()

    harvests = []
    
    # Pre-process product info for quick lookup
    product_map = products_df.set_index('product_name')['product_id'].to_dict()
    product_details = products_df.set_index('product_id')[['avg_growing_days', 'season']].to_dict('index')

    count = 0
    for _, farmer in farmers_df.iterrows():
        # Each farmer has 1-3 harvests
        num_harvests = random.randint(1, 3)
        
        farmer_id = farmer['farmer_id']
        primary_crop = farmer['primary_crop']
        
        # Get product ID for their primary crop
        # If primary crop not in products list, pick a random product
        if primary_crop in product_map:
            product_id = product_map[primary_crop]
        else:
            product_id = random.choice(list(product_map.values()))
            
        growing_days = product_details[product_id]['avg_growing_days'] or 90
        
        for _ in range(num_harvests):
            count += 1
            harvest_id = f"HRV{str(count).zfill(7)}"
            
            # Dates
            harvest_date_obj = datetime.now() - timedelta(days=random.randint(10, 365))
            planting_date_obj = harvest_date_obj - timedelta(days=growing_days + random.randint(-10, 10))
            
            planting_date = planting_date_obj.strftime('%Y-%m-%d')
            harvest_date = harvest_date_obj.strftime('%Y-%m-%d')
            
            # Quantity based on farm size (approx 500-2000kg per acre)
            farm_size = float(farmer['farm_size_acres'])
            yield_per_acre = random.uniform(500, 2000)
            quantity_kg = round(farm_size * yield_per_acre * random.uniform(0.5, 1.0), 2)
            
            quality = random.choices(QUALITY_GRADES, weights=[0.4, 0.4, 0.2])[0]
            
            # Post harvest loss (5-30%)
            loss_pct = round(random.uniform(5.0, 30.0), 2)
            
            season = random.choice(SEASONS)
            storage = random.choice(STORAGE_METHODS)
            
            harvest = {
                'harvest_id': harvest_id,
                'farmer_id': farmer_id,
                'product_id': product_id,
                'planting_date': planting_date,
                'harvest_date': harvest_date,
                'quantity_kg': quantity_kg,
                'quality_assessment': quality,
                'post_harvest_loss_pct': loss_pct,
                'storage_method': storage,
                'season': season,
                'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            harvests.append(harvest)
            
    harvests_df = pd.DataFrame(harvests)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_path = f"{output_dir}/harvests.csv"
    harvests_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path} ({len(harvests_df)} records)")
    
    return harvests_df

if __name__ == "__main__":
    print("This module requires farmers and products dataframes to run.")
