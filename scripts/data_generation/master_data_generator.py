"""
Master Data Generator for Agricultural Supply Chain Data Warehouse
Generates synthetic data with ≥1,000 rows for all entities
Ensures referential integrity across all datasets
"""

import os
import sys
from datetime import datetime


# Import all generator modules
from generate_farmers import generate_farmers
from generate_products import generate_products
from generate_markets import generate_markets
from generate_transactions import generate_transactions
from generate_pricing import generate_pricing
from generate_buyers import generate_buyers
from generate_harvests import generate_harvests
from generate_weather import generate_weather
from generate_subsidies import generate_subsidies

def main():
    """
    Main orchestration function to generate all synthetic data
    """
    print("=" * 80)
    print("AGRICULTURAL SUPPLY CHAIN DATA WAREHOUSE - DATA GENERATION")
    print("=" * 80)
    print(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Create output directory
    output_dir = "../../data"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Generate Products (needed first for referential integrity)
        print("[1/9] Generating Products...")
        products_df = generate_products(num_products=100, output_dir=output_dir)
        print(f"✓ Generated {len(products_df)} products")
        print()
        
        # Step 2: Generate Markets
        print("[2/9] Generating Markets...")
        markets_df = generate_markets(num_markets=200, output_dir=output_dir)
        print(f"✓ Generated {len(markets_df)} markets")
        print()
        
        # Step 3: Generate Farmers
        print("[3/9] Generating Farmers...")
        farmers_df = generate_farmers(
            num_farmers=2000, 
            products_df=products_df,
            output_dir=output_dir
        )
        print(f"✓ Generated {len(farmers_df)} farmers")
        print()

        # Step 4: Generate Buyers
        print("[4/9] Generating Buyers...")
        buyers_df = generate_buyers(num_buyers=500, output_dir=output_dir)
        print(f"✓ Generated {len(buyers_df)} buyers")
        print()
        
        # Step 5: Generate Transactions
        print("[5/9] Generating Transactions...")
        transactions_df = generate_transactions(
            num_transactions=10000,
            farmers_df=farmers_df,
            products_df=products_df,
            markets_df=markets_df,
            buyers_df=buyers_df,
            output_dir=output_dir
        )
        print(f"✓ Generated {len(transactions_df)} transactions")
        print()
        
        # Step 6: Generate Pricing Data
        print("[6/9] Generating Market Pricing...")
        pricing_df = generate_pricing(
            num_days=365,
            products_df=products_df,
            markets_df=markets_df,
            output_dir=output_dir
        )
        print(f"✓ Generated {len(pricing_df)} pricing records")
        print()

        # Step 7: Generate Harvests
        print("[7/9] Generating Harvests...")
        harvests_df = generate_harvests(
            farmers_df=farmers_df,
            products_df=products_df,
            output_dir=output_dir
        )
        print(f"✓ Generated {len(harvests_df)} harvest records")
        print()

        # Step 8: Generate Weather
        print("[8/9] Generating Weather Data...")
        weather_df = generate_weather(num_days=365, output_dir=output_dir)
        print(f"✓ Generated {len(weather_df)} weather records")
        print()

        # Step 9: Generate Subsidies
        print("[9/9] Generating Subsidies...")
        subsidies_df = generate_subsidies(farmers_df=farmers_df, output_dir=output_dir)
        print(f"✓ Generated {len(subsidies_df)} subsidy records")
        print()
        
        # Summary
        print("=" * 80)
        print("DATA GENERATION COMPLETE")
        print("=" * 80)
        total_records = (
            len(products_df) + len(markets_df) + len(farmers_df) + 
            len(buyers_df) + len(transactions_df) + len(pricing_df) +
            len(harvests_df) + len(weather_df) + len(subsidies_df)
        )
        print(f"Total Records Generated: {total_records:,}")
        print()
        print("Files Created:")
        print(f"  - {output_dir}/products.csv ({len(products_df)} rows)")
        print(f"  - {output_dir}/markets.csv ({len(markets_df)} rows)")
        print(f"  - {output_dir}/farmers.csv ({len(farmers_df)} rows)")
        print(f"  - {output_dir}/buyers.csv ({len(buyers_df)} rows)")
        print(f"  - {output_dir}/transactions.csv ({len(transactions_df)} rows)")
        print(f"  - {output_dir}/pricing.csv ({len(pricing_df)} rows)")
        print(f"  - {output_dir}/harvests.csv ({len(harvests_df)} rows)")
        print(f"  - {output_dir}/weather.csv ({len(weather_df)} rows)")
        print(f"  - {output_dir}/subsidies.csv ({len(subsidies_df)} rows)")
        print()
        print(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
