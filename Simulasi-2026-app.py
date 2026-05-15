import streamlit as st
import pandas as pd
import numpy_financial as npf

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (GOLDMAN SACHS INSPIRED) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stNumberInput, .stSelectbox { border-radius: 5px; }
    .stButton>button { width: 100%; background-color: #d4af37; color: white; border: none; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #233554; }
    
    /* Animasi Teks Berjalan */
    .marquee {
        width: 100%; overflow: hidden; white-space: nowrap;
        box-sizing: border-box; background: #112240; padding: 10px;
        color: #d4af37; font-weight: bold; border-bottom: 2px solid #d4af37;
    }
    .marquee p {
        display: inline-block; padding-left: 100%;
        animation: marquee 20s linear infinite;
    }
    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    </style>
    <div class="marquee"><p>RUANG MASBAY PROPERTY INTELLIGENT SINCE 2018 — EXPERT REAL ESTATE ANALYSIS — PROFESSIONAL MARKETING SERVICE</p></div>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH ---
def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# --- SISTEM LOGIN ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("Secure Access | Private Banking")
    password = st.text_input("Enter Access Key", type="password")
    if st.button("Unlock System"):
        if password == "Property2025":
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Invalid Access Key")
    st.stop()

# --- LAYOUT UTAMA ---
st.title("Property Investment Simulation 🏦")
st.markdown("---")

# --- INPUT GLOBAL ---
with st.sidebar:
    st.header("Global Input")
    harga_input = st.number_input("Harga Properti (Inc. PPN 11%)", min_value=0, step=50000000, value=2500000000, format="%d")
    utj = st.number_input("Uang Tanda Jadi (UTJ)", min_value=1000000, max_value=50000000, step=1000000, value=25000000)
    
    harga_excl_ppn = harga_input / 1.11
    st.info(f"**Harga Exclude PPN:** \n\n {format_rp(harga_excl_ppn)}")

# --- TAB MENU ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap", "🏠 Simulasi KPR"])

# --- TAB 1: CASH BERTAHAP (NPV LOGIC) ---
with tab1:
    col1, col2 = st.columns(2)
    with col1:
        tenor_cash = st.slider("Tenor Cash Bertahap (Bulan)", 1, 180, 12)
        disc_rate = st.selectbox("Discount Rate / NPV (Annual)", [i/10 for i in range(90, 130, 5)]) / 100
    
    # Kalkulasi NPV: Harga disesuaikan karena nilai uang di masa depan
    # Rumus sederhana: PV = FV / (1 + r)^n
    rate_monthly = disc_rate / 12
    sisa_harga = harga_input - utj
    angsuran_flat = sisa_harga / tenor_cash
    
    # Hitung NPV dari arus kas
    npv_value = npf.pv(rate_monthly, tenor_cash, -angsuran_flat) + utj
    
    with col2:
        st.metric("Estimasi Cicilan per Bulan", format_rp(angsuran_flat))
        st.metric("Net Present Value (NPV)", format_rp(npv_value))

# --- TAB 2: SIMULASI KPR ---
with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        dp_percent = st.slider("Persentase DP (%)", 5, 50, 20)
        dp_cicil = st.number_input("Cicil DP (Kali Payment)", 1, 12, 1)
    with c2:
        bunga_kpr = st.selectbox("Suku Bunga KPR (%)", list(range(1, 15)), index=4) / 100
        tenor_kpr = st.number_input("Tenor KPR (Tahun)", 1, 30, 15)
    with c3:
        biaya_akad_rate = st.selectbox("Biaya Akad (%)", list(range(1, 7)), index=2) / 100

    # Logika Harga vs Cicil DP (Adjustment Factor)
    # Semakin lama cicil DP, ada penambahan biaya (misal 0.5% per bulan cicilan)
    adj_price = harga_input * (1 + (0.005 * (dp_cicil - 1)))
    
    total_dp = (adj_price * (dp_percent / 100))
    plafon_kpr = adj_price - total_dp
    
    # Amortisasi
    monthly_rate = bunga_kpr / 12
    total_months = tenor_kpr * 12
    angsuran_kpr = npf.pmt(monthly_rate, total_months, -plafon_kpr)
    biaya_akad = plafon_kpr * biaya_akad_rate

    st.markdown("### KPR Executive Summary")
    sc1, sc2, sc3 = st.columns(3)
    sc1.metric("Total DP (Inc. UTJ)", format_rp(total_dp))
    sc2.metric("Plafon Pinjaman Bank", format_rp(plafon_kpr))
    sc3.metric("Angsuran KPR / Bulan", format_rp(angsuran_kpr))

    st.markdown("---")
    st.subheader("Detail Biaya Awal")
    st.write(f"Sisa DP setelah UTJ: **{format_rp(total_dp - utj)}**")
    st.write(f"Estimasi Biaya Akad KPR: **{format_rp(biaya_akad)}**")
    st.caption("*Catatan: Harga dapat berubah sesuai durasi cicilan DP (Time Value of Money adjustment).*")
