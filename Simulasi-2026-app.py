import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SIMULASI BERTAHAP SUMMARECON", layout="wide")

# --- CUSTOM CSS (GOLD & DARK THEME) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stTextInput input { 
        background-color: #112240 !important; 
        color: #d4af37 !important; 
        border: 1px solid #d4af37 !important; 
        font-size: 1.5rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stMetric { 
        background-color: #112240; 
        padding: 20px; 
        border-radius: 15px; 
        border: 2px solid #d4af37; 
    }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 2.2rem !important; }
    label { font-size: 1.1rem !important; color: #ccd6f6 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def format_rp(angka):
    return f"Rp {int(angka):,.0f}".replace(",", ".")

def clean_number(text):
    return re.sub(r'[^0-9]', '', text)

# --- HEADER ---
st.title("🏛️ Summarecon Emerald Karawang")
st.subheader("Simulasi Bertahap - UTJ Memotong Harga")
st.markdown("---")

# --- INPUT PANEL ---
col_1, col_2, col_3 = st.columns([2, 2, 1.5])

with col_1:
    input_raw = st.text_input("Harga Tunai Keras 3x", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0

with col_2:
    # UTJ Dinamis sesuai permintaan (1jt - 50jt)
    utj_input = st.slider("Nominal UTJ (Memotong Harga)", 1000000, 50000000, 25000000, step=1000000)
    st.write(f"UTJ Terpilih: **{format_rp(utj_input)}**")

with col_3:
    list_tenor = [12, 24, 36, 48, 60]
    tenor = st.selectbox("Tenor (Bulan)", list_tenor, index=2)

st.markdown("---")

# --- LOGIKA PERHITUNGAN (Sesuai Pricelist Verena/Emerald) ---
# Faktor pengali 36x Flat Match: 1.1507922650
faktor_tetap_36x = 1.1507922650
margin_per_bulan = (faktor_tetap_36x - 1) / 36

# 1. Hitung Harga Jual Final berdasarkan Tenor
harga_jual_final = harga_dasar * (1 + (margin_per_bulan * tenor))

# 2. Kurangi Harga dengan UTJ (UTJ Memangkas Harga)
sisa_plafon_cicilan = harga_jual_final - utj_input

# 3. Hitung Cicilan per Bulan
cicilan_bulanan = sisa_plafon_cicilan / tenor

# --- DISPLAY HASIL ---
st.markdown(f"### Hasil Simulasi Bertahap {tenor}x")
c1, c2, c3 = st.columns(3)

with c1:
    st.metric("Total Harga Jual", format_rp(harga_jual_final))

with c2:
    st.metric("Uang Tanda Jadi (UTJ)", format_rp(utj_input))

with c3:
    st.metric("Angsuran per Bulan", format_rp(cicilan_bulanan))

# --- TABEL ESTIMASI CEPAT ---
st.markdown("---")
st.write("💡 **Tabel Referensi Cepat (Sisa Plafon Setelah UTJ):**")

data_utj = [10000000, 25000000, 50000000]
cols = st.columns(len(data_utj))

for i, nominal in enumerate(data_utj):
    sisa = harga_jual_final - nominal
    cicil = sisa / tenor
    with cols[i]:
        st.info(f"**UTJ {format_rp(nominal)}**\n\nCicilan: {format_rp(cicil)}")

st.caption("RUANG MASBAY | Verified Marketing Tool 2026")
