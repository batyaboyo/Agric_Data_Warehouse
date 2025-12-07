# DAX Measures for Power BI
## Agricultural Supply Chain Data Warehouse

**IMPORTANT**: In Power BI Desktop, you must create each measure **individually**. 
1. Click "New Measure".
2. Paste **ONE** measure definition (Name = Formula).
3. Press Enter.
4. Repeat for the next measure.
**DO NOT paste multiple measures at once.**

### Base Metrics (Create These First)

```dax
Total Revenue = SUM('dw.fact_transaction'[total_amount])
```

```dax
Transaction Count = SUM('dw.fact_transaction'[transaction_count])
```

```dax
Total Quantity (kg) = SUM('dw.fact_transaction'[quantity_kg])
```

### Blockchain Metrics (Traceability)

```dax
Blockchain Verification Rate % = 
DIVIDE(
    CALCULATE(
        [Transaction Count],
        NOT(ISBLANK('dw.fact_transaction'[blockchain_hash]))
    ),
    [Transaction Count],
    0
) * 100
```

```dax
Verified Transactions = 
CALCULATE(
    [Transaction Count],
    NOT(ISBLANK('dw.fact_transaction'[blockchain_hash]))
)
```

```dax
Unverified Transactions = 
CALCULATE(
    [Transaction Count],
    ISBLANK('dw.fact_transaction'[blockchain_hash])
)
```

### Revenue Metrics

```dax
Total Revenue YTD = 
TOTALYTD([Total Revenue], 'dw.dim_date'[full_date])
```

```dax
Revenue Previous Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR('dw.dim_date'[full_date])
)
```

```dax
Revenue YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Previous Year],
    [Revenue Previous Year],
    0
) * 100
```

```dax
Revenue MTD = 
TOTALMTD([Total Revenue], 'dw.dim_date'[full_date])
```

```dax
Revenue QTD = 
TOTALQTD([Total Revenue], 'dw.dim_date'[full_date])
```

```dax
Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH('dw.dim_date'[full_date])
)
```

```dax
Revenue MoM Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Last Month],
    [Revenue Last Month],
    0
) * 100
```

```dax
Average Transaction Value = 
AVERAGE('dw.fact_transaction'[total_amount])
```

### Volume Metrics

```dax
Average Price per kg = 
DIVIDE(
    [Total Revenue],
    [Total Quantity (kg)],
    0
)
```

```dax
Average Quantity per Transaction = 
AVERAGE('dw.fact_transaction'[quantity_kg])
```

### Farmer Metrics

```dax
Active Farmers = 
DISTINCTCOUNT('dw.fact_transaction'[farmer_key])
```

```dax
Total Registered Farmers = 
COUNTROWS(
    FILTER(
        'dw.dim_farmer',
        'dw.dim_farmer'[is_current] = TRUE
    )
)
```

```dax
New Farmers This Month = 
CALCULATE(
    DISTINCTCOUNT('dw.dim_farmer'[farmer_id]),
    FILTER(
        'dw.dim_farmer',
        'dw.dim_farmer'[registration_date] >= STARTOFMONTH(TODAY()) &&
        'dw.dim_farmer'[registration_date] <= TODAY() &&
        'dw.dim_farmer'[is_current] = TRUE
    )
)
```

```dax
Average Revenue per Farmer = 
DIVIDE(
    [Total Revenue],
    [Active Farmers],
    0
)
```

```dax
Average Transactions per Farmer = 
DIVIDE(
    [Transaction Count],
    [Active Farmers],
    0
)
```

### Market Metrics

```dax
Active Markets = 
DISTINCTCOUNT('dw.fact_transaction'[market_key])
```

```dax
Market Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL('dw.dim_market')
    ),
    0
) * 100
```

```dax
Top Market by Revenue = 
FIRSTNONBLANK(
    TOPN(
        1,
        VALUES('dw.dim_market'[market_name]),
        [Total Revenue],
        DESC
    ),
    1
)
```

### Product Metrics

```dax
Active Products = 
DISTINCTCOUNT('dw.fact_transaction'[product_key])
```

```dax
Top Product by Revenue = 
FIRSTNONBLANK(
    TOPN(
        1,
        VALUES('dw.dim_product'[product_name]),
        [Total Revenue],
        DESC
    ),
    1
)
```

```dax
Product Revenue Rank = 
RANKX(
    ALL('dw.dim_product'[product_name]),
    [Total Revenue],
    ,
    DESC,
    DENSE
)
```

### Quality Metrics

```dax
Premium Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        'dw.dim_quality'[quality_grade] = "A"
    ),
    [Total Quantity (kg)],
    0
) * 100
```

```dax
Standard Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        'dw.dim_quality'[quality_grade] = "B"
    ),
    [Total Quantity (kg)],
    0
) * 100
```

```dax
Below Standard Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        'dw.dim_quality'[quality_grade] = "C"
    ),
    [Total Quantity (kg)],
    0
) * 100
```

```dax
Average Quality Score = 
AVERAGEX(
    'dw.fact_transaction',
    RELATED('dw.dim_quality'[quality_score])
)
```

### Payment Metrics

```dax
Mobile Money Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_payment_method'[payment_method] = "Mobile Money"
)
```

```dax
Mobile Money % = 
DIVIDE(
    [Mobile Money Revenue],
    [Total Revenue],
    0
) * 100
```

```dax
Cash Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_payment_method'[payment_method] = "Cash"
)
```

```dax
Digital Payment % = 
DIVIDE(
    CALCULATE(
        [Total Revenue],
        'dw.dim_payment_method'[is_digital] = TRUE
    ),
    [Total Revenue],
    0
) * 100
```

```dax
Payment Success Rate % = 
DIVIDE(
    CALCULATE(
        [Transaction Count],
        'dw.fact_transaction'[payment_status] = "Paid"
    ),
    [Transaction Count],
    0
) * 100
```

### Regional Metrics

```dax
Central Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Central"
)
```

```dax
Eastern Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Eastern"
)
```

```dax
Northern Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Northern"
)
```

```dax
Western Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Western"
)
```

### Comparative Metrics

```dax
Revenue vs Target = 
VAR TargetRevenue = 1000000000  -- 1 Billion UGX target
RETURN
DIVIDE(
    [Total Revenue],
    TargetRevenue,
    0
) * 100
```

```dax
Revenue vs Budget % = 
VAR Budget = 1000000000
RETURN
DIVIDE(
    [Total Revenue] - Budget,
    Budget,
    0
) * 100
```

### Trend Indicators

```dax
Revenue Trend Indicator = 
IF(
    [Revenue MoM Growth %] > 0,
    "▲ Increasing",
    IF(
        [Revenue MoM Growth %] < 0,
        "▼ Decreasing",
        "■ Stable"
    )
)
```

### Calculated Columns (Reference)

*Create these in Power BI on the respective tables*

**On fact_transaction table:**
```dax
Transaction Month = FORMAT('dw.fact_transaction'[transaction_timestamp], "YYYY-MM")
```

```dax
Transaction Year = YEAR('dw.fact_transaction'[transaction_timestamp])
```

```dax
Transaction Quarter = "Q" & QUARTER('dw.fact_transaction'[transaction_timestamp])
```

**On dim_farmer table:**
```dax
Farmer Age = DATEDIFF('dw.dim_farmer'[date_of_birth], TODAY(), YEAR)
```
