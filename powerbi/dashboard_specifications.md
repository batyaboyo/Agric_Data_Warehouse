# Power BI Dashboard Specifications
## Agricultural Supply Chain Data Warehouse

---

## Dashboard 1: Executive Overview

### Purpose
High-level KPIs and trends for executive decision-making.

### Visualizations

#### 1.1 KPI Cards (Top Row)
- **Total Revenue (YTD)**
  - Measure: `SUM(total_amount)`
  - Format: Currency (UGX)
  - Comparison: vs. Previous Year
  
- **Total Transactions**
  - Measure: `COUNT(transaction_id)`
  - Format: Number with thousands separator
  
- **Active Farmers**
  - Measure: `DISTINCTCOUNT(farmer_id)`
  - Format: Number
  
- **Average Transaction Value**
  - Measure: `AVERAGE(total_amount)`
  - Format: Currency (UGX)

#### 1.2 Revenue Trend (Line Chart)
- **X-Axis**: Month/Year
- **Y-Axis**: Total Revenue
- **Legend**: Product Category
- **Tooltip**: Transaction Count, Average Price

#### 1.3 Top 10 Products by Revenue (Bar Chart)
- **X-Axis**: Product Name
- **Y-Axis**: Total Revenue
- **Color**: Product Category
- **Data Labels**: Revenue values

#### 1.4 Regional Distribution (Map)
- **Location**: District (GPS coordinates)
- **Size**: Total Revenue
- **Color**: Number of Farmers
- **Tooltip**: District name, revenue, farmer count

---

## Dashboard 2: Farmer Analytics

### Purpose
Insights into farmer demographics, performance, and engagement.

### Visualizations

#### 2.1 Farmer Demographics (Donut Charts)
- **Gender Distribution**
  - Values: Male, Female
  - Measure: Count of farmers
  
- **Farm Size Category**
  - Values: Small, Medium, Large
  - Measure: Count of farmers
  
- **Age Group Distribution**
  - Values: Youth, Adult, Senior
  - Measure: Count of farmers

#### 2.2 Top 20 Farmers by Revenue (Table)
- **Columns**:
  - Farmer Name
  - District
  - Primary Crop
  - Transaction Count
  - Total Revenue
  - Average Price per kg
- **Conditional Formatting**: Revenue (color scale)

#### 2.3 Farmer Engagement Over Time (Area Chart)
- **X-Axis**: Month
- **Y-Axis**: Number of Active Farmers
- **Legend**: Region
- **Tooltip**: New farmers registered

#### 2.4 Cooperative Performance (Clustered Bar Chart)
- **X-Axis**: Cooperative Name
- **Y-Axis**: Total Revenue, Member Count
- **Tooltip**: Average revenue per member

---

## Dashboard 3: Product & Market Analysis

### Purpose
Product performance, pricing trends, and market dynamics.

### Visualizations

#### 3.1 Product Category Performance (Treemap)
- **Group**: Category
- **Values**: Total Revenue
- **Color**: Profit Margin %
- **Tooltip**: Transaction count, average price

#### 3.2 Price Trends (Line Chart with Forecast)
- **X-Axis**: Date
- **Y-Axis**: Average Price
- **Legend**: Top 5 Products
- **Analytics**: Trend line, forecast (30 days)

#### 3.3 Market Type Distribution (Stacked Column Chart)
- **X-Axis**: Market Type
- **Y-Axis**: Transaction Volume (kg)
- **Legend**: Product Category
- **Tooltip**: Revenue, transaction count

#### 3.4 Quality Grade Analysis (Clustered Column Chart)
- **X-Axis**: Product Category
- **Y-Axis**: Quantity (kg)
- **Legend**: Quality Grade (A, B, C)
- **Data Labels**: Percentage of total

---

## Dashboard 4: Financial Performance

### Purpose
Financial metrics, payment methods, and revenue analysis.

### Visualizations

#### 4.1 Revenue by Payment Method (Pie Chart)
- **Values**: Total Revenue
- **Legend**: Payment Method
- **Data Labels**: Percentage

#### 4.2 Monthly Revenue & Transactions (Combo Chart)
- **X-Axis**: Month
- **Y-Axis (Primary)**: Total Revenue (Column)
- **Y-Axis (Secondary)**: Transaction Count (Line)
- **Tooltip**: Average transaction value

#### 4.3 Revenue by Region (Matrix)
- **Rows**: Region, District
- **Columns**: Year, Quarter, Month
- **Values**: Total Revenue
- **Conditional Formatting**: Heat map

#### 4.4 Payment Status Analysis (Funnel Chart)
- **Stages**: Total Transactions → Paid → Pending → Failed
- **Values**: Transaction count
- **Conversion Rate**: Calculated measure

---

## Dashboard 5: Supply Chain Traceability

### Purpose
Blockchain-verified transactions and traceability metrics.

### Visualizations

#### 5.1 Blockchain Verification Rate (Gauge)
- **Value**: % of transactions with blockchain hash
- **Target**: 95%
- **Color Coding**: Red (<80%), Yellow (80-95%), Green (>95%)

#### 5.2 Traceability Timeline (Gantt Chart)
- **Task**: Product Name
- **Start**: Planting Date
- **End**: Transaction Date
- **Color**: Quality Grade
- **Tooltip**: Farmer, market, quantity

#### 5.3 Farm-to-Market Journey (Sankey Diagram)
- **Flow**: Farmer → Product → Market → Buyer
- **Width**: Transaction volume
- **Color**: Product category

#### 5.4 Transaction Verification Table
- **Columns**:
  - Transaction ID
  - Date
  - Farmer
  - Product
  - Quantity
  - Amount
  - Blockchain Hash (truncated)
  - Verification Status
- **Filter**: Date range, product, farmer

---

## DAX Measures

### Revenue Metrics

```dax
Total Revenue = SUM(fact_transaction[total_amount])

Total Revenue YTD = 
TOTALYTD([Total Revenue], dim_date[full_date])

Revenue Previous Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(dim_date[full_date])
)

Revenue YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Previous Year],
    [Revenue Previous Year],
    0
) * 100

Average Transaction Value = 
AVERAGE(fact_transaction[total_amount])
```

### Volume Metrics

```dax
Total Quantity (kg) = SUM(fact_transaction[quantity_kg])

Total Transactions = COUNT(fact_transaction[transaction_id])

Average Price per kg = 
DIVIDE(
    [Total Revenue],
    [Total Quantity (kg)],
    0
)
```

### Farmer Metrics

```dax
Active Farmers = 
DISTINCTCOUNT(fact_transaction[farmer_key])

New Farmers This Month = 
CALCULATE(
    DISTINCTCOUNT(dim_farmer[farmer_id]),
    FILTER(
        dim_farmer,
        dim_farmer[registration_date] >= STARTOFMONTH(TODAY()) &&
        dim_farmer[registration_date] <= TODAY()
    )
)

Average Revenue per Farmer = 
DIVIDE(
    [Total Revenue],
    [Active Farmers],
    0
)
```

### Market Metrics

```dax
Market Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL(dim_market)
    ),
    0
) * 100

Top Product by Revenue = 
FIRSTNONBLANK(
    TOPN(
        1,
        VALUES(dim_product[product_name]),
        [Total Revenue],
        DESC
    ),
    1
)
```

### Quality Metrics

```dax
Premium Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        dim_quality[quality_grade] = "A"
    ),
    [Total Quantity (kg)],
    0
) * 100

Average Quality Score = 
AVERAGEX(
    fact_transaction,
    RELATED(dim_quality[quality_score])
)
```

### Blockchain Metrics

```dax
Blockchain Verification Rate % = 
DIVIDE(
    CALCULATE(
        [Total Transactions],
        NOT(ISBLANK(fact_transaction[blockchain_hash]))
    ),
    [Total Transactions],
    0
) * 100

Verified Transactions = 
CALCULATE(
    [Total Transactions],
    NOT(ISBLANK(fact_transaction[blockchain_hash]))
)
```

### Time Intelligence

```dax
Revenue MTD = 
TOTALMTD([Total Revenue], dim_date[full_date])

Revenue QTD = 
TOTALQTD([Total Revenue], dim_date[full_date])

Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH(dim_date[full_date])
)

Revenue MoM Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Last Month],
    [Revenue Last Month],
    0
) * 100
```

---

## Filters and Slicers

### Global Filters (All Dashboards)
- **Date Range**: Date picker (from/to)
- **Region**: Multi-select dropdown
- **Product Category**: Multi-select dropdown
- **Fiscal Year**: Single select

### Dashboard-Specific Filters

#### Farmer Analytics
- Gender
- Farm Size Category
- Cooperative

#### Product & Market Analysis
- Product Name
- Market Type
- Quality Grade

#### Financial Performance
- Payment Method
- Payment Status

#### Supply Chain Traceability
- Blockchain Verification Status
- Farmer ID
- Transaction ID

---

## Interactions and Drill-Through

### Cross-Filtering
- Clicking on any visual filters related visuals on the same page
- Region map filters all other visuals

### Drill-Through Pages

#### Farmer Detail Page
- **Trigger**: Right-click on farmer name
- **Content**:
  - Farmer profile (demographics, farm details)
  - Transaction history
  - Revenue trend
  - Product mix
  - Quality performance

#### Product Detail Page
- **Trigger**: Right-click on product name
- **Content**:
  - Product information
  - Price trend over time
  - Top markets
  - Top farmers
  - Quality distribution

---

## Refresh Schedule

- **Dataset Refresh**: Daily at 6:00 AM
- **Incremental Refresh**: Last 30 days (full refresh monthly)
- **Data Source**: CSV export from `powerbi/powerbi_dataset.csv`

---

## Performance Optimization

1. **Aggregations**: Use `fact_transaction_daily_summary` for date-level analysis
2. **Relationships**: Star schema with single direction filters
3. **Calculated Columns**: Minimize use, prefer measures
4. **Data Types**: Optimize (e.g., INTEGER for keys, DECIMAL for measures)
5. **Visuals per Page**: Maximum 10 visuals per dashboard page

---

## Export and Sharing

- **Export to PDF**: Enabled for all dashboards
- **Export Data**: Enabled for tables only
- **Sharing**: Publish to Power BI Service workspace
- **Row-Level Security**: Filter by region for regional managers

---

**Last Updated**: 2025-12-04  
**Version**: 1.0
