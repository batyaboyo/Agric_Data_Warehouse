# Complete Setup Guide - Step by Step
## Agricultural Supply Chain Data Warehouse

**For Complete Beginners - No Prior Setup Required**

---

## 📋 Table of Contents

1. [Prerequisites Installation](#prerequisites-installation)
2. [Project Setup](#project-setup)
3. [Database Setup](#database-setup)
4. [Data Generation](#data-generation)
5. [ETL Execution](#etl-execution)
6. [Power BI Setup](#power-bi-setup)
7. [Verification & Testing](#verification--testing)
8. [Troubleshooting](#troubleshooting)
9. [Next Steps](#next-steps)

---

## 1. Prerequisites Installation

### 1.1 Install PostgreSQL (Database)

**Why**: PostgreSQL is our data warehouse database.

**Steps**:

1. **Download PostgreSQL**:
   - Go to: https://www.postgresql.org/download/windows/
   - Click "Download the installer"
   - Choose version 15.x or 16.x (latest stable)
   - Download the Windows x86-64 installer

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Click "Next" on welcome screen
   - **Installation Directory**: Keep default (`C:\Program Files\PostgreSQL\15`)
   - **Select Components**: Check ALL boxes:
     - ✅ PostgreSQL Server
     - ✅ pgAdmin 4 (GUI tool - very important!)
     - ✅ Stack Builder
     - ✅ Command Line Tools
   - Click "Next"

3. **Data Directory**: Keep default (`C:\Program Files\PostgreSQL\15\data`)

4. **Set Password** (VERY IMPORTANT!):
   - Enter a password for the `postgres` user
   - **Remember this password!** You'll need it many times
   - Example: `postgres123` (use something you'll remember)
   - Re-enter to confirm
   - Click "Next"

5. **Port**: Keep default `5432`

6. **Locale**: Keep default (Default locale)

7. **Summary**: Review and click "Next"

8. **Installation**: Click "Next" to start installation (takes 2-3 minutes)

9. **Finish**: 
   - Uncheck "Launch Stack Builder" (not needed now)
   - Click "Finish"

**Verify Installation**:
```powershell
# Open PowerShell (Windows key + X, then select PowerShell)
psql --version
```
Expected output: `psql (PostgreSQL) 15.x`

If you get "command not found", you need to add PostgreSQL to PATH:
1. Search "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Click "Edit"
5. Click "New"
6. Add: `C:\Program Files\PostgreSQL\15\bin`
7. Click "OK" on all windows
8. **Close and reopen PowerShell**

---

### 1.2 Install Python

**Why**: Python runs our data generation and ETL scripts.

**Steps**:

1. **Download Python**:
   - Go to: https://www.python.org/downloads/
   - Click the big yellow "Download Python 3.12.x" button
   - Save the installer

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - **CRITICAL**: ✅ Check "Add python.exe to PATH" at the bottom!
   - Click "Install Now"
   - Wait for installation (1-2 minutes)
   - Click "Close"

**Verify Installation**:
```powershell
# In PowerShell
python --version
pip --version
```
Expected output:
```
Python 3.12.x
pip 24.x from ...
```

If you get "command not found":
1. Restart PowerShell
2. If still not working, reinstall Python and make sure to check "Add to PATH"

---

### 1.3 Install Git (Optional but Recommended)

**Why**: For version control and downloading code if needed.

**Steps**:

1. **Download Git**:
   - Go to: https://git-scm.com/download/win
   - Download will start automatically
   - Or click "Click here to download"

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Click "Next" through most screens (defaults are fine)
   - **Important screens**:
     - "Adjusting your PATH": Select "Git from the command line and also from 3rd-party software"
     - "Choosing the default editor": Select "Use Visual Studio Code" (or Notepad++)
     - Everything else: Keep defaults
   - Click "Install"
   - Click "Finish"

**Verify Installation**:
```powershell
git --version
```
Expected output: `git version 2.x.x`

---

### 1.4 Install Visual Studio Code (Recommended)

**Why**: Best editor for viewing and editing project files.

**Steps**:

1. **Download VS Code**:
   - Go to: https://code.visualstudio.com/
   - Click "Download for Windows"

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Accept license agreement
   - Keep default installation location
   - **Important**: Check these boxes:
     - ✅ Add "Open with Code" action to Windows Explorer file context menu
     - ✅ Add "Open with Code" action to Windows Explorer directory context menu
     - ✅ Add to PATH
   - Click "Next" and "Install"
   - Click "Finish"

3. **Install Useful Extensions** (Optional):
   - Open VS Code
   - Click Extensions icon (left sidebar, or Ctrl+Shift+X)
   - Search and install:
     - "Python" by Microsoft
     - "PostgreSQL" by Chris Kolkman
     - "Markdown PDF" by yzane (for converting reports to PDF)
     - "PlantUML" by jebbs (for viewing diagrams)

---

### 1.5 Install Power BI Desktop (For Analytics)

**Why**: To create dashboards and visualizations.

**Steps**:

1. **Download Power BI**:
   - Go to: https://powerbi.microsoft.com/desktop/
   - Click "Download free"
   - Or go to Microsoft Store and search "Power BI Desktop"

2. **Install**:
   - If downloaded from website: Run the `.exe` file
   - If from Microsoft Store: Click "Install"
   - Wait for installation (5-10 minutes)

3. **First Launch**:
   - Open Power BI Desktop
   - Sign in with Microsoft account (or skip for now)
   - Close welcome screens

**Note**: Power BI is optional for initial setup. You can install it later when ready to create dashboards.

---

## 2. Project Setup

### 2.1 Verify Project Files

**Check that you have the project folder**:

```powershell
# Open PowerShell
cd c:\Users\batzt\Desktop\agric_dw

# List files
dir
```

You should see folders like:
- `data/`
- `diagrams/`
- `docs/`
- `sql/`
- `scripts/`
- `powerbi/`
- Files like `README.md`, `SETUP_GUIDE.md`, `quick_start.bat`

If you don't see these files, the project hasn't been created yet. Let me know!

---

### 2.2 Install Python Dependencies

**What this does**: Installs all Python libraries needed for data generation and ETL.

**Steps**:

1. **Open PowerShell as Administrator**:
   - Press Windows key
   - Type "PowerShell"
   - Right-click "Windows PowerShell"
   - Select "Run as administrator"
   - Click "Yes" on UAC prompt

2. **Navigate to project folder**:
   ```powershell
   cd c:\Users\batzt\Desktop\agric_dw
   ```

3. **Check if requirements.txt exists**:
   ```powershell
   cat requirements.txt
   ```
   You should see a list of Python packages.

4. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

   This will install:
   - pandas (data manipulation)
   - numpy (numerical operations)
   - faker (fake data generation)
   - psycopg2-binary (PostgreSQL connection)
   - And others...

   **Expected output**:
   ```
   Collecting pandas==2.1.4
   Downloading pandas-2.1.4-...
   Installing collected packages: ...
   Successfully installed pandas-2.1.4 numpy-1.26.2 ...
   ```

   **Time**: 2-5 minutes depending on internet speed

5. **Verify installation**:
   ```powershell
   pip list
   ```
   You should see all installed packages.

**Troubleshooting**:
- If you get "pip is not recognized": Reinstall Python with "Add to PATH" checked
- If you get permission errors: Make sure you're running PowerShell as Administrator
- If specific package fails: Try installing individually: `pip install pandas`

---

## 3. Database Setup

### 3.1 Open pgAdmin (PostgreSQL GUI)

**Steps**:

1. **Launch pgAdmin**:
   - Press Windows key
   - Type "pgAdmin"
   - Click "pgAdmin 4"
   - Wait for it to open in your browser (it's a web app)

2. **First-time setup**:
   - Set a master password for pgAdmin (can be same as postgres password)
   - Click "OK"

3. **Connect to PostgreSQL**:
   - In left sidebar, expand "Servers"
   - Click "PostgreSQL 15" (or your version)
   - Enter the password you set during PostgreSQL installation
   - Check "Save password" (optional)
   - Click "OK"

You should now see:
- Databases
  - postgres (default database)
  - template0
  - template1

---

### 3.2 Create the Database Using pgAdmin

**Step 1: Create Empty Database**

1. In pgAdmin, in the left sidebar, expand **"Servers"** → **"PostgreSQL 15"** (or your version)
2. Right-click **"Databases"**
3. Select **"Create"** → **"Database..."**
4. In the dialog:
   - **Database name**: `agri_dw`
   - **Owner**: `postgres` (should be default)
   - Leave other settings as default
5. Click **"Save"**

You should now see `agri_dw` in the databases list.

**Step 2: Run Database Setup Script**

1. Right-click the new **`agri_dw`** database
2. Select **"Query Tool"**
3. In the Query Tool window:
   - Click the **folder icon** (📁 "Open File") in the toolbar
   - Navigate to: `c:\Users\batzt\Desktop\agric_dw\sql\ddl\`
   - Select: **`01_create_database.sql`**
   - Click **"Open"**
4. The SQL script will load in the editor
5. Click the **"Execute/Refresh"** button (▶️ icon) or press **F5**

**Expected Output** (in the "Messages" tab at bottom):
```
CREATE SCHEMA
CREATE SCHEMA
CREATE SCHEMA
CREATE EXTENSION
CREATE EXTENSION
CREATE TABLE
CREATE TABLE
CREATE INDEX
CREATE INDEX
GRANT
GRANT
NOTICE:  ========================================
NOTICE:  Database agri_dw created successfully!
NOTICE:  Schemas created: staging, dw, audit
NOTICE:  Extensions enabled: uuid-ossp, pgcrypto
NOTICE:  ========================================

Query returned successfully in XXX msec.
```

**Verify**:
1. In left sidebar, expand **`agri_dw`** database
2. Expand **"Schemas"**
3. You should see:
   - `audit`
   - `dw`
   - `public`
   - `staging`

---

**Alternative: Using Command Line (Advanced Users)**

If you prefer command line:

```powershell
cd c:\Users\batzt\Desktop\agric_dw
psql -U postgres -f sql/ddl/01_create_database.sql
```

**Note**: This won't work as-is because the script contains `\c` command. Use pgAdmin method above instead.

---

### 3.3 Create Staging Tables

**Using pgAdmin Query Tool**:

1. In the Query Tool (should still be open from previous step)
   - If closed: Right-click **`agri_dw`** database → Select **"Query Tool"**
2. Click the **folder icon** (📁 "Open File")
3. Navigate to: `c:\Users\batzt\Desktop\agric_dw\sql\ddl\`
4. Select: **`02_staging_tables.sql`**
5. Click **"Open"**
6. Click the **"Execute/Refresh"** button (▶️ icon) or press **F5**

**Expected Output**:
```
CREATE TABLE
CREATE TABLE
... (9 times for 9 tables)
CREATE INDEX
CREATE INDEX
... (multiple indexes)
NOTICE:  ========================================
NOTICE:  Staging tables created successfully!
NOTICE:  Tables: farmers, products, markets, buyers, transactions, harvests, pricing, weather, subsidies
NOTICE:  ========================================

Query returned successfully in XXX msec.
```

**Verify in pgAdmin**:
1. In left sidebar, expand **`agri_dw`** database
2. Expand **"Schemas"**
3. Expand **"staging"**
4. Expand **"Tables"**
5. You should see 9 tables:
   - `stg_farmers`
   - `stg_products`
   - `stg_markets`
   - `stg_buyers`
   - `stg_transactions`
   - `stg_harvests`
   - `stg_pricing`
   - `stg_weather`
   - `stg_subsidies`

**Alternative (Command Line)**:
```powershell
psql -U postgres -d agri_dw -f sql/ddl/02_staging_tables.sql
```

---

### 3.4 Create Dimension Tables

**Using pgAdmin Query Tool**:

1. In the Query Tool, click the **folder icon** (📁 "Open File")
2. Navigate to: `c:\Users\batzt\Desktop\agric_dw\sql\ddl\`
3. Select: **`03_dimension_tables.sql`**
4. Click **"Open"**
5. Click the **"Execute/Refresh"** button (▶️ icon) or press **F5**

**Expected Output**:
```
CREATE TABLE
... (8 times for 8 dimension tables)
INSERT 0 5  (payment methods)
INSERT 0 3  (quality grades)
NOTICE:  ========================================
NOTICE:  Dimension tables created successfully!
NOTICE:  Tables: dim_date, dim_farmer, dim_product, dim_market, dim_buyer, dim_location, dim_payment_method, dim_quality
NOTICE:  SCD Type 2 implemented for: farmer, product, market, buyer
NOTICE:  ========================================

Query returned successfully in XXX msec.
```

**Verify in pgAdmin**:
1. In left sidebar, expand **"dw"** schema
2. Expand **"Tables"**
3. You should see 8 tables starting with `dim_`:
   - `dim_buyer`
   - `dim_date`
   - `dim_farmer`
   - `dim_location`
   - `dim_market`
   - `dim_payment_method`
   - `dim_product`
   - `dim_quality`

**Alternative (Command Line)**:
```powershell
psql -U postgres -d agri_dw -f sql/ddl/03_dimension_tables.sql
```

---

### 3.5 Create Fact Tables

**Using pgAdmin Query Tool**:

1. In the Query Tool, click the **folder icon** (📁 "Open File")
2. Navigate to: `c:\Users\batzt\Desktop\agric_dw\sql\ddl\`
3. Select: **`04_fact_tables.sql`**
4. Click **"Open"**
5. Click the **"Execute/Refresh"** button (▶️ icon) or press **F5**

**Expected Output**:
```
CREATE TABLE
... (4 times for 4 fact tables + 1 summary)
NOTICE:  ========================================
NOTICE:  Fact tables created successfully!
NOTICE:  Tables: fact_transaction, fact_harvest, fact_pricing, fact_subsidy
NOTICE:  Summary table: fact_transaction_daily_summary
NOTICE:  ========================================

Query returned successfully in XXX msec.
```

**Verify in pgAdmin**:
1. In **"dw"** schema → **"Tables"**
2. You should see 5 tables starting with `fact_`:
   - `fact_harvest`
   - `fact_pricing`
   - `fact_subsidy`
   - `fact_transaction`
   - `fact_transaction_daily_summary`

**Alternative (Command Line)**:
```powershell
psql -U postgres -d agri_dw -f sql/ddl/04_fact_tables.sql
```

---

### 3.6 Verify Complete Database Structure

**Using pgAdmin Query Tool**:

1. In the Query Tool (should still be open)
2. **Clear the editor** (Ctrl+A, then Delete)
3. **Copy and paste** this verification query:
   ```sql
   SELECT 
       schemaname,
       COUNT(*) as table_count
   FROM pg_tables
   WHERE schemaname IN ('staging', 'dw', 'audit')
   GROUP BY schemaname
   ORDER BY schemaname;
   ```
4. Click the **"Execute/Refresh"** button (▶️ icon) or press **F5**

**Expected Result** (in the "Data Output" tab):
| schemaname | table_count |
|------------|-------------|
| audit      | 2           |
| dw         | 13          |
| staging    | 9           |

**Total: 24 tables created!**

**Visual Verification in pgAdmin**:
1. In left sidebar, right-click **`agri_dw`** database
2. Select **"Refresh"**
3. Expand each schema and count tables:
   - **staging**: 9 tables (stg_*)
   - **dw**: 13 tables (8 dim_* + 5 fact_*)
   - **audit**: 2 tables (etl_execution_log, data_quality_log)

---

**Alternative (Command Line)**:
```powershell
psql -U postgres -d agri_dw -c "SELECT schemaname, COUNT(*) as table_count FROM pg_tables WHERE schemaname IN ('staging', 'dw', 'audit') GROUP BY schemaname ORDER BY schemaname;"
```

---

## 4. Data Generation

### 4.1 Understanding Data Generation

**What we're generating**:
- 2,000 farmers
- 100 products
- 200 markets
- 10,000 transactions
- 18,250+ pricing records
- **Total: 30,550+ rows**

**Output files** (in `data/` folder):
- CSV files (for loading with COPY command)
- SQL files (for loading with INSERT statements)

---

### 4.2 Generate All Data

**Option 1: Using Master Script (Easiest)**

```powershell
cd c:\Users\batzt\Desktop\agric_dw\scripts\data_generation
python master_data_generator.py
```

**Expected output**:
```
========================================
AGRICULTURAL DATA WAREHOUSE - DATA GENERATION
========================================

[1/5] Generating Products...
✓ Generated 100 products
  - CSV: ../../data/products.csv
  - SQL: ../../data/products_insert.sql

[2/5] Generating Markets...
✓ Generated 200 markets
  - CSV: ../../data/markets.csv
  - SQL: ../../data/markets_insert.sql

[3/5] Generating Farmers...
✓ Generated 2000 farmers
  - CSV: ../../data/farmers.csv
  - SQL: ../../data/farmers_insert.sql

[4/5] Generating Transactions...
✓ Generated 10000 transactions
  - CSV: ../../data/transactions.csv
  - SQL: ../../data/transactions_insert.sql

[5/5] Generating Market Pricing...
✓ Generated 18250 pricing records
  - CSV: ../../data/pricing.csv
  - SQL: ../../data/pricing_insert.sql

========================================
DATA GENERATION COMPLETE!
========================================
Total Records Generated: 30,550
Total Files Created: 10
Time Taken: ~45 seconds
========================================
```

**Time**: 30-60 seconds

---

### 4.3 Verify Generated Data

**Check data folder**:

```powershell
cd c:\Users\batzt\Desktop\agric_dw\data
dir
```

You should see 10 files:
- `farmers.csv` and `farmers_insert.sql`
- `products.csv` and `products_insert.sql`
- `markets.csv` and `markets_insert.sql`
- `transactions.csv` and `transactions_insert.sql`
- `pricing.csv` and `pricing_insert.sql`

**Check file sizes**:
- farmers.csv: ~500 KB
- transactions.csv: ~1.5 MB
- pricing.csv: ~2 MB

**Preview data** (optional):
```powershell
# View first 5 lines of farmers.csv
Get-Content farmers.csv -Head 5
```

Or open in Excel/VS Code to inspect.

---

### 4.4 Load Data into Staging Tables

**Using pgAdmin Import/Export Tool (Recommended for GUI users)**

pgAdmin has a built-in Import/Export tool that makes loading CSV files easy:

**Step 1: Load Farmers Data**

1. In pgAdmin, expand **`agri_dw`** → **Schemas** → **staging** → **Tables**
2. Right-click on **`stg_farmers`** table
3. Select **"Import/Export Data..."**
4. In the dialog:
   - **Import/Export**: Select **"Import"**
   - **Filename**: Click the folder icon and browse to:
     `c:\Users\batzt\Desktop\agric_dw\data\farmers.csv`
   - **Format**: Select **"csv"**
   - **Header**: Toggle **ON** (✅)
   - **Delimiter**: `,` (comma)
   - **Quote**: `"` (double quote)
   - **Escape**: `"` (double quote)
5. Click **"OK"**
6. Wait for import to complete (should show "2000 rows imported")

**Step 2: Load Products Data**

1. Right-click **`stg_products`** table
2. Select **"Import/Export Data..."**
3. Configure:
   - **Import/Export**: **"Import"**
   - **Filename**: `c:\Users\batzt\Desktop\agric_dw\data\products.csv`
   - **Format**: **"csv"**
   - **Header**: **ON** (✅)
4. Click **"OK"**
5. Should import 100 rows

**Step 3: Load Markets Data**

1. Right-click **`stg_markets`** table
2. Select **"Import/Export Data..."**
3. Configure:
   - **Import/Export**: **"Import"**
   - **Filename**: `c:\Users\batzt\Desktop\agric_dw\data\markets.csv`
   - **Format**: **"csv"**
   - **Header**: **ON** (✅)
4. Click **"OK"**
5. Should import 200 rows

**Step 4: Load Transactions Data**

1. Right-click **`stg_transactions`** table
2. Select **"Import/Export Data..."**
3. Configure:
   - **Import/Export**: **"Import"**
   - **Filename**: `c:\Users\batzt\Desktop\agric_dw\data\transactions.csv`
   - **Format**: **"csv"**
   - **Header**: **ON** (✅)
4. Click **"OK"**
5. Should import 10,000 rows (may take 10-20 seconds)

**Step 5: Load Pricing Data**

1. Right-click **`stg_pricing`** table
2. Select **"Import/Export Data..."**
3. Configure:
   - **Import/Export**: **"Import"**
   - **Filename**: `c:\Users\batzt\Desktop\agric_dw\data\pricing.csv`
   - **Format**: **"csv"**
   - **Header**: **ON** (✅)
4. Click **"OK"**
5. Should import 18,250 rows (may take 20-30 seconds)

**Expected Results:**
- ✅ Farmers: 2,000 rows
- ✅ Products: 100 rows
- ✅ Markets: 200 rows
- ✅ Transactions: 10,000 rows
- ✅ Pricing: 18,250 rows
- **Total: 30,550 rows loaded!**

---

**Alternative: Using Command Line (Advanced Users)**

If you prefer command line or the GUI import fails:

**Option A: Using psql with \copy command**

```powershell
# Open psql
psql -U postgres -d agri_dw
```

In the psql prompt, run:
```sql
\copy staging.stg_farmers FROM 'c:/Users/batzt/Desktop/agric_dw/data/farmers.csv' WITH CSV HEADER;
\copy staging.stg_products FROM 'c:/Users/batzt/Desktop/agric_dw/data/products.csv' WITH CSV HEADER;
\copy staging.stg_markets FROM 'c:/Users/batzt/Desktop/agric_dw/data/markets.csv' WITH CSV HEADER;
\copy staging.stg_transactions FROM 'c:/Users/batzt/Desktop/agric_dw/data/transactions.csv' WITH CSV HEADER;
\copy staging.stg_pricing FROM 'c:/Users/batzt/Desktop/agric_dw/data/pricing.csv' WITH CSV HEADER;
\q
```

**Option B: Using SQL INSERT files (slowest but most compatible)**

```powershell
cd c:\Users\batzt\Desktop\agric_dw
psql -U postgres -d agri_dw -f data/farmers_insert.sql
psql -U postgres -d agri_dw -f data/products_insert.sql
psql -U postgres -d agri_dw -f data/markets_insert.sql
psql -U postgres -d agri_dw -f data/transactions_insert.sql
psql -U postgres -d agri_dw -f data/pricing_insert.sql
```

---

### 4.5 Verify Data Load

**Check row counts**:

```powershell
psql -U postgres -d agri_dw
```

```sql
SELECT 'Farmers' as table_name, COUNT(*) as row_count FROM staging.stg_farmers
UNION ALL SELECT 'Products', COUNT(*) FROM staging.stg_products
UNION ALL SELECT 'Markets', COUNT(*) FROM staging.stg_markets
UNION ALL SELECT 'Transactions', COUNT(*) FROM staging.stg_transactions
UNION ALL SELECT 'Pricing', COUNT(*) FROM staging.stg_pricing;
```

**Expected result**:
| table_name   | row_count |
|--------------|-----------|
| Farmers      | 2000      |
| Products     | 100       |
| Markets      | 200       |
| Transactions | 10000     |
| Pricing      | 18250     |

**View sample data**:
```sql
SELECT * FROM staging.stg_farmers LIMIT 5;
```

You should see 5 farmers with Uganda-specific names, districts, etc.

---

## 5. ETL Execution

### 5.1 Understanding the ETL Process

**What the ETL does**:
1. **Loads DimDate**: Pre-populates dates from 2020-2030
2. **Loads Dimensions**: Farmers, products, markets with SCD Type 2
3. **Loads Facts**: Transactions with dimension key lookups
4. **Logs Execution**: Records in audit tables

---

### 5.2 Configure ETL

**Check ETL configuration**:

```powershell
cd c:\Users\batzt\Desktop\agric_dw\scripts\etl
cat etl_config.yaml
```

**Update password if needed**:
1. Open `etl_config.yaml` in VS Code or Notepad
2. Find the `database` section
3. Update `password` to your postgres password
4. Save file

Example:
```yaml
database:
  host: localhost
  port: 5432
  database: agri_dw
  user: postgres
  password: postgres123  # Change this to your password
```

---

### 5.3 Run ETL Pipeline

```powershell
cd c:\Users\batzt\Desktop\agric_dw\scripts\etl
python etl_staging_to_dw.py
```

**Expected output**:
```
2025-12-06 16:42:01 - INFO - Database connection established
2025-12-06 16:42:01 - INFO - Started ETL job: Full ETL Pipeline (ID: 10)
2025-12-06 16:42:01 - INFO - Loading dim_date...
2025-12-06 16:42:01 - INFO - dim_date already loaded, skipping
2025-12-06 16:42:01 - INFO - Loading dim_farmer...
2025-12-06 16:42:02 - INFO - Inserted 2000 new farmers into dim_farmer
2025-12-06 16:42:02 - INFO - Loading dim_product...
2025-12-06 16:42:02 - INFO - Inserted 100 products into dim_product
2025-12-06 16:42:02 - INFO - Loading dim_market...
2025-12-06 16:42:03 - INFO - Inserted 200 markets into dim_market
2025-12-06 16:42:03 - INFO - Loading dim_buyer...
2025-12-06 16:42:03 - INFO - Inserted 500 buyers into dim_buyer
2025-12-06 16:42:03 - INFO - Loading dim_location...
2025-12-06 16:42:03 - INFO - Inserted 175 locations into dim_location
2025-12-06 16:42:03 - INFO - Loading fact_transaction...
2025-12-06 16:42:03 - INFO - Inserted 15000 transactions into fact_transaction
2025-12-06 16:42:04 - INFO - Loading fact_harvest...
2025-12-06 16:42:04 - INFO - Inserted 6000 harvests into fact_harvest
2025-12-06 16:42:04 - INFO - Loading fact_pricing...
2025-12-06 16:42:04 - INFO - Inserted 12000 pricing records into fact_pricing
2025-12-06 16:42:04 - INFO - Loading fact_weather...
2025-12-06 16:42:04 - INFO - Inserted 5840 weather records into fact_weather
2025-12-06 16:42:04 - INFO - Loading fact_subsidy...
2025-12-06 16:42:04 - INFO - Inserted 1000 subsidy records into fact_subsidy
2025-12-06 16:42:04 - INFO - ETL job completed with status: Success
2025-12-06 16:42:04 - INFO - ETL pipeline completed successfully. Total rows inserted: 42815
2025-12-06 16:42:04 - INFO - Database connection closed
```

**Time**: 15-30 seconds

---

### 5.4 Verify ETL Results

**Check dimension row counts**:

```powershell
# We have a script for this!
cd c:\Users\batzt\Desktop\agric_dw\scripts\etl
python verify_dw_counts.py
```

**Expected result**:
```
DW Row Counts:
====================
dim_buyer: 500
dim_date: 4018
dim_farmer: 2000
dim_location: 175
dim_market: 200
dim_payment_method: 5
dim_product: 100
dim_quality: 3
fact_harvest: 6000
fact_pricing: 12000
fact_subsidy: 1000
fact_transaction: 15000
fact_weather: 5840
```

**Check ETL audit log**:
```sql
SELECT * FROM audit.etl_execution_log ORDER BY start_time DESC LIMIT 1;
```

You should see your ETL execution with status 'Success'.

---

## 6. Power BI Setup

### 6.1 Export Data for Power BI

```powershell
cd c:\Users\batzt\Desktop\agric_dw\scripts\powerbi
python export_powerbi_data.py
```

**Expected output**:
```
2025-12-04 21:05:00 - INFO - Starting Power BI dataset export...
2025-12-04 21:05:01 - INFO - Executing query...
2025-12-04 21:05:05 - INFO - Retrieved 10000 rows
2025-12-04 21:05:06 - INFO - Saved to ../../powerbi/powerbi_dataset.csv

================================================================================
POWER BI DATASET EXPORT COMPLETE
================================================================================
Total Rows: 10,000
Total Revenue: UGX 850,000,000
Date Range: 2024-01-01 to 2024-12-04
Unique Farmers: 2,000
Unique Products: 100
Unique Markets: 200

File saved: ../../powerbi/powerbi_dataset.csv
================================================================================
```

---

### 6.2 Import into Power BI

1. **Open Power BI Desktop**

2. **Get Data**:
   - Click "Get Data" on Home ribbon
   - Select "Text/CSV"
   - Click "Connect"

3. **Select File**:
   - Navigate to: `c:\Users\batzt\Desktop\agric_dw\powerbi\`
   - Select `powerbi_dataset.csv`
   - Click "Open"

4. **Preview**:
   - Power BI shows data preview
   - Check that you see 10,000 rows
   - Click "Load"

5. **Verify Data**:
   - In right sidebar, you should see all columns:
     - transaction_id
     - farmer_name
     - product_name
     - quantity_kg
     - total_amount
     - etc.

---

### 6.3 Create DAX Measures (Optional)

1. **Open DAX Measures File**:
   - Open `powerbi/dax_measures.txt` in Notepad or VS Code

2. **Create Measures in Power BI**:
   - In Power BI, right-click on your table in Fields pane
   - Select "New measure"
   - Copy a measure from `dax_measures.txt`
   - Paste into formula bar
   - Press Enter

3. **Example - Create "Total Revenue" measure**:
   ```dax
   Total Revenue = SUM(powerbi_dataset[total_amount])
   ```

4. **Repeat for other measures** (50+ available in the file)

---

### 6.4 Create Dashboards (Optional)

Follow the specifications in `powerbi/dashboard_specifications.md` to create:
1. Executive Overview
2. Farmer Analytics
3. Product & Market Analysis
4. Financial Performance
5. Supply Chain Traceability

**Or**: Just capture screenshots of the data loaded for your submission.

---

## 7. Verification & Testing

### 7.1 Run Sample Analytics Queries

**Top 10 Farmers by Revenue**:

```sql
SELECT 
    f.full_name,
    f.district,
    COUNT(t.transaction_key) as transaction_count,
    SUM(t.total_amount) as total_revenue
FROM dw.fact_transaction t
JOIN dw.dim_farmer f ON t.farmer_key = f.farmer_key
WHERE f.is_current = TRUE
GROUP BY f.full_name, f.district
ORDER BY total_revenue DESC
LIMIT 10;
```

**Revenue by Product Category**:

```sql
SELECT 
    p.category,
    COUNT(t.transaction_key) as transaction_count,
    SUM(t.quantity_kg) as total_quantity_kg,
    SUM(t.total_amount) as total_revenue,
    AVG(t.unit_price) as avg_price_per_kg
FROM dw.fact_transaction t
JOIN dw.dim_product p ON t.product_key = p.product_key
WHERE p.is_current = TRUE
GROUP BY p.category
ORDER BY total_revenue DESC;
```

**Monthly Revenue Trend**:

```sql
SELECT 
    d.year,
    d.month,
    d.month_name,
    COUNT(t.transaction_key) as transactions,
    SUM(t.total_amount) as revenue
FROM dw.fact_transaction t
JOIN dw.dim_date d ON t.date_key = d.date_key
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
```

---

### 7.2 Test SCD Type 2 (Optional)

**View farmer history**:

```sql
SELECT 
    farmer_key,
    farmer_id,
    full_name,
    farm_size_acres,
    effective_date,
    end_date,
    is_current,
    version
FROM dw.dim_farmer
WHERE farmer_id = 'FMR000001'
ORDER BY version;
```

Currently, you'll only see version 1 since we haven't updated any farmers yet.

---

## 8. Troubleshooting

### 8.1 PostgreSQL Issues

**Problem**: `psql: command not found`

**Solution**:
1. Add PostgreSQL to PATH (see section 1.1)
2. Or use full path: `"C:\Program Files\PostgreSQL\15\bin\psql.exe"`

---

**Problem**: `psql: FATAL: password authentication failed`

**Solution**:
1. Make sure you're using the correct password
2. Reset password:
   - Open pgAdmin
   - Right-click "PostgreSQL 15" → Properties
   - Go to "Connection" tab
   - Update password

---

**Problem**: `psql: could not connect to server`

**Solution**:
1. Check if PostgreSQL is running:
   ```powershell
   Get-Service -Name postgresql*
   ```
2. If not running, start it:
   ```powershell
   Start-Service -Name postgresql-x64-15
   ```

---

### 8.2 Python Issues

**Problem**: `ModuleNotFoundError: No module named 'pandas'`

**Solution**:
```powershell
pip install pandas
# Or reinstall all:
pip install -r requirements.txt
```

---

**Problem**: `pip: command not found`

**Solution**:
1. Reinstall Python with "Add to PATH" checked
2. Or use: `python -m pip install -r requirements.txt`

---

**Problem**: Data generation script fails

**Solution**:
1. Check you're in correct directory:
   ```powershell
   cd c:\Users\batzt\Desktop\agric_dw\scripts\data_generation
   ```
2. Check Python version:
   ```powershell
   python --version  # Should be 3.10+
   ```
3. Run individual generators to find which one fails

---

### 8.3 ETL Issues

**Problem**: `psycopg2.OperationalError: could not connect`

**Solution**:
1. Check `etl_config.yaml` has correct password
2. Check PostgreSQL is running
3. Check database exists: `psql -U postgres -l`

---

**Problem**: ETL fails with "relation does not exist"

**Solution**:
1. Make sure you ran all DDL scripts (01-04)
2. Check tables exist:
   ```sql
   \dt staging.*
   \dt dw.*
   ```

---

**Problem**: "No data in staging tables"

**Solution**:
1. Make sure you loaded data (section 4.4)
2. Check staging tables:
   ```sql
   SELECT COUNT(*) FROM staging.stg_farmers;
   ```

---

## 9. Next Steps

### 9.1 For Your Submission

Now that everything is set up and running:

1. **Capture Screenshots** (see `SUBMISSION_CHECKLIST.md`):
   - Database structure in pgAdmin
   - Sample data from tables
   - ETL execution output
   - Power BI data loaded

2. **Render Diagrams**:
   - Go to http://www.plantuml.com/plantuml/uml/
   - Render all 4 `.puml` files
   - Save as PNG/PDF

3. **Convert Report to PDF**:
   - Open `FINAL_REPORT.md` in VS Code
   - Use "Markdown PDF" extension
   - Or use online converter

4. **Create PowerPoint**:
   - Use `PRESENTATION_SLIDES.md` as guide
   - Add diagrams and screenshots
   - Save as .pptx and .pdf

5. **Organize Submission**:
   - Follow structure in `SUBMISSION_CHECKLIST.md`
   - Zip and submit

---

### 9.2 Optional Enhancements

If you have time:

1. **Build Power BI Dashboards**:
   - Follow `powerbi/dashboard_specifications.md`
   - Create all 5 dashboards
   - Capture screenshots

2. **Add More Data**:
   - Modify data generators to create more rows
   - Re-run ETL

3. **Test SCD Type 2**:
   - Manually update a farmer's farm size
   - Re-run ETL
   - Verify version history

4. **Explore Blockchain/Kafka** (Advanced):
   - Read `docs/04_implementation.md`
   - Set up Docker for Kafka
   - Deploy Hyperledger Fabric

---

## 10. Quick Reference Commands

### Database
```powershell
# Connect to database
psql -U postgres -d agri_dw

# List tables
\dt staging.*
\dt dw.*

# Run SQL file
psql -U postgres -d agri_dw -f script.sql

# Exit psql
\q
```

### Data Generation
```powershell
cd scripts/data_generation
python master_data_generator.py
```

### ETL
```powershell
cd scripts/etl
python etl_staging_to_dw.py
```

### Power BI Export
```powershell
cd scripts/powerbi
python export_powerbi_data.py
```

---

## 📞 Need Help?

If you encounter issues:

1. **Check error message carefully** - it usually tells you what's wrong
2. **Review this guide** - most issues are covered in Troubleshooting
3. **Check other docs**:
   - `README.md` - Project overview
   - `PROJECT_DELIVERABLES_SUMMARY.md` - Complete file list
   - `SUBMISSION_CHECKLIST.md` - Submission requirements

---

**You're all set!** Follow this guide step by step, and you'll have a complete, working data warehouse. Good luck! 🎓
