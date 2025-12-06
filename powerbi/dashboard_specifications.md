# Power BI Dashboard Specifications
## Agricultural Supply Chain Data Warehouse

---

## 1. Data Model & Schema Mapping

The Power BI data model is built directly on top of the Data Warehouse (`dw`) schema. All tables and relationships reflect the Star Schema design.

### 1.1 Fact Tables
| Power BI Table | Source Table | Granularity | Description |
| :--- | :--- | :--- | :--- |
| **fact_transaction** | `dw.fact_transaction` | One row per transaction | Core transactional data (sales, payments). |
| **fact_harvest** | `dw.fact_harvest` | One row per harvest | Harvest yields and post-harvest losses. |
| **fact_pricing** | `dw.fact_pricing` | Product-Market-Day | Daily market pricing trends. |

### 1.2 Dimension Tables
| Power BI Table | Source Table | Description | Key Attributes |
| :--- | :--- | :--- | :--- |
| **dim_date** | `dw.dim_date` | Date dimension | `full_date`, `month_name`, `year`, `fiscal_year`. |
| **dim_farmer** | `dw.dim_farmer` | Farmer details (SCD Type 2) | `farmer_id`, `gender`, `farm_size_category`, `cooperative_name`. |
| **dim_product** | `dw.dim_product` | Product details | `product_name`, `category`, `variety`. |
| **dim_market** | `dw.dim_market` | Market details | `market_name`, `market_type`, `district`, `region`. |
| **dim_buyer** | `dw.dim_buyer` | Buyer details | `buyer_name`, `buyer_type`. |
| **dim_location** | `dw.dim_location` | Geographic reference | `district`, `subcounty`, `region`. |
| **dim_quality** | `dw.dim_quality` | Quality grades | `quality_grade`, `quality_score`. |
| **dim_payment_method** | `dw.dim_payment_method` | Payment modes | `payment_method`, `is_digital`. |

### 1.3 Relationships
- All relationships are **One-to-Many** from Dimension to Fact.
- **Cross-filter direction**: Single (Dimension filters Fact).

---

## 2. Dashboard 1: Executive Overview

### Purpose
High-level KPIs and trends for executive decision-making.

### Visualizations

#### 2.1 KPI Cards (Top Row)
- **Total Revenue (YTD)**
  - Measure: `[Total Revenue YTD]`
  - Source: `dw.fact_transaction`
  - Comparison: vs. Previous Year

- **Total Transactions**
  - Measure: `[Total Transactions]`
  - Source: `dw.fact_transaction`

- **Active Farmers**
  - Measure: `[Active Farmers]`
  - Source: `dw.fact_transaction` & `dw.dim_farmer`

- **Average Transaction Value**
  - Measure: `[Average Transaction Value]`
  - Source: `dw.fact_transaction`

#### 2.2 Revenue Trend (Line Chart)
- **X-Axis**: `dw.dim_date[month_name]` / `dw.dim_date[year]`
- **Y-Axis**: `[Total Revenue]`
- **Legend**: `dw.dim_product[category]`

#### 2.3 Top 10 Products by Revenue (Bar Chart)
- **X-Axis**: `dw.dim_product[product_name]`
- **Y-Axis**: `[Total Revenue]`
- **Color**: `dw.dim_product[category]`

#### 2.4 Regional Distribution (Map)
- **Location**: `dw.dim_location[district]` (or `dw.dim_market[district]`)
- **Size**: `[Total Revenue]`
- **Color**: `[Active Farmers]`

---

## 3. Dashboard 2: Farmer Analytics

### Purpose
Insights into farmer demographics, performance, and engagement.

### Visualizations

#### 3.1 Farmer Demographics (Donut Charts)
- **Gender Distribution**
  - Field: `dw.dim_farmer[gender]`
  - Measure: `DISTINCTCOUNT(dw.dim_farmer[farmer_id])`
  
- **Farm Size Category**
  - Field: `dw.dim_farmer[farm_size_category]`
  
- **Age Group Distribution**
  - Field: `dw.dim_farmer[age_group]`

#### 3.2 Top 20 Farmers by Revenue (Table)
- **Columns**: `dw.dim_farmer[full_name]`, `dw.dim_farmer[district]`, `dw.dim_farmer[primary_crop]`, `[Transaction Count]`, `[Total Revenue]`.
- **Conditional Formatting**: Revenue (Data Bars).

#### 3.3 Farmer Engagement Over Time (Area Chart)
- **X-Axis**: `dw.dim_date[month]`
- **Y-Axis**: `[Active Farmers]`
- **Legend**: `dw.dim_farmer[region]`

---

## 4. Dashboard 3: Product & Market Analysis

### Purpose
Product performance, pricing trends, and market dynamics.

### Visualizations

#### 4.1 Product Category Performance (Treemap)
- **Group**: `dw.dim_product[category]`
- **Values**: `[Total Revenue]`
- **Tooltip**: `[Average Price per kg]`

#### 4.2 Price Trends (Line Chart)
- **X-Axis**: `dw.dim_date[full_date]`
- **Y-Axis**: `dw.fact_pricing[wholesale_price]` (Average)
- **Legend**: `dw.dim_product[product_name]`

#### 4.3 Market Type Distribution (Stacked Column Chart)
- **X-Axis**: `dw.dim_market[market_type]`
- **Y-Axis**: `dw.fact_transaction[quantity_kg]` (Sum)
- **Legend**: `dw.dim_product[category]`

#### 4.4 Quality Grade Analysis (Clustered Column Chart)
- **X-Axis**: `dw.dim_product[category]`
- **Y-Axis**: `dw.fact_transaction[quantity_kg]`
- **Legend**: `dw.dim_quality[quality_grade]` (A, B, C)

---

## 5. Dashboard 5: Supply Chain Traceability

### Purpose
Blockchain-verified transactions and traceability metrics.

### Visualizations

#### 5.1 Blockchain Verification Rate (Gauge)
- **Value**: `[Blockchain Verification Rate %]`
- **Target**: 95%

#### 5.2 Transaction Verification Table
- **Columns**:
  - `dw.fact_transaction[transaction_id]`
  - `dw.dim_date[full_date]`
  - `dw.dim_farmer[full_name]`
  - `dw.dim_product[product_name]`
  - `dw.fact_transaction[quantity_kg]`
  - `dw.fact_transaction[blockchain_hash]` (Truncated)
- **Filter**: `dw.fact_transaction[blockchain_hash]` is not blank.

---

## 6. DAX Measures

### Revenue Metrics
```dax
Total Revenue = SUM(dw.fact_transaction[total_amount])

Total Revenue YTD = 
TOTALYTD([Total Revenue], dw.dim_date[full_date])

Revenue Previous Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(dw.dim_date[full_date])
)

Average Transaction Value = 
AVERAGE(dw.fact_transaction[total_amount])
```

### Volume & Price Metrics
```dax
Total Quantity (kg) = SUM(dw.fact_transaction[quantity_kg])

Total Transactions = COUNT(dw.fact_transaction[transaction_id])

Average Price per kg = 
DIVIDE([Total Revenue], [Total Quantity (kg)], 0)
```

### Farmer Metrics
```dax
Active Farmers = 
DISTINCTCOUNT(dw.fact_transaction[farmer_key])

Count of Farmers = DISTINCTCOUNT(dw.dim_farmer[farmer_id])

New Farmers This Month = 
CALCULATE(
    DISTINCTCOUNT(dw.dim_farmer[farmer_id]),
    FILTER(
        dw.dim_farmer,
        dw.dim_farmer[registration_date] >= STARTOFMONTH(TODAY()) &&
        dw.dim_farmer[registration_date] <= TODAY()
    )
)
```

### Blockchain Metrics
```dax
Blockchain Verification Rate % = 
DIVIDE(
    CALCULATE(
        [Total Transactions],
        NOT(ISBLANK(dw.fact_transaction[blockchain_hash]))
    ),
    [Total Transactions],
    0
) * 100

Verified Transactions = 
CALCULATE(
    [Total Transactions],
    NOT(ISBLANK(dw.fact_transaction[blockchain_hash]))
)
```

---

## 7. Performance Optimization

1. **Referencing Integrity**: Ensure all Foreign Keys in `dw.fact_transaction` map successfully to Dimensions to avoid "(Blank)" members.
2. **Aggregations**: Utilize `dw.fact_transaction_daily_summary` for high-level date/product/market analysis if detail-level performance lags.

---

**Last Updated**: 2025-12-06
