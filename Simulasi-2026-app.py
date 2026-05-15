import streamlit as st
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
    .stSelectbox div[data-baseweb="select"] { background-color: #112240 !important; border: 1px solid #d4af37 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- FUNGSI HELPER ---
def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

def clean_number(text):
    # Membersihkan titik agar bisa dihitung secara matematis
    return re.sub(r'[^0-9]', '', text)

# --- HEADER ---
st.title("Summarecon Property Intelligent Simulator 🏛️")
st.caption("Custom Input System - Synchronized with Summarecon Emerald Karawang Pricelist")
st.markdown("---")

# --- INPUT UTAMA ---
col_in1, col_in2 = st.columns(2)

with col_in1:
    # User bisa mengetik harga langsung dengan titik
    input_raw = st.text_input("Harga Tunai Keras 3x (Include PPN 11%)", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0
    st.write(f"Harga Dasar Terbaca: **{format_rp(harga_dasar)}**")

with col_in2:
    utj_raw = st.text_input("Uang Tanda Jadi (UTJ)", value="25.000.000")
    utj_bersih = float(clean_number(utj_raw)) if clean_number(utj_raw) else 0
    st.write(f"UTJ Terbaca: **{format_rp(utj_bersih)}**")

st.markdown("---")

# --- LOGIKA SIMULASI ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap (3 - 60 Bulan)", "🏠 Simulasi KPR"])

# --- TAB 1: CASH BERTAHAP ---
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        # Pilihan tenor lengkap sesuai permintaan Mas Bayu
        list_tenor = list(range(3, 13)) + [18, 24, 30, 36, 48, 60]
        tenor_pilihan = st.selectbox("Pilih Tenor Cicilan (Bulan)", list_tenor, index=10) # Default 36 bulan
        
        # LOGIKA KENAIKAN HARGA (FAKTOR SUMMARECON)
        # 36x Flat memiliki faktor kenaikan ~15.0792% dari Tunai 3x
        # Kita buat skala linear untuk tenor lainnya agar tetap masuk akal
        faktor_tahunan = 0.15079227 / 36 # Mencari kenaikan per bulan
        faktor_final = 1 + (faktor_tahunan * tenor_pilihan)
        
        harga_final_bertahap = harga_dasar * faktor_final
        
    with c2:
        st.metric(f"Harga Jual Bertahap {tenor_pilihan}x", format_rp(harga_final_bertahap))
        cicilan_per_bulan = (harga_final_bertahap - utj_bersih) / tenor_pilihan
        st.metric("Cicilan Flat per Bulan", format_rp(cicilan_per_bulan))
        
    st.info(f"Catatan: Faktor pengali harga untuk {tenor_pilihan} bulan adalah {faktor_final:.4f}")

# --- TAB 2: KPR ---
with tab2:
    k1, k2 = st.columns(2)
    with k1:
        # Faktor KPR DP 10% (5x) sesuai pricelist: 1.041666
        harga_kpr = harga_dasar * 1.04166627
        st.metric("Harga Jual KPR (Incl. PPN)", format_rp(harga_kpr))
        
        dp_persen = st.slider("Persentase DP (%)", 10, 30, 10)
        total_dp = harga_kpr * (dp_persen / 100)
        plafon_kpr = harga_kpr - total_dp
        
        cicil_dp_kali = st.number_input("Cicil DP Berapa Kali?", value=5)
        cicilan_dp = (total_dp - utj_bersih) / cicil_dp_kali

    with k2:
        bunga_kpr = st.number_input("Suku Bunga KPR (%)", value=5.0) / 100
        tenor_kpr_thn = st.number_input("Tenor KPR (Tahun)", value=20)
        
        # Hitungan angsuran KPR (PMT)
        angsuran_kpr = npf.pmt(bunga_kpr/12, tenor_kpr_thn*12, -plafon_kpr)
        
        st.metric("Cicilan DP per Bulan", format_rp(cicilan_dp))
        st.metric("Estimasi Angsuran KPR", format_rp(angsuran_kpr))

st.markdown("---")
st.caption("RUANG MASBAY | Versi Sinkronisasi 60 Bulan - Summarecon Emerald Karawang")
