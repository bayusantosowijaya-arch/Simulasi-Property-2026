import streamlit as st
import pandas as pd
import numpy_financial as npf

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (PREMIUM BANKING AESTHETIC) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stNumberInput input { background-color: #112240 !important; color: white !important; border: 1px solid #d4af37 !important; font-size: 1.1rem !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #112240 !important; border: 1px solid #d4af37 !important; }
    .stMetric { background-color: #112240; padding: 20px; border-radius: 12px; border: 1px solid #d4af37; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }
    div[data-testid="stMetricValue"] { color: #d4af37 !important; font-weight: bold; }
    
    /* Animasi Teks Berjalan */
    .marquee {
        width: 100%; overflow: hidden; white-space: nowrap;
        box-sizing: border-box; background: #112240; padding: 12px;
        color: #d4af37; font-weight: bold; border-bottom: 2px solid #d4af37;
        font-family: 'Arial', sans-serif; letter-spacing: 2px;
    }
    .marquee p {
        display: inline-block; padding-left: 100%;
        animation: marquee 25s linear infinite;
        margin-bottom: 0;
    }
    @keyframes marquee {
        0% { transform: translate(0, 0); }
        100% { transform: translate(-100%, 0); }
    }
    </style>
    <div class="marquee"><p>RUANG MASBAY PROPERTY INTELLIGENT SINCE 2018 — EXPERT REAL ESTATE ANALYSIS — PROFESSIONAL MARKETING SERVICE — STRATEGIC INVESTMENT ADVISORY</p></div>
    """, unsafe_allow_html=True)

# --- FUNGSI FORMAT RUPIAH ---
def format_rp(angka):
    return f"Rp {angka:,.0f}".replace(",", ".")

# --- SISTEM LOGIN ---
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

if not st.session_state['auth']:
    st.title("🔒 Private Wealth Access")
    st.markdown("Please authenticate to access the Property Intelligent System.")
    password = st.text_input("Access Key", type="password")
    if st.button("Unlock System"):
        if password == "Property2025":
            st.session_state['auth'] = True
            st.rerun()
        else:
            st.error("Access Denied: Invalid Key")
    st.stop()

# --- HEADER APLIKASI ---
st.title("Real Estate Investment Simulator 🏛️")
st.markdown("---")

# --- INPUT GLOBAL (MANUAL) ---
col_global1, col_global2 = st.columns(2)

with col_global1:
    # User Input Harga Cash Keras (Baseline)
    harga_base = st.number_input("Input Harga Cash Keras (Inc. PPN 11%)", 
                                min_value=0, value=2500000000, step=10000000, format="%d")
    
    harga_excl = harga_base / 1.11
    st.write(f"Harga Exclude PPN 11%: **{format_rp(harga_excl)}**")

with col_global2:
    # User Input UTJ
    utj = st.number_input("Uang Tanda Jadi / UTJ (Rp 1 Juta - 50 Juta)", 
                          min_value=1000000, max_value=50000000, value=25000000, step=1000000)
    st.info("UTJ telah termasuk dalam total harga.")

st.markdown("---")

# --- TAB MENU ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap (Dynamic Pricing)", "🏠 Simulasi KPR"])

# --- TAB 1: CASH BERTAHAP (LOGIKA NPV/FV) ---
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        tenor_cash = st.slider("Tenor Cicilan (Bulan)", 1, 180, 36)
        list_disc = [9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5]
        disc_rate_val = st.selectbox("Discount Rate / Cost of Fund (%)", list_disc, index=1) / 100
    
    # LOGIKA: Harga Naik jika Tenor diperpanjang (Future Value)
    rate_m = disc_rate_val / 12
    if tenor_cash > 1:
        # Menyesuaikan harga berdasarkan tenor agar NPV tetap setara cash keras
        harga_jual_baru = npf.fv(rate_m, tenor_cash, 0, -harga_base)
    else:
        harga_jual_baru = harga_base

    sisa_cash = harga_jual_baru - utj
    cicilan_cash = sisa_cash / tenor_cash
    
    with c2:
        st.metric("Harga Jual (Adjusted by Tenor)", format_rp(harga_jual_baru))
        st.metric("Cicilan Flat per Bulan", format_rp(cicilan_cash))
        st.caption(f"Penyesuaian harga didasarkan pada Time Value of Money ({disc_rate_val*100}% p.a)")

# --- TAB 2: SIMULASI KPR ---
with tab2:
    k1, k2, k3 = st.columns(3)
    with k1:
        dp_percent = st.slider("Persentase DP (%)", 5, 50, 20)
        dp_cicil = st.number_input("Cicil DP (Kali)", 1, 12, 1)
    with k2:
        # Suku bunga detail (loncatan 0.25%)
        bunga_list = [round(x * 0.25, 2) for x in range(4, 57)]
        bunga_kpr = st.selectbox("Suku Bunga KPR (%)", bunga_list, index=16) / 100
        tenor_kpr = st.number_input("Tenor KPR (Tahun)", 1, 30, 15)
    with k3:
        akad_rate = st.selectbox("Biaya Akad (% dari Plafon)", list(range(1, 7)), index=2) / 100

    # Logika KPR: Semakin lama cicil DP, harga sedikit disesuaikan
    harga_kpr_adj = harga_base * (1 + (0.003 * (dp_cicil - 1)))
    
    total_dp_rp = harga_kpr_adj * (dp_percent / 100)
    plafon = harga_kpr_adj - total_dp_rp
    
    # Amortisasi
    m_rate = bunga_kpr / 12
    m_tenor = tenor_kpr * 12
    angsuran = npf.pmt(m_rate, m_tenor, -plafon)
    biaya_akad = plafon * akad_rate

    st.markdown("### KPR Executive Summary")
    sk1, sk2, sk3 = st.columns(3)
    sk1.metric("Plafon Pinjaman Bank", format_rp(plafon))
    sk2.metric("Angsuran per Bulan", format_rp(angsuran))
    sk3.metric("Estimasi Biaya Akad", format_rp(biaya_akad))
    
    st.write(f"Total DP: **{format_rp(total_dp_rp)}**")
    st.write(f"Sisa DP (Setelah UTJ): **{format_rp(total_dp_rp - utj)}**")
    if dp_cicil > 1:
        st.write(f"Cicilan DP: **{format_rp((total_dp_rp - utj) / dp_cicil)}** selama {dp_cicil} bulan.")

st.markdown("---")
st.caption("© 2018-2026 RUANG MASBAY PROPERTY INTELLIGENT. All calculations are simulations for professional advisory use.")
