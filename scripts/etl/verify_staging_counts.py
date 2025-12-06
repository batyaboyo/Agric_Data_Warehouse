"""
Verify Staging Counts
Checks row counts in staging tables
"""
import psycopg2
import yaml
import os

def load_config(config_path='etl_config.yaml'):
    if not os.path.exists(config_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'etl_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def check_counts():
    config = load_config()
    db_config = config['database']
    
    tables = [
        "staging.stg_products",
        "staging.stg_markets",
        "staging.stg_buyers",
        "staging.stg_farmers",
        "staging.stg_weather",
        "staging.stg_pricing",
        "staging.stg_transactions",
        "staging.stg_harvests",
        "staging.stg_subsidies"
    ]
    
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        print("Staging Table Row Counts:")
        print("-" * 30)
        
        total_rows = 0
        for table in tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"{table}: {count}")
                total_rows += count
            except Exception as e:
                print(f"{table}: ERROR - {e}")
                conn.rollback()
        
        print("-" * 30)
        print(f"Total Rows: {total_rows}")
        
    except Exception as e:
        print(f"Connection Failed: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    check_counts()
