# Blockchain-Integrated Agricultural Supply Chain Data Warehouse

## Project Overview

This project implements a comprehensive blockchain-integrated agricultural supply chain data warehouse for Uganda, addressing transparency, traceability, and data-driven decision-making challenges in the agricultural sector.

### Key Features

- **30,000+ Synthetic Data Records**: 2,000 farmers, 100 products, 200 markets, 10,000 transactions, 18,000+ pricing records.
- **Complete PostgreSQL Data Warehouse**: Star schema, SCD Type 2 dimensions, and fact tables.
- **PlantUML Diagrams**: ERD, star schema, system architecture, ETL flow.
- **ETL Pipeline**: With audit logging and data quality checks.
- **Power BI Dashboards**: 5 dashboards with 50+ DAX measures.
- **Blockchain Integration**: Hyperledger Fabric architecture.
- **Streaming Pipeline**: Apache Kafka configuration.
- **Identity Management**: Keycloak integration.

## Project Structure

```
agric_dw/
├── data/                       # Generated CSV files
├── diagrams/                   # PlantUML diagrams
├── docs/                       # Narrative documentation
├── sql/                        # Database scripts (DDL)
├── scripts/                    # Python scripts (Data Gen, ETL, etc.)
├── powerbi/                    # Dashboard specs & measures
└── requirements.txt            # Python dependencies
```

---

## 🚀 Quick Start & Setup Guide

### 1. Prerequisites

- **PostgreSQL 15+**: [Download](https://www.postgresql.org/download/windows/)
- **Python 3.10+**: [Download](https://www.python.org/downloads/) (Check "Add to PATH" during install)
- **Power BI Desktop**: [Download](https://powerbi.microsoft.com/desktop/)

### 2. Project Installation

1.  **Open PowerShell** as Administrator.
2.  **Navigate to the project folder**:
    ```powershell
    cd c:\Users\batzt\Desktop\agric_dw
    ```
3.  **Install Python Dependencies**:
    ```powershell
    pip install -r requirements.txt
    ```

### 3. Database Setup (PostgreSQL)

1.  **Open pgAdmin 4** and connect to your server.
2.  **Create Database**: Right-click Databases > Create > Database... Name it `agri_dw`.
3.  **Run DDL Scripts**: Open the Query Tool for `agri_dw` and execute the following files from the `sql/ddl/` folder in order:
    1.  `01_create_database.sql`
    2.  `02_staging_tables.sql`
    3.  `03_dimension_tables.sql`
    4.  `04_fact_tables.sql`

    *Alternatively, via PowerShell:*
    ```powershell
    psql -U postgres -d agri_dw -f sql/ddl/02_staging_tables.sql
    psql -U postgres -d agri_dw -f sql/ddl/03_dimension_tables.sql
    psql -U postgres -d agri_dw -f sql/ddl/04_fact_tables.sql
    ```

### 4. Data Generation & Loading (ETL)

**Generate Verification Data**:
```powershell
cd scripts/data_generation
python master_data_generator.py
```
*This will create synthetic CSV files in the `data/` directory.*

**Run ETL Pipeline**:
```powershell
cd ../etl
python etl_staging_to_dw.py
```
*This transforms data from Staging to the Data Warehouse schema.*

### 5. Verification

Run this query in pgAdmin to verify data counts:
```sql
SELECT 'Farmers' as entity, COUNT(*) as rows FROM dw.dim_farmer
UNION ALL SELECT 'Products', COUNT(*) FROM dw.dim_product
UNION ALL SELECT 'Markets', COUNT(*) FROM dw.dim_market
UNION ALL SELECT 'Transactions', COUNT(*) FROM dw.fact_transaction;
```

---

## Power BI Integration

1.  Open **Power BI Desktop**.
2.  Get Data -> **PostgreSQL Database**.
    -   Server: `localhost`
    -   Database: `agri_dw`
    -   Import mode: **Import**
3.  Load the tables from the `dw` schema (e.g., `dw.fact_transaction`, `dw.dim_farmer`).
4.  Refer to `powerbi/dashboard_specifications.md` for visualization details and `powerbi/dax_measures.txt` for formulas.

---

## Assessment Criteria & Deliverables

| Criterion | Status | Location |
|-----------|--------|----------|
| **Problem Identification** | ✅ Complete | `docs/01_problem_justification.md` |
| **Data Source Selection** | ✅ Complete | `docs/02_data_sources.md` |
| **Data Warehouse Design** | ✅ Complete | `diagrams/*.puml`, `docs/03_dw_design.md` |
| **Implementation & ETL** | ✅ Complete | `sql/ddl/*.sql`, `scripts/etl/*.py` |
| **Analysis & Reporting** | ✅ Complete | `powerbi/dashboard_specifications.md` |
| **Documentation** | ✅ Complete | This `README.md` |

## Authors
Data Warehousing Team - 2025
