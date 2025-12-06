# Designing a Blockchain-Integrated Agricultural Supply Chain Data Warehouse for Data Transparency and Traceability in Uganda

**Final Project Report**

**Course**: Data Warehousing  
**Date**: December 6, 2025  
**Project Type**: Blockchain-Integrated Data Warehouse Implementation

---

## Background of the Study

Agriculture is the main source of livelihood for most Ugandans, employing more than 70% of the population and greatly contributing to the country’s economy, according to the recent national population census findings. However, farmers continue to face challenges such as unfair market prices, lack of transparency, limited access to loans, and poor record keeping. These challenges are made worse by the absence of reliable data and poor traceability of agricultural produce. As a result, farmers earn less, consumers lose trust, and policy makers lack accurate information to make good decisions. To address these issues, this project proposes a simple but powerful solution — combining blockchain technology with a data warehouse. Blockchain ensures that agricultural data and transactions are secure, transparent, and tamper-proof, while a data warehouse brings all the information together for easy analysis and decision-making.

## Problem Statement

Uganda’s agricultural supply chain system lacks transparency, reliable data, and proper traceability of produce. This has led to low farmer incomes, unfair pricing, and weak decision-making. There is a need for a trusted digital system that connects farmers, markets, and institutions while ensuring that all data is accurate, transparent, and easy to share.

## Main Objective

To create a blockchain-based agricultural supply chain data warehouse that improves transparency, traceability, and data-driven decision-making in Uganda’s agriculture sector.

## Specific Objectives

1. To build a secure traceability system for agricultural produce from farm to market.
2. To promote fair and transparent agricultural pricing and trade.
3. To create a central data warehouse that combines agricultural information from different sources.
4. To provide farmers with digital identities that make it easier to access loans and government programs.
5. To give stakeholders useful reports and insights for better agricultural supply chain planning and management.

## Tools to Achieve Specific Objectives

| Specific Objective | Tool | Why This Tool? |
| :--- | :--- | :--- |
| Build a secure traceability system for produce. | Hyperledger Fabric | A reliable, secure blockchain framework that records transactions and data transparently. |
| Promote fair and transparent pricing. | Apache Kafka | Handles real-time data updates and connects easily with blockchain systems to keep market data current. |
| Create a central agricultural data warehouse. | PostgreSQL | A trusted and scalable data warehouse that stores and analyzes large amounts of agricultural data. |
| Provide farmers with digital identities. | Keycloak | Helps manage user identities securely and integrates well with blockchain systems for authentication. |
| Offer data insights and reports for decision-making. | Power BI | An easy-to-use tool that turns agricultural data into visual insights and dashboards. |

---

## Data Collection and Source Identification

### Data Sources
1.  **Farmer Registration System**: Collects demographics, farm details, and location via mobile app.
2.  **Transaction Recording System**: Captures sales data (product, quantity, price) at point-of-sale.
3.  **Market Pricing System**: Daily wholesale and retail prices from market surveys.
4.  **Government Databases**: Subsidy programs and beneficiary data.

### Data Collection Methods
-   **Mobile Application**: Farmers and cooperatives use an Android app to record data offline/online.
-   **API Integration**: Automated fetching of weather and external pricing data.
-   **Synthetic Data Generation**: For this project demonstration, we generated **30,550 realistic rows** of data (farmers, products, markets, transactions) using Python scripts (`Faker` library) to simulate the Ugandan agricultural ecosystem with high referential integrity.

### Data Quality Assurance
-   **Validation**: Automated checks for missing fields and data types during entry.
-   **Integrity**: Foreign key constraints in the database ensure valid relationships.
-   **Consistency**: Standardized naming conventions (e.g., district names).

---

## Data Warehouse Design

### Schema Design
The data warehouse uses a **Star Schema** optimized for analytical queries:

-   **Fact Tables** (Center):
    -   `fact_transaction`: Core sales and movements.
    -   `fact_harvest`: Production yields.
    -   `fact_pricing`: Daily market prices.
-   **Dimension Tables** (Surrounding):
    -   `dim_farmer`: Farmer details (SCD Type 2).
    -   `dim_product`: Crop varieties and categories.
    -   `dim_market`: Market locations and types.
    -   `dim_date`: Time dimension for trend analysis.

### Entity Relationship Diagram (ERD)
The design includes 13 tables arranged to support the business processes. The **SCD Type 2** (Slowly Changing Dimension) technique is used for Farmers and Products to track historical changes (e.g., farm size growth) over time, ensuring accurate historical reporting.

![Entity Relationship Diagram (ERD)](diagrams/schema_erd.png)
*Figure 1: Entity Relationship Diagram showing relationships between 13 tables*

---

## Implementation

### Data Warehouse Construction
-   **Platform**: PostgreSQL 15
-   **Structure**: Three schemas (`staging` for raw data, `dw` for the data warehouse, `audit` for logs).
-   **Storage**: Implemented with appropriate data types (DECIMAL for money, TEXT for names) and indexing for performance.

### Data Population
We populated the data warehouse with **30,550 rows** of synthetic data:
-   2,000 Farmers
-   10,000 Transactions
-   18,250 Pricing records
-   100 Products & 200 Markets

![Data Generation Output](screenshots/data_generation.png)
*Figure 2: Console output showing successful generation of 30,550 rows*

### ETL Process
The **Extract, Transform, Load (ETL)** pipeline was built using Python:
1.  **Extract**: Read raw CSV data into Staging tables.
2.  **Transform**: Apply cleaning rules, look up surrogate keys, and handle SCD Type 2 logic (versioning).
3.  **Load**: Insert clean, structured data into Fact and Dimension tables.
4.  **Audit**: Log execution time and row counts for every run.

![ETL Process Execution](screenshots/etl_execution.png)
*Figure 3: ETL Pipeline execution logs showing row counts and success status*

---

## Analysis and Reporting

### Analytical Dashboards
Using Power BI, we created 5 dashboards to provide actionable insights:

1.  **Executive Overview**: High-level KPIs (Total Revenue, Active Farmers) for quick decision-making.
    
    ![Executive Overview Dashboard](screenshots/dashboard_executive.png)
    *Figure 4: Executive Overview Dashboard showing key performance indicators*

2.  **Farmer Analytics**: detailed view of farmer demographics, productivity, and income levels.
    
    ![Farmer Analytics Dashboard](screenshots/dashboard_farmer.png)
    *Figure 5: Farmer Analytics Dashboard*

3.  **Product & Market Analysis**: Price trends and popularity of different crop varieties.
    
    ![Product Analysis Dashboard](screenshots/dashboard_product.png)
    *Figure 6: Product & Market Analysis Dashboard*

4.  **Financial Performance**: Analysis of payment methods (Mobile Money vs Cash) and revenue growth.

    ![Financial Performance Dashboard](screenshots/dashboard_financial.png)
    *Figure 7: Financial Performance Dashboard*

5.  **Supply Chain Traceability**: Tracks the journey of produce and verifies blockchain hashes.

    ![Traceability Dashboard](screenshots/dashboard_traceability.png)
    *Figure 8: Supply Chain Traceability Dashboard showing blockchain verification*

### Interpretation of Results
-   **Transparency**: The system successfully links every transaction to a farmer and a verified blockchain hash, reducing fraud.
-   **Fair Pricing**: Price trend analysis helps farmers negotiate better rates based on market data.
-   **Credit Access**: Documented transaction histories provide the proof needed for farmers to access loans.

---

## Conclusions

This project successfully designed and implemented a blockchain-integrated data warehouse for Uganda's agricultural sector. By combining the secure, immutable nature of Hyperledger Fabric with the analytical power of a PostgreSQL data warehouse, we solved the key problems of transparency and data availability. The system not only tracks produce from farm to market but also empowers farmers with data to improve their livelihoods.

---

## References

1. Uganda Bureau of Statistics (2023). *Statistical Abstract 2023*. Kampala: UBOS.
2. Ministry of Agriculture, Animal Industry and Fisheries (2023). *Agriculture Sector Strategic Plan 2023-2028*. Kampala: MAAIF.
3. Kimball, R., & Ross, M. (2013). *The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling*. Wiley.
4. Hyperledger Foundation (2024). *Hyperledger Fabric Documentation*.
5. PostgreSQL Global Development Group (2024). *PostgreSQL 15 Documentation*.

---

## Appendices

### Appendix A: Diagrams

**(Please insert the generated images here for the final submission)**
- Figure 1: Entity Relationship Diagram (`diagrams/schema_erd.puml`)
- Figure 2: Star Schema Diagram (`diagrams/star_schema.puml`)
- Figure 3: System Architecture (`diagrams/system_architecture.puml`)
- Figure 4: ETL Flow (`diagrams/etl_flow.puml`)

### Appendix B: Verification Screenshots
- Database Row Counts (30,550 rows)
- ETL Execution Logs
- Power BI Dashboard snapshots
