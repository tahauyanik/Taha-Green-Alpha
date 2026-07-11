import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# Sitenin Başlığı ve Arayüzü
st.set_page_config(page_title="Taha Uyanık Green Tech Fund", layout="wide")

# 3. AŞAMA: ZAMAN MAKİNESİ (Sidebar Paneli)
st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y"], index=1)

st.title("🌍 Taha Uyanık | İslami Yeşil Finans Algoritması v1.3")
st.markdown("BIST100 vs. Gerçek Yeşil Enerji/Katılım Hisseleri Volatilite ve Alfa Analizi")

# GERÇEK MERMİLER (Katılım + Yeşil Enerji Filtresi)
hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

# Veri Çekme ve Normalizasyon (Artık DİNAMİK!)
veri = yf.download(hisseler, period=periyot)['Close']
normalize_veri = (veri / veri.iloc[0]) * 100

# Taha Yeşil Fonu Oluşturma
normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

# Grafik Çizimi
st.subheader(f"📊 Algoritmik Kıyaslama ({periyot})")
fig, ax = plt.subplots(figsize=(10,4))
ax.plot(normalize_veri.index, normalize_veri['TAHA_YESIL_FON'], label='Taha Yeşil Fon', linewidth=3)
ax.plot(normalize_veri.index, normalize_veri['XU100.IS'], label='BIST100', linewidth=1.5, alpha=0.7)
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
