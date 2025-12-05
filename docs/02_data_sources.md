# Data Source Selection & Collection

## 1. Overview

This section describes the data sources, collection methods, governance framework, and quality assurance processes for the agricultural supply chain data warehouse. All data sources are designed to be realistic and implementable in the Uganda context.

## 2. Data Source Categories

### 2.1 Primary Data Sources (Direct Collection)

#### 2.1.1 Farmer Registration Data
**Source**: Agricultural Extension Officers, Farmer Cooperatives  
**Collection Method**: Mobile application with offline capability  
**Frequency**: Initial registration + quarterly updates  
**Volume**: 10,000+ farmers

**Data Elements**:
- Farmer demographics (name, age, gender, contact)
- Location (district, sub-county, village, GPS coordinates)
- Farm characteristics (size, ownership type, irrigation)
- Crops grown (primary and secondary)
- Livestock (if applicable)
- Cooperative membership
- National ID or farmer registration number

**Collection Process**:
1. Extension officers visit farmers with tablets/smartphones
2. Data entered into mobile app (Android-based)
3. Offline storage with sync when connectivity available
4. GPS coordinates captured automatically
5. Photo ID verification
6. Digital signature or thumbprint

#### 2.1.2 Transaction Data
**Source**: Market collection points, cooperative buying centers  
**Collection Method**: Point-of-sale terminals, mobile money integration  
**Frequency**: Real-time (per transaction)  
**Volume**: 50,000+ transactions annually

**Data Elements**:
- Transaction ID (unique)
- Farmer ID (linked to registration)
- Product/crop type
- Quantity (kg or units)
- Quality grade (A, B, C)
- Price per unit
- Total amount
- Buyer/trader ID
- Market location
- Transaction timestamp
- Payment method (cash, mobile money, bank transfer)
- Blockchain transaction hash

**Collection Process**:
1. Farmer delivers produce to collection point
2. Quality inspection and grading
3. Weighing and quantity verification
4. Price negotiation or fixed price application
5. Transaction recorded in POS system
6. Simultaneous recording on blockchain
7. Payment processed (mobile money preferred)
8. Receipt generated (SMS + printed)

#### 2.1.3 Harvest Data
**Source**: Farmers (self-reported), field officers (verified)  
**Collection Method**: Mobile app, SMS, USSD  
**Frequency**: Per harvest season (2-3 times/year)  
**Volume**: 20,000+ harvest records annually

**Data Elements**:
- Farmer ID
- Crop type and variety
- Planting date
- Harvest date
- Quantity harvested
- Quality assessment
- Post-harvest losses
- Storage method
- Intended market

### 2.2 Secondary Data Sources (External Integration)

#### 2.2.1 Market Price Data
**Source**: Uganda Commodity Exchange (UCE), Ministry of Agriculture  
**Collection Method**: API integration, web scraping  
**Frequency**: Daily  
**Volume**: 365 records per commodity per market annually

**Data Elements**:
- Date
- Commodity
- Market location
- Wholesale price
- Retail price
- Price trend (up/down/stable)

**Integration Method**:
- Automated daily fetch via Python script
- API endpoints where available
- Web scraping for markets without APIs
- Data validation against historical ranges
- Storage in staging tables

#### 2.2.2 Weather Data
**Source**: Uganda National Meteorological Authority (UNMA)  
**Collection Method**: API integration  
**Frequency**: Daily  
**Volume**: 365 records per location annually

**Data Elements**:
- Date
- Location (weather station)
- Temperature (min, max, average)
- Rainfall (mm)
- Humidity
- Wind speed
- Weather conditions

**Purpose**: Correlate weather patterns with harvest yields and prices

#### 2.2.3 Government Subsidy Programs
**Source**: Ministry of Agriculture, Animal Industry and Fisheries (MAAIF)  
**Collection Method**: Data sharing agreements, CSV imports  
**Frequency**: Quarterly  
**Volume**: 5,000+ beneficiary records

**Data Elements**:
- Farmer ID
- Program name
- Subsidy type (seeds, fertilizer, equipment)
- Amount/value
- Distribution date
- Verification status

### 2.3 Blockchain-Generated Data

#### 2.3.1 Immutable Transaction Ledger
**Source**: Hyperledger Fabric blockchain network  
**Collection Method**: Chaincode execution  
**Frequency**: Real-time (per transaction)  
**Volume**: All transactions recorded immutably

**Data Elements**:
- Transaction hash
- Block number
- Timestamp
- Farmer wallet address
- Buyer wallet address
- Product details
- Quantity and price
- Previous transaction hash (traceability chain)

### 2.4 Identity Management Data

#### 2.4.1 Digital Identity Records
**Source**: Keycloak identity provider  
**Collection Method**: User registration and authentication  
**Frequency**: Initial registration + updates  
**Volume**: 10,000+ user accounts

**Data Elements**:
- User ID (Keycloak)
- Farmer ID (linked)
- Blockchain wallet address
- Authentication credentials (hashed)
- Roles and permissions
- Registration date
- Last login

## 3. Data Collection Methods

### 3.1 Mobile Data Collection

**Technology Stack**:
- Android mobile application
- Offline-first architecture (local SQLite database)
- Automatic sync when internet available
- GPS integration for location capture
- Camera for photo documentation

**Advantages**:
- Works in areas with poor connectivity
- Reduces data entry errors through validation
- Enables real-time data capture
- Lower cost than paper-based systems

**Challenges and Mitigations**:
| Challenge | Mitigation |
|-----------|------------|
| Limited smartphone penetration | Provide tablets to extension officers |
| Low digital literacy | Simplified UI with visual guides |
| Battery life in rural areas | Solar chargers, power banks |
| Data security | Encryption at rest and in transit |

### 3.2 Point-of-Sale (POS) Systems

**Deployment Locations**:
- Cooperative collection centers
- Major market hubs
- Aggregation points

**Features**:
- Barcode/QR code scanning for farmer ID
- Digital weighing scale integration
- Mobile money payment integration
- Blockchain transaction recording
- Receipt printing and SMS notification

### 3.3 API Integration

**External APIs**:
- Uganda Commodity Exchange (market prices)
- UNMA (weather data)
- Mobile money providers (payment verification)

**Integration Architecture**:
```
External API → Python ETL Script → Kafka Topic → Staging Table → Data Warehouse
```

### 3.4 Manual Data Entry (Legacy Systems)

For data not yet digitized:
- Web-based data entry portal
- Validation rules to ensure data quality
- Audit trail of all entries
- Supervisor approval workflow

## 4. Data Schemas and Structures

### 4.1 Farmer Registration Schema

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| farmer_id | VARCHAR(20) | PRIMARY KEY | Unique farmer identifier |
| national_id | VARCHAR(14) | UNIQUE | Uganda national ID |
| first_name | VARCHAR(50) | NOT NULL | Farmer's first name |
| last_name | VARCHAR(50) | NOT NULL | Farmer's last name |
| gender | CHAR(1) | CHECK (M/F) | Gender |
| date_of_birth | DATE | NOT NULL | Date of birth |
| phone_number | VARCHAR(15) | NOT NULL | Primary contact |
| district | VARCHAR(50) | NOT NULL | District location |
| subcounty | VARCHAR(50) | NOT NULL | Sub-county |
| village | VARCHAR(50) | NOT NULL | Village |
| gps_latitude | DECIMAL(10,8) | | Farm GPS latitude |
| gps_longitude | DECIMAL(11,8) | | Farm GPS longitude |
| farm_size_acres | DECIMAL(8,2) | CHECK > 0 | Farm size in acres |
| primary_crop | VARCHAR(50) | NOT NULL | Main crop grown |
| cooperative_id | VARCHAR(20) | FOREIGN KEY | Cooperative membership |
| registration_date | TIMESTAMP | DEFAULT NOW() | Registration timestamp |
| blockchain_wallet | VARCHAR(64) | UNIQUE | Blockchain wallet address |

### 4.2 Transaction Schema

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| transaction_id | VARCHAR(30) | PRIMARY KEY | Unique transaction ID |
| farmer_id | VARCHAR(20) | FOREIGN KEY | Farmer identifier |
| buyer_id | VARCHAR(20) | FOREIGN KEY | Buyer identifier |
| product_id | VARCHAR(20) | FOREIGN KEY | Product identifier |
| quantity_kg | DECIMAL(10,2) | CHECK > 0 | Quantity in kg |
| quality_grade | CHAR(1) | CHECK (A/B/C) | Quality grade |
| unit_price | DECIMAL(10,2) | CHECK > 0 | Price per kg |
| total_amount | DECIMAL(12,2) | CHECK > 0 | Total transaction value |
| market_id | VARCHAR(20) | FOREIGN KEY | Market location |
| transaction_date | TIMESTAMP | NOT NULL | Transaction timestamp |
| payment_method | VARCHAR(20) | NOT NULL | Payment method |
| blockchain_hash | VARCHAR(64) | UNIQUE | Blockchain tx hash |
| payment_status | VARCHAR(20) | NOT NULL | Paid/Pending/Failed |

### 4.3 Harvest Schema

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| harvest_id | VARCHAR(30) | PRIMARY KEY | Unique harvest ID |
| farmer_id | VARCHAR(20) | FOREIGN KEY | Farmer identifier |
| product_id | VARCHAR(20) | FOREIGN KEY | Product identifier |
| planting_date | DATE | NOT NULL | Planting date |
| harvest_date | DATE | NOT NULL | Harvest date |
| quantity_kg | DECIMAL(10,2) | CHECK > 0 | Quantity harvested |
| quality_assessment | VARCHAR(20) | | Quality rating |
| post_harvest_loss_pct | DECIMAL(5,2) | CHECK 0-100 | Loss percentage |
| storage_method | VARCHAR(50) | | Storage method |
| season | VARCHAR(20) | NOT NULL | Growing season |

### 4.4 Market Price Schema

| Field Name | Data Type | Constraints | Description |
|------------|-----------|-------------|-------------|
| price_id | VARCHAR(30) | PRIMARY KEY | Unique price record ID |
| product_id | VARCHAR(20) | FOREIGN KEY | Product identifier |
| market_id | VARCHAR(20) | FOREIGN KEY | Market identifier |
| price_date | DATE | NOT NULL | Price date |
| wholesale_price | DECIMAL(10,2) | CHECK > 0 | Wholesale price/kg |
| retail_price | DECIMAL(10,2) | CHECK > 0 | Retail price/kg |
| price_trend | VARCHAR(10) | | Up/Down/Stable |
| source | VARCHAR(50) | NOT NULL | Data source |

## 5. Data Governance Framework

### 5.1 Data Ownership

| Data Type | Owner | Steward | Access Rights |
|-----------|-------|---------|---------------|
| Farmer personal data | Individual farmer | Cooperative/Extension office | Farmer, authorized officers |
| Transaction data | Shared (farmer + buyer) | Market authority | Parties involved, auditors |
| Market prices | Public | Uganda Commodity Exchange | Public access |
| Blockchain ledger | Decentralized | Network validators | All network participants |
| Analytical insights | Government/Cooperatives | Data warehouse admin | Authorized stakeholders |

### 5.2 Data Privacy and Security

**Compliance**:
- Uganda Data Protection and Privacy Act, 2019
- General Data Protection Regulation (GDPR) principles
- Blockchain data minimization (no PII on-chain)

**Security Measures**:
1. **Encryption**:
   - Data at rest: AES-256 encryption
   - Data in transit: TLS 1.3
   - Blockchain: Cryptographic hashing

2. **Access Control**:
   - Role-based access control (RBAC) via Keycloak
   - Multi-factor authentication for sensitive operations
   - Audit logging of all data access

3. **Data Anonymization**:
   - Personal identifiers removed from analytical datasets
   - Aggregated reporting to prevent individual identification
   - Blockchain uses wallet addresses, not names

### 5.3 Data Quality Assurance

**Quality Dimensions**:
- **Accuracy**: Data correctly represents reality
- **Completeness**: All required fields populated
- **Consistency**: No contradictions across sources
- **Timeliness**: Data available when needed
- **Validity**: Data conforms to defined formats and rules

**Quality Control Processes**:

1. **Input Validation**:
   - Field-level validation (data type, range, format)
   - Cross-field validation (e.g., harvest date after planting date)
   - Referential integrity checks

2. **Automated Quality Checks**:
   ```python
   # Example quality check
   - Quantity > 0
   - Price within historical range (mean ± 3 std dev)
   - GPS coordinates within Uganda boundaries
   - Phone numbers match Uganda format
   ```

3. **Manual Review**:
   - Supervisor approval for high-value transactions
   - Periodic audits of random samples
   - Farmer verification of their own data

4. **Data Cleansing**:
   - Standardization (e.g., district names)
   - Deduplication
   - Outlier detection and correction

### 5.4 Metadata Management

**Metadata Strategy**:
- **Technical Metadata**: Data types, schemas, relationships
- **Business Metadata**: Definitions, business rules, ownership
- **Operational Metadata**: ETL lineage, refresh schedules, quality metrics

**Metadata Repository**:
- Centralized metadata catalog
- Data lineage tracking (source to report)
- Impact analysis for schema changes

## 6. Synthetic Data Generation Strategy

For this project, synthetic data will be generated to simulate realistic scenarios:

### 6.1 Data Generation Approach

**Tools**: Python with Faker library, NumPy, Pandas

**Realistic Constraints**:
- Uganda-specific names, locations, phone numbers
- Seasonal crop patterns (planting and harvest dates)
- Price correlations (wholesale < retail)
- Quantity distributions based on farm sizes
- Quality grade distributions (normal distribution centered on B)

### 6.2 Data Volume Requirements

| Entity | Minimum Rows | Target Rows |
|--------|--------------|-------------|
| Farmers | 1,000 | 2,000 |
| Products | 50 | 100 |
| Markets | 100 | 200 |
| Transactions | 1,000 | 10,000 |
| Harvests | 1,000 | 5,000 |
| Prices | 1,000 | 5,000 |
| **Total** | **4,150** | **22,400** |

### 6.3 Referential Integrity

All synthetic data will maintain referential integrity:
- Every transaction references valid farmer, product, and market
- Harvest dates align with crop growing seasons
- Transaction quantities do not exceed harvest quantities
- Prices align with market price data

## 7. Data Collection Workflow

```
1. Farmer Registration
   ↓
2. Digital Identity Creation (Keycloak)
   ↓
3. Blockchain Wallet Assignment
   ↓
4. Harvest Recording (Mobile App)
   ↓
5. Market Transaction (POS System)
   ↓
6. Blockchain Recording (Immutable)
   ↓
7. Kafka Streaming (Real-time)
   ↓
8. Data Warehouse Loading (Batch/Streaming)
   ↓
9. Analytics and Reporting (Power BI)
```

## 8. Data Retention and Archival

| Data Type | Retention Period | Archival Strategy |
|-----------|------------------|-------------------|
| Transaction data | 7 years | Compressed storage after 2 years |
| Farmer profiles | Active + 3 years | Archive inactive farmers |
| Market prices | 10 years | Aggregate to monthly after 3 years |
| Blockchain ledger | Permanent | Distributed immutable storage |
| Audit logs | 5 years | Compressed archive |

## 9. Conclusion

The data source selection and collection strategy is designed to be realistic, implementable, and aligned with Uganda's agricultural context. The combination of primary data collection (farmers, transactions), secondary data integration (market prices, weather), and blockchain-generated data creates a comprehensive information ecosystem. The governance framework ensures data quality, security, and compliance while enabling data-driven decision-making.

---

**Assessment Criteria Addressed**: Data Source Selection & Collection (10 marks)
- Realistic data sources identified
- Collection methods described
- Data governance framework
- Detailed schemas provided
- Quality assurance processes
- Synthetic data generation strategy (≥1,000 rows)
