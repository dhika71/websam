import requests
import pandas as pd
import datetime
import os
from supabase import create_client, Client

# Load dari secrets environment
TRADING_ECONOMICS_API_KEY = os.getenv("TRADING_ECONOMICS_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_macro_data():
    try:
        url = f"https://api.tradingeconomics.com/indicators?c={TRADING_ECONOMICS_API_KEY}"
        response = requests.get(url)

        if response.status_code != 200:
            print("Gagal fetch data dari TradingEconomics:", response.text)
            return None

        data = response.json()
        df = pd.DataFrame(data)

        df = df[[
            "country", "title", "latestValue", "latestValueDate", "unit", "source"
        ]].rename(columns={
            "country": "country",
            "title": "indicator",
            "latestValue": "value",
            "latestValueDate": "date",
            "unit": "unit",
            "source": "source"
        })

        df["date"] = pd.to_datetime(df["date"], errors='coerce').dt.date
        df = df.dropna(subset=["date", "value"])
        return df

    except Exception as e:
        print("Error saat fetch:", e)
        return None

def upload_to_supabase(df: pd.DataFrame):
    try:
        records = df.to_dict(orient="records")
        batch_size = 500
        for i in range(0, len(records), batch_size):
            batch = records[i:i+batch_size]
            supabase.table("macro_data").upsert(batch).execute()
            print(f"Uploaded batch {i//batch_size+1} with {len(batch)} rows.")
    except Exception as e:
        print("Upload error:", e)

def main():
    df = fetch_macro_data()
    if df is not None and not df.empty:
        print(f"Fetched {len(df)} rows.")
        upload_to_supabase(df)
    else:
        print("Data kosong atau tidak valid.")

if __name__ == "__main__":
    main()
