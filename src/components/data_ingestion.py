import pandas as pd
from src.loggers import logging  

# Base Google Sheets URL
BASE_URL = "https://docs.google.com/spreadsheets/d/"
SHEET_ID = "1P2M9_wVO5rcy4Hp8CNyKwJXs4Dwi-roea8TbmnCcU1A"
EXPORT_FORMAT = "/gviz/tq?tqx=out:csv"

# Construct public sheet URL
PUBLIC_SHEET_URL = f"{BASE_URL}{SHEET_ID}{EXPORT_FORMAT}"

def fetch_google_sheet(url):
    """Fetch data from Google Sheets and return a Pandas DataFrame."""
    try:
        logging.info("Fetching data from Google Sheets...")
        df = pd.read_csv(url)
        logging.info("Data fetched successfully!")
        df.to_csv("artifacts/data.csv", index=False)
        return df
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return None

if __name__ == "__main__":
    df = fetch_google_sheet(PUBLIC_SHEET_URL)

    if df is not None:
        logging.info(f"📊 Loaded {len(df)} rows from Google Sheets.")
        print(df.head())  
