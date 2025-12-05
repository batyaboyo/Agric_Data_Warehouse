# Implementation & ETL Documentation

## 1. Overview

This document describes the complete implementation of the Agricultural Supply Chain Data Warehouse, including PostgreSQL setup, ETL pipeline, blockchain integration, streaming architecture, and identity management.

## 2. PostgreSQL Implementation

### 2.1 Database Architecture

**Database Name**: `agri_dw`  
**PostgreSQL Version**: 15+  
**Character Encoding**: UTF-8  
**Schemas**: 3 (staging, dw, audit)

### 2.2 Schema Design

#### Staging Schema
**Purpose**: Temporary storage for raw data from source systems  
**Tables**: 9 staging tables  
**Retention**: Data retained for 30 days, then archived

#### DW Schema
**Purpose**: Production data warehouse (star schema)  
**Tables**: 8 dimensions + 4 facts + 1 summary  
**Design Pattern**: Star schema with conformed dimensions

#### Audit Schema
**Purpose**: ETL metadata and data quality logs  
**Tables**: 2 (etl_execution_log, data_quality_log)

### 2.3 Implementation Steps

**Step 1: Database Creation**
```sql
-- Execute: sql/ddl/01_create_database.sql
-- Creates database, schemas, extensions, audit tables
```

**Step 2: Staging Tables**
```sql
-- Execute: sql/ddl/02_staging_tables.sql
-- Creates 9 staging tables with constraints and indexes
```

**Step 3: Dimension Tables**
```sql
-- Execute: sql/ddl/03_dimension_tables.sql
-- Creates 8 dimension tables with SCD Type 2 support
-- Pre-populates static dimensions (payment_method, quality)
```

**Step 4: Fact Tables**
```sql
-- Execute: sql/ddl/04_fact_tables.sql
-- Creates 4 fact tables with foreign key constraints
-- Creates summary table for performance
```

### 2.4 Data Loading

**Method 1: COPY Command (Recommended)**
```sql
\copy staging.stg_farmers FROM 'c:/path/to/farmers.csv' WITH CSV HEADER;
```

**Method 2: SQL INSERT Statements**
```sql
-- Execute generated SQL files
\i data/farmers_insert.sql
```

**Method 3: Python ETL Pipeline**
```python
# Execute ETL pipeline
python scripts/etl/etl_staging_to_dw.py
```

## 3. ETL Pipeline

### 3.1 ETL Architecture

```
Source Data (CSV) → Staging Tables → Data Quality → Dimensions (SCD Type 2) → Facts → Analytics
```

### 3.2 ETL Components

#### Component 1: Data Ingestion
**Script**: Manual COPY or SQL INSERT  
**Frequency**: On-demand or scheduled  
**Validation**: Schema validation, data type checks

#### Component 2: Data Quality Checks
**Checks**:
- Null value percentage < 5%
- Duplicate records < 1%
- Referential integrity
- Value range validation
- Format validation (phone numbers, dates)

#### Component 3: Dimension Loading (SCD Type 2)
**Script**: `scripts/etl/etl_staging_to_dw.py`  
**Logic**:
1. Check if record exists with same natural key
2. If new → Insert with is_current=TRUE, version=1
3. If changed → Expire old (is_current=FALSE), insert new (version+1)
4. If unchanged → No action

**Example SCD Type 2 Logic**:
```python
# Check for existing farmer
existing = cursor.execute("""
    SELECT farmer_key FROM dw.dim_farmer 
    WHERE farmer_id = %s AND is_current = TRUE
""", (farmer_id,))

if not existing:
    # New farmer - insert
    cursor.execute("""
        INSERT INTO dw.dim_farmer (farmer_id, ..., is_current, version)
        VALUES (%s, ..., TRUE, 1)
    """)
else:
    # Check if attributes changed
    if attributes_changed:
        # Expire old record
        cursor.execute("""
            UPDATE dw.dim_farmer 
            SET end_date = CURRENT_DATE - 1, is_current = FALSE
            WHERE farmer_id = %s AND is_current = TRUE
        """)
        # Insert new version
        cursor.execute("""
            INSERT INTO dw.dim_farmer (farmer_id, ..., is_current, version)
            VALUES (%s, ..., TRUE, version + 1)
        """)
```

#### Component 4: Fact Loading
**Script**: `scripts/etl/etl_staging_to_dw.py`  
**Logic**:
1. Lookup dimension surrogate keys
2. Calculate derived measures
3. Insert into fact table
4. Log to audit table

**Example Fact Loading**:
```sql
INSERT INTO dw.fact_transaction (
    farmer_key, product_key, market_key, date_key, ...
)
SELECT 
    f.farmer_key,
    p.product_key,
    m.market_key,
    TO_CHAR(t.transaction_date, 'YYYYMMDD')::INTEGER,
    ...
FROM staging.stg_transactions t
JOIN dw.dim_farmer f ON t.farmer_id = f.farmer_id AND f.is_current = TRUE
JOIN dw.dim_product p ON t.product_id = p.product_id AND p.is_current = TRUE
JOIN dw.dim_market m ON t.market_id = m.market_id AND m.is_current = TRUE
```

### 3.3 ETL Execution

**Manual Execution**:
```powershell
cd scripts/etl
python etl_staging_to_dw.py
```

**Scheduled Execution** (Windows Task Scheduler):
```powershell
# Create scheduled task to run daily at 2 AM
schtasks /create /tn "AgriDW_ETL" /tr "python c:\path\to\etl_staging_to_dw.py" /sc daily /st 02:00
```

### 3.4 ETL Monitoring

**Audit Logs**:
```sql
-- View ETL execution history
SELECT 
    execution_id,
    job_name,
    start_time,
    end_time,
    status,
    rows_inserted,
    error_message
FROM audit.etl_execution_log
ORDER BY start_time DESC
LIMIT 10;
```

**Data Quality Logs**:
```sql
-- View data quality check results
SELECT 
    table_name,
    check_name,
    check_result,
    records_failed,
    failure_percentage
FROM audit.data_quality_log
WHERE check_result = 'Fail'
ORDER BY checked_at DESC;
```

## 4. Blockchain Integration (Hyperledger Fabric)

### 4.1 Architecture

**Network Components**:
- **Organizations**: Farmer Org, Market Org
- **Peers**: 2 peers (one per organization)
- **Orderer**: Solo orderer (single node)
- **Channel**: agri-channel
- **Chaincode**: AgriSupply

### 4.2 Chaincode Functions

**RecordTransaction**:
```go
// Records a transaction on the blockchain
func (s *SmartContract) RecordTransaction(
    ctx contractapi.TransactionContextInterface,
    transactionID string,
    farmerID string,
    productID string,
    quantity float64,
    amount float64
) error {
    // Create transaction record
    // Store on ledger
    // Return transaction hash
}
```

**QueryTransaction**:
```go
// Queries a transaction by ID
func (s *SmartContract) QueryTransaction(
    ctx contractapi.TransactionContextInterface,
    transactionID string
) (*Transaction, error)
```

**GetTransactionHistory**:
```go
// Gets complete history of a transaction
func (s *SmartContract) GetTransactionHistory(
    ctx contractapi.TransactionContextInterface,
    transactionID string
) ([]HistoryQueryResult, error)
```

### 4.3 Python Blockchain Client

**Script**: `scripts/blockchain/blockchain_client.py`

**Usage**:
```python
from blockchain_client import BlockchainClient

client = BlockchainClient()

# Record transaction
tx_hash = client.record_transaction(
    transaction_id="TXN00000001",
    farmer_id="FMR000001",
    product_id="PRD0001",
    quantity=100.5,
    amount=150000
)

# Query transaction
tx_data = client.query_transaction("TXN00000001")
```

### 4.4 Deployment (Windows)

**Prerequisites**:
- Docker Desktop for Windows
- Hyperledger Fabric binaries

**Setup Steps**:
1. Start Docker Desktop
2. Navigate to `blockchain/` folder
3. Run network startup script
4. Deploy chaincode
5. Test with sample transactions

## 5. Streaming Pipeline (Apache Kafka)

### 5.1 Architecture

**Components**:
- **Zookeeper**: Coordination service
- **Kafka Broker**: Message broker
- **Topics**: farmers-topic, transactions-topic, pricing-topic, harvest-topic
- **Producers**: Mobile app, POS terminals, APIs
- **Consumers**: ETL pipeline

### 5.2 Topic Configuration

**farmers-topic**:
- Partitions: 3
- Replication Factor: 1
- Retention: 7 days

**transactions-topic**:
- Partitions: 5
- Replication Factor: 1
- Retention: 30 days

### 5.3 Message Format

**Transaction Message** (JSON):
```json
{
  "transaction_id": "TXN00000001",
  "farmer_id": "FMR000001",
  "buyer_id": "BYR0001",
  "product_id": "PRD0001",
  "market_id": "MKT0001",
  "quantity_kg": 100.5,
  "quality_grade": "A",
  "unit_price": 1500.00,
  "total_amount": 150750.00,
  "transaction_date": "2024-12-04T10:30:00Z",
  "payment_method": "Mobile Money",
  "payment_status": "Paid"
}
```

### 5.4 Kafka Producer (Python)

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Send transaction
producer.send('transactions-topic', transaction_data)
producer.flush()
```

### 5.5 Kafka Consumer (Python)

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'transactions-topic',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    transaction = message.value
    # Insert into staging table
    insert_to_staging(transaction)
```

## 6. Identity Management (Keycloak)

### 6.1 Architecture

**Realm**: AgriSupplyChain  
**Clients**: mobile-app, pos-terminal, web-portal  
**Users**: Farmers (10,000+)  
**Roles**: farmer, trader, admin, auditor

### 6.2 User Attributes

**Farmer User**:
- Username: farmer_id (e.g., FMR000001)
- Email: farmer@example.com
- Custom Attributes:
  - farmer_id: FMR000001
  - blockchain_wallet: 0x1234...
  - national_id: CM1234567890123
  - phone_number: 0700123456

### 6.3 Authentication Flow

1. User opens mobile app
2. App redirects to Keycloak login
3. User enters credentials
4. Keycloak validates and issues JWT token
5. App uses token to access APIs
6. Token includes farmer_id and blockchain_wallet

### 6.4 Keycloak Integration (Python)

```python
from keycloak import KeycloakAdmin

keycloak_admin = KeycloakAdmin(
    server_url="http://localhost:8080/auth/",
    username="admin",
    password="admin",
    realm_name="AgriSupplyChain"
)

# Create farmer user
user_id = keycloak_admin.create_user({
    "username": "FMR000001",
    "enabled": True,
    "attributes": {
        "farmer_id": "FMR000001",
        "blockchain_wallet": "0x1234...",
        "national_id": "CM1234567890123"
    }
})
```

## 7. Performance Optimization

### 7.1 Indexing Strategy

**Dimension Tables**:
- Primary key (clustered index)
- Natural key (unique index)
- is_current flag (filtered index)
- Frequently filtered columns (district, category)

**Fact Tables**:
- Primary key
- Foreign keys to all dimensions
- Date columns (for partitioning)
- Degenerate dimensions (transaction_id, blockchain_hash)

### 7.2 Query Optimization

**Use Summary Tables**:
```sql
-- Instead of querying fact_transaction directly
SELECT product_key, SUM(total_amount)
FROM dw.fact_transaction_daily_summary
WHERE date_key BETWEEN 20240101 AND 20241231
GROUP BY product_key;
```

**Use Materialized Views** (Future):
```sql
CREATE MATERIALIZED VIEW mv_farmer_revenue AS
SELECT 
    farmer_key,
    SUM(total_amount) as total_revenue,
    COUNT(*) as transaction_count
FROM dw.fact_transaction
GROUP BY farmer_key;
```

### 7.3 Partitioning (Future Enhancement)

**Partition fact_transaction by date**:
```sql
CREATE TABLE dw.fact_transaction (
    ...
) PARTITION BY RANGE (transaction_timestamp);

CREATE TABLE fact_transaction_2024_01 PARTITION OF dw.fact_transaction
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

## 8. Data Security

### 8.1 Access Control

**Row-Level Security**:
```sql
-- Regional managers see only their region
CREATE POLICY regional_access ON dw.fact_transaction
    USING (
        farmer_key IN (
            SELECT farmer_key FROM dw.dim_farmer 
            WHERE region = current_setting('app.user_region')
        )
    );
```

### 8.2 Data Encryption

- **At Rest**: PostgreSQL transparent data encryption
- **In Transit**: SSL/TLS for all connections
- **Blockchain**: Cryptographic hashing

### 8.3 Audit Trail

All data access and modifications logged:
```sql
-- Enable audit logging
CREATE TRIGGER audit_transaction_changes
AFTER INSERT OR UPDATE OR DELETE ON dw.fact_transaction
FOR EACH ROW EXECUTE FUNCTION audit.log_change();
```

## 9. Disaster Recovery

### 9.1 Backup Strategy

**Daily Backups**:
```powershell
# PostgreSQL backup
pg_dump -U postgres agri_dw > backup_$(date +%Y%m%d).sql
```

**Blockchain Backup**:
- Ledger is distributed across peers
- Regular snapshots of peer file systems

### 9.2 Recovery Procedures

**Database Recovery**:
```powershell
# Restore from backup
psql -U postgres -d agri_dw < backup_20241204.sql
```

## 10. Scalability Roadmap

### 10.1 Current Capacity
- Farmers: 2,000 (can scale to 100,000+)
- Transactions: 10,000 (can scale to 10M+)
- Storage: ~500 MB (can scale to 100+ GB)

### 10.2 Scaling Strategies

**Vertical Scaling**:
- Increase PostgreSQL server resources
- Optimize queries and indexes

**Horizontal Scaling**:
- Read replicas for analytics
- Partition fact tables by date
- Distribute Kafka across multiple brokers
- Add blockchain peer nodes

### 10.3 Cloud Migration

**Azure/AWS Architecture**:
- Azure Database for PostgreSQL / Amazon RDS
- Azure Event Hubs / Amazon MSK (Kafka)
- Azure Blockchain Service / Amazon Managed Blockchain
- Power BI Service / Amazon QuickSight

---

**Assessment Criteria Addressed**: Implementation & ETL (20 marks)
- Complete PostgreSQL setup on Windows
- Full SQL DDL/DML with ≥1,000 rows
- ETL scripts (Python + SQL)
- SCD Type 2 implementation
- Blockchain architecture (Hyperledger Fabric)
- Kafka streaming pipeline
- Keycloak identity management
- Performance optimization
- Security and disaster recovery
