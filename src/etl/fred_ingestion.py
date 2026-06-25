import os
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
from logger import get_logger

logger = get_logger(__name__)

# You can set this as an environment variable or load it from config.yaml
FRED_API_KEY = os.environ.get("FRED_API_KEY", "3ecfc31416a5a9fe77a653f839e10543")
BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

# Key Series IDs for the Federal Reserve:
# CPIAUCSL: Consumer Price Index for All Urban Consumers (Inflation)
# FEDFUNDS: Federal Funds Effective Rate (Policy Rate)
# DGS10: 10-Year Treasury Constant Maturity Rate (Yield)
# DGS2: 2-Year Treasury Constant Maturity Rate

def fetch_fred_data(series_id: str, start_date: str = "2010-01-01") -> pd.DataFrame:
    """Fetch time series data from the FRED API."""
    logger.info(f"Fetching data for FRED series: {series_id}")
    
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "observation_start": start_date
    }
    
    response = requests.get(BASE_URL, params=params)
    
    if response.status_code != 200:
        logger.error(f"API Request failed with status code {response.status_code}: {response.text}")
        response.raise_for_status()
    
    data = response.json()
    observations = data.get("observations", [])
    
    df = pd.DataFrame(observations)
    if not df.empty:
        df = df[['date', 'value']]
        df['date'] = pd.to_datetime(df['date'])
        df['value'] = pd.to_numeric(df['value'], errors='coerce')
        df['series_id'] = series_id
    
    logger.info(f"Retrieved {len(df)} records for {series_id}")
    return df

if __name__ == "__main__":
    if FRED_API_KEY == "YOUR_API_KEY_HERE":
        logger.warning("FRED_API_KEY is not set! You must get a free API key from https://fred.stlouisfed.org/docs/api/api_key.html")
    
    try:
        # Example: Fetch 10-Year Treasury Yields for Market Trust calculation
        series = "DGS10"
        df_10y = fetch_fred_data(series)
        
        if not df_10y.empty:
            print(df_10y.tail())
            
            # Save to raw data folder
            output_dir = Path(__file__).parent.parent.parent / "data" / "raw"
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / f"fred_{series.lower()}.csv"
            df_10y.to_csv(output_path, index=False)
            logger.info(f"Saved {series} data to {output_path}")
            
    except Exception as e:
        logger.error(f"Failed to fetch FRED data: {e}")
