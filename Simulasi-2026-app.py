import streamlit as st
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #d4af37; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

st.title("Summarecon Emerald Karawang Simulator 🏦")

# --- INPUT UTAMA ---
col1, col2 = st.columns(2)
with col1:
    # Masukkan harga Tunai Keras 3x sebagai patokan pricelist
    harga_tunai_3x = st.number_input("Harga Tunai Keras 3x (Sesuai Pricelist)", value=3191045760, step=1000000)
    utj = st.number_input("Uang Tanda Jadi (UTJ)", value=25000000)

with col2:
    cara_bayar = st.selectbox("Pilih Cara Bayar", ["Tunai Keras 3x", "KPR DP 10% (Cicil 5x)", "Bertahap 36x FLAT"])

# --- LOGIKA HARGA BERDASARKAN PRICELIST ---
if cara_bayar == "Tunai Keras 3x":
    harga_final = harga_tunai_3x
    deskripsi = "Pembayaran Tunai Keras 3 bulan flat."
elif cara_bayar == "KPR DP 10% (Cicil 5x)":
    # Kenaikan rata-rata ~4.16% dari Tunai 3x berdasarkan data pricelist
    harga_final = harga_tunai_3x * 1.041666
    deskripsi = "KPR dengan DP 10% yang dicicil selama 5 bulan."
else: # Bertahap 36x FLAT
    # Kenaikan rata-rata ~15.08% dari Tunai 3x berdasarkan data pricelist
    harga_final = harga_tunai_3x * 1.15079
    deskripsi = "Cicilan bertahap ke developer selama 36 bulan flat."

st.markdown("---")
st.subheader(f"Hasil Simulasi: {cara_bayar}")
m1, m2 = st.columns(2)
m1.metric("Harga Jual (Incl. PPN)", format_rp(harga_final))

if cara_bayar == "Bertahap 36x FLAT":
    cicilan = (harga_final - utj) / 36
    m2.metric("Cicilan per Bulan (36x)", format_rp(cicilan))
elif cara_bayar == "KPR DP 10% (Cicil 5x)":
    dp_total = harga_final * 0.10
    cicilan_dp = (dp_total - utj) / 5
    m2.metric("Cicilan DP per Bulan (5x)", format_rp(cicilan_dp))

st.info(deskripsi)
st.caption("Catatan: Perhitungan ini menggunakan asumsi kenaikan harga flat sesuai rata-rata pricelist Summarecon Emerald Karawang.")
