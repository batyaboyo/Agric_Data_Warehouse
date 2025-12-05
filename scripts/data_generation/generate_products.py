"""
Generate Products Data
Creates synthetic agricultural product/crop records
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Uganda agricultural products
PRODUCTS_DATA = [
    # Cereals
    {"name": "Maize", "category": "Cereals", "variety": "Longe 10H", "season": "Both", "growing_days": 120, "perishable": False},
    {"name": "Maize", "category": "Cereals", "variety": "Longe 5", "season": "Both", "growing_days": 110, "perishable": False},
    {"name": "Maize", "category": "Cereals", "variety": "Hybrid", "season": "Both", "growing_days": 100, "perishable": False},
    {"name": "Rice", "category": "Cereals", "variety": "NERICA", "season": "Both", "growing_days": 120, "perishable": False},
    {"name": "Rice", "category": "Cereals", "variety": "WITA 9", "season": "Both", "growing_days": 130, "perishable": False},
    {"name": "Millet", "category": "Cereals", "variety": "Finger Millet", "season": "First", "growing_days": 120, "perishable": False},
    {"name": "Sorghum", "category": "Cereals", "variety": "Local", "season": "First", "growing_days": 110, "perishable": False},
    
    # Legumes
    {"name": "Beans", "category": "Legumes", "variety": "NABE 15", "season": "Both", "growing_days": 90, "perishable": False},
    {"name": "Beans", "category": "Legumes", "variety": "K132", "season": "Both", "growing_days": 85, "perishable": False},
    {"name": "Beans", "category": "Legumes", "variety": "Masindi Yellow", "season": "Both", "growing_days": 95, "perishable": False},
    {"name": "Groundnuts", "category": "Legumes", "variety": "Red Beauty", "season": "First", "growing_days": 100, "perishable": False},
    {"name": "Groundnuts", "category": "Legumes", "variety": "Serenut", "season": "First", "growing_days": 110, "perishable": False},
    {"name": "Soybeans", "category": "Legumes", "variety": "Maksoy", "season": "Both", "growing_days": 120, "perishable": False},
    {"name": "Cowpeas", "category": "Legumes", "variety": "SECOW", "season": "Both", "growing_days": 70, "perishable": False},
    
    # Root Crops
    {"name": "Cassava", "category": "Root Crops", "variety": "NASE 14", "season": "Year-round", "growing_days": 365, "perishable": True},
    {"name": "Cassava", "category": "Root Crops", "variety": "TME 14", "season": "Year-round", "growing_days": 330, "perishable": True},
    {"name": "Sweet Potato", "category": "Root Crops", "variety": "NASPOT 10", "season": "Both", "growing_days": 120, "perishable": True},
    {"name": "Sweet Potato", "category": "Root Crops", "variety": "Ejumula", "season": "Both", "growing_days": 110, "perishable": True},
    {"name": "Irish Potato", "category": "Root Crops", "variety": "Victoria", "season": "Both", "growing_days": 100, "perishable": True},
    {"name": "Irish Potato", "category": "Root Crops", "variety": "Kachpot", "season": "Both", "growing_days": 90, "perishable": True},
    
    # Plantains & Bananas
    {"name": "Matooke", "category": "Plantains", "variety": "Mbwazirume", "season": "Year-round", "growing_days": 365, "perishable": True},
    {"name": "Matooke", "category": "Plantains", "variety": "Nakitembe", "season": "Year-round", "growing_days": 365, "perishable": True},
    {"name": "Banana", "category": "Fruits", "variety": "Bogoya", "season": "Year-round", "growing_days": 365, "perishable": True},
    {"name": "Banana", "category": "Fruits", "variety": "Sukali Ndiizi", "season": "Year-round", "growing_days": 365, "perishable": True},
    
    # Cash Crops
    {"name": "Coffee", "category": "Cash Crops", "variety": "Arabica", "season": "Year-round", "growing_days": 730, "perishable": False},
    {"name": "Coffee", "category": "Cash Crops", "variety": "Robusta", "season": "Year-round", "growing_days": 730, "perishable": False},
    {"name": "Cotton", "category": "Cash Crops", "variety": "BPA", "season": "First", "growing_days": 150, "perishable": False},
    {"name": "Tobacco", "category": "Cash Crops", "variety": "Burley", "season": "First", "growing_days": 120, "perishable": False},
    {"name": "Tea", "category": "Cash Crops", "variety": "Clonal", "season": "Year-round", "growing_days": 1095, "perishable": False},
    {"name": "Cocoa", "category": "Cash Crops", "variety": "Hybrid", "season": "Year-round", "growing_days": 1095, "perishable": False},
    
    # Vegetables
    {"name": "Tomato", "category": "Vegetables", "variety": "MT 56", "season": "Both", "growing_days": 75, "perishable": True},
    {"name": "Tomato", "category": "Vegetables", "variety": "Moneymaker", "season": "Both", "growing_days": 80, "perishable": True},
    {"name": "Cabbage", "category": "Vegetables", "variety": "Gloria", "season": "Both", "growing_days": 70, "perishable": True},
    {"name": "Onion", "category": "Vegetables", "variety": "Red Creole", "season": "Both", "growing_days": 90, "perishable": False},
    {"name": "Carrot", "category": "Vegetables", "variety": "Nantes", "season": "Both", "growing_days": 75, "perishable": True},
    {"name": "Eggplant", "category": "Vegetables", "variety": "Black Beauty", "season": "Both", "growing_days": 80, "perishable": True},
    {"name": "Pepper", "category": "Vegetables", "variety": "Hot Pepper", "season": "Both", "growing_days": 70, "perishable": True},
    {"name": "Leafy Greens", "category": "Vegetables", "variety": "Dodo", "season": "Both", "growing_days": 30, "perishable": True},
    
    # Fruits
    {"name": "Pineapple", "category": "Fruits", "variety": "Smooth Cayenne", "season": "Year-round", "growing_days": 365, "perishable": True},
    {"name": "Mango", "category": "Fruits", "variety": "Apple Mango", "season": "Seasonal", "growing_days": 730, "perishable": True},
    {"name": "Passion Fruit", "category": "Fruits", "variety": "Purple", "season": "Year-round", "growing_days": 180, "perishable": True},
    {"name": "Papaya", "category": "Fruits", "variety": "Solo", "season": "Year-round", "growing_days": 270, "perishable": True},
    {"name": "Avocado", "category": "Fruits", "variety": "Hass", "season": "Seasonal", "growing_days": 730, "perishable": True},
    {"name": "Jackfruit", "category": "Fruits", "variety": "Local", "season": "Seasonal", "growing_days": 730, "perishable": True},
    
    # Oilseeds
    {"name": "Sunflower", "category": "Oilseeds", "variety": "PAN 7033", "season": "Both", "growing_days": 90, "perishable": False},
    {"name": "Sesame", "category": "Oilseeds", "variety": "Sesim 1", "season": "First", "growing_days": 90, "perishable": False},
]

def generate_products(num_products=100, output_dir="../../data"):
    """
    Generate synthetic product data
    
    Args:
        num_products: Number of product records to generate
        output_dir: Output directory for CSV files
    
    Returns:
        DataFrame with product data
    """
    
    print(f"Generating {num_products} product records...")
    
    products = []
    
    # Use all predefined products and add variations if needed
    for i in range(num_products):
        if i < len(PRODUCTS_DATA):
            base_product = PRODUCTS_DATA[i]
        else:
            # Cycle through products for additional records
            base_product = PRODUCTS_DATA[i % len(PRODUCTS_DATA)]
        
        product_id = f"PRD{str(i+1).zfill(4)}"
        
        # Add some variation to growing days
        growing_days = base_product["growing_days"] + random.randint(-5, 5)
        
        product = {
            'product_id': product_id,
            'product_name': base_product["name"],
            'category': base_product["category"],
            'variety': base_product["variety"],
            'unit_of_measure': 'kg',
            'season': base_product["season"],
            'avg_growing_days': max(growing_days, 30),  # Minimum 30 days
            'is_perishable': base_product["perishable"]
        }
        
        products.append(product)
    
    # Create DataFrame
    products_df = pd.DataFrame(products)
    
    # Save to CSV
    csv_path = f"{output_dir}/products.csv"
    products_df.to_csv(csv_path, index=False)
    print(f"  Saved to {csv_path}")
    
    # Generate SQL INSERT statements
    sql_path = f"{output_dir}/products_insert.sql"
    with open(sql_path, 'w', encoding='utf-8') as f:
        f.write("-- Product Data INSERT Statements\n")
        f.write("-- Generated: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        
        for _, row in products_df.iterrows():
            sql = f"""INSERT INTO staging.stg_products (product_id, product_name, category, variety, unit_of_measure, season, avg_growing_days, is_perishable) VALUES ('{row['product_id']}', '{row['product_name']}', '{row['category']}', '{row['variety']}', '{row['unit_of_measure']}', '{row['season']}', {row['avg_growing_days']}, {row['is_perishable']});\n"""
            f.write(sql)
    
    print(f"  Saved SQL to {sql_path}")
    
    # Print summary statistics
    print("\n  Summary Statistics:")
    print(f"    Total Products: {len(products_df)}")
    print(f"    Categories: {products_df['category'].nunique()}")
    print(f"    Perishable: {len(products_df[products_df['is_perishable'] == True])}")
    print(f"    Non-Perishable: {len(products_df[products_df['is_perishable'] == False])}")
    print(f"\n    Category Breakdown:")
    for category, count in products_df['category'].value_counts().items():
        print(f"      {category}: {count}")
    
    return products_df

if __name__ == "__main__":
    # Test generation
    df = generate_products(num_products=100)
    print(f"\n✓ Successfully generated {len(df)} products")
