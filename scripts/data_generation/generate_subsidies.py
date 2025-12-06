"""
Generate Subsidies Data
Creates synthetic government subsidy records for farmers
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(45)
np.random.seed(45)
random.seed(45)

PROGRAMS = [
    "NAADS Agricultural Input Support",
    "Operation Wealth Creation (OWC)",
    "Parish Development Model (PDM)",
    "Small-Scale Irrigation Program",
    "Fertilizer Access Initiative"
]

SUBSIDY_TYPES = {
    "NAADS Agricultural Input Support": ["Seeds", "Saplings"],
    "Operation Wealth Creation (OWC)": ["Livestock", "Coffee Seedlings", "Fruit Trees"],
    "Parish Development Model (PDM)": ["Cash Grant", "Revolving Fund"],
    "Small-Scale Irrigation Program": ["Irrigation Equipment"],
    "Fertilizer Access Initiative": ["Fertilizer"]
}

def generate_subsidies(farmers_df, output_dir="../../data"):
    """
    Generate synthetic subsidy data
    
    Args:
        farmers_df: DataFrame of farmers
        output_dir: Output directory
    """
    print(f"Generating subsidy records for farmers...")
    
    if farmers_df is None:
        print("Error: farmers_df is required")
        return pd.DataFrame()

    subsidies = []
    
    # 30% of farmers receive subsidies
    beneficiaries = farmers_df.sample(frac=0.3, random_state=45)
    
    count = 0
    for _, farmer in beneficiaries.iterrows():
        count += 1
        farmer_subsidy_id = f"SUB{str(count).zfill(6)}"
        farmer_id = farmer['farmer_id']
        
        program = random.choice(PROGRAMS)
        subsidy_type = random.choice(SUBSIDY_TYPES[program])
        subsidy_id = f"PRG-{random.randint(100, 999)}"
        
        # Value
        if program == "Parish Development Model (PDM)":
            amount = round(random.uniform(500000, 1000000), 0)
        elif subsidy_type == "Fertilizer":
            amount = round(random.uniform(50000, 200000), 0)
        elif subsidy_type == "Irrigation Equipment":
            amount = round(random.uniform(1000000, 5000000), 0)
        else:
            amount = round(random.uniform(100000, 500000), 0)
            
        dist_date = datetime.now() - timedelta(days=random.randint(30, 730))
        
        status = random.choices(
            ['Verified', 'Pending', 'Disbursed', 'Received'],
            weights=[0.3, 0.1, 0.3, 0.3]
        )[0]
        
        record = {
            'farmer_subsidy_id': farmer_subsidy_id,
            'farmer_id': farmer_id,
            'subsidy_id': subsidy_id,
            'program_name': program,
            'subsidy_type': subsidy_type,
            'amount_value': amount,
            'distribution_date': dist_date.strftime('%Y-%m-%d'),
            'verification_status': status,
            'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        subsidies.append(record)
            
    subsidies_df = pd.DataFrame(subsidies)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_path = f"{output_dir}/subsidies.csv"
    subsidies_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path} ({len(subsidies_df)} records)")
    
    return subsidies_df

if __name__ == "__main__":
    print("This module requires farmers dataframe to run.")
