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

/* Üstteki Streamlit Menü Çubuğunu ve Footer'ı Gizle (Amatör İzleri Silme) */
#MainMenu {visibility: hidden;}
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

# Matplotlib için Karanlık Tema ve Şeffaf Arka Plan Ayarları
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10,4))
fig.patch.set_facecolor('#0E1117')  # Streamlit arka planı ile aynı renk
ax.set_facecolor('#0E1117')

ax.plot(normalize_veri.index, normalize_veri['TAHA_YESIL_FON'], label='Taha Yeşil Fon', color='#DEFF9A', linewidth=3)
ax.plot(normalize_veri.index, normalize_veri['XU100.IS'], label='BIST100', color='#FFFFFF', linewidth=1.5, alpha=0.5)

ax.legend(facecolor='#161A22', edgecolor='#DEFF9A')
ax.grid(color='#2D323C', linestyle='--', linewidth=0.5)
plt.xticks(rotation=45)

st.pyplot(fig)

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
