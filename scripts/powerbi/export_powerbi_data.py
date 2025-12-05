"""
Export Power BI Dataset
Generates denormalized CSV file for Power BI with ≥1,000 rows
"""

import psycopg2
import pandas as pd
from datetime import datetime
import yaml
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_config():
    """Load database configuration"""
    with open('../etl/etl_config.yaml', 'r') as f:
        return yaml.safe_load(f)

def export_powerbi_dataset():
    """
    Export denormalized dataset for Power BI
    Combines fact_transaction with all dimensions
    """
    logger.info("Starting Power BI dataset export...")
    
    config = load_config()
    
    # Connect to database
    conn = psycopg2.connect(
        host=config['database']['host'],
        port=config['database']['port'],
        database=config['database']['database'],
        user=config['database']['user'],
        password=config['database']['password']
    )
    
    # SQL query to create denormalized dataset
    query = """
    SELECT 
        -- Transaction Details
        ft.transaction_id,
        ft.transaction_timestamp,
        ft.payment_status,
        ft.blockchain_hash,
        
        -- Date Dimensions
        dd.full_date as transaction_date,
        dd.year as transaction_year,
        dd.quarter as transaction_quarter,
        dd.month as transaction_month,
        dd.month_name as transaction_month_name,
        dd.day_name as transaction_day_name,
        dd.is_weekend,
        dd.season,
        
        -- Farmer Dimensions
        df.farmer_id,
        df.full_name as farmer_name,
        df.gender as farmer_gender,
        df.age_group as farmer_age_group,
        df.district as farmer_district,
        df.region as farmer_region,
        df.farm_size_acres,
        df.farm_size_category,
        df.primary_crop as farmer_primary_crop,
        df.cooperative_id,
        
        -- Product Dimensions
        dp.product_id,
        dp.product_name,
        dp.category as product_category,
        dp.category_group as product_category_group,
        dp.variety as product_variety,
        dp.is_perishable,
        dp.perishability_category,
        
        -- Market Dimensions
        dm.market_id,
        dm.market_name,
        dm.market_type,
        dm.district as market_district,
        dm.region as market_region,
        dm.capacity_category as market_capacity_category,
        
        -- Buyer Dimensions
        db.buyer_id,
        db.buyer_name,
        db.buyer_type,
        db.buyer_category,
        
        -- Payment Dimensions
        dpm.payment_method,
        dpm.payment_category,
        dpm.is_digital as is_digital_payment,
        
        -- Quality Dimensions
        dq.quality_grade,
        dq.quality_description,
        dq.quality_score,
        
        -- Measures
        ft.quantity_kg,
        ft.unit_price,
        ft.total_amount,
        ft.payment_fee,
        ft.net_amount,
        ft.transaction_count
        
    FROM dw.fact_transaction ft
    JOIN dw.dim_date dd ON ft.date_key = dd.date_key
    JOIN dw.dim_farmer df ON ft.farmer_key = df.farmer_key
    JOIN dw.dim_product dp ON ft.product_key = dp.product_key
    JOIN dw.dim_market dm ON ft.market_key = dm.market_key
    JOIN dw.dim_buyer db ON ft.buyer_key = db.buyer_key
    JOIN dw.dim_payment_method dpm ON ft.payment_key = dpm.payment_key
    JOIN dw.dim_quality dq ON ft.quality_key = dq.quality_key
    ORDER BY ft.transaction_timestamp DESC
    """
    
    logger.info("Executing query...")
    df = pd.read_sql_query(query, conn)
    
    # Close connection
    conn.close()
    
    logger.info(f"Retrieved {len(df)} rows")
    
    # Save to CSV
    output_path = '../../powerbi/powerbi_dataset.csv'
    df.to_csv(output_path, index=False)
    
    logger.info(f"Saved to {output_path}")
    
    # Print summary
    print("\n" + "="*80)
    print("POWER BI DATASET EXPORT COMPLETE")
    print("="*80)
    print(f"Total Rows: {len(df):,}")
    print(f"Total Revenue: UGX {df['total_amount'].sum():,.0f}")
    print(f"Date Range: {df['transaction_date'].min()} to {df['transaction_date'].max()}")
    print(f"Unique Farmers: {df['farmer_id'].nunique():,}")
    print(f"Unique Products: {df['product_id'].nunique():,}")
    print(f"Unique Markets: {df['market_id'].nunique():,}")
    print(f"\nFile saved: {output_path}")
    print("="*80)
    
    return df

if __name__ == "__main__":
    export_powerbi_dataset()
