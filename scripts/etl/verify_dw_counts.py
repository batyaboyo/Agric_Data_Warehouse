import psycopg2
import yaml

with open('etl_config.yaml', 'r') as f:
    config = yaml.safe_load(f)
    
db = config['database']
try:
    conn = psycopg2.connect(
        host=db['host'],
        port=db['port'],
        database=db['database'],
        user=db['user'],
        password=db['password']
    )
    cursor = conn.cursor()
    
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='dw' ORDER BY table_name")
    tables = [t[0] for t in cursor.fetchall()]
    
    print("\nDW Row Counts:")
    print("=" * 20)
    for t in tables:
        cursor.execute(f"SELECT count(*) FROM dw.{t}")
        count = cursor.fetchone()[0]
        print(f"{t}: {count}")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
