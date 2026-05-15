import streamlit as st
import pandas as pd
import numpy_financial as npf

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="RUANG MASBAY PROPERTY INTELLIGENT", layout="wide")

# --- CUSTOM CSS (GOLDMAN SACHS INSPIRED) ---
st.markdown("""
    <style>
    .main { background-color: #0a192f; color: #ffffff; }
    .stNumberInput input { background-color: #112240 !important; color: white !important; border: 1px solid #d4af37 !important; }
    .stSelectbox div[data-baseweb="select"] { background-color: #112240 !important; }
    .stMetric { background-color: #112240; padding: 15px; border-radius: 10px; border: 1px solid #d4af37; }
    
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

# --- INPUT UTAMA (MANUAL) ---
st.title("Property Intelligent Simulator 🏦")
st.markdown("---")

col_main1, col_main2 = st.columns(2)

with col_main1:
    # User Input Harga Include PPN 11%
    harga_inc_ppn = st.number_input("Input Harga Properti (Include PPN 11%)", 
                                   min_value=0, value=2500000000, step=10000000, format="%d")
    
    # Otomatis Hitung Exclude PPN
    harga_excl_ppn = harga_inc_ppn / 1.11
    st.write(f"Harga Exclude PPN 11%: **{format_rp(harga_excl_ppn)}**")

with col_main2:
    # User Input UTJ 1jt - 50jt
    utj = st.number_input("Uang Tanda Jadi / UTJ (Rp 1 Juta - 50 Juta)", 
                          min_value=1000000, max_value=50000000, value=25000000, step=1000000)
    st.caption("UTJ akan otomatis mengurangi harga/DP.")

st.markdown("---")

# --- TAB MENU ---
tab1, tab2 = st.tabs(["💵 Cash Bertahap", "🏠 Simulasi KPR"])

# --- TAB 1: CASH BERTAHAP ---
with tab1:
    c1, c2 = st.columns(2)
    with c1:
        tenor_cash = st.slider("Tenor Cash Bertahap (Bulan)", 1, 180, 12)
        # Discount Rate dengan pilihan lengkap
        list_disc = [9.0, 9.5, 10.0, 10.5, 11.0, 11.5, 12.0, 12.5]
        disc_rate_val = st.selectbox("Discount Rate / NPV (Annual %)", list_disc) / 100
        
    # Logika Cash Bertahap: Sisa Harga setelah UTJ
    sisa_cash = harga_inc_ppn - utj
    cicilan_cash = sisa_cash / tenor_cash
    
    # Hitung NPV
    # r = discount rate per bulan, n = tenor
    rate_m = disc_rate_val / 12
    # NPV = PV dari cicilan + UTJ (karena UTJ dibayar di awal/bulan 0)
    npv_val = npf.pv(rate_m, tenor_cash, -cicilan_cash) + utj
    
    with c2:
        st.metric("Cicilan per Bulan", format_rp(cicilan_cash))
        st.metric("Net Present Value (NPV)", format_rp(npv_val))
        st.info("NPV menunjukkan nilai investasi saat ini berdasarkan tenor yang dipilih.")

# --- TAB 2: SIMULASI KPR ---
with tab2:
    k1, k2, k3 = st.columns(3)
    with k1:
        dp_percent = st.slider("Persentase DP (%)", 5, 50, 10)
        dp_cicil = st.number_input("Cicil DP (1 - 12 Kali Payment)", 1, 12, 1)
    with k2:
        # Suku Bunga Lebih Detail (1.0% - 13.5%)
        bunga_list = [round(x * 0.25, 2) for x in range(4, 55)] # loncatan 0.25%
        bunga_kpr = st.selectbox("Suku Bunga KPR (%)", bunga_list, index=16) / 100
        tenor_kpr = st.number_input("Tenor KPR (Maks 30 Tahun)", 1, 30, 20)
    with k3:
        # Estimasi Biaya Akad 1-6%
        akad_rate = st.selectbox("Estimasi Biaya Akad (% Plafon)", list(range(1, 7)), index=2) / 100

    # Logika KPR
    # Semakin lama cicil DP, harga disesuaikan sedikit (NPV factor)
    harga_adj = harga_inc_ppn * (1 + (0.003 * (dp_cicil - 1))) 
    
    total_dp_rupiah = harga_adj * (dp_percent / 100)
    sisa_dp_setelah_utj = total_dp_rupiah - utj
    plafon_kpr = harga_adj - total_dp_rupiah
    
    # Amortisasi Bank
    m_rate_kpr = bunga_kpr / 12
    m_tenor_kpr = tenor_kpr * 12
    angsuran_kpr = npf.pmt(m_rate_kpr, m_tenor_kpr, -plafon_kpr)
    total_biaya_akad = plafon_kpr * akad_rate

    st.markdown("### Executive Summary KPR")
    sk1, sk2, sk3 = st.columns(3)
    sk1.metric("Total DP", format_rp(total_dp_rupiah))
    sk2.metric("Plafon Pinjaman", format_rp(plafon_kpr))
    sk3.metric("Angsuran / Bulan", format_rp(angsuran_kpr))
    
    st.write(f"Sisa DP yang harus dibayar (Setelah UTJ): **{format_rp(sisa_dp_setelah_utj)}**")
    if dp_cicil > 1:
        st.write(f"Cicilan DP per bulan: **{format_rp(sisa_dp_setelah_utj / dp_cicil)}** (Selama {dp_cicil}x)")
    st.write(f"Estimasi Biaya Akad KPR: **{format_rp(total_biaya_akad)}**")

st.markdown("---")
st.caption("Aplikasi ini didesain khusus untuk Ruang Masbay Property Intelligent. Perhitungan bersifat simulasi.")
