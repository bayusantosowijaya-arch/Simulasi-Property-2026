import streamlit as st
import re

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="SIMULASI BERTAHAP SUMMARECON", layout="wide")

# --- CUSTOM CSS (KUNCIAN MAS BAYU) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stTextInput input { 
        background-color: #112240 !important; 
        color: #d4af37 !important; 
        border: 1px solid #d4af37 !important; 
        font-size: 1.6rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    .stMetric { 
        background-color: #112240; 
        padding: 25px; 
        border-radius: 15px; 
        border: 2px solid #d4af37; 
    }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-size: 2.5rem !important; }
    label { font-size: 1.2rem !important; color: #ccd6f6 !important; }
    </style>
    """, unsafe_allow_html=True)

def format_rp(angka):
    return f"Rp {int(angka):,.0f}".replace(",", ".")

def clean_number(text):
    return re.sub(r'[^0-9]', '', text)

st.title("🏛️ Summarecon Emerald Karawang")
st.subheader("Simulasi Bertahap (UTJ Memangkas Harga)")
st.markdown("---")

# --- INPUT PANEL ---
col_a, col_b, col_c = st.columns(3)

with col_a:
    input_raw = st.text_input("Harga Tunai Keras 3x", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0

with col_b:
    # INPUT UTJ DISINI
    utj_raw = st.text_input("Input UTJ (1jt - 50jt)", value="25.000.000")
    utj_val = float(clean_number(utj_raw)) if clean_number(utj_raw) else 0

with col_c:
    list_tenor = [12, 24, 36, 48, 60]
    tenor = st.selectbox("Pilih Tenor", list_tenor, index=2)

st.markdown("### Hasil Simulasi")

# --- LOGIKA KUNCIAN PRICELIST (JANGAN DIUBAH) ---
# Faktor ini tetap untuk menjaga agar Harga Jual Final sesuai Brosur
faktor_tetap_36x = 1.15079365
margin_per_bulan = (faktor_tetap_36x - 1) / 36
harga_jual_final = harga_dasar * (1 + (margin_per_bulan * tenor))

# --- LOGIKA BARU: UTJ MEMANGKAS HARGA ---
# Harga Jual Final dikurangi UTJ dulu, baru sisa-nya dibagi tenor
sisa_plafon = harga_jual_final - utj_val
cicilan_bulanan = sisa_plafon / tenor

# --- DISPLAY PANEL ---
c1, c2, c3 = st.columns(3)

with c1:
    st.metric(f"Harga Jual ({tenor}x)", format_rp(harga_jual_final))

with c2:
    st.metric("UTJ (Booking)", format_rp(utj_val))

with c3:
    st.metric("Cicilan per Bulan", format_rp(cicilan_bulanan))

st.markdown("---")
st.info(f"💡 **Logika:** Harga Jual Final dikurangi UTJ {format_rp(utj_val)}, kemudian sisanya dibagi rata {tenor} bulan.")
st.caption("RUANG MASBAY | Verified Marketing Tool 2026")
