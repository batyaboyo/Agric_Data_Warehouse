"""
Initialize Database
Executes DDL scripts to set up schemas and tables
"""
import psycopg2
import yaml
import os
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_config(config_path='etl_config.yaml'):
    if not os.path.exists(config_path):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_dir, 'etl_config.yaml')
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def run_init():
    config = load_config()
    db_config = config['database']
    
    # Define DDL files in order
    # Assuming scripts are in sql/ddl relative to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(script_dir))
    ddl_dir = os.path.join(project_root, 'sql', 'ddl')
    
    ddl_files = [
        "02_staging_tables.sql",
        "03_dimension_tables.sql",
        "04_fact_tables.sql"
    ]
    
    conn = None
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        conn.autocommit = False # Use transaction
        cursor = conn.cursor()
        
        logger.info(f"Connected to {db_config['database']}")
        
        # Create staging schema if it doesn't exist (it's in search_path usually but safer to create)
        cursor.execute("CREATE SCHEMA IF NOT EXISTS staging;")
        cursor.execute("CREATE SCHEMA IF NOT EXISTS dw;")
        logger.info("Ensured schemas 'staging' and 'dw' exist")

        for ddl_file in ddl_files:
            file_path = os.path.join(ddl_dir, ddl_file)
            if not os.path.exists(file_path):
                logger.warning(f"DDL file not found: {file_path}")
                continue
                
            logger.info(f"Executing {ddl_file}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                sql_content = f.read()
                cursor.execute(sql_content)
                
        conn.commit()
        logger.info("=" * 40)
        logger.info("Database initialized successfully")
        logger.info("=" * 40)
        
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    run_init()
