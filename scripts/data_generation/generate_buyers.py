"""
Generate Buyers Data
Creates synthetic buyer/trader records for the Agricultural Data Warehouse
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime
import hashlib
import os

# Initialize Faker
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Uganda Districts (Same as farmers for consistency)
UGANDA_DISTRICTS = [
    "Kampala", "Wakiso", "Mukono", "Jinja", "Mbale", "Gulu", "Lira", "Mbarara",
    "Masaka", "Kasese", "Hoima", "Soroti", "Arua", "Fort Portal", "Kabale",
    "Tororo", "Iganga", "Bushenyi", "Masindi", "Kitgum", "Moroto", "Nebbi",
    "Apac", "Kabarole", "Rukungiri", "Bundibugyo", "Kisoro", "Ntungamo",
    "Kamuli", "Pallisa", "Kapchorwa", "Katakwi", "Kumi", "Mayuge", "Sironko"
]

BUYER_TYPES = ["Wholesaler", "Retailer", "Processor", "Exporter", "Cooperative"]

def generate_blockchain_wallet(buyer_id):
    """Generate a mock blockchain wallet address"""
    hash_input = f"buyer_{buyer_id}_{datetime.now().isoformat()}"
    return "0x" + hashlib.sha256(hash_input.encode()).hexdigest()[:40]

def generate_buyers(num_buyers=500, output_dir="../../data"):
    """
    Generate synthetic buyer data
    
    Args:
        num_buyers: Number of buyers to generate
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with buyer data
    """
    print(f"Generating {num_buyers} buyer records...")
    
    buyers = []
    
    for i in range(num_buyers):
        buyer_id = f"BYR{str(i+1).zfill(5)}"
        buyer_type = random.choice(BUYER_TYPES)
        
        # Company/Business Name
        if buyer_type == "Cooperative":
            buyer_name = f"{fake.city()} Farmers Coop"
        else:
            buyer_name = f"{fake.company()} {random.choice(['Trading', 'Limited', 'Agro', 'Foods'])}"
            
        contact_person = fake.name()
        
        # Phone (Uganda format)
        prefixes = ["0700", "0701", "0702", "0703", "0704", "0750", "0751", "0752", "0753", "0754", "0770", "0771"]
        phone_number = f"{random.choice(prefixes)}{random.randint(100000, 999999)}"
        
        email = f"{contact_person.lower().replace(' ', '.')}@{fake.free_email_domain()}"
        district = random.choice(UGANDA_DISTRICTS)
        
        # Registration Number
        reg_year = random.randint(2010, 2023)
        registration_number = f"REG/{reg_year}/{random.randint(1000, 9999)}"
        
        blockchain_wallet = generate_blockchain_wallet(buyer_id)
        
        buyer = {
            'buyer_id': buyer_id,
            'buyer_name': buyer_name,
            'buyer_type': buyer_type,
            'contact_person': contact_person,
            'phone_number': phone_number,
            'email': email,
            'district': district,
            'registration_number': registration_number,
            'blockchain_wallet': blockchain_wallet,
            'is_active': True,
            'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        buyers.append(buyer)
        
    buyers_df = pd.DataFrame(buyers)
    
    # Save to CSV
    os.makedirs(output_dir, exist_ok=True)
    csv_path = f"{output_dir}/buyers.csv"
    buyers_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    return buyers_df

if __name__ == "__main__":
    generate_buyers()
