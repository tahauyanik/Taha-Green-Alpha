import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Taha Uyanık | Green Alpha", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Karanlık Tema ve Ana Arka Plan */
.stApp { background-color: #0E1117 !important; }

/* Üstteki Streamlit Menü Çubuğunu ve Footer'ı Gizle */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Arka Planı ve Çizgisi */
[data-testid="stSidebar"] {
    background-color: #12151B !important;
    border-right: 1px solid #2D323C !important;
}

/* KUSURSUZ SELECTBOX (BEYAZ KUTU İMHASI) */
div[data-baseweb="select"] { background-color: #161A22 !important; }
div[data-baseweb="select"] > div {
    background-color: #161A22 !important;
    color: #F5F5F5 !important;
    border: 1px solid #DEFF9A !important; 
    border-radius: 8px !important;
}
div[data-baseweb="select"] svg { color: #DEFF9A !important; }
div[role="listbox"], ul[role="listbox"], ul[data-testid="stSelectboxVirtualDropdown"] {
    background-color: #161A22 !important;
    border: 1px solid #2D323C !important;
}
li[role="option"] {
    color: #F5F5F5 !important;
    background-color: #161A22 !important;
}
li[role="option"]:hover {
    background-color: #2D323C !important;
    color: #DEFF9A !important;
}

/* METRİK KUTULARI (3D KART ETKİSİ) */
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
[data-testid="stMetricValue"] { color: #DEFF9A !important; font-weight: 800 !important; }

/* Delta (Artış/Azalış) Renkleri */
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }

/* Yazı Başlıkları ve Etiketleri */
h1, h2, h3, p, label { color: #F5F5F5 !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

st.title("🌍 Taha Uyanık | Green Alpha Quant Fund")
st.markdown("BIST100 vs. Katılım Endeksli Yeşil Enerji Algoritması (Volatilite ve Alfa Analizi)")

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

def safe_float(val):
    """Zehirli verileri (NaN/Inf) UI'a gitmeden temizler ve çöküşü (Oh no) engeller."""
    try:
        v = float(val)
        if np.isnan(v) or np.isinf(v): return 0.0
        return v
    except:
        return 0.0

# BUM! SİNSİ DÜŞMAN YOK EDİLDİ: @st.cache_data (Önbellek) TAMAMEN SİLİNDİ!
# Streamlit 1 aylık veriyi hafızaya alırken kendi kendini patlatıyordu, bu zaafiyeti kaldırdık.
def veri_indir(hisseler, periyot):
    df = yf.download(hisseler, period=periyot, interval="1d", progress=False, threads=False)
    
    # Yfinance kütüphanesinin yeni versiyonlarındaki sütun hatasına karşı zırh
    if isinstance(df.columns, pd.MultiIndex):
        df = df['Close']
    elif 'Close' in df.columns:
        df = df['Close']
        
    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)
    return df

try:
    with st.spinner('Kuantum algoritmaları piyasa verilerini tarıyor...'):
        veri = veri_indir(hisseler, periyot)
    
    if veri.empty or len(veri) < 2:
        st.error("Şu an piyasadan yeterli veri akışı sağlanamıyor. Lütfen farklı bir zaman aralığı seçin.")
        st.stop()
        
    veri = veri.ffill().bfill() 
    
    ilk_degerler = veri.iloc[0].copy()
    ilk_degerler[ilk_degerler == 0] = 0.0001 
    
    normalize_veri = (veri / ilk_degerler) * 100
    normalize_veri = normalize_veri.replace([np.inf, -np.inf], np.nan).ffill().fillna(100)
    
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    st.subheader(f"📊 Algoritmik Kıyaslama ({periyot})")

    guvenli_tarihler = normalize_veri.index.strftime('%Y-%m-%d').tolist()
    y_yesil = normalize_veri['TAHA_YESIL_FON'].apply(safe_float).tolist()
    y_bist = normalize_veri['XU100.IS'].apply(safe_float).tolist()

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=guvenli_tarihler, y=y_yesil, mode='lines',
        name='Taha Yeşil Fon', line=dict(color='#DEFF9A', width=3),
        hovertemplate="<b>Taha Yeşil Fon:</b> %{y:.2f}<extra></extra>"
    ))
    fig.add_trace(go.Scatter(
        x=guvenli_tarihler, y=y_bist, mode='lines',
        name='BIST100', line=dict(color='#B0C4DE', width=2.5), 
        hovertemplate="<b>BIST100:</b> %{y:.2f}<extra></extra>"
    ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
        xaxis=dict(showgrid=True, gridcolor='#2D323C', tickangle=-45, rangeslider=dict(visible=False)),
        yaxis=dict(showgrid=True, gridcolor='#2D323C'),
        legend=dict(bgcolor='rgba(22, 26, 34, 0.9)', bordercolor='#DEFF9A', borderwidth=1, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=50, b=0), hovermode='x unified',
        hoverlabel=dict(bgcolor="#161A22", font_size=14, font_family="Arial", font_color="#F5F5F5", bordercolor="#DEFF9A")
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.subheader("💰 100.000 TL Simülasyon Sonuçları")
    
    bist_sonuc = safe_float(100000 * (y_bist[-1] / 100))
    yesil_sonuc = safe_float(100000 * (y_yesil[-1] / 100))
    fark = yesil_sonuc - bist_sonuc
    
    fon_buyumesi = safe_float(((yesil_sonuc - 100000) / 100000) * 100)

    col1, col2, col3 = st.columns(3)
    col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} TL")
    col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} TL", delta=f"{fon_buyumesi:.1f}% Fon Büyümesi")
    col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} TL", delta="Piyasayı Yendi" if fark > 0 else "- Piyasaya Yenildi")

    st.subheader("⚖️ Kantitatif Risk Analizi")
    getiriler = veri.pct_change().dropna()
    
    if len(getiriler) > 2:
        portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)
        
        islem_gunu = len(getiriler)
        yillik_carpan = 252 if islem_gunu > 21 else islem_gunu
        
        bist_vol = safe_float(getiriler['XU100.IS'].std() * (yillik_carpan ** 0.5) * 100)
        fon_vol = safe_float(portfoy_getiri.std() * (yillik_carpan ** 0.5) * 100)

        fon_kumulatif = (1 + portfoy_getiri).cumprod()
        fon_zirve = fon_kumulatif.cummax()
        fon_dd = safe_float(((fon_kumulatif - fon_zirve) / fon_zirve).min() * 100)

        r_col1, r_col2, r_col3 = st.columns(3)
        r_col1.metric("BIST100 Volatilite", f"%{bist_vol:.2f}", delta="Risk Endeksi", delta_color="off")
        r_col2.metric("Taha Yeşil Fon Volatilite", f"%{fon_vol:.2f}", delta="Agresif Büyüme Riski", delta_color="off")
        r_col3.metric("Maksimum Düşüş (Max Drawdown)", f"%{fon_dd:.2f}", delta="Kriz Direnci", delta_color="off")
    else:
        st.warning("Seçilen periyotta risk metriklerini hesaplayacak kadar işlem günü verisi yok.")

except Exception as e:
    st.error("Kritik Sunucu Hatası Engellendi. Yahoo Finance bağlantısı geçici olarak kurulamadı.")
