# DAX Measures for Power BI
## Agricultural Supply Chain Data Warehouse

Copy these measures into Power BI Desktop individually using the "New Measure" button.

### Revenue Metrics

```dax
Total Revenue = SUM('dw.fact_transaction'[total_amount])

Total Revenue YTD = 
TOTALYTD([Total Revenue], 'dw.dim_date'[full_date])

Revenue Previous Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR('dw.dim_date'[full_date])
)

Revenue YoY Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Previous Year],
    [Revenue Previous Year],
    0
) * 100

Revenue MTD = 
TOTALMTD([Total Revenue], 'dw.dim_date'[full_date])

Revenue QTD = 
TOTALQTD([Total Revenue], 'dw.dim_date'[full_date])

Revenue Last Month = 
CALCULATE(
    [Total Revenue],
    PREVIOUSMONTH('dw.dim_date'[full_date])
)

Revenue MoM Growth % = 
DIVIDE(
    [Total Revenue] - [Revenue Last Month],
    [Revenue Last Month],
    0
) * 100

Average Transaction Value = 
AVERAGE('dw.fact_transaction'[total_amount])
```

### Volume Metrics

```dax
Total Quantity (kg) = SUM('dw.fact_transaction'[quantity_kg])

Total Transactions = COUNT('dw.fact_transaction'[transaction_id])

Average Price per kg = 
DIVIDE(
    [Total Revenue],
    [Total Quantity (kg)],
    0
)

Average Quantity per Transaction = 
AVERAGE('dw.fact_transaction'[quantity_kg])
```

### Farmer Metrics

```dax
Active Farmers = 
DISTINCTCOUNT('dw.fact_transaction'[farmer_key])

Total Registered Farmers = 
COUNTROWS(
    FILTER(
        'dw.dim_farmer',
        'dw.dim_farmer'[is_current] = TRUE
    )
)

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

Average Revenue per Farmer = 
DIVIDE(
    [Total Revenue],
    [Active Farmers],
    0
)

Average Transactions per Farmer = 
DIVIDE(
    [Total Transactions],
    [Active Farmers],
    0
)
```

### Market Metrics

```dax
Active Markets = 
DISTINCTCOUNT('dw.fact_transaction'[market_key])

Market Share % = 
DIVIDE(
    [Total Revenue],
    CALCULATE(
        [Total Revenue],
        ALL('dw.dim_market')
    ),
    0
) * 100

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

Standard Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        'dw.dim_quality'[quality_grade] = "B"
    ),
    [Total Quantity (kg)],
    0
) * 100

Below Standard Quality % = 
DIVIDE(
    CALCULATE(
        [Total Quantity (kg)],
        'dw.dim_quality'[quality_grade] = "C"
    ),
    [Total Quantity (kg)],
    0
) * 100

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

Mobile Money % = 
DIVIDE(
    [Mobile Money Revenue],
    [Total Revenue],
    0
) * 100

Cash Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_payment_method'[payment_method] = "Cash"
)

Digital Payment % = 
DIVIDE(
    CALCULATE(
        [Total Revenue],
        'dw.dim_payment_method'[is_digital] = TRUE
    ),
    [Total Revenue],
    0
) * 100

Payment Success Rate % = 
DIVIDE(
    CALCULATE(
        [Total Transactions],
        'dw.fact_transaction'[payment_status] = "Paid"
    ),
    [Total Transactions],
    0
) * 100
```

### Blockchain Metrics

```dax
Blockchain Verification Rate % = 
DIVIDE(
    CALCULATE(
        [Total Transactions],
        NOT(ISBLANK('dw.fact_transaction'[blockchain_hash]))
    ),
    [Total Transactions],
    0
) * 100

Verified Transactions = 
CALCULATE(
    [Total Transactions],
    NOT(ISBLANK('dw.fact_transaction'[blockchain_hash]))
)

Unverified Transactions = 
CALCULATE(
    [Total Transactions],
    ISBLANK('dw.fact_transaction'[blockchain_hash])
)
```

### Regional Metrics

```dax
Central Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Central"
)

Eastern Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Eastern"
)

Northern Region Revenue = 
CALCULATE(
    [Total Revenue],
    'dw.dim_farmer'[region] = "Northern"
)

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
Transaction Year = YEAR('dw.fact_transaction'[transaction_timestamp])
Transaction Quarter = "Q" & QUARTER('dw.fact_transaction'[transaction_timestamp])
```

**On dim_farmer table:**
```dax
Farmer Age = DATEDIFF('dw.dim_farmer'[date_of_birth], TODAY(), YEAR)
```
