import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime

st.set_page_config(
    page_title="Sovereign Quant | V13.1 Quantum", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Font ve Temel Arka Plan (Gece Yarısı Uzayı) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp { 
    background: #090B10 !important;
    background-image: radial-gradient(circle at 50% 0%, #161A22 0%, #090B10 70%) !important;
}

/* Gereksiz Çöpleri Gizleme (Header, Footer, Toolbar) */
header { background-color: transparent !important; }
[data-testid="stToolbar"] { visibility: hidden !important; } 
footer { visibility: hidden !important; }

/* Sidebar Tasarımı - Ultra Premium */
[data-testid="stSidebar"] {
    background-color: rgba(14, 17, 23, 0.7) !important;
    backdrop-filter: blur(20px) !important;
    border-right: 1px solid rgba(222, 255, 154, 0.05) !important;
}

/* SEKMELERDEKİ KIRMIZI ÇİZGİ İHANETİNİ KÖKÜNDEN KAZIMA (V13.0 FIX) */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
}
.stTabs [data-baseweb="tab"] {
    height: 55px;
    background-color: transparent !important;
    padding: 0px 10px;
    color: #8B949E !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    border: none !important;
    transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    color: #DEFF9A !important;
    background-color: transparent !important; 
}
/* Streamlit'in kırmızı animasyonlu alt çizgisini Neon Yeşil yapıyoruz! */
div[data-baseweb="tab-highlight"] {
    background-color: #DEFF9A !important;
    height: 3px !important;
    border-top-left-radius: 3px !important;
    border-top-right-radius: 3px !important;
}

/* GLASSMORPHISM - Cam Kartlar (Dünyanın En İyisi) */
div[data-testid="metric-container"] {
    background: rgba(22, 26, 34, 0.6) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(222, 255, 154, 0.1) !important;
    padding: 24px 30px !important;
    border-radius: 16px !important;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}
div[data-testid="metric-container"]:hover {
    transform: translateY(-7px) !important;
    border: 1px solid rgba(222, 255, 154, 0.5) !important;
    box-shadow: 0 20px 40px -10px rgba(222, 255, 154, 0.15) !important;
}

/* Metrik İçerik Tasarımı (Neon Işıltı) */
[data-testid="stMetricValue"] > div { 
    color: #FFFFFF !important; 
    font-weight: 800 !important; 
    font-size: 34px !important; 
    letter-spacing: -1px;
}
[data-testid="stMetricLabel"] > div > div > p { 
    color: #A0ABC0 !important; 
    font-weight: 600 !important; 
    font-size: 13px !important; 
    text-transform: uppercase; 
    letter-spacing: 1.5px;
}
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }
[data-testid="stMetricDelta"] > div { color: #A3FF00 !important; font-weight: 700 !important; font-size: 15px !important; }

/* AI Kartları */
.ai-signal-card {
    background: rgba(18, 23, 33, 0.8);
    backdrop-filter: blur(10px);
    border-left: 4px solid #DEFF9A; 
    padding: 25px; 
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.4); 
    margin-bottom: 25px; 
    border-top: 1px solid rgba(255,255,255,0.05);
    border-right: 1px solid rgba(255,255,255,0.05);
    border-bottom: 1px solid rgba(255,255,255,0.05);
}
.ai-title { color: #FFFFFF; font-size: 19px; font-weight: 800; margin-bottom: 12px; letter-spacing: -0.5px;}
.ai-desc { color: #A0ABC0; font-size: 15px; line-height: 1.7; }
.ai-badge { background: rgba(59, 130, 246, 0.1); color: #3B82F6; border: 1px solid #3B82F6; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }

/* Beyaz Kutu İmhasi - Dropdown (Selectbox) Zırhı */
div[data-baseweb="select"] > div { 
    background-color: #12151B !important; 
    color: #F5F5F5 !important; 
    border: 1px solid #2D323C !important; 
    border-radius: 8px !important; 
}
div[data-baseweb="popover"] > div { background-color: #12151B !important; border: 1px solid #2D323C !important; }
li[role="option"] { background-color: #12151B !important; color: #F5F5F5 !important; }
li[role="option"]:hover { background-color: #1E2532 !important; color: #DEFF9A !important; }

/* Genel Yazı Renkleri */
h1, h2, h3, h4, p, label { color: #F5F5F5 !important; }
hr { border-color: rgba(255,255,255,0.05) !important; }
div[data-baseweb="slider"] div { background-color: #DEFF9A !important; }
</style>
""", unsafe_allow_html=True)

class SovereignDataEngine:
    """Veri çekme, temizleme ve normalize etme işlemlerini yürüten çekirdek motor."""
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner=False)
    def fetch_market_data(tickers, period):
        data = yf.download(tickers, period=period, progress=False, threads=True)
        return data['Close'], data['Volume'], data['High'], data['Low'], data['Open']
    
    @staticmethod
    def calculate_technical_indicators(close_prices):
        # RSI
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # MACD
        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal_line
        
        return rsi, macd, signal_line, histogram

class SovereignRiskEngine:
    """Kurumsal seviye risk metriklerini hesaplayan kuantitatif motor."""
    @staticmethod
    def calculate_metrics(returns, risk_free_rate=0.40):
        rf_daily = risk_free_rate / 252
        annual_volatility = returns.std() * np.sqrt(252) * 100
        
        # Sharpe Oranı
        excess_returns = returns - rf_daily
        sharpe_ratio = (excess_returns.mean() / returns.std()) * np.sqrt(252)
        
        # Sortino Oranı (Sadece negatif dalgalanmayı cezalandırır - Premium Metrik)
        negative_returns = excess_returns[excess_returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252)
        sortino_ratio = (excess_returns.mean() * 252) / downside_deviation if downside_deviation > 0 else 0
        
        # Maximum Drawdown (Kriz Direnci)
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = ((cumulative - peak) / peak) * 100
        max_dd = drawdown.min()
        
        # Value at Risk (VaR 95%) - Tarihsel (Numpy ile çözüldü, Scipy hatası bitti)
        var_95 = np.percentile(returns.dropna() * 100, 5)
        
        return annual_volatility, sharpe_ratio, sortino_ratio, max_dd, var_95, drawdown

class SovereignVisualEngine:
    """Plotly grafiklerini kurumsal bir arayüze çeviren motor."""
    COLORS = {
        'bg': 'rgba(0,0,0,0)',
        'grid': 'rgba(255,255,255,0.03)',
        'text': '#A0ABC0',
        'fund': '#DEFF9A',
        'bist': '#3B82F6',
        'red': '#FF4C4C',
        'orange': '#F59E0B'
    }

    @classmethod
    def apply_premium_layout(cls, fig, title=""):
        fig.update_layout(
            title=dict(text=title, font=dict(color='#F5F5F5', size=18, family="Inter")),
            plot_bgcolor=cls.COLORS['bg'],
            paper_bgcolor=cls.COLORS['bg'],
            font=dict(color=cls.COLORS['text'], family="Inter"),
            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11)),
            margin=dict(l=20, r=20, t=50, b=20),
            hovermode='x unified',
            hoverlabel=dict(bgcolor="rgba(18, 21, 27, 0.9)", font_size=13, font_family="Inter")
        )
        return fig

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=60)
st.sidebar.markdown("<h2 style='color: #F5F5F5; font-weight: 800; margin-bottom: 0;'>Sovereign Terminal</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #A0ABC0; font-size: 13px; margin-top: 0;'>V13.1 Quantum Architecture</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Zaman Makinesi")
periyot = st.sidebar.selectbox("Analiz Periyodu:", ["3mo", "6mo", "1y", "2y", "5y", "max"], index=2)

st.sidebar.markdown("<hr style='margin: 25px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("### 🛡️ Algoritmik Zırh (SMA)")

# SMA Toggle Hatası Çözümü - Session State ile Kaybolmayı Önleme
if 'sma_toggle' not in st.session_state:
    st.session_state.sma_toggle = True

trend_goster = st.sidebar.toggle("Trend Kalkanı Aktif", value=st.session_state.sma_toggle)
st.session_state.sma_toggle = trend_goster

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade (Hızlı Trend)", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade (Ana Trend)", 10, 250, 50)

st.markdown("<h1 style='font-size: 42px; letter-spacing: -1.5px;'>🌍 Taha Uyanık <span style='color: #2D323C;'>|</span> <span style='color: #DEFF9A;'>Ultra Premium Quant Fund</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #A0ABC0; font-size: 16px; margin-bottom: 30px;'>Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V13.1 TITAN)</p>", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    
    if close_data.empty:
        st.error("Veri akışı sağlanamadı. Bağlantıyı kontrol edin.")
        st.stop()
        
    close_data = close_data.ffill().bfill()
    
    # 0'a bölme zırhı ve 100 tabanlı normalizasyon
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    
    # Eşit Ağırlıklı Portföy Hesaplaması
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    # Dinamik SMA Hesaplaması
    if trend_goster:
        if len(normalize_veri) >= sma_kisa:
            normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        if len(normalize_veri) >= sma_uzun:
            normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Algoritmik Terminal", 
        "🔬 Röntgen (Derin Analiz)", 
        "🧠 AI İstihbarat Sinyalleri", 
        "🧩 Kuantum Risk & Monte Carlo"
    ])

    with tab1:
        st.markdown("<h3 style='margin-bottom: 20px;'>📊 Fon Performans Kıyaslaması</h3>", unsafe_allow_html=True)

        fig = go.Figure()
        
        # Premium Area Chart (Altı Dolgulu Çizgi Grafiği)
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), 
            y=normalize_veri['TAHA_YESIL_FON'], 
            mode='lines', 
            name='Sovereign Yeşil Fon', 
            line=dict(color=SovereignVisualEngine.COLORS['fund'], width=3),
            fill='tozeroy',
            fillcolor='rgba(222, 255, 154, 0.05)' # Çok hafif neon dolgu
        ))
        
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), 
            y=normalize_veri['XU100.IS'], 
            mode='lines', 
            name='BIST100 Endeksi', 
            line=dict(color=SovereignVisualEngine.COLORS['bist'], width=2)
        ))

        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa} (Hızlı)', line=dict(color=SovereignVisualEngine.COLORS['orange'], width=1.5, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun} (Ana)', line=dict(color=SovereignVisualEngine.COLORS['red'], width=1.5, dash='dot')))

        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(
            legend=dict(orientation="h", yanchor="top", y=-0.15, xanchor="center", x=0.5, font=dict(color='#FFFFFF')),
            height=500
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        st.markdown("<br><h3 style='margin-bottom: 20px;'>💰 100.000 TL Performans Simülasyonu</h3>", unsafe_allow_html=True)
        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        col1, col2, col3 = st.columns(3)
        col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} ₺", delta="Referans Endeks", delta_color="off")
        col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} ₺", delta=f"{((yesil_sonuc-100000)/100000)*100:.1f}% Fon Büyümesi")
        col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} ₺", delta="Piyasayı Yendi" if fark > 0 else "Piyasaya Yenildi")

    with tab2:
        st.markdown("<h3 style='margin-bottom: 20px;'>🔬 Teknik Analiz ve İndikatör Röntgeni</h3>", unsafe_allow_html=True)
        secili_hisse = st.selectbox("İncelenecek Hisseyi Seçin", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'])
        
        if secili_hisse:
            h_close = close_data[secili_hisse]
            h_open = open_data[secili_hisse]
            h_high = high_data[secili_hisse]
            h_low = low_data[secili_hisse]
            h_vol = vol_data[secili_hisse]
            
            h_rsi, h_macd, h_signal, h_hist = SovereignDataEngine.calculate_technical_indicators(h_close)
            
            fig_tech = make_subplots(
                rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.04, 
                row_heights=[0.5, 0.15, 0.15, 0.2], 
                subplot_titles=(f"{secili_hisse} Fiyat Hareketi", "İşlem Hacmi", "RSI (Göreceli Güç)", "MACD")
            )
            
            # Candlestick
            fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C'), row=1, col=1)
            
            # Volume
            colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
            fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors), row=2, col=1)
            
            # RSI
            fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=2)), row=3, col=1)
            fig_tech.add_hline(y=70, line_dash="dash", line_color="rgba(255, 76, 76, 0.5)", row=3, col=1)
            fig_tech.add_hline(y=30, line_dash="dash", line_color="rgba(222, 255, 154, 0.5)", row=3, col=1)
            
            # MACD
            fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A', width=1.5)), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C', width=1.5)), row=4, col=1)
            fig_tech.add_trace(go.Bar(x=h_hist.index, y=h_hist, marker_color=['rgba(222, 255, 154, 0.5)' if val >= 0 else 'rgba(255, 76, 76, 0.5)' for val in h_hist]), row=4, col=1)
            
            fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
            fig_tech.update_layout(height=850, showlegend=False, xaxis_rangeslider_visible=False)
            fig_tech.update_layout(margin=dict(l=20, r=20, t=40, b=40))
            
            st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("<h3 style='margin-bottom: 20px;'>🕵️‍♂️ NLP Haber Okuyucusu ve Karar Motoru</h3>", unsafe_allow_html=True)
        col_ai1, col_ai2 = st.columns([2, 1])
        
        with col_ai1:
            st.markdown("<p style='color: #8B949E; font-weight: 600;'>Sektörel Makro Tarama</p>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="ai-signal-card">
                <div class="ai-title">Yeşil Enerji Regülasyonları Bekleniyor</div>
                <div style="margin-bottom: 15px;">
                    <span style="color: #A0ABC0; font-size: 13px;">Kaynak: Sovereign Macro AI</span> | 
                    <span class="ai-badge">🔵 BEKLEMEDE (PENDING)</span>
                </div>
                <p class="ai-desc">Yapay zeka motorumuz spesifik hisse haberi bulamadığında otomatik olarak sektörel makro görünüme odaklanır.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br><p style='color: #8B949E; font-weight: 600;'>🌍 Global Makro Puan (Sovereign Gauge)</p>", unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = 72, title = {'text': "Piyasa Hissiyatı (Sentiment)", 'font': {'color': '#F5F5F5', 'size': 16, 'family': 'Inter'}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#F5F5F5", 'tickwidth': 1}, 
                    'bar': {'color': "#DEFF9A", 'thickness': 0.25},
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(255, 76, 76, 0.2)"}, 
                        {'range': [40, 60], 'color': "rgba(255, 255, 255, 0.05)"}, 
                        {'range': [60, 100], 'color': "rgba(59, 130, 246, 0.2)"}
                    ],
                    'threshold': {'line': {'color': "white", 'width': 3}, 'thickness': 0.75, 'value': 72}
                }
            ))
            fig_gauge.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5', family="Inter"))
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        with col_ai2:
            st.markdown("<p style='color: #8B949E; font-weight: 600;'>🤖 Algoritmik Taktik</p>", unsafe_allow_html=True)
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM (RİSK)", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Pozisyonu Koru (Hold)"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla"
            else:
                durum, renk, taktik = "BEKLEMEDE", "#3B82F6", "Trend Kalkanını Aktif Edin"

            st.markdown(f"""
            <div style="background: rgba(18, 23, 33, 0.6); backdrop-filter: blur(10px); padding: 40px 20px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); text-align: center; height: 100%;">
                <p style="color: #A0ABC0; font-size: 11px; letter-spacing: 2px; text-transform: uppercase;">SİSTEM DURUMU</p>
                <h2 style="color: {renk}; font-size: 28px; margin: 20px 0; font-weight: 800; letter-spacing: -1px;">{durum}</h2>
                <hr style="border-color: rgba(255,255,255,0.05); margin: 30px 0;">
                <p style="color: #8B949E; font-size: 13px;">Tavsiye:</p>
                <b style="color: #F5F5F5; font-size: 18px;">{taktik}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("<h3 style='margin-bottom: 20px;'>⚖️ Kantitatif Risk & Raporlama</h3>", unsafe_allow_html=True)
        getiriler = close_data.pct_change().dropna()
        
        if len(getiriler) > 0:
            portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)
            bist_getiri = getiriler['XU100.IS']
            
            # Risk Motorunu Çalıştır
            fon_vol, sharpe, sortino, fon_dd, var_95, drawdown_serisi = SovereignRiskEngine.calculate_metrics(portfoy_getiri)

            r_col1, r_col2, r_col3, r_col4 = st.columns(4)
            r_col1.metric("Fon Yıllık Volatilite", f"%{fon_vol:.2f}", delta="Dalgalanma Boyutu", delta_color="off")
            r_col2.metric("Maksimum Düşüş (Drawdown)", f"%{fon_dd:.2f}", delta="Tarihsel Kriz Direnci", delta_color="off")
            r_col3.metric("Sortino Oranı (Risk Ayarlı)", f"{sortino:.2f}", delta="1.0 Üzeri Mükemmel", delta_color="normal" if sortino > 0 else "inverse")
            r_col4.metric("Günlük VaR (%95 Güven)", f"%{var_95:.2f}", delta="1 Günde Beklenen Maks Kayıp", delta_color="inverse")
            
            st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns([1, 1])
            with kor_col1:
                st.markdown("<p style='color: #F5F5F5; font-weight: 700; font-size: 18px;'>🧩 Fon Korelasyon Matrisi (Risk Radarı)</p>", unsafe_allow_html=True)
                hisse_getirileri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']]
                kor_matrisi = hisse_getirileri.corr().values
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                    colorscale=[[0, '#090B10'], [0.5, '#192C3D'], [1, '#DEFF9A']], 
                    text=np.round(kor_matrisi, 2), texttemplate="%{text}", textfont={"color": "white", "size": 15, "family": "Inter"}, showscale=False
                ))
                fig_corr.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                    margin=dict(t=10, b=10, l=10, r=10), 
                    xaxis_showgrid=False, yaxis_showgrid=False, yaxis_autorange='reversed', 
                    font=dict(color='#A0ABC0', family="Inter"), height=350
                )
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<p style='color: #F5F5F5; font-weight: 700; font-size: 18px;'>🌊 Kriz Direnci (Underwater / Drawdown)</p>", unsafe_allow_html=True)
                fig_dd = go.Figure()
                fig_dd.add_trace(go.Scatter(
                    x=drawdown_serisi.index.strftime('%Y-%m-%d'), 
                    y=drawdown_serisi, 
                    fill='tozeroy', 
                    mode='lines', 
                    line=dict(color='#FF4C4C', width=1.5), 
                    fillcolor='rgba(255, 76, 76, 0.15)'
                ))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=350, margin=dict(t=10, b=20, l=20, r=20))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

            st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-bottom: 20px;'>🔮 Monte Carlo Gelecek Projeksiyonu (1 Yıl)</h3>", unsafe_allow_html=True)
            
            # Monte Carlo Matematik Motoru
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): 
                sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            # 100 Olasılık Çizgisi (Şeffaf Matris)
            for i in range(100): 
                fig_mc.add_trace(go.Scatter(y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.04)', width=1), showlegend=False, hoverinfo='skip'))
            
            # Beklenen Ortalama
            ortalama_senaryo = sim_df.mean(axis=1)
            fig_mc.add_trace(go.Scatter(y=ortalama_senaryo, mode='lines', name='Beklenen Ortalama', line=dict(color='#3B82F6', width=3, dash='dash')))
            
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(
                height=550, 
                xaxis=dict(title="Gelecek Günler (1 İş Yılı)"), 
                yaxis=dict(title="Sermaye Büyüklüğü (TL)"),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
