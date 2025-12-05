"""
Generate Markets Data
Creates synthetic market/trading center records
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime
from faker import Faker

# Set seeds for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Uganda districts (same as farmers)
UGANDA_DISTRICTS = [
    "Kampala", "Wakiso", "Mukono", "Jinja", "Mbale", "Gulu", "Lira", "Mbarara",
    "Masaka", "Kasese", "Hoima", "Soroti", "Arua", "Fort Portal", "Kabale",
    "Tororo", "Iganga", "Bushenyi", "Masindi", "Kitgum", "Moroto", "Nebbi",
    "Apac", "Kabarole", "Rukungiri", "Bundibugyo", "Kisoro", "Ntungamo",
    "Kamuli", "Pallisa", "Kapchorwa", "Katakwi", "Kumi", "Mayuge", "Sironko"
]

MARKET_TYPES = [
    "Urban Market",
    "Rural Market",
    "Collection Center",
    "Cooperative Center",
    "Wholesale Market",
    "Export Hub",
    "Processing Center"
]

MARKET_NAME_PREFIXES = [
    "Central", "Main", "New", "Old", "Modern", "Community", "Farmers'",
    "Regional", "District", "Town", "Village", "Trading"
]

OPERATING_DAYS = [
    "Monday-Friday",
    "Monday-Saturday",
    "Daily",
    "Tuesday, Thursday, Saturday",
    "Wednesday, Saturday",
    "Daily except Sunday"
]

def generate_markets(num_markets=200, output_dir="../../data"):
    """
    Generate synthetic market data
    
    Args:
        num_markets: Number of markets to generate
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with market data
    """
    
    print(f"Generating {num_markets} market records...")
    
    markets = []
    
    for i in range(num_markets):
        market_id = f"MKT{str(i+1).zfill(4)}"
        
        # Location
        district = random.choice(UGANDA_DISTRICTS)
        subcounty = f"{district} {random.choice(['North', 'South', 'East', 'West', 'Central'])}"
        
        # Market name
        prefix = random.choice(MARKET_NAME_PREFIXES)
        market_name = f"{prefix} {district} Market"
        
        # Market type (distribution: 40% rural, 30% urban, 20% collection, 10% other)
        market_type = random.choices(
            MARKET_TYPES,
            weights=[0.3, 0.4, 0.15, 0.05, 0.05, 0.03, 0.02]
        )[0]
        
        # GPS coordinates (Uganda bounds)
        gps_latitude = round(random.uniform(-1.48, 4.22), 6)
        gps_longitude = round(random.uniform(29.57, 35.04), 6)
        
        # Operating days
        operating_days = random.choice(OPERATING_DAYS)
        
        # Capacity based on market type
        if market_type in ["Urban Market", "Wholesale Market"]:
            capacity_kg = round(random.uniform(50000, 200000), 2)
        elif market_type in ["Rural Market", "Collection Center"]:
            capacity_kg = round(random.uniform(5000, 30000), 2)
        else:
            capacity_kg = round(random.uniform(10000, 50000), 2)
        
        market = {
            'market_id': market_id,
            'market_name': market_name,
            'market_type': market_type,
            'district': district,
            'subcounty': subcounty,
            'gps_latitude': gps_latitude,
            'gps_longitude': gps_longitude,
            'operating_days': operating_days,
            'capacity_kg': capacity_kg,
            'is_active': True
        }
        
        markets.append(market)
    
    # Create DataFrame
    markets_df = pd.DataFrame(markets)
    
    # Save to CSV
    csv_path = f"{output_dir}/markets.csv"
    markets_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    # Generate SQL INSERT statements
    sql_path = f"{output_dir}/markets_insert.sql"
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Market Data INSERT Statements\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        
        for _, row in markets_df.iterrows():
            sql = f"""INSERT INTO staging.stg_markets (market_id, market_name, market_type, district, subcounty, gps_latitude, gps_longitude, operating_days, capacity_kg, is_active) VALUES ('{row['market_id']}', '{row['market_name']}', '{row['market_type']}', '{row['district']}', '{row['subcounty']}', {row['gps_latitude']}, {row['gps_longitude']}, '{row['operating_days']}', {row['capacity_kg']}, {row['is_active']});\n"""
            f.write(sql)
    
    print(f"  Saved SQL to {sql_path}")
    
    # Print summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total Markets: {len(markets_df)}")
    print(f"    Districts Covered: {markets_df['district'].nunique()}")
    print(f"    Average Capacity: {markets_df['capacity_kg'].mean():,.0f} kg")
    print(f"\n    Market Type Breakdown:")
    for mtype, count in markets_df['market_type'].value_counts().items():
        print(f"      {mtype}: {count}")
    
    return markets_df

if __name__ == "__main__":
    # Test generation
    df = generate_markets(num_markets=200)
    print(f"\n✓ Successfully generated {len(df)} markets")
