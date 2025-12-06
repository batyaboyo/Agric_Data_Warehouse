"""
ETL Pipeline - Staging to Data Warehouse
Loads data from staging tables to dimension and fact tables with SCD Type 2
"""

import psycopg2
from psycopg2 import sql
from datetime import datetime, date
import yaml
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ETLPipeline:
    def __init__(self, config_path='etl_config.yaml'):
        """Initialize ETL pipeline with configuration"""
        self.config = self.load_config(config_path)
        self.conn = None
        self.execution_id = None
        
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def connect_db(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                host=self.config['database']['host'],
                port=self.config['database']['port'],
                database=self.config['database']['database'],
                user=self.config['database']['user'],
                password=self.config['database']['password']
            )
            self.conn.autocommit = False
            logger.info("Database connection established")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            raise
    
    def close_db(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def log_execution_start(self, job_name):
        """Log ETL job start"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO audit.etl_execution_log (job_name, status)
            VALUES (%s, 'Running')
            RETURNING execution_id
        """, (job_name,))
        self.execution_id = cursor.fetchone()[0]
        self.conn.commit()
        logger.info(f"Started ETL job: {job_name} (ID: {self.execution_id})")
        return self.execution_id
    
    def log_execution_end(self, status, rows_read=0, rows_inserted=0, rows_updated=0, error_message=None):
        """Log ETL job completion"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE audit.etl_execution_log
            SET end_time = CURRENT_TIMESTAMP,
                status = %s,
                rows_read = %s,
                rows_inserted = %s,
                rows_updated = %s,
                error_message = %s
            WHERE execution_id = %s
        """, (status, rows_read, rows_inserted, rows_updated, error_message, self.execution_id))
        self.conn.commit()
        logger.info(f"ETL job completed with status: {status}")
    
    def load_dim_date(self):
        """Load date dimension (one-time)"""
        logger.info("Loading dim_date...")
        cursor = self.conn.cursor()
        
        # Check if already loaded
        cursor.execute("SELECT COUNT(*) FROM dw.dim_date")
        if cursor.fetchone()[0] > 0:
            logger.info("dim_date already loaded, skipping")
            return
        
        # Generate dates for 10 years (2020-2030)
        cursor.execute("""
            INSERT INTO dw.dim_date (
                date_key, full_date, day_of_week, day_name, day_of_month, day_of_year,
                week_of_year, month, month_name, quarter, quarter_name, year,
                is_weekend, season, fiscal_year, fiscal_quarter, fiscal_month
            )
            SELECT 
                TO_CHAR(date_series, 'YYYYMMDD')::INTEGER as date_key,
                date_series as full_date,
                EXTRACT(DOW FROM date_series)::INTEGER as day_of_week,
                TO_CHAR(date_series, 'Day') as day_name,
                EXTRACT(DAY FROM date_series)::INTEGER as day_of_month,
                EXTRACT(DOY FROM date_series)::INTEGER as day_of_year,
                EXTRACT(WEEK FROM date_series)::INTEGER as week_of_year,
                EXTRACT(MONTH FROM date_series)::INTEGER as month,
                TO_CHAR(date_series, 'Month') as month_name,
                EXTRACT(QUARTER FROM date_series)::INTEGER as quarter,
                'Q' || EXTRACT(QUARTER FROM date_series)::TEXT as quarter_name,
                EXTRACT(YEAR FROM date_series)::INTEGER as year,
                CASE WHEN EXTRACT(DOW FROM date_series) IN (0,6) THEN TRUE ELSE FALSE END as is_weekend,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_series) IN (3,4,5) THEN 'First Season'
                    WHEN EXTRACT(MONTH FROM date_series) IN (9,10,11) THEN 'Second Season'
                    ELSE 'Off Season'
                END as season,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_series) >= 7 THEN EXTRACT(YEAR FROM date_series)::INTEGER + 1
                    ELSE EXTRACT(YEAR FROM date_series)::INTEGER
                END as fiscal_year,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_series) IN (7,8,9) THEN 1
                    WHEN EXTRACT(MONTH FROM date_series) IN (10,11,12) THEN 2
                    WHEN EXTRACT(MONTH FROM date_series) IN (1,2,3) THEN 3
                    ELSE 4
                END as fiscal_quarter,
                CASE 
                    WHEN EXTRACT(MONTH FROM date_series) >= 7 THEN EXTRACT(MONTH FROM date_series)::INTEGER - 6
                    ELSE EXTRACT(MONTH FROM date_series)::INTEGER + 6
                END as fiscal_month
            FROM generate_series('2020-01-01'::DATE, '2030-12-31'::DATE, '1 day'::INTERVAL) as date_series
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Loaded {rows_inserted} rows into dim_date")
    
    def load_dim_farmer(self):
        """Load farmer dimension with SCD Type 2"""
        logger.info("Loading dim_farmer...")
        cursor = self.conn.cursor()
        
        # Insert new farmers
        cursor.execute("""
            INSERT INTO dw.dim_farmer (
                farmer_id, national_id, first_name, last_name, full_name, gender,
                date_of_birth, age_group, phone_number, district, subcounty, village,
                region, gps_latitude, gps_longitude, farm_size_acres, farm_size_category,
                primary_crop, cooperative_id, blockchain_wallet, registration_date,
                effective_date, is_current, version
            )
            SELECT 
                s.farmer_id,
                s.national_id,
                s.first_name,
                s.last_name,
                s.first_name || ' ' || s.last_name as full_name,
                s.gender,
                s.date_of_birth,
                CASE 
                    WHEN EXTRACT(YEAR FROM AGE(s.date_of_birth)) < 30 THEN 'Youth (18-29)'
                    WHEN EXTRACT(YEAR FROM AGE(s.date_of_birth)) < 50 THEN 'Adult (30-49)'
                    ELSE 'Senior (50+)'
                END as age_group,
                s.phone_number,
                s.district,
                s.subcounty,
                s.village,
                CASE 
                    WHEN s.district IN ('Kampala', 'Wakiso', 'Mukono', 'Masaka', 'Luwero') THEN 'Central'
                    WHEN s.district IN ('Jinja', 'Mbale', 'Tororo', 'Iganga', 'Soroti', 'Pallisa', 'Kamuli') THEN 'Eastern'
                    WHEN s.district IN ('Gulu', 'Lira', 'Kitgum', 'Arua', 'Nebbi', 'Apac', 'Moroto') THEN 'Northern'
                    ELSE 'Western'
                END as region,
                s.gps_latitude,
                s.gps_longitude,
                s.farm_size_acres,
                CASE 
                    WHEN s.farm_size_acres < 2 THEN 'Small (< 2 acres)'
                    WHEN s.farm_size_acres < 10 THEN 'Medium (2-10 acres)'
                    ELSE 'Large (10+ acres)'
                END as farm_size_category,
                s.primary_crop,
                s.cooperative_id,
                s.blockchain_wallet,
                s.registration_date::DATE,
                CURRENT_DATE as effective_date,
                TRUE as is_current,
                1 as version
            FROM staging.stg_farmers s
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.dim_farmer d 
                WHERE d.farmer_id = s.farmer_id AND d.is_current = TRUE
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} new farmers into dim_farmer")
        
        return rows_inserted
    
    def load_dim_product(self):
        """Load product dimension"""
        logger.info("Loading dim_product...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.dim_product (
                product_id, product_name, category, category_group, variety,
                unit_of_measure, season, avg_growing_days, growing_period_category,
                is_perishable, perishability_category,
                effective_date, is_current, version
            )
            SELECT 
                s.product_id,
                s.product_name,
                s.category,
                CASE 
                    WHEN s.category IN ('Cereals', 'Legumes') THEN 'Grains & Legumes'
                    WHEN s.category IN ('Root Crops', 'Plantains') THEN 'Roots & Tubers'
                    WHEN s.category IN ('Vegetables', 'Fruits') THEN 'Horticulture'
                    ELSE 'Cash Crops'
                END as category_group,
                s.variety,
                s.unit_of_measure,
                s.season,
                s.avg_growing_days,
                CASE 
                    WHEN s.avg_growing_days < 90 THEN 'Short (< 3 months)'
                    WHEN s.avg_growing_days < 180 THEN 'Medium (3-6 months)'
                    ELSE 'Long (6+ months)'
                END as growing_period_category,
                s.is_perishable,
                CASE 
                    WHEN s.is_perishable THEN 'Perishable'
                    ELSE 'Non-Perishable'
                END as perishability_category,
                CURRENT_DATE as effective_date,
                TRUE as is_current,
                1 as version
            FROM staging.stg_products s
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.dim_product d 
                WHERE d.product_id = s.product_id AND d.is_current = TRUE
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} products into dim_product")
        
        return rows_inserted
    
    def load_dim_market(self):
        """Load market dimension"""
        logger.info("Loading dim_market...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.dim_market (
                market_id, market_name, market_type, district, subcounty, region,
                gps_latitude, gps_longitude, operating_days, capacity_kg, capacity_category,
                is_active, effective_date, is_current, version
            )
            SELECT 
                s.market_id,
                s.market_name,
                s.market_type,
                s.district,
                s.subcounty,
                CASE 
                    WHEN s.district IN ('Kampala', 'Wakiso', 'Mukono', 'Masaka', 'Luwero') THEN 'Central'
                    WHEN s.district IN ('Jinja', 'Mbale', 'Tororo', 'Iganga', 'Soroti', 'Pallisa', 'Kamuli') THEN 'Eastern'
                    WHEN s.district IN ('Gulu', 'Lira', 'Kitgum', 'Arua', 'Nebbi', 'Apac', 'Moroto') THEN 'Northern'
                    ELSE 'Western'
                END as region,
                s.gps_latitude,
                s.gps_longitude,
                s.operating_days,
                s.capacity_kg,
                CASE 
                    WHEN s.capacity_kg < 10000 THEN 'Small (< 10 tons)'
                    WHEN s.capacity_kg < 50000 THEN 'Medium (10-50 tons)'
                    ELSE 'Large (50+ tons)'
                END as capacity_category,
                s.is_active,
                CURRENT_DATE as effective_date,
                TRUE as is_current,
                1 as version
            FROM staging.stg_markets s
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.dim_market d 
                WHERE d.market_id = s.market_id AND d.is_current = TRUE
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} markets into dim_market")
        
        return rows_inserted
    
    def load_fact_transaction(self):
        """Load transaction fact table"""
        logger.info("Loading fact_transaction...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.fact_transaction (
                farmer_key, buyer_key, product_key, market_key, date_key,
                payment_key, quality_key, transaction_id, blockchain_hash, payment_status,
                quantity_kg, unit_price, total_amount, transaction_count, payment_fee, net_amount,
                transaction_timestamp
            )
            SELECT 
                f.farmer_key,
                COALESCE(b.buyer_key, 1) as buyer_key,  -- Default buyer if not found
                p.product_key,
                m.market_key,
                TO_CHAR(t.transaction_date, 'YYYYMMDD')::INTEGER as date_key,
                pm.payment_key,
                q.quality_key,
                t.transaction_id,
                t.blockchain_hash,
                t.payment_status,
                t.quantity_kg,
                t.unit_price,
                t.total_amount,
                1 as transaction_count,
                t.total_amount * COALESCE(pm.transaction_fee_pct, 0) / 100 as payment_fee,
                t.total_amount - (t.total_amount * COALESCE(pm.transaction_fee_pct, 0) / 100) as net_amount,
                t.transaction_date
            FROM staging.stg_transactions t
            JOIN dw.dim_farmer f ON t.farmer_id = f.farmer_id AND f.is_current = TRUE
            JOIN dw.dim_product p ON t.product_id = p.product_id AND p.is_current = TRUE
            JOIN dw.dim_market m ON t.market_id = m.market_id AND m.is_current = TRUE
            JOIN dw.dim_payment_method pm ON t.payment_method = pm.payment_method
            JOIN dw.dim_quality q ON t.quality_grade = q.quality_grade
            LEFT JOIN dw.dim_buyer b ON t.buyer_id = b.buyer_id AND b.is_current = TRUE
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.fact_transaction ft 
                WHERE ft.transaction_id = t.transaction_id
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} transactions into fact_transaction")
        
        return rows_inserted
    
    def load_dim_buyer(self):
        """Load buyer dimension"""
        logger.info("Loading dim_buyer...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.dim_buyer (
                buyer_id, buyer_name, buyer_type, contact_person, phone_number,
                email, district, region, registration_number, blockchain_wallet,
                is_active, effective_date, is_current, version
            )
            SELECT 
                s.buyer_id,
                s.buyer_name,
                s.buyer_type,
                s.contact_person,
                s.phone_number,
                s.email,
                s.district,
                CASE 
                    WHEN s.district IN ('Kampala', 'Wakiso', 'Mukono', 'Masaka', 'Luwero') THEN 'Central'
                    WHEN s.district IN ('Jinja', 'Mbale', 'Tororo', 'Iganga', 'Soroti', 'Pallisa', 'Kamuli') THEN 'Eastern'
                    WHEN s.district IN ('Gulu', 'Lira', 'Kitgum', 'Arua', 'Nebbi', 'Apac', 'Moroto') THEN 'Northern'
                    ELSE 'Western'
                END as region,
                s.registration_number,
                s.blockchain_wallet,
                s.is_active,
                CURRENT_DATE as effective_date,
                TRUE as is_current,
                1 as version
            FROM staging.stg_buyers s
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.dim_buyer d 
                WHERE d.buyer_id = s.buyer_id AND d.is_current = TRUE
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} buyers into dim_buyer")
        return rows_inserted

    def load_dim_location(self):
        """Load location dimension from farmers data"""
        logger.info("Loading dim_location...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.dim_location (
                district, subcounty, region, created_at
            )
            SELECT DISTINCT
                district,
                subcounty,
                CASE 
                    WHEN district IN ('Kampala', 'Wakiso', 'Mukono', 'Masaka', 'Luwero') THEN 'Central'
                    WHEN district IN ('Jinja', 'Mbale', 'Tororo', 'Iganga', 'Soroti', 'Pallisa', 'Kamuli') THEN 'Eastern'
                    WHEN district IN ('Gulu', 'Lira', 'Kitgum', 'Arua', 'Nebbi', 'Apac', 'Moroto') THEN 'Northern'
                    ELSE 'Western'
                END as region,
                CURRENT_TIMESTAMP
            FROM staging.stg_farmers
            ON CONFLICT (district, subcounty) DO NOTHING
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} locations into dim_location")
        return rows_inserted

    def load_fact_harvest(self):
        """Load harvest fact table"""
        logger.info("Loading fact_harvest...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.fact_harvest (
                harvest_id, farmer_key, product_key, planting_date_key, harvest_date_key, location_key,
                quantity_kg, quality_assessment,
                post_harvest_loss_pct, post_harvest_loss_kg, net_quantity_kg,
                growing_days, season
            )
            SELECT 
                h.harvest_id,
                f.farmer_key,
                p.product_key,
                TO_CHAR(h.planting_date, 'YYYYMMDD')::INTEGER as planting_date_key,
                TO_CHAR(h.harvest_date, 'YYYYMMDD')::INTEGER as harvest_date_key,
                l.location_key,
                h.quantity_kg,
                h.quality_assessment,
                h.post_harvest_loss_pct,
                (h.quantity_kg * h.post_harvest_loss_pct / 100) as post_harvest_loss_kg,
                (h.quantity_kg - (h.quantity_kg * h.post_harvest_loss_pct / 100)) as net_quantity_kg,
                (h.harvest_date - h.planting_date) as growing_days, 
                h.season
            FROM staging.stg_harvests h
            JOIN dw.dim_farmer f ON h.farmer_id = f.farmer_id AND f.is_current = TRUE
            JOIN dw.dim_product p ON h.product_id = p.product_id AND p.is_current = TRUE
            JOIN dw.dim_location l ON f.district = l.district AND f.subcounty = l.subcounty
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.fact_harvest fh WHERE fh.harvest_id = h.harvest_id
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} harvests into fact_harvest")
        return rows_inserted

    def load_fact_pricing(self):
        """Load pricing fact table"""
        logger.info("Loading fact_pricing...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.fact_pricing (
                price_id, product_key, market_key, date_key,
                wholesale_price, retail_price,
                price_spread, price_spread_pct, price_trend, source
            )
            SELECT 
                pr.price_id,
                p.product_key,
                m.market_key,
                TO_CHAR(pr.price_date, 'YYYYMMDD')::INTEGER as date_key,
                pr.wholesale_price,
                pr.retail_price,
                (pr.retail_price - pr.wholesale_price) as price_spread,
                ((pr.retail_price - pr.wholesale_price) / pr.wholesale_price * 100) as price_spread_pct,
                pr.price_trend,
                pr.source
            FROM staging.stg_pricing pr
            JOIN dw.dim_product p ON pr.product_id = p.product_id AND p.is_current = TRUE
            JOIN dw.dim_market m ON pr.market_id = m.market_id AND m.is_current = TRUE
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.fact_pricing fp WHERE fp.price_id = pr.price_id
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} pricing records into fact_pricing")
        return rows_inserted

    def load_fact_weather(self):
        """Load weather fact table"""
        logger.info("Loading fact_weather...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.fact_weather (
                weather_id, location_key, date_key, weather_date,
                temperature_min, temperature_max, temperature_avg,
                rainfall_mm, humidity_pct, wind_speed_kmh,
                weather_condition, source
            )
            SELECT 
                w.weather_id,
                l.location_key,
                TO_CHAR(w.weather_date, 'YYYYMMDD')::INTEGER as date_key,
                w.weather_date,
                w.temperature_min,
                w.temperature_max,
                w.temperature_avg,
                w.rainfall_mm,
                w.humidity_pct,
                w.wind_speed_kmh,
                w.weather_condition,
                w.source
            FROM staging.stg_weather w
            JOIN dw.dim_location l ON w.district = l.district 
            WHERE l.location_key IN (SELECT MIN(location_key) FROM dw.dim_location GROUP BY district)
            AND NOT EXISTS (
                SELECT 1 FROM dw.fact_weather fw WHERE fw.weather_id = w.weather_id
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} weather records into fact_weather")
        return rows_inserted

    def load_fact_subsidy(self):
        """Load subsidy fact table"""
        logger.info("Loading fact_subsidy...")
        cursor = self.conn.cursor()
        
        cursor.execute("""
            INSERT INTO dw.fact_subsidy (
                farmer_subsidy_id, farmer_key, date_key,
                program_name, subsidy_type, amount_value,
                distribution_date, verification_status
            )
            SELECT 
                s.farmer_subsidy_id,
                f.farmer_key,
                TO_CHAR(s.distribution_date, 'YYYYMMDD')::INTEGER as date_key,
                s.program_name,
                s.subsidy_type,
                s.amount_value,
                s.distribution_date,
                s.verification_status
            FROM staging.stg_subsidies s
            JOIN dw.dim_farmer f ON s.farmer_id = f.farmer_id AND f.is_current = TRUE
            WHERE NOT EXISTS (
                SELECT 1 FROM dw.fact_subsidy fs WHERE fs.farmer_subsidy_id = s.farmer_subsidy_id
            )
        """)
        
        rows_inserted = cursor.rowcount
        self.conn.commit()
        logger.info(f"Inserted {rows_inserted} subsidy records into fact_subsidy")
        return rows_inserted

    def run_full_etl(self):
        """Run complete ETL pipeline"""
        try:
            self.connect_db()
            self.log_execution_start('Full ETL Pipeline')
            
            total_rows_inserted = 0
            
            # Load dimensions
            self.load_dim_date()
            total_rows_inserted += self.load_dim_farmer()
            total_rows_inserted += self.load_dim_product()
            total_rows_inserted += self.load_dim_market()
            total_rows_inserted += self.load_dim_buyer()
            total_rows_inserted += self.load_dim_location()
            
            # Load facts
            total_rows_inserted += self.load_fact_transaction()
            total_rows_inserted += self.load_fact_harvest()
            total_rows_inserted += self.load_fact_pricing()
            total_rows_inserted += self.load_fact_weather()
            total_rows_inserted += self.load_fact_subsidy()
            
            self.log_execution_end('Success', rows_inserted=total_rows_inserted)
            logger.info(f"ETL pipeline completed successfully. Total rows inserted: {total_rows_inserted}")
            
        except Exception as e:
            logger.error(f"ETL pipeline failed: {e}")
            import traceback
            logger.error(traceback.format_exc())
            if self.conn:
                self.conn.rollback()
            self.log_execution_end('Failed', error_message=str(e))
            raise
        finally:
            self.close_db()

if __name__ == "__main__":
    etl = ETLPipeline()
    etl.run_full_etl()
