# Complete Data Dictionary
## Agricultural Supply Chain Data Warehouse

---

## Staging Schema Tables

### stg_farmers
**Purpose**: Staging table for farmer registration data

| Column Name | Data Type | Constraints | Description | Example |
|-------------|-----------|-------------|-------------|---------|
| farmer_id | VARCHAR(20) | PRIMARY KEY | Unique farmer identifier | FMR000001 |
| national_id | VARCHAR(14) | UNIQUE | Uganda national ID | CM1234567890123 |
| first_name | VARCHAR(50) | NOT NULL | Farmer's first name | Mukasa |
| last_name | VARCHAR(50) | NOT NULL | Farmer's last name | Musoke |
| gender | CHAR(1) | CHECK (M/F) | Gender | M |
| date_of_birth | DATE | | Date of birth | 1985-03-15 |
| phone_number | VARCHAR(15) | | Primary contact number | 0700123456 |
| district | VARCHAR(50) | | District location | Kampala |
| subcounty | VARCHAR(50) | | Sub-county | Kampala Central |
| village | VARCHAR(50) | | Village name | Nakasero Village |
| gps_latitude | DECIMAL(10,8) | | GPS latitude | 0.347596 |
| gps_longitude | DECIMAL(11,8) | | GPS longitude | 32.582520 |
| farm_size_acres | DECIMAL(8,2) | CHECK > 0 | Farm size in acres | 5.50 |
| primary_crop | VARCHAR(50) | | Main crop grown | Maize |
| cooperative_id | VARCHAR(20) | | Cooperative membership | COOP001 |
| blockchain_wallet | VARCHAR(64) | UNIQUE | Blockchain wallet address | 0x1234abcd... |
| registration_date | TIMESTAMP | | Registration timestamp | 2024-01-15 10:30:00 |
| is_active | BOOLEAN | DEFAULT TRUE | Active status | TRUE |
| loaded_at | TIMESTAMP | DEFAULT NOW() | Load timestamp | 2024-12-04 10:00:00 |

### stg_products
**Purpose**: Staging table for agricultural products

| Column Name | Data Type | Constraints | Description | Example |
|-------------|-----------|-------------|-------------|---------|
| product_id | VARCHAR(20) | PRIMARY KEY | Unique product identifier | PRD0001 |
| product_name | VARCHAR(50) | NOT NULL | Product name | Maize |
| category | VARCHAR(30) | | Product category | Cereals |
| variety | VARCHAR(50) | | Product variety | Longe 10H |
| unit_of_measure | VARCHAR(10) | | Unit of measure | kg |
| season | VARCHAR(20) | | Growing season | Both |
| avg_growing_days | INTEGER | | Average growing period | 120 |
| is_perishable | BOOLEAN | | Perishability flag | FALSE |
| loaded_at | TIMESTAMP | DEFAULT NOW() | Load timestamp | 2024-12-04 10:00:00 |

### stg_transactions
**Purpose**: Staging table for market transactions

| Column Name | Data Type | Constraints | Description | Example |
|-------------|-----------|-------------|-------------|---------|
| transaction_id | VARCHAR(30) | PRIMARY KEY | Unique transaction ID | TXN00000001 |
| farmer_id | VARCHAR(20) | | Farmer identifier | FMR000001 |
| buyer_id | VARCHAR(20) | | Buyer identifier | BYR0001 |
| product_id | VARCHAR(20) | | Product identifier | PRD0001 |
| market_id | VARCHAR(20) | | Market identifier | MKT0001 |
| quantity_kg | DECIMAL(10,2) | CHECK > 0 | Quantity in kg | 100.50 |
| quality_grade | CHAR(1) | CHECK (A/B/C) | Quality grade | A |
| unit_price | DECIMAL(10,2) | CHECK > 0 | Price per kg (UGX) | 1500.00 |
| total_amount | DECIMAL(12,2) | CHECK > 0 | Total transaction value | 150750.00 |
| transaction_date | TIMESTAMP | NOT NULL | Transaction timestamp | 2024-12-04 14:30:00 |
| payment_method | VARCHAR(20) | | Payment method | Mobile Money |
| payment_status | VARCHAR(20) | | Payment status | Paid |
| blockchain_hash | VARCHAR(64) | UNIQUE | Blockchain tx hash | 0xabcd1234... |
| loaded_at | TIMESTAMP | DEFAULT NOW() | Load timestamp | 2024-12-04 15:00:00 |

---

## Data Warehouse Schema - Dimensions

### dim_farmer (SCD Type 2)
**Purpose**: Farmer dimension with historical tracking

| Column Name | Data Type | Description | Business Rule |
|-------------|-----------|-------------|---------------|
| farmer_key | BIGSERIAL | Surrogate key | Auto-generated |
| farmer_id | VARCHAR(20) | Natural key | From source system |
| full_name | VARCHAR(100) | Full name | first_name + last_name |
| age_group | VARCHAR(20) | Age category | Youth/Adult/Senior |
| farm_size_category | VARCHAR(20) | Farm size category | Small/Medium/Large |
| region | VARCHAR(30) | Region | Central/Eastern/Northern/Western |
| effective_date | DATE | SCD start date | When version became active |
| end_date | DATE | SCD end date | 9999-12-31 for current |
| is_current | BOOLEAN | Current version flag | TRUE for latest version |
| version | INTEGER | Version number | Increments with each change |

**SCD Type 2 Example**:
```
farmer_key | farmer_id | farm_size_acres | effective_date | end_date   | is_current | version
-----------|-----------|-----------------|----------------|------------|------------|--------
1          | FMR000001 | 2.5             | 2024-01-01     | 2024-06-30 | FALSE      | 1
2          | FMR000001 | 5.0             | 2024-07-01     | 9999-12-31 | TRUE       | 2
```

### dim_product (SCD Type 2)
**Purpose**: Product dimension with historical tracking

| Column Name | Data Type | Description | Derived Logic |
|-------------|-----------|-------------|---------------|
| product_key | BIGSERIAL | Surrogate key | Auto-generated |
| product_id | VARCHAR(20) | Natural key | From source |
| category_group | VARCHAR(30) | Category grouping | Grains & Legumes / Roots & Tubers / Horticulture / Cash Crops |
| growing_period_category | VARCHAR(20) | Growing period | Short (<3mo) / Medium (3-6mo) / Long (6+mo) |
| perishability_category | VARCHAR(20) | Perishability | Perishable / Non-Perishable |

### dim_date
**Purpose**: Date dimension for time-based analysis

| Column Name | Data Type | Description | Calculation |
|-------------|-----------|-------------|-------------|
| date_key | INTEGER | Surrogate key (YYYYMMDD) | TO_CHAR(date, 'YYYYMMDD')::INTEGER |
| full_date | DATE | Actual date | |
| fiscal_year | INTEGER | Fiscal year | Year + 1 if month >= 7 |
| fiscal_quarter | INTEGER | Fiscal quarter | 1-4 based on fiscal year |
| season | VARCHAR(20) | Agricultural season | First Season (Mar-May) / Second Season (Sep-Nov) / Off Season |

**Season Logic**:
- First Season: March, April, May
- Second Season: September, October, November
- Off Season: All other months

---

## Data Warehouse Schema - Facts

### fact_transaction
**Purpose**: Transaction fact table (immutable)

| Column Name | Data Type | Measure Type | Description |
|-------------|-----------|--------------|-------------|
| transaction_key | BIGSERIAL | | Surrogate key |
| farmer_key | BIGINT | | FK to dim_farmer |
| product_key | BIGINT | | FK to dim_product |
| date_key | INTEGER | | FK to dim_date |
| quantity_kg | DECIMAL(10,2) | Additive | Quantity sold |
| unit_price | DECIMAL(10,2) | Non-additive | Price per kg |
| total_amount | DECIMAL(12,2) | Additive | Total transaction value |
| payment_fee | DECIMAL(10,2) | Additive | Transaction fee |
| net_amount | DECIMAL(12,2) | Additive | Amount after fees |
| transaction_count | INTEGER | Additive | Always 1 (for counting) |

**Measure Calculations**:
- `net_amount = total_amount - payment_fee`
- `payment_fee = total_amount * payment_fee_pct / 100`

### fact_pricing
**Purpose**: Daily pricing snapshot

| Column Name | Data Type | Measure Type | Description |
|-------------|-----------|--------------|-------------|
| pricing_key | BIGSERIAL | | Surrogate key |
| product_key | BIGINT | | FK to dim_product |
| market_key | BIGINT | | FK to dim_market |
| date_key | INTEGER | | FK to dim_date |
| wholesale_price | DECIMAL(10,2) | Semi-additive | Wholesale price |
| retail_price | DECIMAL(10,2) | Semi-additive | Retail price |
| price_spread | DECIMAL(10,2) | Semi-additive | Retail - Wholesale |
| price_spread_pct | DECIMAL(5,2) | Semi-additive | (Spread / Wholesale) * 100 |

**Note**: Prices are semi-additive (can sum across products/markets but not across time)

---

## Business Rules

### Data Quality Rules

1. **Referential Integrity**
   - All foreign keys must reference valid dimension records
   - Orphan records rejected during ETL

2. **Data Validation**
   - `farm_size_acres > 0`
   - `quantity_kg > 0`
   - `unit_price > 0`
   - `total_amount = quantity_kg * unit_price` (within 1% tolerance)
   - `wholesale_price < retail_price`

3. **Completeness**
   - Required fields must not be NULL
   - Minimum 95% completeness for critical fields

### Derived Attributes

1. **Age Group**
   ```sql
   CASE 
       WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 30 THEN 'Youth (18-29)'
       WHEN EXTRACT(YEAR FROM AGE(date_of_birth)) < 50 THEN 'Adult (30-49)'
       ELSE 'Senior (50+)'
   END
   ```

2. **Farm Size Category**
   ```sql
   CASE 
       WHEN farm_size_acres < 2 THEN 'Small (< 2 acres)'
       WHEN farm_size_acres < 10 THEN 'Medium (2-10 acres)'
       ELSE 'Large (10+ acres)'
   END
   ```

3. **Region**
   ```sql
   CASE 
       WHEN district IN ('Kampala', 'Wakiso', 'Mukono', 'Masaka', 'Luwero') THEN 'Central'
       WHEN district IN ('Jinja', 'Mbale', 'Tororo', 'Iganga', 'Soroti') THEN 'Eastern'
       WHEN district IN ('Gulu', 'Lira', 'Kitgum', 'Arua', 'Nebbi') THEN 'Northern'
       ELSE 'Western'
   END
   ```

---

## Lookup Tables

### Quality Grades

| Grade | Description | Score | Price Premium % |
|-------|-------------|-------|-----------------|
| A | Premium Quality | 100 | +25% |
| B | Standard Quality | 80 | 0% |
| C | Below Standard | 60 | -20% |

### Payment Methods

| Method | Category | Digital | Fee % | Settlement Days |
|--------|----------|---------|-------|-----------------|
| Mobile Money | Digital | TRUE | 1.5% | 0 |
| Cash | Physical | FALSE | 0% | 0 |
| Bank Transfer | Digital | TRUE | 0.5% | 1 |
| Cooperative Account | Digital | TRUE | 0% | 0 |

---

## Metadata

### Data Lineage

```
Source System → Kafka Topic → Staging Table → Dimension/Fact → Power BI
```

### Refresh Schedule

| Table | Refresh Frequency | Method |
|-------|-------------------|--------|
| Staging Tables | Real-time | Kafka streaming |
| Dimension Tables | Daily (2 AM) | ETL pipeline |
| Fact Tables | Daily (3 AM) | ETL pipeline |
| Summary Tables | Daily (4 AM) | ETL pipeline |

### Data Retention

| Schema | Retention Period | Archival Strategy |
|--------|------------------|-------------------|
| Staging | 30 days | Delete after ETL |
| DW | 7 years | Compress after 2 years |
| Audit | 5 years | Archive to cold storage |

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
