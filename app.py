import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. SAYFA ARAYÜZ AYARLARI VE AGRESİF CSS ENJEKSİYONU (Kusursuz Jilet UI)
st.set_page_config(page_title="Taha Uyanık | Green Alpha", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Karanlık Tema ve Ana Arka Plan */
.stApp {
    background-color: #0E1117 !important;
}

/* Üstteki Streamlit Menü Çubuğunu ve Footer'ı Gizle */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Arka Planı ve Çizgisi */
[data-testid="stSidebar"] {
    background-color: #12151B !important;
    border-right: 1px solid #2D323C !important;
}

/* ---------------------------------------------------
   KUSURSUZ SELECTBOX (BEYAZ KUTU İMHASI)
--------------------------------------------------- */
div[data-baseweb="select"] {
    background-color: #161A22 !important;
}
div[data-baseweb="select"] > div {
    background-color: #161A22 !important;
    color: #F5F5F5 !important;
    border: 1px solid #DEFF9A !important; 
    border-radius: 8px !important;
}
div[data-baseweb="select"] svg {
    color: #DEFF9A !important; 
}
div[role="listbox"], ul[role="listbox"] {
    background-color: #161A22 !important;
    border: 1px solid #2D323C !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] {
    background-color: #161A22 !important;
}
li[role="option"] {
    color: #F5F5F5 !important;
    background-color: #161A22 !important;
}
li[role="option"]:hover {
    background-color: #2D323C !important;
    color: #DEFF9A !important;
}

/* ---------------------------------------------------
   METRİK KUTULARI (3D KART ETKİSİ)
--------------------------------------------------- */
div[data-testid="metric-container"] {
    background-color: #161A22 !important;
    border: 1px solid #DEFF9A !important; 
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 10px rgba(222, 255, 154, 0.05) !important;
    transition: all 0.3s ease-in-out !important;
}

div[data-testid="metric-container"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 8px 20px rgba(222, 255, 154, 0.2) !important;
    border: 1px solid #A3FF00 !important;
}

/* Rakamların Rengi (Neon Yeşil Vurgu) */
[data-testid="stMetricValue"] {
    color: #DEFF9A !important; 
    font-weight: 800 !important;
}

/* Delta (Artış/Azalış) Renkleri */
[data-testid="stMetricDelta"] svg {
    fill: #A3FF00 !important; 
}

/* Yazı Başlıkları ve Etiketleri */
h1, h2, h3, p, label {
    color: #F5F5F5 !important;
}
</style>
""", unsafe_allow_html=True)

# 2. ZAMAN MAKİNESİ (Sidebar Paneli)
st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

st.title("🌍 Taha Uyanık | Green Alpha Quant Fund")
st.markdown("BIST100 vs. Katılım Endeksli Yeşil Enerji Algoritması (Volatilite ve Alfa Analizi)")

# GERÇEK MERMİLER
hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    # Veri Çekme ve Zırhlı NaN Tamiri
    veri = yf.download(hisseler, period=periyot)['Close']
    
    if veri.empty:
        st.error("Yahoo Finance'tan şu an veri çekilemiyor (Piyasa verisi boş). Lütfen farklı bir aralık seçin.")
        st.stop()
        
    veri = veri.ffill().bfill() # Hem ileri hem geri doldur, boşluk bırakma!
    
    normalize_veri = (veri / veri.iloc[0]) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    # 3. GRAFİK ÇİZİMİ
    st.subheader(f"📊 Algoritmik Kıyaslama ({periyot})")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=normalize_veri.index, 
        y=normalize_veri['TAHA_YESIL_FON'],
        mode='lines',
        name='Taha Yeşil Fon',
        line=dict(color='#DEFF9A', width=3),
        hovertemplate="<b>Taha Yeşil Fon:</b> %{y:.2f}<extra></extra>"
    ))

    # BIST100 Çizgisi (Canlı Buz Mavisi/Gümüş)
    fig.add_trace(go.Scatter(
        x=normalize_veri.index, 
        y=normalize_veri['XU100.IS'],
        mode='lines',
        name='BIST100',
        line=dict(color='#B0C4DE', width=2.5), 
        hovertemplate="<b>BIST100:</b> %{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor='rgba(0,0,0,0)', 
        font=dict(color='#F5F5F5'),
        xaxis=dict(showgrid=True, gridcolor='#2D323C', tickangle=-45, rangeslider=dict(visible=False)),
        yaxis=dict(showgrid=True, gridcolor='#2D323C'),
        legend=dict(bgcolor='rgba(22, 26, 34, 0.9)', bordercolor='#DEFF9A', borderwidth=1, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0),
        hovermode='x unified',
        hoverlabel=dict(bgcolor="#161A22", font_size=14, font_family="Arial", font_color="#F5F5F5", bordercolor="#DEFF9A")
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Finansal Vurgun (Backtest)
    st.subheader("💰 100.000 TL Simülasyon Sonuçları")
    bist_sonuc = 100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100)
    yesil_sonuc = 100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100)
    fark = yesil_sonuc - bist_sonuc

    col1, col2, col3 = st.columns(3)
    col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} TL")
    col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} TL", delta=f"{((yesil_sonuc-100000)/100000)*100:.1f}% Fon Büyümesi")
    col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} TL", delta="Piyasayı Yendi" if fark > 0 else "- Piyasaya Yenildi")

    # AĞIR SIKLET RİSK METRİKLERİ
    st.subheader("⚖️ Kantitatif Risk Analizi")
    getiriler = veri.pct_change().dropna()
    
    if len(getiriler) > 0:
        portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

        bist_vol = getiriler['XU100.IS'].std() * (252 ** 0.5) * 100
        fon_vol = portfoy_getiri.std() * (252 ** 0.5) * 100

        fon_kumulatif = (1 + portfoy_getiri).cumprod()
        fon_zirve = fon_kumulatif.cummax()
        fon_dd = ((fon_kumulatif - fon_zirve) / fon_zirve).min() * 100

        r_col1, r_col2, r_col3 = st.columns(3)
        r_col1.metric("BIST100 Yıllık Volatilite", f"%{bist_vol:.2f}", delta="Risk Endeksi", delta_color="off")
        r_col2.metric("Taha Yeşil Fon Volatilite", f"%{fon_vol:.2f}", delta="Agresif Büyüme Riski", delta_color="off")
        r_col3.metric("Maksimum Düşüş (Max Drawdown)", f"%{fon_dd:.2f}", delta="Kriz Direnci", delta_color="off")
    else:
        st.warning("Seçilen periyotta risk metriklerini hesaplayacak kadar işlem günü verisi bulunamadı.")

except Exception as e:
    st.error(f"Sistem Kritik Bir Veri Hatasını Engelledi. Hata Kodu: {e}")
    st.info("Yahoo Finance 1 aylık verilerde bazen eksik paket gönderdiği için sistem güvenlik moduna geçti. Lütfen '3mo' veya üzerini seçin.")
