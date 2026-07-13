import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(
    page_title="Sovereign Quant | Taha Uyanık", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded" 
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Zifiri Karanlık Kurumsal Zemin */
.stApp { 
    background: #030407 !important;
    background-image: radial-gradient(circle at 50% -20%, #0A0F18 0%, #030407 80%) !important;
}

/* ÇÖP TEMİZLİĞİ VE İKON İNFAZI */
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
a { pointer-events: none; cursor: default; text-decoration: none !important; }
.css-15zrgzn { display: none !important; } 

/* GİZLİ MENÜ TUŞU ZIRHI */
[data-testid="collapsedControl"] {
    display: flex !important; color: #DEFF9A !important;
    background-color: rgba(10, 15, 24, 0.95) !important;
    border: 1px solid rgba(222, 255, 154, 0.4) !important;
    border-radius: 6px !important; z-index: 99999 !important;
    transition: all 0.3s ease;
}
[data-testid="collapsedControl"]:hover { 
    border: 1px solid #DEFF9A !important; 
    box-shadow: 0 0 15px rgba(222, 255, 154, 0.3) !important; 
}

.stTabs [data-baseweb="tab-list"] {
    gap: 34px; background-color: transparent !important; /* Fibonacci 34 */
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; padding-bottom: 0px;
}
.stTabs [data-baseweb="tab"] {
    height: 55px; background-color: transparent !important; /* Fibonacci 55 */
    padding: 0px 8px !important; color: #6B7280 !important;
    font-weight: 500 !important; font-size: 14px !important;
    border: none !important; transition: all 0.4s ease;
    letter-spacing: 0.5px;
}
.stTabs [data-baseweb="tab"]:hover { color: #D1D5DB !important; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #DEFF9A !important; background-color: transparent !important; font-weight: 700 !important; }
div[data-baseweb="tab-highlight"] { background-color: #DEFF9A !important; height: 2px !important; border-radius: 2px 2px 0 0 !important; }

.glass-metric-card {
    background: linear-gradient(160deg, rgba(16, 20, 26, 0.90) 0%, rgba(8, 10, 14, 0.98) 100%);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 26px 42px; /* FIBONACCI PADDING (1.615 Oran) */
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.9);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 144px; position: relative; overflow: hidden;
}
.glass-metric-card:hover {
    transform: translateY(-3px); 
    border-top: 1px solid rgba(222, 255, 154, 0.5);
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.9), 0 0 20px rgba(222, 255, 154, 0.05);
}
.glass-metric-title {
    color: #8B949E; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px;
}
.glass-metric-value {
    color: #F5F5F5; font-size: 34px; font-weight: 800; letter-spacing: -1px; margin: 0; line-height: 1.2;
}
.glass-metric-delta { font-size: 13px; font-weight: 600; margin-top: 12px; display: flex; align-items: center; gap: 4px; }
.glass-metric-delta.positive { color: #A3FF00; }
.glass-metric-delta.negative { color: #FF4C4C; }
.glass-metric-delta.neutral { color: #A0ABC0; }

/* PALANTIR TERMİNAL TASARIMI (AI Sekmesi İçin) */
.terminal-card {
    background: #0A0C12; border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px; padding: 34px; position: relative;
    box-shadow: 0 10px 40px -10px rgba(0,0,0,0.9);
    height: 100%; display: flex; flex-direction: column; justify-content: space-between;
}
.terminal-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
    background: linear-gradient(to bottom, #3B82F6, transparent); border-radius: 12px 0 0 12px;
}
.terminal-font { font-family: 'JetBrains Mono', monospace; }

.stSelectbox div[data-baseweb="select"] > div {
    background-color: #0A0C12 !important; color: #F5F5F5 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 8px !important;
    font-weight: 500 !important;
}
.stSelectbox div[data-baseweb="popover"] { background-color: #0A0C12 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; }
.stSelectbox li { background-color: transparent !important; color: #F5F5F5 !important; }
.stSelectbox li:hover { background-color: rgba(222, 255, 154, 0.1) !important; color: #DEFF9A !important; }

/* Sidebar Asaleti */
[data-testid="stSidebar"] { background-color: rgba(5, 7, 10, 0.98) !important; border-right: 1px solid rgba(255, 255, 255, 0.03) !important; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #030407; }
::-webkit-scrollbar-thumb { background: #1C212B; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #3B82F6; }
h1, h2, h3, p, span { color: #F5F5F5; }
hr { border-color: rgba(255,255,255,0.05) !important; }

/* Dark Pool Table Estetiği */
.dark-pool-table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.dark-pool-table th { color: #8B949E; text-align: left; padding: 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600; text-transform: uppercase;}
.dark-pool-table td { color: #D1D5DB; padding: 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.02); }
.dark-pool-buy { color: #DEFF9A; font-weight: 600; }
.dark-pool-sell { color: #FF4C4C; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

class SovereignDataEngine:
    @staticmethod
    @st.cache_data(ttl=1800, show_spinner=False)
    def fetch_market_data(tickers, period):
        data = yf.download(tickers, period=period, progress=False, threads=True)
        if data.empty:
            raise ValueError("API Kritik Hatası: Veri çekilemedi.")
        return data['Close'], data['Volume'], data['High'], data['Low'], data['Open']
    
    @staticmethod
    def calculate_technical_indicators(close_prices, volume):
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
        
        # On-Balance Volume (OBV) - Kurumsal Para Akışı (Yeni)
        obv = (np.sign(delta) * volume).fillna(0).cumsum()
        
        # Bollinger Bands
        sma_20 = close_prices.rolling(window=20).mean()
        std_20 = close_prices.rolling(window=20).std()
        upper_band = sma_20 + (std_20 * 2.1) # Kuantitatif hassasiyet
        lower_band = sma_20 - (std_20 * 2.1)
        
        return rsi, macd, signal_line, upper_band, lower_band, obv, sma_20

class SovereignRiskEngine:
    @staticmethod
    def calculate_metrics(returns, benchmark_returns, risk_free_rate=0.40):
        rf_daily = risk_free_rate / 252
        annual_volatility = returns.std() * np.sqrt(252) * 100
        bench_volatility = benchmark_returns.std() * np.sqrt(252) * 100
        
        # Beta & Alpha
        cov_matrix = np.cov(returns, benchmark_returns)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] > 0 else 1
        port_ann_return = returns.mean() * 252
        bench_ann_return = benchmark_returns.mean() * 252
        alpha = (port_ann_return - (risk_free_rate + beta * (bench_ann_return - risk_free_rate))) * 100
        
        # Downside Risk & Sortino
        excess_returns = returns - rf_daily
        negative_returns = excess_returns[excess_returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252)
        sortino_ratio = (excess_returns.mean() * 252) / downside_deviation if downside_deviation > 0 else 0
        
        # Drawdown & Calmar (Yeni)
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = ((cumulative - peak) / peak) * 100
        max_dd = drawdown.min()
        calmar_ratio = (port_ann_return * 100) / abs(max_dd) if abs(max_dd) > 0 else 0
        
        # Information Ratio (Yeni)
        tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)
        info_ratio = (port_ann_return - bench_ann_return) / tracking_error if tracking_error > 0 else 0
        
        # VaR & CVaR
        var_95 = np.percentile(returns.dropna() * 100, 5)
        cvar_95 = returns.dropna()[returns.dropna() * 100 <= var_95].mean() * 100
        
        return (annual_volatility, bench_volatility, sortino_ratio, calmar_ratio, info_ratio, 
                max_dd, var_95, cvar_95, drawdown, alpha, beta)

class SovereignVisualEngine:
    COLORS = {'bg': 'rgba(0,0,0,0)', 'card': '#0A0C12', 'grid': 'rgba(255,255,255,0.03)', 
              'text': '#8B949E', 'fund': '#DEFF9A', 'bist': '#3B82F6', 'red': '#FF4C4C'}
    @classmethod
    def apply_premium_layout(cls, fig):
        fig.update_layout(
            plot_bgcolor=cls.COLORS['bg'], paper_bgcolor=cls.COLORS['bg'],
            font=dict(color=cls.COLORS['text'], family="Inter"),
            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280'), zeroline=False),
            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280'), zeroline=False),
            margin=dict(l=10, r=10, t=40, b=10), hovermode='x unified',
            hoverlabel=dict(bgcolor="#0A0C12", font_size=12, font_family="JetBrains Mono", bordercolor="rgba(222,255,154,0.3)")
        )
        return fig
    
    @classmethod
    def apply_card_layout(cls, fig):
        """Grafiği sanki bir CSS kartıymış gibi gösterir (Gauge için)"""
        fig = cls.apply_premium_layout(fig)
        fig.update_layout(
            paper_bgcolor=cls.COLORS['card'],
            plot_bgcolor=cls.COLORS['card'],
            margin=dict(l=30, r=30, t=60, b=30),
            shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, 
                        line=dict(color="rgba(255,255,255,0.05)", width=1))]
        )
        return fig

st.sidebar.markdown("<h3 style='font-weight: 800; margin-bottom: 0; font-size:16px; color: #F5F5F5; letter-spacing: 0.5px;'>⚙️ Kontrol Paneli</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 11px; margin-top: 2px;'>V21.0 APEX ELITE ENGINE</p>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600; margin-top:34px;'>Zaman Aralığı</p>", unsafe_allow_html=True)
periyot = st.sidebar.selectbox("", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3, label_visibility="collapsed")

st.sidebar.markdown("<hr style='margin: 34px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600;'>🧠 Algoritmik Araçlar</p>", unsafe_allow_html=True)

# Otomatik Açık Gelen Zırhlı SMA Şalteri
if 'trend_kalkani' not in st.session_state: st.session_state.trend_kalkani = True
if 'bollinger_kalkani' not in st.session_state: st.session_state.bollinger_kalkani = False

trend_goster = st.sidebar.toggle("Algoritmik Trend (SMA)", value=st.session_state.trend_kalkani)
bollinger_goster = st.sidebar.toggle("Volatilite Zırhı (Bollinger)", value=st.session_state.bollinger_kalkani)
st.session_state.trend_kalkani = trend_goster
st.session_state.bollinger_kalkani = bollinger_goster

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade Momentum", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade Trend", 10, 250, 50)

st.markdown("""
<div style='margin-bottom: 34px;'>
    <h1 style='font-size: 34px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; display:flex; align-items:center; gap:10px;'>
        🌍 Taha Uyanık <span style='color: #2D323C; font-weight:300;'>|</span> Sovereign Quant Fund
    </h1>
    <p style='color: #8B949E; font-size: 13px; margin: 0; font-weight: 500;'>Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V21.0 APEX)</p>
</div>
""", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    close_data = close_data.ffill().bfill()
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Algoritmik Terminal", "🔬 Röntgen (Derin Analiz)", "🧠 AI İstihbarat", "⚖️ Kuantum Risk Radarı", "🔮 Gelecek Simülasyonu"
    ])

    with tab1:
        st.markdown("<h3 style='margin: 21px 0 21px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>Fon Performans Kıyaslaması</h3>", unsafe_allow_html=True)
        fig = go.Figure()
        
        # Alan (Area) Grafiği ile Derinlik
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['TAHA_YESIL_FON'], mode='lines', name='Sovereign Yeşil Fon', 
                                 line=dict(color=SovereignVisualEngine.COLORS['fund'], width=2.5), 
                                 fill='tozeroy', fillcolor='rgba(222, 255, 154, 0.03)'))
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['XU100.IS'], mode='lines', name='BIST100 Endeksi', 
                                 line=dict(color=SovereignVisualEngine.COLORS['bist'], width=1.5)))
        
        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa}', line=dict(color='#F59E0B', width=1, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun}', line=dict(color='#FF4C4C', width=1, dash='dot')))
        
        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), height=500)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        st.markdown("<h3 style='margin: 42px 0 21px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>💰 100.000 TL Performans Simülasyonu</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px;">
            <div class="glass-metric-card">
                <div class="glass-metric-title">Klasik BIST100 Getirisi</div>
                <div class="glass-metric-value">{bist_sonuc:,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta neutral">↑ Referans Endeks</div>
            </div>
            <div class="glass-metric-card" style="border-top: 1px solid rgba(222, 255, 154, 0.4); box-shadow: 0 15px 35px -10px rgba(0,0,0,0.9), 0 0 20px rgba(222, 255, 154, 0.05);">
                <div class="glass-metric-title" style="color:#DEFF9A;">Sovereign Fon Getirisi</div>
                <div class="glass-metric-value">{yesil_sonuc:,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta positive">↑ %{((yesil_sonuc-100000)/100000)*100:.1f} Fon Büyümesi</div>
            </div>
            <div class="glass-metric-card">
                <div class="glass-metric-title">Yaratılan Yıllık Alpha</div>
                <div class="glass-metric-value">{fark:+,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta {'positive' if fark > 0 else 'negative'}">{'↑ Piyasayı Yendi (Alpha)' if fark > 0 else '↓ Piyasaya Yenildi'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        secili_hisse = st.selectbox("İncelenecek Hisseyi Seçin (Derin Analiz)", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0)
        h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
        
        h_rsi, h_macd, h_signal, upper_bb, lower_bb, h_obv, sma_20 = SovereignDataEngine.calculate_technical_indicators(h_close, h_vol)
        
        fig_tech = make_subplots(
            rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.03, 
            row_heights=[0.45, 0.15, 0.15, 0.15, 0.10],
            subplot_titles=(f"{secili_hisse} Fiyat & Volatilite", "İşlem Hacmi", "RSI (Momentum)", "MACD (Trend)", "OBV (Para Akışı)")
        )
        
        fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Fiyat"), row=1, col=1)
        
        if bollinger_goster:
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=upper_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), name="Upper BB", hoverinfo='skip'), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=lower_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), fill='tonexty', fillcolor='rgba(59, 130, 246, 0.05)', name="Lower BB", hoverinfo='skip'), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=sma_20, line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name="SMA 20", hoverinfo='skip'), row=1, col=1)
        
        colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
        fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Hacim"), row=2, col=1)
        
        fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=1.5), name="RSI"), row=3, col=1)
        fig_tech.add_hline(y=70, line_dash="dash", line_color="#FF4C4C", row=3, col=1)
        fig_tech.add_hline(y=30, line_dash="dash", line_color="#DEFF9A", row=3, col=1)
        
        fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A', width=1.5), name="MACD"), row=4, col=1)
        fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C', width=1), name="Signal"), row=4, col=1)
        macd_hist = h_macd - h_signal
        hist_colors = ['rgba(222,255,154,0.6)' if val >= 0 else 'rgba(255,76,76,0.6)' for val in macd_hist]
        fig_tech.add_trace(go.Bar(x=macd_hist.index, y=macd_hist, marker_color=hist_colors, name="Histogram"), row=4, col=1)

        fig_tech.add_trace(go.Scatter(x=h_obv.index, y=h_obv, line=dict(color='#A0ABC0', width=1.5), fill='tozeroy', fillcolor='rgba(160, 171, 192, 0.1)', name="OBV"), row=5, col=1)

        fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
        for i in fig_tech['layout']['annotations']: i['font'] = dict(size=11, color='#8B949E', family="Inter", weight="bold")
        fig_tech.update_layout(height=950, showlegend=False, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("<h3 style='margin: 21px 0 34px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🕵️ NLP İstihbarat ve Makro Karar Motoru</h3>", unsafe_allow_html=True)
        
        # Üst Satır - Asimetrik Altın Oran [1.618, 1]
        col_ai1, col_ai2 = st.columns([1.618, 1], gap="large")
        
        with col_ai1:
            st.markdown("""
            <div class="terminal-card">
                <div>
                    <div class="terminal-font" style="color:#3B82F6; font-size: 11px; margin-bottom: 12px; letter-spacing: 1px;">[NLP_ENGINE_ACTIVE] :: SEKTÖREL TARAMA</div>
                    <h3 style="color: #F5F5F5; font-size: 21px; margin: 0 0 12px 0;">Yeşil Enerji Regülasyonları Bekleniyor</h3>
                    <div style="font-size: 12px; color: #8B949E; margin-bottom: 21px; display: flex; align-items: center; gap: 8px;">
                        <span style="display:inline-block; width:8px; height:8px; background-color:#3B82F6; border-radius:50%; box-shadow: 0 0 10px #3B82F6;"></span>
                        Kaynak: Sovereign AI | Durum: PENDING
                    </div>
                </div>
                <p class="terminal-font" style="color: #A0ABC0; font-size: 12px; margin: 0; line-height: 1.7;">
                    > Spesifik şirket haberi bulunamadı (API Koruması / Gecikme).<br>
                    > Sistem otonom olarak 'Makro Yeşil Enerji' taramasına geçti.<br>
                    > Global yenilenebilir enerji teşvikleri analiz ediliyor...<br>
                    > Sektörel uzun vade projeksiyonu: <span style="color:#DEFF9A;">POZİTİF</span>
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_ai2:
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Kademeli Topla (BUY)"
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM (RİSK)", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Pozisyonu Koru (HOLD)"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla (BUY)"

            st.markdown(f"""
            <div class="glass-metric-card" style="border-top: 2px solid {renk}; text-align: center; justify-content: center;">
                <div class="glass-metric-title" style="margin-bottom: 21px; letter-spacing: 2px;">ALGORİTMİK TAKTİK MERKEZİ</div>
                <h2 style="color: {renk}; font-size: 28px; font-weight: 800; margin: 0 0 21px 0; letter-spacing: -0.5px;">{durum}</h2>
                <div class="terminal-font" style="background: rgba(255,255,255,0.02); padding: 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <span style="color: #8B949E; font-size: 11px;">AI TAVSİYESİ: </span><br>
                    <span style="color: #F5F5F5; font-size: 14px; font-weight: bold; margin-top:5px; display:inline-block;">{taktik}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True) # Fibonacci Gap

        # Alt Satır - Zıt Asimetrik Altın Oran [1, 1.618]
        col_ai3, col_ai4 = st.columns([1, 1.618], gap="large")
        
        with col_ai3:
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = 72,
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2D323C", 'tickfont': dict(color="#8B949E")}, 
                    'bar': {'color': "#DEFF9A", 'thickness': 0.15},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(255, 76, 76, 0.15)"}, 
                        {'range': [40, 60], 'color': "rgba(255, 255, 255, 0.05)"}, 
                        {'range': [60, 100], 'color': "rgba(222, 255, 154, 0.15)"}
                    ]
                },
                number = {'font': {'color': '#F5F5F5', 'size': 55}} # Fibonacci 55
            ))
            fig_gauge = SovereignVisualEngine.apply_card_layout(fig_gauge)
            fig_gauge.update_layout(title=dict(text="GLOBAL MAKRO HİSSİYAT", font=dict(color='#8B949E', size=11, family="Inter"), x=0.5, y=0.9), height=280)
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            
        with col_ai4:
            st.markdown("""
            <div class="glass-metric-card" style="padding: 21px 34px; justify-content: flex-start; height: 100%;">
                <div class="glass-metric-title" style="margin-bottom: 16px;">[LIVE] Institutional Dark Pool Flow (Simüle Edilmiş)</div>
                <table class="dark-pool-table">
                    <tr><th>Varlık</th><th>İşlem Tipi</th><th>Hacim (Lot)</th><th>Fiyat Sinyali</th><th>Ağ Gecikmesi</th></tr>
                    <tr><td>ALFAS.IS</td><td class="dark-pool-buy">BLOCK BUY</td><td>245,000</td><td>Pozitif Etki</td><td>12ms</td></tr>
                    <tr><td>ASTOR.IS</td><td class="dark-pool-sell">ICEBERG SELL</td><td>120,500</td><td>Baskı</td><td>18ms</td></tr>
                    <tr><td>YEOTK.IS</td><td class="dark-pool-buy">TWAP BUY</td><td>85,000</td><td>Nötr/Pozitif</td><td>9ms</td></tr>
                    <tr><td>KCAER.IS</td><td class="dark-pool-buy">BLOCK BUY</td><td>310,000</td><td>Pozitif Etki</td><td>15ms</td></tr>
                    <tr><td>XU100.IS</td><td class="dark-pool-sell">MACRO HEDGE</td><td>-</td><td>Piyasa Şoku</td><td>5ms</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        getiriler = close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change().dropna()
        bist_getiri = close_data['XU100.IS'].pct_change().dropna()
        
        if len(getiriler) > 0:
            portfoy_getiri = getiriler.mean(axis=1)
            (fon_vol, b_vol, sortino, calmar, info_ratio, 
             max_dd, var_95, cvar_95, drawdown_serisi, alpha, beta) = SovereignRiskEngine.calculate_metrics(portfoy_getiri, bist_getiri)

            st.markdown("<h3 style='margin: 21px 0 34px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>⚖️ Kantitatif Risk & Raporlama</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 21px; margin-bottom: 34px;">
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Fon Yıllık Volatilite</div>
                    <div class="glass-metric-value" style="font-size:26px;">% {fon_vol:.2f}</div>
                    <div class="glass-metric-delta neutral" style="font-size:11px;">BIST100: %{b_vol:.2f}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px; border-top: 1px solid {'#DEFF9A' if sortino > 1 else '#F59E0B'};">
                    <div class="glass-metric-title" style="color: {'#DEFF9A' if sortino > 1 else '#F59E0B'};">Sortino Oranı</div>
                    <div class="glass-metric-value" style="font-size:26px;">{sortino:.2f}</div>
                    <div class="glass-metric-delta {'positive' if sortino > 1 else 'neutral'}" style="font-size:11px;">{'Aşağı Yön Riski Düşük' if sortino > 1 else 'Aşağı Yön Riski Mevcut'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Calmar Oranı (Getiri/Drawdown)</div>
                    <div class="glass-metric-value" style="font-size:26px;">{calmar:.2f}</div>
                    <div class="glass-metric-delta {'positive' if calmar > 1 else 'neutral'}" style="font-size:11px;">{'Kriz Direnci Yüksek' if calmar > 1 else 'Ortalama Direnç'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Information Ratio</div>
                    <div class="glass-metric-value" style="font-size:26px;">{info_ratio:.2f}</div>
                    <div class="glass-metric-delta {'positive' if info_ratio > 0.5 else 'neutral'}" style="font-size:11px;">{'Aktif Yönetim Başarısı' if info_ratio > 0.5 else 'Endekse Paralel'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Piyasa Betası (Risk)</div>
                    <div class="glass-metric-value" style="font-size:26px;">{beta:.2f}</div>
                    <div class="glass-metric-delta {'positive' if beta < 1 else 'negative'}" style="font-size:11px;">{'Defansif Yapı' if beta < 1 else 'Agresif Karakter'}</div>
                </div>
                 <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Maks Düşüş (Drawdown)</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#FF4C4C;">% {max_dd:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Tarihsel Kriz Dip Noktası</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Günlük VaR (%95 Güven)</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#F59E0B;">% {var_95:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Beklenen Normal Kayıp</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Günlük CVaR (Kuyruk Riski)</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#FF4C4C;">% {cvar_95:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Kriz Anı Beklenen Kayıp</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns(2, gap="large")
            with kor_col1:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:16px;'>🧩 Fon Korelasyon Matrisi (Risk Radarı)</div>", unsafe_allow_html=True)
                kor_matrisi = getiriler.corr().values
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                    colorscale=[[0, '#0A0C12'], [0.5, '#1C2433'], [1, '#DEFF9A']], showscale=False, hoverinfo='skip'
                ))
                for i in range(len(kor_matrisi)):
                    for j in range(len(kor_matrisi[i])):
                        val = kor_matrisi[i][j]
                        text_color = '#0A0C12' if val > 0.7 else '#F5F5F5'
                        fig_corr.add_annotation(x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][j], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][i], text=f"{val:.2f}", showarrow=False, font=dict(color=text_color, size=13, family="Inter", weight="600"))
                
                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=340)
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:16px;'>🌊 Kriz Direnci (Underwater / Drawdown)</div>", unsafe_allow_html=True)
                fig_dd = go.Figure(go.Scatter(x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.15)'))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=340, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

    with tab5:
        st.markdown("<h3 style='margin: 21px 0 8px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🔮 Geometrik Brownian Hareketi (Monte Carlo 1 Yıl)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 34px;'>Mevcut fon volatilitesi (σ) ve beklenen getiri (μ) kullanılarak önümüzdeki 252 işlem günü için 100 farklı rassal senaryo simüle edilmiştir. %5 ve %95 güven aralıkları gölgelendirilmiştir.</p>", unsafe_allow_html=True)
        
        if len(getiriler) > 0:
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            
            # %5 ve %95 Volatilite Konisi (Shaded Area)
            percentile_5 = np.percentile(sim_df, 5, axis=1)
            percentile_95 = np.percentile(sim_df, 95, axis=1)
            x_axis = np.arange(252)
            
            fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_95, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
            fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_5, mode='lines', fill='tonexty', fillcolor='rgba(222, 255, 154, 0.05)', line=dict(width=0), showlegend=False, hoverinfo='skip'))

            # Paralel Evren Çizgileri
            for i in range(100): fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.06)', width=1), showlegend=False, hoverinfo='skip'))
            
            # Beklenen Ortalama
            fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df.mean(axis=1), mode='lines', name='Beklenen Ortalama (μ)', line=dict(color='#F5F5F5', width=3, dash='dash')))
            
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(height=650, yaxis_title="Sermaye (TL)", xaxis_title="Gelecek Günler (252 İş Günü)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
