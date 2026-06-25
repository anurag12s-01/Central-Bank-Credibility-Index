import argparse
import pandas as pd
from pathlib import Path
from logger import get_logger
from db_utils import setup_database, get_db_connection
from validation import MacroIndicator, MarketData
from psycopg2.extras import execute_batch

logger = get_logger(__name__)

def extract():
    logger.info("Starting Data Extraction...")
    # Locate the CSV we downloaded via fred_ingestion.py
    data_file = Path(__file__).parent.parent.parent / "data" / "raw" / "fred_dgs10.csv"
    if not data_file.exists():
        logger.warning("Data file not found. Run fred_ingestion.py first.")
        return []
        
    df = pd.read_csv(data_file)
    logger.info(f"Extracted {len(df)} rows from {data_file.name}")
    return df

def transform(raw_df):
    logger.info("Starting Data Transformation...")
    valid_data = []
    
    # 1. Convert to datetime and clean numerics
    raw_df['date'] = pd.to_datetime(raw_df['date'], errors='coerce')
    raw_df['value'] = pd.to_numeric(raw_df['value'], errors='coerce')
    raw_df = raw_df.dropna(subset=['date']).sort_values('date')
    
    # 2. Impute missing dates (weekends/holidays) using Forward-Fill
    logger.info("Applying Forward-Fill Imputation for missing financial days...")
    raw_df = raw_df.set_index('date').asfreq('D').ffill().reset_index()
    
    for _, row in raw_df.iterrows():
        try:
            if pd.isna(row['value']):
                continue
                
            # Map the raw FRED data to our strict database schema
            transformed_row = {
                'cb_id': 'FED',
                'date': row['date'].strftime('%Y-%m-%d'),
                'instrument': row['series_id'] if pd.notna(row['series_id']) else 'DGS10',
                'close_price': float(row['value']),
                'volatility': None
            }
            # This triggers the Pydantic validation
            validated_item = MarketData(**transformed_row)
            valid_data.append(validated_item)
        except Exception as e:
            logger.debug(f"Validation failed: {e}")
            
    logger.info(f"Successfully transformed and validated {len(valid_data)} records.")
    return valid_data

def load(clean_data):
    logger.info("Starting Data Loading...")
    if not clean_data:
        logger.info("No data to load.")
        return
        
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # 1. Ensure the Federal Reserve exists in our dimension table first (Foreign Key constraint)
            logger.info("Ensuring 'FED' dimension exists...")
            insert_dim = """
                INSERT INTO dim_central_bank (cb_id, bank_name, country, target_inflation)
                VALUES ('FED', 'Federal Reserve', 'United States', 2.0)
                ON CONFLICT (cb_id) DO NOTHING;
            """
            cur.execute(insert_dim)
            
            # 2. Bulk insert the market data into the fact table
            insert_fact = """
                INSERT INTO fact_market_data (cb_id, date, instrument, close_price)
                VALUES (%(cb_id)s, %(date)s, %(instrument)s, %(close_price)s)
                ON CONFLICT (cb_id, date, instrument) DO NOTHING;
            """
            # Convert Pydantic models back to dictionaries for psycopg2
            data_dicts = [item.dict() for item in clean_data]
            
            logger.info(f"Executing PostgreSQL bulk insert for {len(data_dicts)} records...")
            execute_batch(cur, insert_fact, data_dicts)
            
        conn.commit()
        logger.info(f"Successfully loaded {len(clean_data)} records into 'fact_market_data' table.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Failed to load data: {e}")
    finally:
        conn.close()

def run_etl():
    logger.info("--- CBCI ETL Pipeline Started ---")
    raw_data = extract()
    clean_data = transform(raw_data)
    load(clean_data)
    logger.info("--- CBCI ETL Pipeline Completed ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CBCI ETL Pipeline")
    parser.add_argument("--setup-db", action="store_true", help="Initialize the database schema")
    args = parser.parse_args()

    if args.setup_db:
        schema_file = Path(__file__).parent / "schema.sql"
        setup_database(str(schema_file))
    else:
        run_etl()
