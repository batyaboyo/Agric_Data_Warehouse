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

**Card 1: Total Revenue (YTD)**
- **Visual Type**: Card
- **Values**: `[Total Revenue YTD]` (DAX Measure)
- **Source Tables**: `dw.fact_transaction[total_amount]`, `dw.dim_date[full_date]`
- **Format**: Currency (UGX)
- **Comparison Indicator**: vs. Previous Year

**Card 2: Total Transactions**
- **Visual Type**: Card
- **Values**: `[Total Transactions]` (DAX Measure)
- **Source Tables**: `dw.fact_transaction[transaction_id]`
- **Format**: Number with thousands separator

**Card 3: Active Farmers**
- **Visual Type**: Card
- **Values**: `[Active Farmers]` (DAX Measure)
- **Source Tables**: `dw.fact_transaction[farmer_key]`
- **Format**: Number

**Card 4: Average Transaction Value**
- **Visual Type**: Card
- **Values**: `[Average Transaction Value]` (DAX Measure)
- **Source Tables**: `dw.fact_transaction[total_amount]`
- **Format**: Currency (UGX)

#### 2.2 Revenue Trend (Line Chart)

- **Visual Type**: Line Chart
- **X-Axis**: `dw.dim_date[month_name]` and `dw.dim_date[year]` (Date Hierarchy)
- **Y-Axis**: `[Total Revenue]` (DAX Measure)
- **Legend**: `dw.dim_product[category]`
- **Tooltips**: 
  - `dw.dim_date[full_date]`
  - `dw.dim_product[category]`
  - `[Total Revenue]`
  - `[Total Transactions]`
  - `[Average Price per kg]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_date`, `dw.dim_product`

#### 2.3 Top 10 Products by Revenue (Bar Chart)

- **Visual Type**: Horizontal Bar Chart
- **Y-Axis (Categories)**: `dw.dim_product[product_name]` (Top 10 by Revenue)
- **X-Axis (Values)**: `[Total Revenue]` (DAX Measure)
- **Legend**: `dw.dim_product[category]`
- **Data Labels**: Revenue values (Currency format)
- **Tooltips**:
  - `dw.dim_product[product_name]`
  - `dw.dim_product[category]`
  - `[Total Revenue]`
  - `[Total Quantity (kg)]`
  - `[Total Transactions]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_product`

#### 2.4 Regional Distribution (Map)

- **Visual Type**: Filled Map
- **Location**: `dw.dim_market[district]` or `dw.dim_location[district]`
- **Size (Bubble Size)**: `[Total Revenue]` (DAX Measure)
- **Color Saturation**: `[Active Farmers]` (DAX Measure)
- **Tooltips**:
  - `dw.dim_market[district]`
  - `dw.dim_market[region]`
  - `[Total Revenue]`
  - `[Active Farmers]`
  - `[Total Transactions]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_market`, `dw.dim_location`

---

## 3. Dashboard 2: Farmer Analytics

### Purpose
Insights into farmer demographics, performance, and engagement.

### Visualizations

#### 3.1 Farmer Demographics (Donut Charts)

**Chart 1: Gender Distribution**
- **Visual Type**: Donut Chart
- **Legend**: `dw.dim_farmer[gender]`
- **Values**: `[Count of Farmers]` (DAX Measure: `DISTINCTCOUNT(dw.dim_farmer[farmer_id])`)
- **Data Labels**: Percentage
- **Tooltips**:
  - `dw.dim_farmer[gender]`
  - `[Count of Farmers]`
  - Percentage of Total
- **Source Tables**: `dw.dim_farmer`

**Chart 2: Farm Size Category**
- **Visual Type**: Donut Chart
- **Legend**: `dw.dim_farmer[farm_size_category]`
- **Values**: `[Count of Farmers]`
- **Data Labels**: Percentage
- **Tooltips**:
  - `dw.dim_farmer[farm_size_category]`
  - `[Count of Farmers]`
  - Percentage of Total
- **Source Tables**: `dw.dim_farmer`

**Chart 3: Age Group Distribution**
- **Visual Type**: Donut Chart
- **Legend**: `dw.dim_farmer[age_group]`
- **Values**: `[Count of Farmers]`
- **Data Labels**: Percentage
- **Tooltips**:
  - `dw.dim_farmer[age_group]`
  - `[Count of Farmers]`
  - Percentage of Total
- **Source Tables**: `dw.dim_farmer`

#### 3.2 Top 20 Farmers by Revenue (Table)

- **Visual Type**: Table
- **Columns**:
  1. `dw.dim_farmer[full_name]`
  2. `dw.dim_farmer[district]`
  3. `dw.dim_farmer[primary_crop]`
  4. `[Total Transactions]` (DAX Measure)
  5. `[Total Revenue]` (DAX Measure)
  6. `[Average Price per kg]` (DAX Measure)
- **Conditional Formatting**: 
  - Revenue column: Data Bars (Green gradient)
  - Background color scale on Revenue
- **Filters**: Top 20 by `[Total Revenue]`
- **Source Tables**: `dw.dim_farmer`, `dw.fact_transaction`

#### 3.3 Farmer Engagement Over Time (Area Chart)

- **Visual Type**: Area Chart
- **X-Axis**: `dw.dim_date[month]` and `dw.dim_date[year]`
- **Y-Axis**: `[Active Farmers]` (DAX Measure)
- **Legend**: `dw.dim_farmer[region]`
- **Tooltips**:
  - `dw.dim_date[month_name]`
  - `dw.dim_date[year]`
  - `dw.dim_farmer[region]`
  - `[Active Farmers]`
  - `[New Farmers This Month]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_farmer`, `dw.dim_date`

#### 3.4 Cooperative Performance (Clustered Bar Chart)

- **Visual Type**: Clustered Bar Chart
- **Y-Axis (Categories)**: `dw.dim_farmer[cooperative_name]`
- **X-Axis (Values)**: `[Total Revenue]` and `[Count of Farmers]`
- **Legend**: Metric Type (Revenue vs. Member Count)
- **Tooltips**:
  - `dw.dim_farmer[cooperative_name]`
  - `[Total Revenue]`
  - `[Count of Farmers]`
  - `[Average Revenue per Farmer]` (Calculated: Revenue / Count)
- **Source Tables**: `dw.dim_farmer`, `dw.fact_transaction`

---

## 4. Dashboard 3: Product & Market Analysis

### Purpose
Product performance, pricing trends, and market dynamics.

### Visualizations

#### 4.1 Product Category Performance (Treemap)

- **Visual Type**: Treemap
- **Category (Group)**: `dw.dim_product[category]`
- **Details**: `dw.dim_product[product_name]`
- **Values**: `Sum of dw.fact_transaction[total_amount]`
- **Color Saturation**: `Sum of dw.fact_transaction[total_amount]`
- **Tooltips**:
  - `dw.dim_product[category]`
  - `dw.dim_product[product_name]`
  - `Sum of dw.fact_transaction[total_amount]`
  - `Count of dw.fact_transaction[transaction_id]`
  - `Average of dw.fact_transaction[unit_price]` (if available)
- **Source Tables**: `dw.fact_transaction`, `dw.dim_product`

#### 4.2 Price Trends (Line Chart with Forecast)

- **Visual Type**: Line Chart
- **X-Axis**: `dw.dim_date[full_date]`
- **Y-Axis**: `AVERAGE(dw.fact_pricing[wholesale_price])`
- **Legend**: `dw.dim_product[product_name]` (Top 5 products)
- **Analytics Line**: Trend line + 30-day forecast
- **Tooltips**:
  - `dw.dim_date[full_date]`
  - `dw.dim_product[product_name]`
  - `dw.fact_pricing[wholesale_price]`
  - `dw.fact_pricing[retail_price]`
  - `dw.fact_pricing[price_spread]`
- **Source Tables**: `dw.fact_pricing`, `dw.dim_product`, `dw.dim_date`

#### 4.3 Market Type Distribution (Stacked Column Chart)

- **Visual Type**: Stacked Column Chart
- **X-Axis (Categories)**: `dw.dim_market[market_type]`
- **Y-Axis (Values)**: `Sum of dw.fact_transaction[quantity_kg]`
- **Legend**: `dw.dim_product[category]`
- **Tooltips**:
  - `dw.dim_market[market_type]`
  - `dw.dim_product[category]`
  - `Sum of dw.fact_transaction[quantity_kg]`
  - `Sum of dw.fact_transaction[total_amount]`
  - `Count of dw.fact_transaction[transaction_id]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_market`, `dw.dim_product`

#### 4.4 Quality Grade Analysis (Clustered Column Chart)

- **Visual Type**: Clustered Column Chart
- **X-Axis (Categories)**: `dw.dim_product[category]`
- **Y-Axis (Values)**: `Sum of dw.fact_transaction[quantity_kg]`
- **Legend**: `dw.dim_quality[quality_grade]` (A, B, C)
- **Data Labels**: Percentage of total per category
- **Tooltips**:
  - `dw.dim_product[category]`
  - `dw.dim_quality[quality_grade]`
  - `dw.dim_quality[quality_description]`
  - `Sum of dw.fact_transaction[quantity_kg]`
  - Percentage of Total
- **Source Tables**: `dw.fact_transaction`, `dw.dim_product`, `dw.dim_quality`

---

## 5. Dashboard 4: Financial Performance

### Purpose
Financial metrics, payment methods, and revenue analysis.

### Visualizations

#### 5.1 Revenue by Payment Method (Pie Chart)

- **Visual Type**: Pie Chart
- **Legend**: `dw.dim_payment_method[payment_method]`
- **Values**: `[Total Revenue]` (DAX Measure)
- **Data Labels**: Percentage
- **Tooltips**:
  - `dw.dim_payment_method[payment_method]`
  - `dw.dim_payment_method[payment_category]`
  - `[Total Revenue]`
  - `[Total Transactions]`
  - Percentage of Total Revenue
- **Source Tables**: `dw.fact_transaction`, `dw.dim_payment_method`

#### 5.2 Monthly Revenue & Transactions (Combo Chart)

- **Visual Type**: Line and Clustered Column Chart
- **X-Axis (Shared)**: `dw.dim_date[month]` and `dw.dim_date[year]`
- **Column Y-Axis (Primary)**: `[Total Revenue]` (DAX Measure)
- **Line Y-Axis (Secondary)**: `[Total Transactions]` (DAX Measure)
- **Tooltips**:
  - `dw.dim_date[month_name]`
  - `dw.dim_date[year]`
  - `[Total Revenue]`
  - `[Total Transactions]`
  - `[Average Transaction Value]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_date`

#### 5.3 Revenue by Region (Matrix)

- **Visual Type**: Matrix
- **Rows**: `dw.dim_market[region]` → `dw.dim_market[district]`
- **Columns**: `dw.dim_date[year]` → `dw.dim_date[quarter]` → `dw.dim_date[month_name]`
- **Values**: `[Total Revenue]` (DAX Measure)
- **Conditional Formatting**: Heat map (color scale from white to dark green)
- **Tooltips**:
  - Region/District
  - Year/Quarter/Month
  - `[Total Revenue]`
  - `[Total Transactions]`
- **Source Tables**: `dw.fact_transaction`, `dw.dim_market`, `dw.dim_date`

#### 5.4 Payment Status Analysis (Funnel Chart)

- **Visual Type**: Funnel Chart
- **Category**: `dw.fact_transaction[payment_status]`
- **Values**: `[Total Transactions]` (DAX Measure)
- **Stages**: Total → Paid → Pending → Failed
- **Tooltips**:
  - `dw.fact_transaction[payment_status]`
  - `[Total Transactions]`
  - Conversion Rate (%)
- **Source Tables**: `dw.fact_transaction`


**Last Updated**: 2025-12-06  
**Version**: 2.0
