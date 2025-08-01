import streamlit as st
import plotly.express as px
from utils.fetch_data import fetch_stock_data
from datetime import date

st.set_page_config(page_title="Stock Chart Viewer", layout="wide")

# Judul aplikasi
st.title("📈 Stock Price Viewer")

# Pilihan saham
tickers = st.multiselect(
    "Pilih saham (gunakan kode IDX seperti BBCA.JK, BBRI.JK):",
    options=["BBCA.JK", "BMRI.JK", "BBRI.JK", "TLKM.JK", "UNVR.JK"],
    default=["BBCA.JK"]
)

# Rentang tanggal
col1, col2 = st.columns(2)
with col1:
    start = st.date_input("Tanggal mulai", value=date(2022, 1, 1))
with col2:
    end = st.date_input("Tanggal akhir", value=date.today())

# Tombol ambil data
if st.button("📥 Ambil dan Tampilkan Data"):
    with st.spinner("Mengambil data..."):
        df = fetch_stock_data(tickers, start, end)

    if df.empty:
        st.error("Gagal mengambil data atau data kosong.")
    else:
        # Hapus komentar di baris berikut jika ingin menampilkan preview
        # st.dataframe(data)

        # Grafik interaktif dengan Plotly
        fig = px.line(
            df,
            x="Date",
            y="Close",
            color="Ticker",
            title="Harga Penutupan Saham",
            labels={"Close": "Harga Penutupan", "Date": "Tanggal"},
            template="plotly_white"
        )
        st.plotly_chart(fig, use_container_width=True)
