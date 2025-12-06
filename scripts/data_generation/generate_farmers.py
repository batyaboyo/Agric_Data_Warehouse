"""
Generate Farmers Data
Creates synthetic farmer records with Uganda-specific attributes
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import hashlib

# Initialize Faker with seed for reproducibility
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Uganda-specific data
UGANDA_DISTRICTS = [
    "Kampala", "Wakiso", "Mukono", "Jinja", "Mbale", "Gulu", "Lira", "Mbarara",
    "Masaka", "Kasese", "Hoima", "Soroti", "Arua", "Fort Portal", "Kabale",
    "Tororo", "Iganga", "Bushenyi", "Masindi", "Kitgum", "Moroto", "Nebbi",
    "Apac", "Kabarole", "Rukungiri", "Bundibugyo", "Kisoro", "Ntungamo",
    "Kamuli", "Pallisa", "Kapchorwa", "Katakwi", "Kumi", "Mayuge", "Sironko"
]

UGANDA_REGIONS = {
    "Central": ["Kampala", "Wakiso", "Mukono", "Masaka", "Luwero"],
    "Eastern": ["Jinja", "Mbale", "Tororo", "Iganga", "Soroti", "Pallisa", "Kamuli"],
    "Northern": ["Gulu", "Lira", "Kitgum", "Arua", "Nebbi", "Apac", "Moroto"],
    "Western": ["Mbarara", "Kasese", "Hoima", "Fort Portal", "Kabale", "Bushenyi", "Masindi"]
}

UGANDA_FIRST_NAMES = [
    "Mukasa", "Nakato", "Wasswa", "Kato", "Babirye", "Nakku", "Kisakye", "Nambi",
    "Okello", "Akello", "Otim", "Auma", "Odongo", "Apiyo", "Opio", "Acen",
    "Tumusiime", "Ainembabazi", "Byaruhanga", "Tusiime", "Muhwezi", "Natukunda"
]

UGANDA_LAST_NAMES = [
    "Musoke", "Ssemakula", "Namugga", "Kyagulanyi", "Lubega", "Kizza", "Ssentongo",
    "Okoth", "Ouma", "Onyango", "Adong", "Lamwaka", "Atim", "Lakot",
    "Tumwebaze", "Mwesigwa", "Byamugisha", "Kamugisha", "Turyahabwe", "Kabagambe"
]

def generate_blockchain_wallet(farmer_id):
    """Generate a mock blockchain wallet address"""
    hash_input = f"farmer_{farmer_id}_{datetime.now().isoformat()}"
    return "0x" + hashlib.sha256(hash_input.encode()).hexdigest()[:40]

def generate_national_id():
    """Generate Uganda-style national ID (CM + 12 digits = 14 chars)"""
    return f"CM{random.randint(100000000000, 999999999999)}"

def generate_phone_number():
    """Generate Uganda phone number format"""
    prefixes = ["0700", "0701", "0702", "0703", "0704", "0750", "0751", "0752", "0753", "0754", "0775", "0776", "0777", "0778", "0779"]
    return f"{random.choice(prefixes)}{random.randint(100000, 999999)}"

def assign_region(district):
    """Assign region based on district"""
    for region, districts in UGANDA_REGIONS.items():
        if district in districts:
            return region
    return "Central"  # Default

def generate_farmers(num_farmers=2000, products_df=None, output_dir="../../data"):
    """
    Generate synthetic farmer data
    
    Args:
        num_farmers: Number of farmers to generate (default 2000)
        products_df: DataFrame of products for primary crop assignment
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with farmer data
    """
    
    print(f"Generating {num_farmers} farmer records...")
    
    farmers = []
    
    # Get list of crops if products provided
    crops = products_df['product_name'].tolist() if products_df is not None else [
        "Maize", "Coffee", "Beans", "Cassava", "Sweet Potato", "Banana", "Rice", "Millet"
    ]
    
    for i in range(num_farmers):
        farmer_id = f"FMR{str(i+1).zfill(6)}"
        
        # Demographics
        gender = random.choice(['M', 'F'])
        first_name = random.choice(UGANDA_FIRST_NAMES)
        last_name = random.choice(UGANDA_LAST_NAMES)
        
        # Age between 18 and 75
        age = random.randint(18, 75)
        date_of_birth = datetime.now() - timedelta(days=age*365 + random.randint(0, 365))
        
        # Location
        district = random.choice(UGANDA_DISTRICTS)
        region = assign_region(district)
        subcounty = f"{district} {random.choice(['North', 'South', 'East', 'West', 'Central'])}"
        village = f"{fake.word().capitalize()} Village"
        
        # GPS coordinates (Uganda bounds: lat 4.22 to -1.48, lon 29.57 to 35.04)
        gps_latitude = round(random.uniform(-1.48, 4.22), 6)
        gps_longitude = round(random.uniform(29.57, 35.04), 6)
        
        # Farm characteristics
        # Farm size distribution: 60% small (0.5-2 acres), 30% medium (2-10 acres), 10% large (10-50 acres)
        farm_size_category = random.choices(
            ['small', 'medium', 'large'],
            weights=[0.6, 0.3, 0.1]
        )[0]
        
        if farm_size_category == 'small':
            farm_size_acres = round(random.uniform(0.5, 2.0), 2)
        elif farm_size_category == 'medium':
            farm_size_acres = round(random.uniform(2.0, 10.0), 2)
        else:
            farm_size_acres = round(random.uniform(10.0, 50.0), 2)
        
        # Primary crop
        primary_crop = random.choice(crops)
        
        # Cooperative membership (70% are members)
        is_cooperative_member = random.random() < 0.7
        cooperative_id = f"COOP{random.randint(1, 50):03d}" if is_cooperative_member else None
        
        # Registration date (within last 3 years)
        registration_date = datetime.now() - timedelta(days=random.randint(0, 1095))
        
        # Blockchain wallet
        blockchain_wallet = generate_blockchain_wallet(farmer_id)
        
        farmer = {
            'farmer_id': farmer_id,
            'national_id': generate_national_id(),
            'first_name': first_name,
            'last_name': last_name,
            'gender': gender,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
            'phone_number': generate_phone_number(),
            'district': district,
            'subcounty': subcounty,
            'village': village,
            'gps_latitude': gps_latitude,
            'gps_longitude': gps_longitude,
            'farm_size_acres': farm_size_acres,
            'primary_crop': primary_crop,
            'cooperative_id': cooperative_id,
            'blockchain_wallet': blockchain_wallet,
            'registration_date': registration_date.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': True
        }
        
        farmers.append(farmer)
        
        if (i + 1) % 500 == 0:
            print(f"  Generated {i + 1} farmers...")
    
    # Create DataFrame
    farmers_df = pd.DataFrame(farmers)
    
    # Save to CSV
    csv_path = f"{output_dir}/farmers.csv"
    farmers_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    # Generate SQL INSERT statements
    sql_path = f"{output_dir}/farmers_insert.sql"
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Farmer Data INSERT Statements\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        
        for _, row in farmers_df.iterrows():
            cooperative_val = f"'{row['cooperative_id']}'" if row['cooperative_id'] else "NULL"
            sql = f"""INSERT INTO staging.stg_farmers (farmer_id, national_id, first_name, last_name, gender, date_of_birth, phone_number, district, subcounty, village, gps_latitude, gps_longitude, farm_size_acres, primary_crop, cooperative_id, blockchain_wallet, registration_date, is_active) VALUES ('{row['farmer_id']}', '{row['national_id']}', '{row['first_name']}', '{row['last_name']}', '{row['gender']}', '{row['date_of_birth']}', '{row['phone_number']}', '{row['district']}', '{row['subcounty']}', '{row['village']}', {row['gps_latitude']}, {row['gps_longitude']}, {row['farm_size_acres']}, '{row['primary_crop']}', {cooperative_val}, '{row['blockchain_wallet']}', '{row['registration_date']}', {row['is_active']});\n"""
            f.write(sql)
    
    print(f"  Saved SQL to {sql_path}")
    
    # Print summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total Farmers: {len(farmers_df)}")
    print(f"    Male: {len(farmers_df[farmers_df['gender'] == 'M'])} ({len(farmers_df[farmers_df['gender'] == 'M'])/len(farmers_df)*100:.1f}%)")
    print(f"    Female: {len(farmers_df[farmers_df['gender'] == 'F'])} ({len(farmers_df[farmers_df['gender'] == 'F'])/len(farmers_df)*100:.1f}%)")
    print(f"    Cooperative Members: {len(farmers_df[farmers_df['cooperative_id'].notna()])} ({len(farmers_df[farmers_df['cooperative_id'].notna()])/len(farmers_df)*100:.1f}%)")
    print(f"    Average Farm Size: {farmers_df['farm_size_acres'].mean():.2f} acres")
    print(f"    Districts Covered: {farmers_df['district'].nunique()}")
    
    return farmers_df

if __name__ == "__main__":
    # Test generation
    df = generate_farmers(num_farmers=2000)
    print(f"\n✓ Successfully generated {len(df)} farmers")
