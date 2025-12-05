-- ============================================================================
-- Dimension Tables Creation Script (with SCD Type 2)
-- Agricultural Supply Chain Data Warehouse
-- ============================================================================
-- Purpose: Create dimension tables with Slowly Changing Dimension Type 2
-- Schema: dw
-- ============================================================================

\c agri_dw

SET search_path TO dw, public;

-- ============================================================================
-- Dimension: Date (Pre-populated)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE UNIQUE NOT NULL,
    day_of_week INTEGER NOT NULL,
    day_name VARCHAR(10) NOT NULL,
    day_of_month INTEGER NOT NULL,
    day_of_year INTEGER NOT NULL,
    week_of_year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name VARCHAR(10) NOT NULL,
    quarter INTEGER NOT NULL,
    quarter_name VARCHAR(2) NOT NULL,
    year INTEGER NOT NULL,
    is_weekend BOOLEAN NOT NULL,
    is_holiday BOOLEAN DEFAULT FALSE,
    holiday_name VARCHAR(50),
    season VARCHAR(20),
    fiscal_year INTEGER,
    fiscal_quarter INTEGER,
    fiscal_month INTEGER
);

COMMENT ON TABLE dw.dim_date IS 'Date dimension with calendar attributes';

-- ============================================================================
-- Dimension: Farmer (SCD Type 2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_farmer (
    farmer_key BIGSERIAL PRIMARY KEY,
    farmer_id VARCHAR(20) NOT NULL,  -- Natural key
    national_id VARCHAR(14),
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    gender CHAR(1),
    date_of_birth DATE,
    age_group VARCHAR(20),
    phone_number VARCHAR(15),
    district VARCHAR(50),
    subcounty VARCHAR(50),
    village VARCHAR(50),
    region VARCHAR(30),
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8),
    farm_size_acres DECIMAL(8,2),
    farm_size_category VARCHAR(20),
    primary_crop VARCHAR(50),
    cooperative_id VARCHAR(20),
    cooperative_name VARCHAR(100),
    blockchain_wallet VARCHAR(64),
    registration_date DATE,
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_farmer IS 'Farmer dimension with SCD Type 2';

CREATE INDEX idx_dim_farmer_id ON dw.dim_farmer(farmer_id);
CREATE INDEX idx_dim_farmer_current ON dw.dim_farmer(is_current);
CREATE INDEX idx_dim_farmer_district ON dw.dim_farmer(district);
CREATE INDEX idx_dim_farmer_cooperative ON dw.dim_farmer(cooperative_id);

-- ============================================================================
-- Dimension: Product (SCD Type 2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_product (
    product_key BIGSERIAL PRIMARY KEY,
    product_id VARCHAR(20) NOT NULL,  -- Natural key
    product_name VARCHAR(50) NOT NULL,
    category VARCHAR(30),
    category_group VARCHAR(30),
    variety VARCHAR(50),
    unit_of_measure VARCHAR(10),
    season VARCHAR(20),
    avg_growing_days INTEGER,
    growing_period_category VARCHAR(20),
    is_perishable BOOLEAN,
    perishability_category VARCHAR(20),
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_product IS 'Product dimension with SCD Type 2';

CREATE INDEX idx_dim_product_id ON dw.dim_product(product_id);
CREATE INDEX idx_dim_product_current ON dw.dim_product(is_current);
CREATE INDEX idx_dim_product_category ON dw.dim_product(category);
CREATE INDEX idx_dim_product_name ON dw.dim_product(product_name);

-- ============================================================================
-- Dimension: Market (SCD Type 2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_market (
    market_key BIGSERIAL PRIMARY KEY,
    market_id VARCHAR(20) NOT NULL,  -- Natural key
    market_name VARCHAR(100) NOT NULL,
    market_type VARCHAR(30),
    district VARCHAR(50),
    subcounty VARCHAR(50),
    region VARCHAR(30),
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8),
    operating_days VARCHAR(50),
    capacity_kg DECIMAL(12,2),
    capacity_category VARCHAR(20),
    is_active BOOLEAN,
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_market IS 'Market dimension with SCD Type 2';

CREATE INDEX idx_dim_market_id ON dw.dim_market(market_id);
CREATE INDEX idx_dim_market_current ON dw.dim_market(is_current);
CREATE INDEX idx_dim_market_district ON dw.dim_market(district);
CREATE INDEX idx_dim_market_type ON dw.dim_market(market_type);

-- ============================================================================
-- Dimension: Buyer (SCD Type 2)
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_buyer (
    buyer_key BIGSERIAL PRIMARY KEY,
    buyer_id VARCHAR(20) NOT NULL,  -- Natural key
    buyer_name VARCHAR(100) NOT NULL,
    buyer_type VARCHAR(30),
    buyer_category VARCHAR(30),
    contact_person VARCHAR(100),
    phone_number VARCHAR(15),
    email VARCHAR(100),
    district VARCHAR(50),
    region VARCHAR(30),
    registration_number VARCHAR(30),
    blockchain_wallet VARCHAR(64),
    is_active BOOLEAN,
    -- SCD Type 2 attributes
    effective_date DATE NOT NULL DEFAULT CURRENT_DATE,
    end_date DATE DEFAULT '9999-12-31',
    is_current BOOLEAN NOT NULL DEFAULT TRUE,
    version INTEGER NOT NULL DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_buyer IS 'Buyer dimension with SCD Type 2';

CREATE INDEX idx_dim_buyer_id ON dw.dim_buyer(buyer_id);
CREATE INDEX idx_dim_buyer_current ON dw.dim_buyer(is_current);
CREATE INDEX idx_dim_buyer_type ON dw.dim_buyer(buyer_type);

-- ============================================================================
-- Dimension: Location
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_location (
    location_key BIGSERIAL PRIMARY KEY,
    district VARCHAR(50) NOT NULL,
    subcounty VARCHAR(50),
    region VARCHAR(30),
    zone VARCHAR(30),
    gps_latitude DECIMAL(10,8),
    gps_longitude DECIMAL(11,8),
    population INTEGER,
    urban_rural VARCHAR(10),
    market_access_score DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(district, subcounty)
);

COMMENT ON TABLE dw.dim_location IS 'Location dimension';

CREATE INDEX idx_dim_location_district ON dw.dim_location(district);
CREATE INDEX idx_dim_location_region ON dw.dim_location(region);

-- ============================================================================
-- Dimension: Payment Method
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_payment_method (
    payment_key BIGSERIAL PRIMARY KEY,
    payment_method VARCHAR(20) UNIQUE NOT NULL,
    payment_category VARCHAR(30),
    is_digital BOOLEAN,
    transaction_fee_pct DECIMAL(5,2),
    settlement_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_payment_method IS 'Payment method dimension';

-- ============================================================================
-- Dimension: Quality Grade
-- ============================================================================

CREATE TABLE IF NOT EXISTS dw.dim_quality (
    quality_key BIGSERIAL PRIMARY KEY,
    quality_grade CHAR(1) UNIQUE NOT NULL,
    quality_description VARCHAR(50),
    quality_score INTEGER,
    price_premium_pct DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE dw.dim_quality IS 'Quality grade dimension';

-- ============================================================================
-- Pre-populate Static Dimensions
-- ============================================================================

-- Payment Methods
INSERT INTO dw.dim_payment_method (payment_method, payment_category, is_digital, transaction_fee_pct, settlement_days)
VALUES 
    ('Mobile Money', 'Digital', TRUE, 1.5, 0),
    ('Cash', 'Physical', FALSE, 0.0, 0),
    ('Bank Transfer', 'Digital', TRUE, 0.5, 1),
    ('Cooperative Account', 'Digital', TRUE, 0.0, 0),
    ('Check', 'Physical', FALSE, 0.0, 3)
ON CONFLICT (payment_method) DO NOTHING;

-- Quality Grades
INSERT INTO dw.dim_quality (quality_grade, quality_description, quality_score, price_premium_pct)
VALUES 
    ('A', 'Premium Quality', 100, 25.0),
    ('B', 'Standard Quality', 80, 0.0),
    ('C', 'Below Standard', 60, -20.0)
ON CONFLICT (quality_grade) DO NOTHING;

-- ============================================================================
-- Success Message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Dimension tables created successfully!';
    RAISE NOTICE 'Tables: dim_date, dim_farmer, dim_product, dim_market, dim_buyer, dim_location, dim_payment_method, dim_quality';
    RAISE NOTICE 'SCD Type 2 implemented for: farmer, product, market, buyer';
    RAISE NOTICE '========================================';
END $$;
