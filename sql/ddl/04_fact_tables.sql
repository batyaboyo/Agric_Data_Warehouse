-- ============================================================================
-- Fact Tables Creation Script
-- Agricultural Supply Chain Data Warehouse
-- ============================================================================
-- Purpose: Create fact tables for transactions, harvests, and pricing
-- Schema: dw
-- ============================================================================

\c agri_dw

SET search_path TO dw, public;

-- ============================================================================
-- Fact: Transaction
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.fact_transaction (
    transaction_key BIGSERIAL PRIMARY KEY,
    -- Foreign Keys to Dimensions
    farmer_key BIGINT NOT NULL REFERENCES dw.dim_farmer(farmer_key),
    buyer_key BIGINT NOT NULL REFERENCES dw.dim_buyer(buyer_key),
    product_key BIGINT NOT NULL REFERENCES dw.dim_product(product_key),
    market_key BIGINT NOT NULL REFERENCES dw.dim_market(market_key),
    date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    payment_key BIGINT NOT NULL REFERENCES dw.dim_payment_method(payment_key),
    quality_key BIGINT NOT NULL REFERENCES dw.dim_quality(quality_key),
    -- Degenerate Dimensions
    transaction_id VARCHAR(30) NOT NULL,
    blockchain_hash VARCHAR(64),
    payment_status VARCHAR(20),
    -- Measures (Additive)
    quantity_kg DECIMAL(10,2) NOT NULL CHECK (quantity_kg > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount > 0),
    transaction_count INTEGER NOT NULL DEFAULT 1,
    payment_fee DECIMAL(10,2) DEFAULT 0,
    net_amount DECIMAL(12,2),
    -- Timestamps
    transaction_timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.fact_transaction IS 'Transaction fact table - grain: one row per transaction';

-- Indexes for performance
CREATE INDEX idx_fact_transaction_farmer ON dw.fact_transaction(farmer_key);
CREATE INDEX idx_fact_transaction_buyer ON dw.fact_transaction(buyer_key);
CREATE INDEX idx_fact_transaction_product ON dw.fact_transaction(product_key);
CREATE INDEX idx_fact_transaction_market ON dw.fact_transaction(market_key);
CREATE INDEX idx_fact_transaction_date ON dw.fact_transaction(date_key);
CREATE INDEX idx_fact_transaction_timestamp ON dw.fact_transaction(transaction_timestamp);
CREATE INDEX idx_fact_transaction_id ON dw.fact_transaction(transaction_id);
CREATE INDEX idx_fact_transaction_blockchain ON dw.fact_transaction(blockchain_hash);

-- ============================================================================
-- Fact: Harvest
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.fact_harvest (
    harvest_key BIGSERIAL PRIMARY KEY,
    -- Foreign Keys to Dimensions
    farmer_key BIGINT NOT NULL REFERENCES dw.dim_farmer(farmer_key),
    product_key BIGINT NOT NULL REFERENCES dw.dim_product(product_key),
    planting_date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    harvest_date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    location_key BIGINT REFERENCES dw.dim_location(location_key),
    -- Degenerate Dimensions
    harvest_id VARCHAR(30) NOT NULL,
    quality_assessment VARCHAR(20),
    storage_method VARCHAR(50),
    season VARCHAR(20),
    -- Measures (Additive)
    quantity_kg DECIMAL(10,2) NOT NULL CHECK (quantity_kg > 0),
    post_harvest_loss_kg DECIMAL(10,2) DEFAULT 0,
    post_harvest_loss_pct DECIMAL(5,2) DEFAULT 0,
    net_quantity_kg DECIMAL(10,2),
    growing_days INTEGER,
    harvest_count INTEGER NOT NULL DEFAULT 1,
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.fact_harvest IS 'Harvest fact table - grain: one row per harvest event';

-- Indexes
CREATE INDEX idx_fact_harvest_farmer ON dw.fact_harvest(farmer_key);
CREATE INDEX idx_fact_harvest_product ON dw.fact_harvest(product_key);
CREATE INDEX idx_fact_harvest_planting_date ON dw.fact_harvest(planting_date_key);
CREATE INDEX idx_fact_harvest_harvest_date ON dw.fact_harvest(harvest_date_key);
CREATE INDEX idx_fact_harvest_location ON dw.fact_harvest(location_key);
CREATE INDEX idx_fact_harvest_id ON dw.fact_harvest(harvest_id);

-- ============================================================================
-- Fact: Pricing
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.fact_pricing (
    pricing_key BIGSERIAL PRIMARY KEY,
    -- Foreign Keys to Dimensions
    product_key BIGINT NOT NULL REFERENCES dw.dim_product(product_key),
    market_key BIGINT NOT NULL REFERENCES dw.dim_market(market_key),
    date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    -- Degenerate Dimensions
    price_id VARCHAR(30) NOT NULL,
    price_trend VARCHAR(10),
    source VARCHAR(50),
    -- Measures (Semi-Additive - can't sum across time)
    wholesale_price DECIMAL(10,2) NOT NULL CHECK (wholesale_price > 0),
    retail_price DECIMAL(10,2) NOT NULL CHECK (retail_price > 0),
    price_spread DECIMAL(10,2),
    price_spread_pct DECIMAL(5,2),
    price_change_pct DECIMAL(5,2),
    price_volatility_index DECIMAL(5,2),
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_key, market_key, date_key)
);

COMMENT ON TABLE dw.fact_pricing IS 'Pricing fact table - grain: one row per product/market/day';

-- Indexes
CREATE INDEX idx_fact_pricing_product ON dw.fact_pricing(product_key);
CREATE INDEX idx_fact_pricing_market ON dw.fact_pricing(market_key);
CREATE INDEX idx_fact_pricing_date ON dw.fact_pricing(date_key);
CREATE INDEX idx_fact_pricing_id ON dw.fact_pricing(price_id);

-- ============================================================================
-- Fact: Subsidy
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.fact_subsidy (
    subsidy_key BIGSERIAL PRIMARY KEY,
    -- Foreign Keys to Dimensions
    farmer_key BIGINT NOT NULL REFERENCES dw.dim_farmer(farmer_key),
    date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    -- Degenerate Dimensions
    farmer_subsidy_id VARCHAR(30) NOT NULL,
    subsidy_id VARCHAR(30),
    program_name VARCHAR(100),
    subsidy_type VARCHAR(50),
    verification_status VARCHAR(20),
    -- Measures (Additive)
    amount_value DECIMAL(10,2) NOT NULL CHECK (amount_value > 0),
    subsidy_count INTEGER NOT NULL DEFAULT 1,
    -- Timestamps
    distribution_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.fact_subsidy IS 'Subsidy fact table - grain: one row per subsidy distribution';

-- Indexes
CREATE INDEX idx_fact_subsidy_farmer ON dw.fact_subsidy(farmer_key);
CREATE INDEX idx_fact_subsidy_date ON dw.fact_subsidy(date_key);
CREATE INDEX idx_fact_subsidy_id ON dw.fact_subsidy(farmer_subsidy_id);
CREATE INDEX idx_fact_subsidy_program ON dw.fact_subsidy(program_name);

-- ============================================================================
-- Create Aggregate/Summary Tables (Optional - for performance)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.fact_transaction_daily_summary (
    summary_key BIGSERIAL PRIMARY KEY,
    date_key INTEGER NOT NULL REFERENCES dw.dim_date(date_key),
    product_key BIGINT NOT NULL REFERENCES dw.dim_product(product_key),
    market_key BIGINT NOT NULL REFERENCES dw.dim_market(market_key),
    total_quantity_kg DECIMAL(12,2),
    total_amount DECIMAL(15,2),
    transaction_count INTEGER,
    avg_unit_price DECIMAL(10,2),
    min_unit_price DECIMAL(10,2),
    max_unit_price DECIMAL(10,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(date_key, product_key, market_key)
);

COMMENT ON TABLE dw.fact_transaction_daily_summary IS 'Daily aggregated transaction summary for performance';

CREATE INDEX idx_fact_txn_summary_date ON dw.fact_transaction_daily_summary(date_key);
CREATE INDEX idx_fact_txn_summary_product ON dw.fact_transaction_daily_summary(product_key);
CREATE INDEX idx_fact_txn_summary_market ON dw.fact_transaction_daily_summary(market_key);

-- ============================================================================
-- Success Message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Fact tables created successfully!';
    RAISE NOTICE 'Tables: fact_transaction, fact_harvest, fact_pricing, fact_subsidy';
    RAISE NOTICE 'Summary table: fact_transaction_daily_summary';
    RAISE NOTICE '========================================';
END $$;
