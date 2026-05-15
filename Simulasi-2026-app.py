import streamlit as st
import pandas as pd
import numpy_financial as npf
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (PREMIUM DARK GOLD) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stTextInput input { 
        background-color: #112240 !important; 
        color: #d4af37 !important; 
        border: 1px solid #d4af37 !important; 
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    label { color: #d4af37 !important; font-size: 1.1rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def clean_number(text):
    # Menghapus semua karakter kecuali angka
    return re.sub(r'[^0-9]', '', text)

# --- HEADER ---
st.title("Summarecon Property Intelligent Simulator 🏛️")
st.caption("Custom Input System - Support Thousand Separator (.)")
st.markdown("---")

# --- INPUT UTAMA ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    # Menggunakan text_input agar user bisa bebas mengetik titik (.)
    input_raw = st.text_input("Harga Tunai Keras 3x (Include PPN 11%)", value="3.191.045.760")
    
    # Proses pembersihan angka agar bisa dihitung
    harga_bersih = float(clean_number(input_raw)) if clean_number(input_raw) else 0
    
    st.write(f"Harga Terbaca Sistem: **{format_rp(harga_bersih)}**")

with col_in2:
    utj_raw = st.text_input("Uang Tanda Jadi (UTJ)", value="25.000.000")
    utj_bersih = float(clean_number(utj_raw)) if clean_number(utj_raw) else 0
    st.write(f"UTJ Terbaca Sistem: **{format_rp(utj_bersih)}**")

st.markdown("---")

# --- LOGIKA SIMULASI SESUAI PRICELIST ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap (Margin Standard)", "🏠 Simulasi KPR"])

# TAB 1: BERTAHAP
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        # Faktor pengali 36x Flat sesuai data pricelist yang diupload sebelumnya
        # (3.672.235.200 / 3.191.045.760) = 1.15079
        tenor = st.selectbox("Pilih Tenor Bertahap", [12, 24, 36], index=2)
        
        if tenor == 36:
            harga_final = harga_bersih * 1.1507923
        elif tenor == 24:
            harga_final = harga_bersih * 1.10
        else:
            harga_final = harga_bersih * 1.05

    with c2:
        st.metric(f"Harga Jual Bertahap {tenor}x", format_rp(harga_final))
        cicilan = (harga_final - utj_bersih) / tenor
        st.metric("Cicilan per Bulan", format_rp(cicilan))

# TAB 2: KPR
with tab2:
    k1, k2 = st.columns(2)
    with k1:
        # Faktor KPR DP 10% (5x) sesuai data pricelist
        # (3.324.006.000 / 3.191.045.760) = 1.041666
        harga_kpr = harga_bersih * 1.041666
        st.metric("Harga Jual KPR (DP 10% Cicil 5x)", format_rp(harga_kpr))
        
        dp_persen = st.slider("Persentase DP (%)", 10, 30, 10)
        total_dp = harga_kpr * (dp_persen / 100)
        plafon = harga_kpr - total_dp

    with k2:
        bunga = st.number_input("Suku Bunga KPR (%)", value=5.0) / 100
        tenor_thn = st.number_input("Tenor KPR (Tahun)", value=20)
        angsuran = npf.pmt(bunga/12, tenor_thn*12, -plafon)
        st.metric("Estimasi Angsuran KPR", format_rp(angsuran))

st.markdown("---")
st.caption("RUANG MASBAY | Data input otomatis dibersihkan dari titik/karakter non-angka untuk akurasi hitungan.")
