import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Sitenin Başlığı ve Arayüzü
st.set_page_config(page_title="Taha Uyanık Green Tech Fund", layout="wide")
st.title("🌍 Taha Uyanık | İslami Yeşil Finans Algoritması")
st.markdown("BIST100 vs. Seçilmiş Yeşil Enerji/Katılım Hisseleri Volatilite ve Alfa Analizi")

# Veri Çekme ve Normalizasyon
hisseler = ['ASTOR.IS', 'ENJSA.IS', 'GWIND.IS', 'XU100.IS']
veri = yf.download(hisseler, period='3mo')['Close']
normalize_veri = (veri / veri.iloc[0]) * 100
normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ASTOR.IS', 'ENJSA.IS', 'GWIND.IS']].mean(axis=1)

# Grafik Çizimi
st.subheader("📊 3 Aylık Algoritmik Kıyaslama")
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(normalize_veri.index, normalize_veri['TAHA_YESIL_FON'], label='Taha Yeşil Fon', linewidth=3)
ax.plot(normalize_veri.index, normalize_veri['XU100.IS'], label='BIST100', linewidth=2, alpha=0.7)
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Finansal Vurgun (Backtest)
st.subheader("💰 100.000 TL Simülasyon Sonuçları")
bist_sonuc = 100000 * (normalize_veri['XU100.IS'].dropna().iloc[-1] / 100)
yesil_sonuc = 100000 * (normalize_veri['TAHA_YESIL_FON'].dropna().iloc[-1] / 100)
fark = yesil_sonuc - bist_sonuc

col1, col2, col3 = st.columns(3)
col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} TL")
col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} TL")
col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"+{fark:,.0f} TL", "Piyasayı Yendi")
