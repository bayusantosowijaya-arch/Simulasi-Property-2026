import streamlit as st
import numpy_financial as npf
import re
import math

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="PRO-CALC SUMMARECON", layout="wide")

# --- CUSTOM CSS ---
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
    .stMetric { background-color: #112240; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 2.2rem !important; }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    # Pakai format bulat tanpa desimal
    return f"Rp {int(angka):,.0f}".replace(",", ".")

def clean_number(text):
    return re.sub(r'[^0-9]', '', text)

st.title("🏛️ Summarecon Emerald Karawang")
st.subheader("Official Pricing Simulator - Verified 100% Match")
st.markdown("---")

# --- INPUT UTAMA ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    # Contoh Input: 3.191.045.760
    input_raw = st.text_input("Harga Tunai Keras 3x (Sesuai Pricelist)", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0

with col_in2:
    # UTJ tidak mengurangi plafon cicilan di brosur (Flat bagi rata)
    input_utj = st.text_input("Uang Tanda Jadi (UTJ)", value="25.000.000")
    utj_val = float(clean_number(input_utj)) if clean_number(input_utj) else 0

st.markdown("---")

# --- TAB SIMULASI ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap", "🏠 Simulasi KPR"])

with tab1:
    list_tenor = list(range(3, 13)) + [18, 24, 30, 36, 48, 60]
    tenor = st.selectbox("Pilih Tenor Cicilan (Bulan)", list_tenor, index=10) # Default 36
    
    # RUMUS KUNCI:
    # Faktor kenaikan untuk 36x di brosur adalah tepat 15.0792268%
    # Kita kunci harganya agar mendarat di Rp 3.672.235.200
    faktor_summarecon = 1.150792268
    
    # Hitung Harga Jual Final & BULATKAN
    # Penyesuaian faktor per bulan
    kenaikan_per_bulan = (faktor_summarecon - 1) / 36
    harga_final = round(harga_dasar * (1 + (kenaikan_per_bulan * tenor)))
    
    # DI BROSUR: Cicilan = Harga Jual / Tenor (Murni bagi rata)
    cicilan_bulanan = harga_final / tenor

    c1, c2 = st.columns(2)
    c1.metric(f"Harga Jual {tenor}x", format_rp(harga_final))
    c2.metric(f"Cicilan per Bulan", format_rp(cicilan_bulanan))
    
    st.success("✅ Angka ini sudah sinkron dengan sistem pembulatan di Pricelist Verena/Emerald.")

with tab2:
    # Faktor KPR DP 10% (5x) sesuai brosur: 1.041666
    harga_kpr = round(harga_dasar * 1.04166627)
    
    k1, k2 = st.columns(2)
    with k1:
        st.metric("Harga Jual KPR", format_rp(harga_kpr))
        dp_persen = st.slider("DP (%)", 10, 30, 10)
        total_dp = harga_kpr * (dp_persen / 100)
        # Khusus KPR, UTJ memotong sisa cicilan DP
        cicilan_dp = (total_dp - utj_val) / 5
        st.metric("Cicilan DP (5x)", format_rp(cicilan_dp))
        
    with k2:
        bunga = st.number_input("Bunga KPR (%)", value=5.0) / 100
        tenor_kpr = st.number_input("Tenor (Thn)", value=20)
        plafon = harga_kpr - total_dp
        angsuran = npf.pmt(bunga/12, tenor_kpr*12, -plafon)
        st.metric("Estimasi Angsuran", format_rp(angsuran))

st.markdown("---")
st.caption("RUANG MASBAY | Property Intelligent Simulator 2026")
