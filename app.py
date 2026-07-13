import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime

st.set_page_config(page_title="Taha Uyanık | Sovereign Quant", page_icon="🌍", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Ana Arka Plan ve Dünyaca Ünlü 'Inter' Font Ailesi */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp { background: linear-gradient(180deg, #090B10 0%, #12151B 100%) !important; }

/* Menüleri ve Çöpleri Gizle */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar - Karanlık ve Seçkin */
[data-testid="stSidebar"] {
    background-color: #0E1117 !important;
    border-right: 1px solid #1E2532 !important;
}

/* KUSURSUZ SEKMELER (TABS) - Sarı/Yeşil Kutu İmhasi! */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background-color: transparent !important;
    padding-bottom: 5px;
    border-bottom: 1px solid #1E2532 !important;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: transparent !important;
    border-radius: 0px !important;
    padding: 10px 20px;
    color: #8B949E !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    color: #DEFF9A !important;
    background-color: transparent !important; /* İğrenç arka planı sildik */
    border-bottom: 3px solid #DEFF9A !important; /* Sadece alt çizgi neon */
    box-shadow: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #FFFFFF !important;
    background-color: rgba(222, 255, 154, 0.05) !important;
}

/* Metrik Kartları - Ultra Premium Glassmorphism */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg, #161A22 0%, #0F131A 100%) !important;
    border: 1px solid rgba(222, 255, 154, 0.1) !important;
    padding: 24px !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-5px) !important;
    border: 1px solid #DEFF9A !important;
    box-shadow: 0 15px 35px -5px rgba(222,255,154,0.15) !important;
}

/* Metrik İçerik Tasarımı */
[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-weight: 800 !important; font-size: 32px !important; letter-spacing: -0.5px;}
[data-testid="stMetricLabel"] > div > div > p { color: #8B949E !important; font-weight: 600 !important; font-size: 14px !important; text-transform: uppercase; letter-spacing: 1px;}
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }
[data-testid="stMetricDelta"] > div { color: #A3FF00 !important; font-weight: 700 !important; font-size: 14px !important; }

/* Custom AI Sinyal Kartları */
.ai-signal-card {
    background: #121721; border-left: 4px solid #DEFF9A; padding: 20px; border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.4); margin-bottom: 20px; border: 1px solid #1E2532;
}
.ai-title { color: #FFFFFF; font-size: 18px; font-weight: 800; margin-bottom: 10px; }
.ai-desc { color: #A0ABC0; font-size: 14px; line-height: 1.6; }

h1, h2, h3, p, label { color: #F5F5F5 !important; }
div[data-baseweb="slider"] div { background-color: #DEFF9A !important; }
div[data-baseweb="select"] > div { background-color: #12151B !important; color: #F5F5F5 !important; border: 1px solid #2D323C !important; border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)

def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data, slow=26, fast=12, signal=9):
    exp1 = data.ewm(span=fast, adjust=False).mean()
    exp2 = data.ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    histogram = macd - signal_line
    return macd, signal_line, histogram

@st.cache_data(ttl=3600)
def load_market_data(tickers, period):
    data = yf.download(tickers, period=period, progress=False, threads=True)
    return data['Close'], data['Volume'], data['High'], data['Low'], data['Open']

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
st.sidebar.title("Sovereign Terminal")
st.sidebar.markdown("---")

st.sidebar.markdown("### ⚙️ Zaman Makinesi")
periyot = st.sidebar.selectbox("Analiz Periyodu", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

st.sidebar.markdown("### 🧠 Algoritmik Zırh")
# Bug'ı çözülen SMA Toggle mekanizması
trend_goster = st.sidebar.toggle("Dinamik SMA Kalkanı", value=True)

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade (Hızlı Trend)", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade (Ana Trend)", 10, 250, 50)

st.title("🌍 Taha Uyanık | Ultra Premium Quant Fund")
st.markdown("Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V11.0)")

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = load_market_data(hisseler, periyot)
    
    if close_data.empty:
        st.error("Veri bağlantısı koptu. Lütfen tekrar deneyin.")
        st.stop()
        
    close_data = close_data.ffill().bfill()
    
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Algoritmik Terminal", 
        "🔬 Röntgen (Derin Analiz)", 
        "🧠 AI İstihbarat Sinyalleri", 
        "🧩 Kuantum Risk & Monte Carlo"
    ])

    with tab1:
        st.markdown("### 📊 Fon Performans Kıyaslaması")

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['TAHA_YESIL_FON'], mode='lines', name='Taha Yeşil Fon', line=dict(color='#DEFF9A', width=3.5)))
        fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['XU100.IS'], mode='lines', name='BIST100 Endeksi', line=dict(color='#3B82F6', width=2)))

        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa}', line=dict(color='#F59E0B', width=1.5, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun}', line=dict(color='#FF4C4C', width=1.5, dash='dot')))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0ABC0'),
            xaxis=dict(showgrid=True, gridcolor='#1E2532', tickangle=-45), yaxis=dict(showgrid=True, gridcolor='#1E2532'),
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5, font=dict(color='#FFFFFF')),
            margin=dict(l=0, r=0, t=10, b=0), hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        st.markdown("<br>### 💰 100.000 TL Sermaye Simülasyonu", unsafe_allow_html=True)
        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        col1, col2, col3 = st.columns(3)
        col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} ₺", delta="Referans Endeks", delta_color="off")
        col2.metric("Sovereign Fon Getirisi", f"{yesil_sonuc:,.0f} ₺", delta=f"{((yesil_sonuc-100000)/100000)*100:.1f}% Büyüme")
        col3.metric("Yaratılan ALFA (Kâr Farkı)", f"{fark:+,.0f} ₺", delta="Piyasayı Yendi" if fark > 0 else "- Piyasaya Yenildi")

    with tab2:
        st.markdown("### 🔬 Teknik Analiz ve İndikatör Röntgeni")
        secili_hisse = st.selectbox("İncelenecek Hisseyi Seçin", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'])
        
        if secili_hisse:
            h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
            h_rsi = calculate_rsi(h_close)
            h_macd, h_signal, h_hist = calculate_macd(h_close)
            
            fig_tech = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.5, 0.15, 0.15, 0.2], subplot_titles=(f"{secili_hisse} Fiyat Hareketi", "İşlem Hacmi", "RSI (Göreceli Güç)", "MACD"))
            fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C'), row=1, col=1)
            fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]), row=2, col=1)
            fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=2)), row=3, col=1)
            fig_tech.add_hline(y=70, line_dash="dot", line_color="red", row=3, col=1)
            fig_tech.add_hline(y=30, line_dash="dot", line_color="green", row=3, col=1)
            fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A')), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C')), row=4, col=1)
            fig_tech.add_trace(go.Bar(x=h_hist.index, y=h_hist, marker_color=['#DEFF9A' if val >= 0 else '#FF4C4C' for val in h_hist]), row=4, col=1)
            
            fig_tech.update_layout(height=800, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0ABC0'), showlegend=False, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=30, b=0))
            fig_tech.update_xaxes(showgrid=True, gridcolor='#1E2532')
            fig_tech.update_yaxes(showgrid=True, gridcolor='#1E2532')
            st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("### 🕵️‍♂️ NLP Haber Okuyucusu ve Karar Motoru")
        col_ai1, col_ai2 = st.columns([2, 1])
        with col_ai1:
            st.markdown("#### Sektörel Makro Tarama")
            st.markdown(f"""
            <div class="ai-signal-card" style="border-left-color: #3B82F6;">
                <div class="ai-title">Yeşil Enerji Regülasyonları Bekleniyor</div>
                <div class="ai-desc">Kaynak: Sovereign Makro AI | Analiz: <span style="color:#3B82F6; font-size:12px; border: 1px solid #3B82F6; padding: 4px 10px; border-radius: 12px;">🔵 BEKLEMEDE (PENDING)</span></div>
                <p style="color:#8B949E; font-size:13px; margin-top:10px;">Yapay zeka motorumuz spesifik hisse haberi bulamadığında otomatik olarak sektörel makro görünüme odaklanır.</p>
            </div>
            """, unsafe_allow_html=True)

        with col_ai2:
            st.markdown("#### 🤖 Algoritmik Taktik")
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#A3FF00", "Pozisyonu Koru"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla"
            else:
                durum, renk, taktik = "BEKLEMEDE", "#8B949E", "Trend Kalkanını Açın"

            st.markdown(f"""
            <div style="background: linear-gradient(145deg, #161A22 0%, #0F131A 100%); padding: 30px; border-radius: 16px; border: 1px solid {renk}; text-align: center;">
                <p style="color: #A0ABC0; font-size: 12px; letter-spacing: 2px;">SİSTEM DURUMU</p>
                <h2 style="color: {renk}; font-size: 26px; margin: 15px 0; font-weight: 800;">{durum}</h2>
                <hr style="border-color: #1E2532;">
                <b style="color: #F5F5F5; font-size: 18px;">Tavsiye: {taktik}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("### ⚖️ Kantitatif Risk & Monte Carlo")
        getiriler = close_data.pct_change().dropna()
        if len(getiriler) > 0:
            portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)
            fon_vol = float(np.nan_to_num(portfoy_getiri.std() * (252 ** 0.5) * 100))
            var_95 = np.percentile(portfoy_getiri, 5) * 100 
            
            fon_kumulatif = (1 + portfoy_getiri).cumprod()
            fon_zirve = fon_kumulatif.cummax()
            drawdown_serisi = ((fon_kumulatif - fon_zirve) / fon_zirve) * 100
            fon_dd = float(np.nan_to_num(drawdown_serisi.min()))

            r_col1, r_col2, r_col3 = st.columns(3)
            r_col1.metric("Fon Yıllık Volatilite", f"%{fon_vol:.2f}", delta="Dalgalanma Boyutu", delta_color="off")
            r_col2.metric("Maksimum Düşüş (Drawdown)", f"%{fon_dd:.2f}", delta="Kriz Direnci", delta_color="off")
            r_col3.metric("Günlük VaR (%95 Güven)", f"%{var_95:.2f}", delta="Beklenen Maks Kayıp", delta_color="off")
            
            st.markdown("---")
            kor_col1, kor_col2 = st.columns([1, 1])
            with kor_col1:
                st.markdown("**🧩 Fon Korelasyon Matrisi**")
                hisse_getirileri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']]
                kor_matrisi = hisse_getirileri.corr().values
                fig_corr = go.Figure(data=go.Heatmap(z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], colorscale=[[0, '#090B10'], [0.5, '#192C3D'], [1, '#DEFF9A']], text=np.round(kor_matrisi, 2), texttemplate="%{text}", textfont={"color": "white", "size": 14}, showscale=False))
                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=20, r=20), xaxis_showgrid=False, yaxis_showgrid=False, yaxis_autorange='reversed')
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("**🌊 Kriz Direnci (Drawdown)**")
                fig_dd = go.Figure(go.Scatter(x=drawdown_serisi.index.strftime('%Y-%m-%d'), y=drawdown_serisi, fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.1)'))
                fig_dd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=20, b=20, l=20, r=20), xaxis=dict(showgrid=True, gridcolor='#1E2532'), yaxis=dict(showgrid=True, gridcolor='#1E2532'))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

            st.markdown("---")
            st.markdown("### 🔮 Monte Carlo Simülasyonu (1 Yıllık)")
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            for i in range(100): fig_mc.add_trace(go.Scatter(y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.03)', width=1), showlegend=False, hoverinfo='skip'))
            fig_mc.add_trace(go.Scatter(y=sim_df.mean(axis=1), mode='lines', name='Beklenen Ortalama', line=dict(color='#3B82F6', width=3, dash='dash')))
            
            fig_mc.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#A0ABC0'), xaxis=dict(showgrid=True, gridcolor='#1E2532'), yaxis=dict(showgrid=True, gridcolor='#1E2532'), margin=dict(t=20, b=20, l=0, r=0), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
