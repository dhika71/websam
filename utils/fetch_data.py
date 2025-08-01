import yfinance as yf
import pandas as pd

def fetch_stock_data(tickers, start_date, end_date):
    all_data = []

    if isinstance(tickers, str):
        tickers = [tickers]

    try:
        # Ambil semua ticker sekaligus
        data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            group_by='ticker'
        )

        for ticker in tickers:
            try:
                df = data[ticker].copy()
                df.reset_index(inplace=True)
                df['Ticker'] = ticker

                if df.empty or not all(col in df.columns for col in ['Open', 'High', 'Low', 'Close', 'Volume']):
                    print(f"Data {ticker} tidak memiliki semua kolom yang dibutuhkan.")
                    continue

                all_data.append(df)
            except Exception as e:
                print(f"Gagal memproses data untuk {ticker}: {e}")

    except Exception as e:
        print(f"Gagal mengambil data: {e}")

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        print("Gagal mengambil data: semua data kosong atau tidak lengkap.")
        return pd.DataFrame()
