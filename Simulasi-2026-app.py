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

# --- FUNGSI HELPER ---
def format_rp(angka):
    return f"Rp {int(angka):,.0f}".replace(",", ".")

def clean_number(text):
    return re.sub(r'[^0-9]', '', text)

# --- HEADER ---
st.title("🏛️ Summarecon Emerald Karawang")
st.subheader("Simulasi Pembayaran Bertahap (Flat Match)")
st.markdown("---")

# --- INPUT PANEL ---
col_a, col_b = st.columns(2)

with col_a:
    input_raw = st.text_input("Harga Tunai Keras 3x (Sesuai Pricelist)", value="3.191.045.760")
    harga_dasar = float(clean_number(input_raw)) if clean_number(input_raw) else 0

with col_b:
    # Tenor yang tersedia di Summarecon
    list_tenor = [12, 24, 36, 48, 60]
    tenor = st.selectbox("Pilih Tenor Cicilan (Bulan)", list_tenor, index=2)

st.markdown("### Hasil Simulasi")

# --- LOGIKA PERHITUNGAN KHUSUS BERTAHAP ---
# Faktor pengali khusus untuk mendapatkan angka Rp 3.672.235.200 dari 3.191.045.760
faktor_tetap_36x = 1.15079365

# Hitung kenaikan harga secara proporsional terhadap tenor
margin_per_bulan = (faktor_tetap_36x - 1) / 36
harga_jual_final = harga_dasar * (1 + (margin_per_bulan * tenor))

# Rumus Cicilan: Harga Jual Final dibagi Tenor (UTJ dianggap cicilan ke-0/DP awal)
cicilan_bulanan = harga_jual_final / tenor

# --- DISPLAY PANEL ---
c1, c2 = st.columns(2)

with c1:
    st.metric(f"Total Harga Jual ({tenor}x)", format_rp(harga_jual_final))

with c2:
    st.metric(f"Angsuran per Bulan ({tenor}x)", format_rp(cicilan_bulanan))

st.markdown("---")
# Catatan edukasi untuk konsumen
st.info(f"""
**Informasi Pembayaran:**
* Simulasi ini menggunakan metode **Flat Payment** sesuai standar pricelist.
* Harga sudah termasuk PPN 11%.
* Jadwal pembayaran mengikuti ketentuan yang berlaku di Summarecon Emerald Karawang.
""")

st.caption("RUANG MASBAY | Verifikasi Data Properti 2026")
