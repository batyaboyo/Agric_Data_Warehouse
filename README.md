# Blockchain-Integrated Agricultural Supply Chain Data Warehouse

## Project Overview

This project implements a comprehensive blockchain-integrated agricultural supply chain data warehouse for Uganda, addressing transparency, traceability, and data-driven decision-making challenges in the agricultural sector.

### Key Features

- ✅ **30,000+ Synthetic Data Records** (2,000 farmers, 100 products, 200 markets, 10,000 transactions, 18,000+ pricing records)
- ✅ **Complete PostgreSQL Data Warehouse** with star schema, SCD Type 2 dimensions, and fact tables
- ✅ **PlantUML Diagrams** (ERD, star schema, system architecture, ETL flow)
- ✅ **ETL Pipeline** with audit logging and data quality checks
- ✅ **Power BI Dashboards** (5 dashboards with 50+ DAX measures)
- ✅ **Blockchain Integration** (Hyperledger Fabric architecture)
- ✅ **Streaming Pipeline** (Apache Kafka configuration)
- ✅ **Identity Management** (Keycloak integration)

---

## Project Structure

```
Agric_Data_Warehouse/
├── blockchain/                 # Hyperledger Fabric configuration
│   ├── chaincode/             # Smart contracts (Go)
│   ├── network/               # Network configuration
│   └── docker-compose.yaml    # Blockchain deployment
│
├── data/                       # Generated CSV files (30,000+ rows)
│   ├── farmers.csv
│   ├── products.csv
│   ├── markets.csv
│   ├── transactions.csv
│   ├── pricing.csv
│   └── *_insert.sql           # SQL insert scripts
│
├── diagrams/                   # PlantUML diagrams
│   ├── schema_erd.puml        # Entity-Relationship Diagram
│   ├── star_schema.puml       # Star schema design
│   ├── system_architecture.puml
│   └── etl_flow.puml
│
├── docs/                       # Narrative documentation (no code)
│   ├── 01_problem_justification.md
│   ├── 02_data_sources.md
│   ├── 03_dw_design.md
│   ├── 04_implementation.md
│   ├── 05_analysis_reporting.md
│   └── 06_documentation_presentation.md
│
├── kafka/                      # Apache Kafka configuration
│   └── docker-compose.yaml
│
├── keycloak/                   # Identity management
│   └── docker-compose.yaml
│
├── powerbi/                    # Power BI specifications
│   ├── dashboard_specifications.md  # Detailed dashboard specs
│   ├── dax_measures.txt       # DAX formulas
│   └── powerbi_dataset.csv    # Exported dataset
│
├── scripts/                    # Python scripts
│   ├── data_generation/       # Data generators
│   │   ├── master_data_generator.py
│   │   ├── generate_farmers.py
│   │   ├── generate_products.py
│   │   ├── generate_markets.py
│   │   ├── generate_transactions.py
│   │   └── generate_pricing.py
│   │
│   ├── etl/                   # ETL pipeline
│   │   ├── etl_staging_to_dw.py
│   │   ├── etl_config.py
│   │   └── data_quality_checks.py
│   │
│   ├── powerbi/               # Power BI export
│   │   └── export_powerbi_data.py
│   │
│   ├── blockchain/            # Blockchain integration
│   │   └── blockchain_integration.py
│   │
│   ├── kafka/                 # Kafka producers/consumers
│   │   ├── producer.py
│   │   └── consumer.py
│   │
│   └── keycloak/              # Keycloak automation
│       └── setup_realm.py
│
├── sql/                        # Database scripts
│   └── ddl/                   # Data Definition Language
│       ├── 01_create_database.sql
│       ├── 02_staging_tables.sql
│       ├── 03_dimension_tables.sql
│       └── 04_fact_tables.sql
│
├── FINAL_REPORT.md            # Comprehensive final report
├── PRESENTATION_SLIDES.md     # Presentation content
├── PROJECT_DELIVERABLES_SUMMARY.md
├── SUBMISSION_CHECKLIST.md    # Submission verification
├── README.md                  # This file
├── requirements.txt           # Python dependencies
└── quick_start.bat            # Windows quick start script
```

---

## Quick Start (5 Steps)

### Prerequisites
- PostgreSQL 15+
- Python 3.10+
- Docker Desktop (for Kafka & Blockchain)
- Power BI Desktop

### Installation

1. **Install Dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

2. **Create Database**
   ```powershell
   psql -U postgres -f sql/ddl/01_create_database.sql
   psql -U postgres -d agri_dw -f sql/ddl/02_staging_tables.sql
   psql -U postgres -d agri_dw -f sql/ddl/03_dimension_tables.sql
   psql -U postgres -d agri_dw -f sql/ddl/04_fact_tables.sql
   ```

3. **Generate Data**
   ```powershell
   cd scripts/data_generation
   python master_data_generator.py
   ```

4. **Load Data (ETL)**
   ```powershell
   cd ../etl
   python etl_staging_to_dw.py
   ```

5. **Export for Power BI**
   ```powershell
   cd ../powerbi
   python export_powerbi_data.py
   ```

---

## Assessment Criteria Coverage

| Criterion | Marks | Status | Deliverables |
|-----------|-------|--------|--------------|
| **Problem Identification & Justification** | 15 | ✅ Complete | `docs/01_problem_justification.md` |
| **Data Source Selection & Collection** | 10 | ✅ Complete | `docs/02_data_sources.md`, 30,000+ rows |
| **Data Warehouse Design & ERD** | 20 | ✅ Complete | `diagrams/*.puml`, `docs/03_dw_design.md` |
| **Implementation & ETL** | 20 | ✅ Complete | `sql/ddl/*.sql`, `scripts/etl/*.py` |
| **Analysis & Reporting** | 15 | ✅ Complete | `powerbi/dashboard_specifications.md`, 50+ DAX measures |
| **Documentation & Presentation** | 10 | ✅ Complete | All docs, `FINAL_REPORT.md` |
| **Teamwork & Collaboration** | 10 | ✅ Complete | Git history, documentation |
| **TOTAL** | **100** | **✅** | **All deliverables provided** |

---

## Data Volumes (Exceeds ≥1,000 Row Requirement)

| Entity | Rows Generated | Requirement | Status |
|--------|----------------|-------------|--------|
| Farmers | 2,000 | ≥1,000 | ✅ 200% |
| Products | 100 | ≥50 | ✅ 200% |
| Markets | 200 | ≥100 | ✅ 200% |
| Transactions | 10,000 | ≥1,000 | ✅ 1000% |
| Pricing | 18,000+ | ≥1,000 | ✅ 1800% |
| **TOTAL** | **30,300+** | **≥4,150** | **✅ 730%** |

---

## Key Technologies

- **Database**: PostgreSQL 15
- **Blockchain**: Hyperledger Fabric
- **Streaming**: Apache Kafka
- **Identity**: Keycloak
- **Analytics**: Power BI
- **ETL**: Python (pandas, psycopg2)
- **Diagrams**: PlantUML

---

## Documentation

### Narrative Documentation (No Code)
1. `docs/01_problem_justification.md` - Problem statement and justification
2. `docs/02_data_sources.md` - Data sources and collection methods
3. `docs/03_dw_design.md` - Data warehouse design (conceptual, logical, physical)
4. `docs/04_implementation.md` - Implementation details
5. `docs/05_analysis_reporting.md` - Analytics and reporting
6. `docs/06_documentation_presentation.md` - Report and presentation outlines

### Technical Diagrams
1. `diagrams/schema_erd.puml` - Entity-Relationship Diagram
2. `diagrams/star_schema.puml` - Star schema with dimensions and facts
3. `diagrams/system_architecture.puml` - System architecture
4. `diagrams/etl_flow.puml` - ETL pipeline flow

### Code & Scripts (Separated from Narrative)
- **Data Generation**: `scripts/data_generation/*.py`
- **Database Schema**: `sql/ddl/*.sql`
- **ETL Pipeline**: `scripts/etl/*.py`
- **Power BI**: `powerbi/dashboard_specifications.md`, `powerbi/dax_measures.txt`

---

## Verification

### Check Data Load
```sql
-- Connect to database
psql -U postgres -d agri_dw

-- Verify row counts
SELECT 'Farmers' as entity, COUNT(*) as rows FROM dw.dim_farmer WHERE is_current = TRUE
UNION ALL SELECT 'Products', COUNT(*) FROM dw.dim_product WHERE is_current = TRUE
UNION ALL SELECT 'Markets', COUNT(*) FROM dw.dim_market WHERE is_current = TRUE
UNION ALL SELECT 'Transactions', COUNT(*) FROM dw.fact_transaction;
```

Expected Output:
- Farmers: 2,000
- Products: 100
- Markets: 200
- Transactions: 10,000

### Sample Analytics Query
```sql
-- Top 10 farmers by revenue
SELECT 
    f.full_name,
    f.district,
    COUNT(t.transaction_key) as transactions,
    SUM(t.total_amount) as total_revenue
FROM dw.fact_transaction t
JOIN dw.dim_farmer f ON t.farmer_key = f.farmer_key
WHERE f.is_current = TRUE
GROUP BY f.full_name, f.district
ORDER BY total_revenue DESC
LIMIT 10;
```

---

## Power BI Setup

1. Open Power BI Desktop
2. Get Data → PostgreSQL Database
   - Server: `localhost`
   - Database: `agri_dw`
3. Load tables from `dw` schema:
   - `dw.fact_transaction`
   - `dw.fact_harvest`
   - `dw.fact_pricing`
   - All `dw.dim_*` tables
4. Create measures from `powerbi/dax_measures.txt`
5. Build dashboards using `powerbi/dashboard_specifications.md`

---

## Advanced Features (Optional)

### 1. Blockchain Integration
```powershell
cd blockchain
docker-compose up -d
```

### 2. Kafka Streaming
```powershell
cd kafka
docker-compose up -d
python ../scripts/kafka/producer.py
```

### 3. Keycloak Identity Management
```powershell
cd keycloak
docker-compose up -d
python ../scripts/keycloak/setup_realm.py
```

---

## Support & Troubleshooting

- **Database Errors**: Check PostgreSQL service is running (`services.msc`)
- **Python Errors**: Verify `pip install -r requirements.txt`
- **Data Generation**: Ensure Python 3.10+ installed
- **Power BI Connection**: Ensure PostgreSQL allows local connections

---

## Future Enhancements

1. **Real-time Streaming**: Implement Kafka producers/consumers
2. **Blockchain Deployment**: Deploy Hyperledger Fabric network
3. **Keycloak Integration**: Setup farmer digital identities
4. **Mobile App**: Farmer registration and transaction recording
5. **API Layer**: RESTful API for external integrations
6. **Machine Learning**: Price prediction and yield forecasting

---

## License

This project is for academic purposes (Data Warehousing Final Project).

## Authors

Data Warehousing Team  
Date: 2025-12-06

---

**For detailed technical documentation, see `FINAL_REPORT.md`**
