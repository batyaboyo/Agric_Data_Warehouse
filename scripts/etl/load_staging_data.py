"""
Load Staging Data
Script to load generated CSV datasets into PostgreSQL staging tables
"""
import psycopg2
import yaml
import os
import sys
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config(config_path='etl_config.yaml'):
    """Load configuration from YAML file"""
    if not os.path.exists(config_path):
        # Try looking in the current directory if relative path fails
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'etl_config.yaml')
        
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_load():
    # Configuration
    config = load_config()
    
    # Path to data directory (relative to this script or absolute)
    # Assuming script is in scripts/etl/ and data is in data/
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    data_dir = os.path.join(project_root, 'data')
    
    logger.info(f"Loading data from: {data_dir}")
    
    # Mapping of CSV files to Staging Tables
    # Order matters for logging purposes, but staging tables are independent
    datasets = [
        {"file": "products.csv", "table": "staging.stg_products"},
        {"file": "markets.csv", "table": "staging.stg_markets"},
        {"file": "buyers.csv", "table": "staging.stg_buyers"},
        {"file": "farmers.csv", "table": "staging.stg_farmers"},
        {"file": "weather.csv", "table": "staging.stg_weather"},
        {"file": "pricing.csv", "table": "staging.stg_pricing"},
        {"file": "transactions.csv", "table": "staging.stg_transactions"},
        # Harvests and subsidies might need specific handling if they have foreign keys, 
        # but staging tables usually don't enforce FKs. 
        # However, we'll load them last just in case.
        {"file": "harvests.csv", "table": "staging.stg_harvests"},
        {"file": "subsidies.csv", "table": "staging.stg_subsidies"},
    ]
    
    conn = None
    try:
        # Connect to Database
        db_config = config['database']
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        conn.autocommit = False
        cursor = conn.cursor()
        
        # Set search path explicitly
        cursor.execute("SET search_path TO staging, public;")
        logger.info("Set search_path to staging, public")
        
        logger.info("Database connection established")
        
        total_rows = 0
        
        for dataset in datasets:
            csv_file = dataset['file']
            table_name = dataset['table']
            file_path = os.path.join(data_dir, csv_file)
            
            if not os.path.exists(file_path):
                logger.warning(f"File not found: {file_path}. Skipping {table_name}.")
                continue
                
            logger.info(f"Processing {csv_file} -> {table_name}")
            
            try:
                # 1. Truncate Staging Table
                truncate_sql = f"TRUNCATE TABLE {table_name} CASCADE;"
                logger.info(f"Executing: {truncate_sql}")
                cursor.execute(truncate_sql)
                logger.info("  Truncated table")
                
                # 2. Load Data from CSV
                with open(file_path, 'r', encoding='utf-8') as f:
                    # Read header to get column names
                    header = f.readline().strip()
                    columns = header.split(',')
                    # Handle BOM if present
                    if columns[0].startswith('\ufeff'):
                        columns[0] = columns[0][1:]
                    
                    column_list = ", ".join(columns)
                    
                    # Reset file pointer to beginning
                    f.seek(0)
                    
                    # Use COPY command with specific columns
                    copy_sql = f"COPY {table_name} ({column_list}) FROM STDIN WITH CSV HEADER"
                    logger.info(f"Executing: COPY {table_name} ...")
                    cursor.copy_expert(copy_sql, f)
                    
                rows_loaded = cursor.rowcount
                total_rows += rows_loaded
                logger.info(f"  Loaded {rows_loaded} rows")
                
                # Commit after each table to checkpoint progress
                conn.commit()
                
            except Exception as table_error:
                logger.error(f"Failed to load {table_name}: {table_error}")
                conn.rollback()
                # Continue to next table instead of stopping completely? 
                # For debugging, let's continue to see which ones work.
                continue
            
        logger.info("=" * 40)
        logger.info(f"SUCCESS: Total rows loaded: {total_rows}")
        logger.info("=" * 40)
        
    except Exception as e:
        logger.error(f"Error during data validation/loading: {e}")
        import traceback
        logger.error(traceback.format_exc())
        if conn:
            conn.rollback()
        # Raise exception to ensure non-zero exit code on failure
        raise e
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    run_load()
