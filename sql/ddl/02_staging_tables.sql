-- ============================================================================
-- Staging Tables Creation Script
-- Agricultural Supply Chain Data Warehouse
-- ============================================================================
-- Purpose: Create staging tables for raw data ingestion from source systems
-- Schema: staging
-- ============================================================================

-- Connect to agri_dw database
-- Note: \c is a psql metacommand and won't work in pgAdmin Query Tool
-- Make sure you're connected to agri_dw database before running this script
-- \c agri_dw

SET search_path TO staging, public;

-- ============================================================================
-- Staging: Farmers
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_farmers (
    farmer_id VARCHAR(20) PRIMARY KEY,
    national_id VARCHAR(14) UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender CHAR(1) CHECK (gender IN ('M', 'F')),
    date_of_birth DATE,
    phone_number VARCHAR(15),
    district VARCHAR(50),
    subcounty VARCHAR(50),
    village VARCHAR(50),
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8),
    farm_size_acres DECIMAL(8,2) CHECK (farm_size_acres > 0),
    primary_crop VARCHAR(50),
    cooperative_id VARCHAR(20),
    blockchain_wallet VARCHAR(64) UNIQUE,
    registration_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_farmers IS 'Staging table for farmer registration data';

-- ============================================================================
-- Staging: Products
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(30),
    variety VARCHAR(50),
    unit_of_measure VARCHAR(10),
    season VARCHAR(20),
    avg_growing_days INTEGER,
    is_perishable BOOLEAN,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_products IS 'Staging table for agricultural products';

-- ============================================================================
-- Staging: Markets
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_markets (
    market_id VARCHAR(20) PRIMARY KEY,
    market_name VARCHAR(100) NOT NULL,
    market_type VARCHAR(30),
    district VARCHAR(50),
    subcounty VARCHAR(50),
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8),
    operating_days VARCHAR(50),
    capacity_kg DECIMAL(12,2),
    is_active BOOLEAN DEFAULT TRUE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_markets IS 'Staging table for markets and collection centers';

-- ============================================================================
-- Staging: Buyers
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_buyers (
    buyer_id VARCHAR(20) PRIMARY KEY,
    buyer_name VARCHAR(100) NOT NULL,
    buyer_type VARCHAR(30),
    contact_person VARCHAR(100),
    phone_number VARCHAR(15),
    email VARCHAR(100),
    district VARCHAR(50),
    registration_number VARCHAR(30),
    blockchain_wallet VARCHAR(64) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_buyers IS 'Staging table for buyers and traders';

-- ============================================================================
-- Staging: Transactions
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,
    farmer_id VARCHAR(20),
    buyer_id VARCHAR(20),
    product_id VARCHAR(20),
    market_id VARCHAR(20),
    quantity_kg DECIMAL(10,2) CHECK (quantity_kg > 0),
    quality_grade CHAR(1) CHECK (quality_grade IN ('A', 'B', 'C')),
    unit_price DECIMAL(10,2) CHECK (unit_price > 0),
    total_amount DECIMAL(12,2) CHECK (total_amount > 0),
    transaction_date TIMESTAMP NOT NULL,
    payment_method VARCHAR(20),
    payment_status VARCHAR(20),
    blockchain_hash VARCHAR(64) UNIQUE,
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_transactions IS 'Staging table for market transactions';

-- ============================================================================
-- Staging: Harvests
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_harvests (
    harvest_id VARCHAR(30) PRIMARY KEY,
    farmer_id VARCHAR(20),
    product_id VARCHAR(20),
    planting_date DATE,
    harvest_date DATE,
    quantity_kg DECIMAL(10,2) CHECK (quantity_kg > 0),
    quality_assessment VARCHAR(20),
    post_harvest_loss_pct DECIMAL(5,2) CHECK (post_harvest_loss_pct >= 0 AND post_harvest_loss_pct <= 100),
    storage_method VARCHAR(50),
    season VARCHAR(20),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_harvests IS 'Staging table for harvest records';

-- ============================================================================
-- Staging: Market Pricing
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_pricing (
    price_id VARCHAR(30) PRIMARY KEY,
    product_id VARCHAR(20),
    market_id VARCHAR(20),
    price_date DATE NOT NULL,
    wholesale_price DECIMAL(10,2) CHECK (wholesale_price > 0),
    retail_price DECIMAL(10,2) CHECK (retail_price > 0),
    price_trend VARCHAR(10),
    source VARCHAR(50),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_pricing IS 'Staging table for market pricing data';

-- ============================================================================
-- Staging: Weather Data
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_weather (
    weather_id VARCHAR(30) PRIMARY KEY,
    district VARCHAR(50),
    weather_date DATE NOT NULL,
    temperature_min DECIMAL(5,2),
    temperature_max DECIMAL(5,2),
    temperature_avg DECIMAL(5,2),
    rainfall_mm DECIMAL(6,2),
    humidity_pct DECIMAL(5,2),
    wind_speed_kmh DECIMAL(5,2),
    weather_condition VARCHAR(30),
    source VARCHAR(50),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_weather IS 'Staging table for weather data';

-- ============================================================================
-- Staging: Subsidies
-- ============================================================================

CREATE TABLE IF NOT EXISTS staging.stg_subsidies (
    farmer_subsidy_id VARCHAR(30) PRIMARY KEY,
    farmer_id VARCHAR(20),
    subsidy_id VARCHAR(30),
    program_name VARCHAR(100),
    subsidy_type VARCHAR(50),
    amount_value DECIMAL(10,2),
    distribution_date DATE,
    verification_status VARCHAR(20),
    loaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE staging.stg_subsidies IS 'Staging table for government subsidy programs';

-- ============================================================================
-- Create Indexes on Staging Tables
-- ============================================================================

-- Farmers
CREATE INDEX idx_stg_farmers_district ON staging.stg_farmers(district);
CREATE INDEX idx_stg_farmers_cooperative ON staging.stg_farmers(cooperative_id);
CREATE INDEX idx_stg_farmers_loaded_at ON staging.stg_farmers(loaded_at);

-- Transactions
CREATE INDEX idx_stg_transactions_farmer ON staging.stg_transactions(farmer_id);
CREATE INDEX idx_stg_transactions_product ON staging.stg_transactions(product_id);
CREATE INDEX idx_stg_transactions_market ON staging.stg_transactions(market_id);
CREATE INDEX idx_stg_transactions_date ON staging.stg_transactions(transaction_date);
CREATE INDEX idx_stg_transactions_loaded_at ON staging.stg_transactions(loaded_at);

-- Harvests
CREATE INDEX idx_stg_harvests_farmer ON staging.stg_harvests(farmer_id);
CREATE INDEX idx_stg_harvests_product ON staging.stg_harvests(product_id);
CREATE INDEX idx_stg_harvests_date ON staging.stg_harvests(harvest_date);

-- Pricing
CREATE INDEX idx_stg_pricing_product ON staging.stg_pricing(product_id);
CREATE INDEX idx_stg_pricing_market ON staging.stg_pricing(market_id);
CREATE INDEX idx_stg_pricing_date ON staging.stg_pricing(price_date);

-- Weather
CREATE INDEX idx_stg_weather_district ON staging.stg_weather(district);
CREATE INDEX idx_stg_weather_date ON staging.stg_weather(weather_date);

-- Subsidies
CREATE INDEX idx_stg_subsidies_farmer ON staging.stg_subsidies(farmer_id);

-- ============================================================================
-- Success Message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Staging tables created successfully!';
    RAISE NOTICE 'Tables: farmers, products, markets, buyers, transactions, harvests, pricing, weather, subsidies';
    RAISE NOTICE '========================================';
END $$;
