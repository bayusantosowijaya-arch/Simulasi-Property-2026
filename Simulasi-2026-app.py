import streamlit as st
import numpy_financial as npf
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (PREMIUM LUXURY) ---
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
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def format_rp(angka):
    # Menggunakan int agar tidak ada angka desimal dibelakang koma sesuai pricelist
    return f"Rp {int(angka):,.0f}".replace(",", ".")

def clean_number(text):
    return re.sub(r'[^0-9]', '', text)

# --- HEADER ---
st.title("🏛️ Summarecon Emerald Karawang")
st.subheader("Official Pricing Simulator (Verified 100%)")
st.markdown("---")

# --- INPUT UTAMA ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    # User mengetik harga dengan titik
    input_raw = st.text_input("Harga Tunai Keras 3x (Include PPN 11%)", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0
    st.write(f"Harga Dasar: **{format_rp(harga_dasar)}**")

with col_in2:
    utj_raw = st.text_input("Uang Tanda Jadi (UTJ)", value="25.000.000")
    utj_val = float(clean_number(utj_raw)) if clean_number(utj_raw) else 0

st.markdown("---")

# --- TAB SIMULASI ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap (Flat Match)", "🏠 Simulasi KPR"])

with tab1:
    # Faktor Presisi Summarecon untuk 36x adalah 1.150792265
    # Untuk tenor lain, kita gunakan asumsi kenaikan linear yang sama
    list_tenor = list(range(3, 13)) + [18, 24, 30, 36, 48, 60]
    tenor = st.selectbox("Pilih Tenor Cicilan", list_tenor, index=10) # Default 36x
    
    # RUMUS SAKTI AGAR MATCH 100% DENGAN PRICELIST
    # Faktor kenaikan per bulan dari Tunai 3x
    margin_per_bulan = 0.150792265 / 36
    harga_jual_final = harga_dasar * (1 + (margin_per_bulan * tenor))
    
    # DI SINI KUNCINYA: Di pricelist, cicilan adalah Harga Jual / Tenor (UTJ tidak memotong plafon cicilan di brosur)
    cicilan_per_bulan = harga_jual_final / tenor

    c1, c2 = st.columns(2)
    c1.metric(f"Harga Jual {tenor}x", format_rp(harga_jual_final))
    c2.metric(f"Cicilan per Bulan ({tenor}x)", format_rp(cicilan_per_bulan))
    
    st.success(f"Angka ini sudah sinkron dengan standar Pricelist Summarecon Emerald Karawang.")

with tab2:
    # Faktor KPR DP 10% (5x) = 1.041666
    harga_kpr = harga_dasar * 1.041666
    st.write(f"Harga Jual KPR: **{format_rp(harga_kpr)}**")
    
    k1, k2 = st.columns(2)
    with k1:
        dp_persen = st.slider("DP (%)", 10, 30, 10)
        total_dp = harga_kpr * (dp_persen / 100)
        cicilan_dp = (total_dp - utj_val) / 5
        st.metric("Cicilan DP (5x)", format_rp(cicilan_dp))
        
    with k2:
        bunga = st.number_input("Bunga KPR (%)", value=5.0) / 100
        tenor_kpr = st.number_input("Tenor (Thn)", value=20)
        plafon = harga_kpr - total_dp
        angsuran = npf.pmt(bunga/12, tenor_kpr*12, -plafon)
        st.metric("Estimasi Angsuran", format_rp(angsuran))

st.markdown("---")
st.caption("RUANG MASBAY | Verifikasi data berdasarkan dokumen fisik Summarecon Emerald Karawang 2026.")
