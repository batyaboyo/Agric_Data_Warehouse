"""
Generate Transactions Data
Creates synthetic transaction records linking farmers, products, buyers, and markets
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import hashlib

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

QUALITY_GRADES = ['A', 'B', 'C']
QUALITY_WEIGHTS = [0.2, 0.6, 0.2]  # Most products are grade B

PAYMENT_METHODS = [
    "Mobile Money",
    "Cash",
    "Bank Transfer",
    "Cooperative Account"
]
PAYMENT_WEIGHTS = [0.5, 0.3, 0.15, 0.05]  # Mobile money most common

PAYMENT_STATUSES = ["Paid", "Pending", "Failed"]
PAYMENT_STATUS_WEIGHTS = [0.92, 0.05, 0.03]  # Most transactions successful

def generate_blockchain_hash(transaction_id, timestamp):
    """Generate a mock blockchain transaction hash"""
    hash_input = f"{transaction_id}_{timestamp}"
    return hashlib.sha256(hash_input.encode()).hexdigest()

def generate_buyer_id():
    """Generate a buyer ID"""
    return f"BYR{random.randint(1, 500):04d}"

def calculate_price_with_quality(base_price, quality_grade):
    """Adjust price based on quality grade"""
    if quality_grade == 'A':
        return base_price * random.uniform(1.15, 1.30)  # 15-30% premium
    elif quality_grade == 'B':
        return base_price * random.uniform(0.95, 1.05)  # Around base price
    else:  # Grade C
        return base_price * random.uniform(0.70, 0.85)  # 15-30% discount

def generate_transactions(num_transactions=10000, farmers_df=None, products_df=None, 
                         markets_df=None, output_dir="../../data"):
    """
    Generate synthetic transaction data
    
    Args:
        num_transactions: Number of transactions to generate
        farmers_df: DataFrame of farmers
        products_df: DataFrame of products
        markets_df: DataFrame of markets
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with transaction data
    """
    
    print(f"Generating {num_transactions} transaction records...")
    
    if farmers_df is None or products_df is None or markets_df is None:
        raise ValueError("farmers_df, products_df, and markets_df are required")
    
    transactions = []
    
    # Base prices for common products (UGX per kg)
    base_prices = {
        "Maize": 1500,
        "Beans": 3000,
        "Coffee": 8000,
        "Rice": 3500,
        "Cassava": 800,
        "Sweet Potato": 1200,
        "Banana": 1000,
        "Matooke": 1500,
        "Tomato": 2000,
        "Cabbage": 1500,
        "Onion": 2500,
        "Irish Potato": 1800,
        "Groundnuts": 4000,
        "Soybeans": 2500,
        "Millet": 2000,
        "Sorghum": 1800,
        "Pineapple": 1500,
        "Passion Fruit": 3000,
        "Avocado": 2500,
        "Mango": 1200
    }
    
    # Generate transactions over the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    for i in range(num_transactions):
        transaction_id = f"TXN{str(i+1).zfill(8)}"
        
        # Random farmer, product, market
        farmer = farmers_df.sample(n=1).iloc[0]
        product = products_df.sample(n=1).iloc[0]
        market = markets_df.sample(n=1).iloc[0]
        
        # Buyer
        buyer_id = generate_buyer_id()
        
        # Transaction date (weighted towards recent dates)
        days_ago = int(np.random.exponential(scale=100))  # Exponential distribution
        days_ago = min(days_ago, 365)  # Cap at 365 days
        transaction_date = end_date - timedelta(days=days_ago)
        
        # Quality grade
        quality_grade = random.choices(QUALITY_GRADES, weights=QUALITY_WEIGHTS)[0]
        
        # Quantity (varies by product type)
        if product['category'] in ['Cereals', 'Legumes', 'Cash Crops']:
            # Larger quantities for grains and cash crops
            quantity_kg = round(random.uniform(50, 1000), 2)
        elif product['category'] in ['Root Crops', 'Plantains']:
            quantity_kg = round(random.uniform(100, 800), 2)
        elif product['category'] in ['Vegetables', 'Fruits']:
            # Smaller quantities for perishables
            quantity_kg = round(random.uniform(20, 300), 2)
        else:
            quantity_kg = round(random.uniform(50, 500), 2)
        
        # Price calculation
        product_name = product['product_name']
        base_price = base_prices.get(product_name, 2000)  # Default if not in dict
        
        # Add some random variation to base price (±20%)
        base_price = base_price * random.uniform(0.8, 1.2)
        
        # Adjust for quality
        unit_price = round(calculate_price_with_quality(base_price, quality_grade), 2)
        
        # Total amount
        total_amount = round(quantity_kg * unit_price, 2)
        
        # Payment method and status
        payment_method = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS)[0]
        payment_status = random.choices(PAYMENT_STATUSES, weights=PAYMENT_STATUS_WEIGHTS)[0]
        
        # Blockchain hash (only for successful transactions)
        blockchain_hash = generate_blockchain_hash(transaction_id, transaction_date.isoformat()) if payment_status == "Paid" else None
        
        transaction = {
            'transaction_id': transaction_id,
            'farmer_id': farmer['farmer_id'],
            'buyer_id': buyer_id,
            'product_id': product['product_id'],
            'market_id': market['market_id'],
            'quantity_kg': quantity_kg,
            'quality_grade': quality_grade,
            'unit_price': unit_price,
            'total_amount': total_amount,
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': payment_method,
            'payment_status': payment_status,
            'blockchain_hash': blockchain_hash
        }
        
        transactions.append(transaction)
        
        if (i + 1) % 2000 == 0:
            print(f"  Generated {i + 1} transactions...")
    
    # Create DataFrame
    transactions_df = pd.DataFrame(transactions)
    
    # Save to CSV
    csv_path = f"{output_dir}/transactions.csv"
    transactions_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    # Generate SQL INSERT statements (sample - first 1000 for file size)
    sql_path = f"{output_dir}/transactions_insert.sql"
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Transaction Data INSERT Statements (Sample)\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write(f"-- Total transactions: {len(transactions_df)}, showing first 1000\n\n")
        
        for _, row in transactions_df.head(1000).iterrows():
            blockchain_val = f"'{row['blockchain_hash']}'" if pd.notna(row['blockchain_hash']) else "NULL"
            sql = f"""INSERT INTO staging.stg_transactions (transaction_id, farmer_id, buyer_id, product_id, market_id, quantity_kg, quality_grade, unit_price, total_amount, transaction_date, payment_method, payment_status, blockchain_hash) VALUES ('{row['transaction_id']}', '{row['farmer_id']}', '{row['buyer_id']}', '{row['product_id']}', '{row['market_id']}', {row['quantity_kg']}, '{row['quality_grade']}', {row['unit_price']}, {row['total_amount']}, '{row['transaction_date']}', '{row['payment_method']}', '{row['payment_status']}', {blockchain_val});\n"""
            f.write(sql)
    
    print(f"  Saved SQL to {sql_path}")
    
    # Print summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total Transactions: {len(transactions_df):,}")
    print(f"    Total Value: UGX {transactions_df['total_amount'].sum():,.0f}")
    print(f"    Average Transaction: UGX {transactions_df['total_amount'].mean():,.0f}")
    print(f"    Date Range: {transactions_df['transaction_date'].min()} to {transactions_df['transaction_date'].max()}")
    print(f"\n    Quality Grade Distribution:")
    for grade, count in transactions_df['quality_grade'].value_counts().sort_index().items():
        pct = count / len(transactions_df) * 100
        print(f"      Grade {grade}: {count:,} ({pct:.1f}%)")
    print(f"\n    Payment Method Distribution:")
    for method, count in transactions_df['payment_method'].value_counts().items():
        pct = count / len(transactions_df) * 100
        print(f"      {method}: {count:,} ({pct:.1f}%)")
    print(f"\n    Payment Status:")
    for status, count in transactions_df['payment_status'].value_counts().items():
        pct = count / len(transactions_df) * 100
        print(f"      {status}: {count:,} ({pct:.1f}%)")
    
    return transactions_df

if __name__ == "__main__":
    # Test generation requires other dataframes
    print("This script requires farmers, products, and markets data.")
    print("Run master_data_generator.py instead.")
