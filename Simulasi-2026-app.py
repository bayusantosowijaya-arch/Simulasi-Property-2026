import streamlit as st
import pandas as pd
import numpy_financial as npf

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (PREMIUM LOOK) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    /* Memperbesar tampilan input angka agar lebih jelas */
    .stNumberInput input { 
        background-color: #112240 !important; 
        color: #d4af37 !important; 
        border: 1px solid #d4af37 !important; 
        font-size: 1.2rem !important;
        font-weight: bold !important;
    }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH ---
# Fungsi ini memastikan tampilan hasil akhir menggunakan titik sebagai pemisah ribuan
def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# --- SISTEM LOGIN ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔒 Secure Investment Access")
    password = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock System"):
        if password == "Property2025":
            st.session_state['auth'] = True
            st.rerun()
    st.stop()

# --- HEADER ---
st.title("Summarecon Property Intelligent Simulator 🏛️")
st.markdown("---")

# --- INPUT UTAMA DENGAN FORMAT TITIK ---
col_main1, col_main2 = st.columns(2)

with col_main1:
    # Menggunakan format="%d" agar otomatis muncul pemisah ribuan saat diketik
    harga_base = st.number_input("Input Harga Cash Keras (Inc. PPN 11%)", 
                                min_value=0, 
                                value=2500000000, 
                                step=1000000, 
                                format="%d",
                                help="Ketik angka tanpa titik, sistem akan otomatis memformatnya.")
    
    st.markdown(f"Konfirmasi Harga: **{format_rp(harga_base)}**")

with col_main2:
    utj = st.number_input("Uang Tanda Jadi (UTJ)", 
                          min_value=0, 
                          value=25000000, 
                          step=1000000, 
                          format="%d")
    st.markdown(f"Konfirmasi UTJ: **{format_rp(utj)}**")

st.markdown("---")

# --- TAB SIMULASI ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap (9.5% NPV)", "🏠 Simulasi KPR"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        tenor_cash = st.slider("Tenor Cicilan (Bulan)", 1, 180, 36)
        discount_rate = 0.095 # Sesuai instruksi Manager 9.5%
        
        # Logika NPV untuk menentukan Harga Jual Baru
        rate_m = discount_rate / 12
        if tenor_cash > 1:
            harga_jual_baru = harga_base * ((1 + rate_m) ** tenor_cash)
        else:
            harga_jual_baru = harga_base
            
    with c2:
        st.metric("Harga Jual (Adjusted 9.5% NPV)", format_rp(harga_jual_baru))
        cicilan = (harga_jual_baru - utj) / tenor_cash
        st.metric("Cicilan per Bulan", format_rp(cicilan))

with tab2:
    k1, k2 = st.columns(2)
    with k1:
        dp_percent = st.slider("DP (%)", 5, 50, 10)
        tenor_kpr = st.number_input("Tenor KPR (Tahun)", 1, 30, 20)
    
    with k2:
        bunga_kpr = st.selectbox("Suku Bunga KPR (%)", [round(x * 0.25, 2) for x in range(4, 57)], index=16) / 100
        
    # Hitungan KPR Sederhana
    total_dp = harga_base * (dp_percent / 100)
    plafon = harga_base - total_dp
    angsuran = npf.pmt(bunga_kpr/12, tenor_kpr*12, -plafon)
    
    st.markdown("### Ringkasan KPR")
    sk1, sk2 = st.columns(2)
    sk1.metric("Plafon Pinjaman", format_rp(plafon))
    sk2.metric("Angsuran per Bulan", format_rp(angsuran))

st.markdown("---")
st.caption("RUANG MASBAY PROPERTY INTELLIGENT | Perhitungan otomatis menggunakan standar 9.5% NPV.")
