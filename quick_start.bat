@echo off
REM ============================================================================
REM Quick Start Script for Agricultural Data Warehouse
REM Windows Batch File
REM ============================================================================

echo ============================================================================
echo AGRICULTURAL SUPPLY CHAIN DATA WAREHOUSE - QUICK START
echo ============================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if PostgreSQL is installed
psql --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: PostgreSQL is not installed or not in PATH
    echo Please install PostgreSQL 15+ from https://www.postgresql.org/download/windows/
    pause
    exit /b 1
)

echo [1/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)
echo.

echo [2/5] Creating database and tables...
echo Please enter PostgreSQL password when prompted
psql -U postgres -f sql/ddl/01_create_database.sql
psql -U postgres -d agri_dw -f sql/ddl/02_staging_tables.sql
psql -U postgres -d agri_dw -f sql/ddl/03_dimension_tables.sql
psql -U postgres -d agri_dw -f sql/ddl/04_fact_tables.sql
if errorlevel 1 (
    echo ERROR: Failed to create database
    pause
    exit /b 1
)
echo.

echo [3/5] Generating synthetic data (30,000+ rows)...
cd scripts\data_generation
python master_data_generator.py
if errorlevel 1 (
    echo ERROR: Failed to generate data
    cd ..\..
    pause
    exit /b 1
)
cd ..\..
echo.

echo [4/5] Running ETL pipeline...
cd scripts\etl
python etl_staging_to_dw.py
if errorlevel 1 (
    echo ERROR: Failed to run ETL
    cd ..\..
    pause
    exit /b 1
)
cd ..\..
echo.

echo [5/5] Exporting data for Power BI...
cd scripts\powerbi
python export_powerbi_data.py
if errorlevel 1 (
    echo ERROR: Failed to export Power BI data
    cd ..\..
    pause
    exit /b 1
)
cd ..\..
echo.

echo ============================================================================
echo SUCCESS! Data warehouse setup complete
echo ============================================================================
echo.
echo Next steps:
echo 1. Open Power BI Desktop
echo 2. Import: powerbi/powerbi_dataset.csv
echo 3. Create measures from: powerbi/dax_measures.txt
echo 4. Build dashboards using: powerbi/dashboard_specifications.md
echo.
echo For verification, run:
echo   psql -U postgres -d agri_dw -c "SELECT COUNT(*) FROM dw.fact_transaction"
echo.
echo ============================================================================
pause
