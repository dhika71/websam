import os
import requests
import pandas as pd
from supabase import create_client, Client

# Ambil credentials dari environment (digunakan oleh GitHub Actions)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
TE_API_KEY = os.environ.get("TRADING_ECONOMICS_API_KEY")

# Inisialisasi Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Daftar indikator makro yang ingin diambil
INDICATORS = ['gdp', 'inflation-rate', 'unemployment-rate']

# Negara target (gunakan 'world' atau ambil semua dari list negara jika kamu ingin full global)
COUNTRY = 'world'

# Fungsi untuk ambil data dari TradingEconomics
def fetch_indicator(indicator: str):
    print(f"Fetching: {indicator}")
    url = (
        f"https://api.tradingeconomics.com/historical/country/{COUNTRY}/indicator/{indicator}"
        f"?c={TE_API_KEY}&f=json"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed fetching {indicator}: {response.text}")
        return pd.DataFrame()

    data = response.json()
    df = pd.DataFrame(data)
    if df.empty:
        print(f"{indicator} data kosong")
        return pd.DataFrame()

    df["indicator"] = indicator
    return df

# Gabungkan semua data indikator
def fetch_all_macro_data():
    all_data = []
    for ind in INDICATORS:
        df = fetch_indicator(ind)
        if not df.empty:
            all_data.append(df)
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# Simpan ke Supabase
def upload_to_supabase(df: pd.DataFrame):
    if df.empty:
        print("Dataframe kosong, tidak ada data untuk disimpan.")
        return

    # Optional: Drop kolom yang tidak perlu
    allowed_cols = ['Country', 'Category', 'DateTime', 'Value', 'indicator']
    df = df[allowed_cols]

    print(f"Mengupload {len(df)} baris ke Supabase...")
    records = df.to_dict(orient='records')

    batch_size = 50
    for i in range(0, len(records), batch_size):
        batch = records[i:i+batch_size]
        res = supabase.table("macro_data").insert(batch).execute()
        print(f"Batch {i//batch_size + 1} upload status:", res)

# Main proses
if __name__ == "__main__":
    df_macro = fetch_all_macro_data()
    upload_to_supabase(df_macro)
    print("✅ Selesai update macro data.")
