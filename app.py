import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 1. SAYFA ARAYÜZ AYARLARI VE CSS ENJEKSİYONU (Jilet Gibi UI)
st.set_page_config(page_title="Taha Uyanık Green Tech Fund", layout="wide")

st.markdown("""
<style>
/* Karanlık Tema ve Ana Arka Plan */
.stApp {
    background-color: #0E1117;
}

/* Üstteki Streamlit Menü Çubuğunu ve Footer'ı Gizle */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Arka Planı ve Seçim Kutusu Düzeltmesi */
[data-testid="stSidebar"] {
    background-color: #161A22;
    border-right: 1px solid #2D323C;
}

/* Sidebar İçindeki Selectbox'ı Koyu Yapma (Beyaz Kutu Sorununu Çözer) */
div[data-baseweb="select"] > div {
    background-color: #1E232E !important;
    color: #F5F5F5 !important;
    border: 1px solid #2D323C !important;
}
div[data-baseweb="select"] * {
    color: #F5F5F5 !important;
}
div[data-baseweb="popover"] ul {
    background-color: #1E232E !important;
}
div[data-baseweb="popover"] li {
    color: #F5F5F5 !important;
}

/* Metrik Kutuları (Card Design ve 3D Etki) - EKSİK KUTU GÖRÜNÜMÜNÜ ZORLAMA */
div[data-testid="metric-container"] {
    background-color: #161A22 !important;
    border: 1px solid #DEFF9A !important; /* Neon Yeşil Çerçeve */
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 10px rgba(222, 255, 154, 0.05) !important;
    transition: transform 0.2s ease-in-out !important;
}

/* Metrik Kutularının Üzerine Gelince Zıplama Efekti */
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 6px 15px rgba(222, 255, 154, 0.15) !important;
}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Arka Planı */
[data-testid="stSidebar"] {
    background-color: #161A22;
    border-right: 1px solid #2D323C;
}

/* Metrik Kutuları (Card Design ve 3D Etki) */
div[data-testid="metric-container"] {
    background-color: #161A22;
    border: 1px solid #DEFF9A; /* Neon Yeşil Çerçeve */
    padding: 15px 20px;
    border-radius: 12px;
    box-shadow: 0 4px 10px rgba(222, 255, 154, 0.05);
    transition: transform 0.2s ease-in-out;
}

/* Metrik Kutularının Üzerine Gelince Zıplama Efekti */
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 15px rgba(222, 255, 154, 0.15);
}

/* Rakamların Rengi (Neon Yeşil Vurgu) */
[data-testid="stMetricValue"] {
    color: #DEFF9A !important; 
    font-weight: 800 !important;
}

/* Delta (Artış/Azalış) Renkleri */
[data-testid="stMetricDelta"] {
    color: #A3FF00 !important;
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
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y"], index=1)

st.title("🌍 Taha Uyanık | İslami Yeşil Finans Algoritması v2.0")
st.markdown("BIST100 vs. Gerçek Yeşil Enerji/Katılım Hisseleri Volatilite ve Alfa Analizi")

# GERÇEK MERMİLER (Katılım + Yeşil Enerji Filtresi)
hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

# Veri Çekme ve Normalizasyon
veri = yf.download(hisseler, period=periyot)['Close']
normalize_veri = (veri / veri.iloc[0]) * 100

# Taha Yeşil Fonu Oluşturma
normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

# 3. GRAFİK ÇİZİMİ (Estetik Güncelleme - Karanlık Tema)
st.subheader(f"📊 Algoritmik Kıyaslama ({periyot})")

import plotly.graph_objects as go

# Grafik Nesnesini Oluşturma (Karanlık Tema ve Neon Renkler)
fig = go.Figure()

# Taha Yeşil Fon Çizgisi
fig.add_trace(go.Scatter(
    x=normalize_veri.index, 
    y=normalize_veri['TAHA_YESIL_FON'],
    mode='lines',
    name='Taha Yeşil Fon',
    line=dict(color='#DEFF9A', width=3)
))

# BIST100 Çizgisi
fig.add_trace(go.Scatter(
    x=normalize_veri.index, 
    y=normalize_veri['XU100.IS'],
    mode='lines',
    name='BIST100',
    line=dict(color='#8892B0', width=2) # Beyaz yerine okunaklı koyu gri/mavi
))

# Grafiğin Genel Temasını ve Arka Planını Ayarlama
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)', # İç grafik arka planı şeffaf
    paper_bgcolor='rgba(0,0,0,0)', # Dış çerçeve arka planı şeffaf
    font=dict(color='#F5F5F5'),
    xaxis=dict(
        showgrid=True, 
        gridcolor='#2D323C', 
        tickangle=-45,
        rangeslider=dict(visible=False) # Alt kısımdaki gereksiz kaydırıcıyı kapatır
    ),
    yaxis=dict(
        showgrid=True, 
        gridcolor='#2D323C'
    ),
    legend=dict(
        bgcolor='rgba(22, 26, 34, 0.8)',
        bordercolor='#DEFF9A',
        borderwidth=1
    ),
    margin=dict(l=0, r=0, t=30, b=0),
    hovermode='x unified' # Mouse ile üzerine gelince her iki değeri aynı anda gösterir
)

# Plotly Grafiğini Ekrana Basma
st.plotly_chart(fig, use_container_width=True)

# Finansal Vurgun (Backtest)
st.subheader("💰 100.000 TL Simülasyon Sonuçları")
bist_sonuc = 100000 * (normalize_veri['XU100.IS'].dropna().iloc[-1] / 100)
yesil_sonuc = 100000 * (normalize_veri['TAHA_YESIL_FON'].dropna().iloc[-1] / 100)
fark = yesil_sonuc - bist_sonuc

col1, col2, col3 = st.columns(3)
col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} TL")
col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} TL")
col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} TL", "Piyasayı Yendi" if fark > 0 else "Piyasaya Yenildi")

# AĞIR SIKLET RİSK METRİKLERİ
st.subheader("⚖️ Kantitatif Risk Analizi")
getiriler = veri.pct_change().dropna()
portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

# Volatilite Hesaplama
bist_vol = getiriler['XU100.IS'].std() * (252 ** 0.5) * 100
fon_vol = portfoy_getiri.std() * (252 ** 0.5) * 100

# Max Drawdown Hesaplama
fon_kumulatif = (1 + portfoy_getiri).cumprod()
fon_zirve = fon_kumulatif.cummax()
fon_dd = ((fon_kumulatif - fon_zirve) / fon_zirve).min() * 100

r_col1, r_col2, r_col3 = st.columns(3)
r_col1.metric("BIST100 Yıllık Volatilite", f"%{bist_vol:.2f}")
r_col2.metric("Taha Yeşil Fon Volatilite", f"%{fon_vol:.2f}")
r_col3.metric("Maksimum Düşüş (Max Drawdown)", f"%{fon_dd:.2f}")
