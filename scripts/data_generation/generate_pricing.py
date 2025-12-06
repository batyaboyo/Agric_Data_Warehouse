"""
Generate Market Pricing Data
Creates time-series pricing data for products across markets
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Base wholesale prices (UGX per kg)
BASE_WHOLESALE_PRICES = {
    "Maize": 1200,
    "Beans": 2500,
    "Coffee": 7000,
    "Rice": 3000,
    "Cassava": 600,
    "Sweet Potato": 900,
    "Banana": 800,
    "Matooke": 1200,
    "Tomato": 1500,
    "Cabbage": 1200,
    "Onion": 2000,
    "Irish Potato": 1500,
    "Groundnuts": 3500,
    "Soybeans": 2000,
    "Millet": 1600,
    "Sorghum": 1400,
    "Pineapple": 1200,
    "Passion Fruit": 2500,
    "Avocado": 2000,
    "Mango": 1000,
    "Cotton": 3000,
    "Tobacco": 5000,
    "Tea": 4000,
    "Cocoa": 6000,
    "Sunflower": 2200,
    "Sesame": 3500
}

# Retail markup (retail = wholesale * markup)
RETAIL_MARKUP_RANGE = (1.20, 1.50)  # 20-50% markup

PRICE_SOURCES = [
    "Uganda Commodity Exchange",
    "Ministry of Agriculture",
    "Market Survey",
    "Cooperative Report"
]

def generate_price_trend(prev_price, volatility=0.05):
    """
    Generate next price based on previous price with random walk
    
    Args:
        prev_price: Previous price
        volatility: Price volatility (std dev of % change)
    
    Returns:
        New price
    """
    # Random walk with slight upward bias (inflation)
    change_pct = np.random.normal(0.001, volatility)  # 0.1% daily drift
    new_price = prev_price * (1 + change_pct)
    return max(new_price, prev_price * 0.5)  # Floor at 50% of previous price

def determine_trend(current_price, previous_price):
    """Determine price trend"""
    if current_price > previous_price * 1.02:
        return "Up"
    elif current_price < previous_price * 0.98:
        return "Down"
    else:
        return "Stable"

def generate_pricing(num_days=365, products_df=None, markets_df=None, output_dir="../../data"):
    """
    Generate synthetic market pricing data
    
    Args:
        num_days: Number of days of pricing data
        products_df: DataFrame of products
        markets_df: DataFrame of markets
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with pricing data
    """
    
    print(f"Generating {num_days} days of pricing data...")
    
    if products_df is None or markets_df is None:
        raise ValueError("products_df and markets_df are required")
    
    pricing_records = []
    
    # Select subset of products that are commonly traded
    traded_products = products_df[products_df['product_name'].isin(BASE_WHOLESALE_PRICES.keys())]
    
    # Select subset of markets (major markets have daily pricing)
    major_markets = markets_df[markets_df['market_type'].isin(['Urban Market', 'Wholesale Market', 'Rural Market'])]
    
    # Limit to reasonable number of product-market combinations
    num_combinations = min(50, len(traded_products) * 2)  # Up to 50 product-market pairs
    
    print(f"  Creating pricing for {num_combinations} product-market combinations...")
    
    # Generate pricing time series for each product-market combination
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=num_days - 1)
    
    combination_count = 0
    
    for _, product in traded_products.iterrows():
        if combination_count >= num_combinations:
            break
        
        # Each product appears in 2-3 markets
        num_markets_for_product = min(random.randint(2, 3), len(major_markets))
        selected_markets = major_markets.sample(n=num_markets_for_product)
        
        for _, market in selected_markets.iterrows():
            combination_count += 1
            
            # Initialize with base price
            product_name = product['product_name']
            base_price = BASE_WHOLESALE_PRICES.get(product_name, 2000)
            
            # Add market-specific variation (±15%)
            current_wholesale = base_price * random.uniform(0.85, 1.15)
            
            # Generate daily prices
            for day_offset in range(num_days):
                current_date = start_date + timedelta(days=day_offset)
                
                # Store previous price for trend calculation
                prev_wholesale = current_wholesale
                
                # Generate new price (random walk)
                # Higher volatility for perishables
                volatility = 0.08 if product['is_perishable'] else 0.03
                current_wholesale = generate_price_trend(current_wholesale, volatility)
                
                # Retail price with markup
                markup = random.uniform(*RETAIL_MARKUP_RANGE)
                current_retail = current_wholesale * markup
                
                # Price spread
                price_spread = current_retail - current_wholesale
                price_spread_pct = (price_spread / current_wholesale) * 100
                
                # Trend
                if day_offset == 0:
                    price_trend = "Stable"
                else:
                    price_trend = determine_trend(current_wholesale, prev_wholesale)
                
                # Source
                source = random.choice(PRICE_SOURCES)
                
                price_id = f"PRC{len(pricing_records)+1:08d}"
                
                pricing_record = {
                    'price_id': price_id,
                    'product_id': product['product_id'],
                    'market_id': market['market_id'],
                    'price_date': current_date.strftime('%Y-%m-%d'),
                    'wholesale_price': round(current_wholesale, 2),
                    'retail_price': round(current_retail, 2),
                    'price_trend': price_trend,
                    'source': source
                }
                
                pricing_records.append(pricing_record)
            
            if combination_count % 10 == 0:
                print(f"    Processed {combination_count} product-market combinations...")
    
    # Create DataFrame
    pricing_df = pd.DataFrame(pricing_records)
    
    # Save to CSV
    csv_path = f"{output_dir}/pricing.csv"
    pricing_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    # Generate SQL INSERT statements (sample - first 1000)
    sql_path = f"{output_dir}/pricing_insert.sql"
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Pricing Data INSERT Statements (Sample)\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
        f.write(f"-- Total pricing records: {len(pricing_df)}, showing first 1000\n\n")
        
        for _, row in pricing_df.head(1000).iterrows():
            sql = f"""INSERT INTO staging.stg_pricing (price_id, product_id, market_id, price_date, wholesale_price, retail_price, price_trend, source) VALUES ('{row['price_id']}', '{row['product_id']}', '{row['market_id']}', '{row['price_date']}', {row['wholesale_price']}, {row['retail_price']}, '{row['price_trend']}', '{row['source']}');\n"""
            f.write(sql)
    
    print(f"  Saved SQL to {sql_path}")
    
    # Print summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total Pricing Records: {len(pricing_df):,}")
    print(f"    Product-Market Combinations: {combination_count}")
    print(f"    Date Range: {pricing_df['price_date'].min()} to {pricing_df['price_date'].max()}")
    print(f"    Average Wholesale Price: UGX {pricing_df['wholesale_price'].mean():,.0f}")
    print(f"    Average Retail Price: UGX {pricing_df['retail_price'].mean():,.0f}")
    print(f"\n    Price Trend Distribution:")
    for trend, count in pricing_df['price_trend'].value_counts().items():
        pct = count / len(pricing_df) * 100
        print(f"      {trend}: {count:,} ({pct:.1f}%)")
    
    return pricing_df

if __name__ == "__main__":
    # Test generation requires other dataframes
    print("This script requires products and markets data.")
    print("Run master_data_generator.py instead.")
