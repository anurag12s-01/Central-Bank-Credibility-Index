import psycopg2
from psycopg2.extras import execute_batch
import yaml
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

def get_db_connection():
    config_path = Path(__file__).parent / "config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
        
    db_config = config['database']
    try:
        conn = psycopg2.connect(
            host=db_config['host'],
            port=db_config['port'],
            dbname=db_config['dbname'],
            user=db_config['user'],
            password=db_config['password']
        )
        return conn
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise

def setup_database(schema_path: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            with open(schema_path, 'r') as f:
                cur.execute(f.read())
        conn.commit()
        logger.info("Database schema initialized successfully.")
    except Exception as e:
        conn.rollback()
        logger.error(f"Error initializing database: {e}")
        raise
    finally:
        conn.close()
