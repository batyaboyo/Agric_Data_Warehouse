-- ============================================================================
-- Database Creation Script
-- Agricultural Supply Chain Data Warehouse
-- ============================================================================
-- Purpose: Create database and schemas
-- Author: Data Warehouse Team
-- Date: 2025-12-04
-- ============================================================================

-- Drop database if exists (for clean setup)
-- DROP DATABASE IF EXISTS agri_dw;

-- Create database
-- Note: Database creation should be done manually in pgAdmin or via psql
-- CREATE DATABASE agri_dw
--     WITH 
--     OWNER = postgres
--     ENCODING = 'UTF8'
--     LC_COLLATE = 'English_United States.1252'
--     LC_CTYPE = 'English_United States.1252'
--     TABLESPACE = pg_default
--     CONNECTION LIMIT = -1;

-- COMMENT ON DATABASE agri_dw IS 'Agricultural Supply Chain Data Warehouse';

-- Connect to the database
-- Note: \c is a psql metacommand and won't work in pgAdmin Query Tool
-- Make sure you're connected to agri_dw database before running this script
-- \c agri_dw

-- ============================================================================
-- Create Schemas
-- ============================================================================

-- Staging schema for raw data ingestion
CREATE SCHEMA IF NOT EXISTS staging;
COMMENT ON SCHEMA staging IS 'Staging area for raw data from source systems';

-- Data warehouse schema for dimensional model
CREATE SCHEMA IF NOT EXISTS dw;
COMMENT ON SCHEMA dw IS 'Data warehouse dimensional model (facts and dimensions)';

-- Audit schema for ETL metadata and logging
CREATE SCHEMA IF NOT EXISTS audit;
COMMENT ON SCHEMA audit IS 'Audit logs and ETL metadata';

-- ============================================================================
-- Create Extensions
-- ============================================================================

-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Cryptographic functions (for hashing)
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ============================================================================
-- Set Search Path
-- ============================================================================

SET search_path TO dw, staging, audit, public;

-- ============================================================================
-- Create Audit Tables
-- ============================================================================

-- ETL execution log
CREATE TABLE IF NOT EXISTS audit.etl_execution_log (
    execution_id BIGSERIAL PRIMARY KEY,
    job_name VARCHAR(100) NOT NULL,
    start_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status VARCHAR(20) NOT NULL CHECK (status IN ('Running', 'Success', 'Failed', 'Cancelled')),
    rows_read INTEGER,
    rows_inserted INTEGER,
    rows_updated INTEGER,
    rows_rejected INTEGER,
    error_message TEXT,
    execution_user VARCHAR(50) DEFAULT CURRENT_USER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE audit.etl_execution_log IS 'Log of all ETL job executions';

-- Data quality log
CREATE TABLE IF NOT EXISTS audit.data_quality_log (
    quality_check_id BIGSERIAL PRIMARY KEY,
    execution_id BIGINT REFERENCES audit.etl_execution_log(execution_id),
    table_name VARCHAR(100) NOT NULL,
    check_name VARCHAR(100) NOT NULL,
    check_type VARCHAR(50) NOT NULL,
    check_result VARCHAR(20) NOT NULL CHECK (check_result IN ('Pass', 'Fail', 'Warning')),
    records_checked INTEGER,
    records_failed INTEGER,
    failure_percentage DECIMAL(5,2),
    check_details TEXT,
    checked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE audit.data_quality_log IS 'Data quality check results';

-- Create indexes on audit tables
CREATE INDEX idx_etl_log_job_name ON audit.etl_execution_log(job_name);
CREATE INDEX idx_etl_log_start_time ON audit.etl_execution_log(start_time);
CREATE INDEX idx_etl_log_status ON audit.etl_execution_log(status);
CREATE INDEX idx_quality_log_execution_id ON audit.data_quality_log(execution_id);
CREATE INDEX idx_quality_log_table_name ON audit.data_quality_log(table_name);

-- ============================================================================
-- Grant Permissions
-- ============================================================================

-- Grant usage on schemas
GRANT USAGE ON SCHEMA staging TO PUBLIC;
GRANT USAGE ON SCHEMA dw TO PUBLIC;
GRANT USAGE ON SCHEMA audit TO PUBLIC;

-- Grant permissions on all tables in schemas
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA staging TO PUBLIC;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA dw TO PUBLIC;
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA audit TO PUBLIC;

-- Grant permissions on sequences
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA staging TO PUBLIC;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA dw TO PUBLIC;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA audit TO PUBLIC;

-- ============================================================================
-- Success Message
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Database agri_dw created successfully!';
    RAISE NOTICE 'Schemas created: staging, dw, audit';
    RAISE NOTICE 'Extensions enabled: uuid-ossp, pgcrypto';
    RAISE NOTICE '========================================';
END $$;
