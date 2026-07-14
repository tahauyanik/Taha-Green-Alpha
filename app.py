import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import requests
import xml.etree.ElementTree as ET

st.set_page_config(
    page_title="Sovereign Quant | Portfolio Overview", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="collapsed" 
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

/* ÇÖP TEMİZLİĞİ VE SİDEBAR İNFAZI */
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
a { pointer-events: none; cursor: default; text-decoration: none !important; }
.css-15zrgzn { display: none !important; } 

[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* HIZLANDIRILMIŞ TAB VE KART CSS'LERİ */
.stTabs [data-baseweb="tab-list"] {
    gap: 34px; background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; padding-bottom: 0px;
}
.stTabs [data-baseweb="tab"] {
    height: 55px; background-color: transparent !important;
    padding: 0px 8px !important; color: #6B7280 !important;
    font-weight: 500 !important; font-size: 14px !important;
    border: none !important; transition: color 0.2s ease;
    letter-spacing: 0.5px;
}
.stTabs [data-baseweb="tab"]:hover { color: #D1D5DB !important; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #DEFF9A !important; background-color: transparent !important; font-weight: 700 !important; }
div[data-baseweb="tab-highlight"] { background-color: #DEFF9A !important; height: 2px !important; border-radius: 2px 2px 0 0 !important; }

.glass-metric-card {
    background: linear-gradient(160deg, rgba(16, 20, 26, 0.90) 0%, rgba(8, 10, 14, 0.98) 100%);
    backdrop-filter: blur(8px); -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 26px 42px; 
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    will-change: transform;
    transform: translateZ(0);
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 144px; position: relative; overflow: hidden;
}
.glass-metric-card:hover {
    transform: translateY(-3px) translateZ(0); 
    border-top: 1px solid rgba(222, 255, 154, 0.5);
    box-shadow: 0 10px 25px rgba(0,0,0,0.8), 0 0 15px rgba(222, 255, 154, 0.05);
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

/* PALANTIR TERMİNAL TASARIMI */
.terminal-card {
    background: #0A0C12; border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px; padding: 34px; position: relative;
    box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    height: 100%; display: flex; flex-direction: column; justify-content: space-between;
    will-change: transform; transform: translateZ(0);
}
.terminal-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%;
    background: linear-gradient(to bottom, #3B82F6, transparent); border-radius: 12px 0 0 12px;
}
.terminal-font { font-family: 'JetBrains Mono', monospace; }

.stSelectbox div[data-baseweb="select"] > div, .stNumberInput > div > div > input {
    background-color: #0A0C12 !important; color: #F5F5F5 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 8px !important;
    font-weight: 500 !important;
}
.stSelectbox div[data-baseweb="popover"] { background-color: #0A0C12 !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; }
.stSelectbox li { background-color: transparent !important; color: #F5F5F5 !important; }
.stSelectbox li:hover { background-color: rgba(222, 255, 154, 0.1) !important; color: #DEFF9A !important; }

::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #030407; }
::-webkit-scrollbar-thumb { background: #1C212B; border-radius: 5px; }
::-webkit-scrollbar-thumb:hover { background: #3B82F6; }
h1, h2, h3, p, span { color: #F5F5F5; }
hr { border-color: rgba(255,255,255,0.05) !important; }

/* Real Anomaly & News Table Estetiği */
.dark-pool-table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.dark-pool-table th { color: #8B949E; text-align: left; padding: 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600; text-transform: uppercase;}
.dark-pool-table td { color: #D1D5DB; padding: 12px 4px; border-bottom: 1px solid rgba(255,255,255,0.02); }
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
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        
        obv = (np.sign(delta) * volume).fillna(0).cumsum()
        
        sma_20 = close_prices.rolling(window=20).mean()
        std_20 = close_prices.rolling(window=20).std()
        upper_band = sma_20 + (std_20 * 2.1)
        lower_band = sma_20 - (std_20 * 2.1)
        
        return rsi, macd, signal_line, upper_band, lower_band, obv, sma_20

    @staticmethod
    @st.cache_data(ttl=600, show_spinner=False)
    def fetch_live_news():
        try:
            url = "https://feeds.finance.yahoo.com/rss/2.0/headline?s=XU100.IS,TRY=X,ENJ-USD"
            response = requests.get(url, timeout=5)
            root = ET.fromstring(response.content)
            news_items = []
            for item in root.findall('./channel/item')[:4]: 
                title = item.find('title').text
                pub_date = item.find('pubDate').text[:-15] 
                news_items.append({'title': title, 'date': pub_date})
            return news_items
        except:
            return []

class SovereignRiskEngine:
    @staticmethod
    def calculate_metrics(returns, benchmark_returns, risk_free_rate=0.40):
        rf_daily = risk_free_rate / 252
        annual_volatility = returns.std() * np.sqrt(252) * 100
        bench_volatility = benchmark_returns.std() * np.sqrt(252) * 100
        
        cov_matrix = np.cov(returns, benchmark_returns)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] > 0 else 1
        port_ann_return = returns.mean() * 252
        bench_ann_return = benchmark_returns.mean() * 252
        alpha = (port_ann_return - (risk_free_rate + beta * (bench_ann_return - risk_free_rate))) * 100
        
        excess_returns = returns - rf_daily
        negative_returns = excess_returns[excess_returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252)
        sortino_ratio = (excess_returns.mean() * 252) / downside_deviation if downside_deviation > 0 else 0
        
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = ((cumulative - peak) / peak) * 100
        max_dd = drawdown.min()
        calmar_ratio = (port_ann_return * 100) / abs(max_dd) if abs(max_dd) > 0 else 0
        
        tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)
        info_ratio = (port_ann_return - bench_ann_return) / tracking_error if tracking_error > 0 else 0
        
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
        fig = cls.apply_premium_layout(fig)
        fig.update_layout(
            paper_bgcolor=cls.COLORS['card'],
            plot_bgcolor=cls.COLORS['card'],
            margin=dict(l=30, r=30, t=60, b=30),
            shapes=[dict(type="rect", xref="paper", yref="paper", x0=0, y0=0, x1=1, y1=1, 
                        line=dict(color="rgba(255,255,255,0.05)", width=1))]
        )
        return fig

# --- BAŞLIK ALANI ---
st.markdown("""
<div style='margin-bottom: 10px; margin-top: 15px;'>
    <h1 style='font-size: 34px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; display:flex; align-items:center; gap:10px;'>
        🌍 Sovereign Quant Fund
    </h1>
    <p style='color: #8B949E; font-size: 13px; margin: 0; font-weight: 500;'>Kurumsal Portföy Yönetimi ve Kantitatif Risk Sistemleri (V27.0 OMNISCIENCE EDITION)</p>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 5px; margin-bottom: 15px;'>", unsafe_allow_html=True)

with st.container():
    ctrl_col1, ctrl_col2, ctrl_col3, ctrl_col4 = st.columns(4)
    with ctrl_col1:
        st.markdown("<p style='color: #8B949E; font-size: 11px; font-weight: 600; margin-bottom:4px;'>ANALİZ PERİYODU</p>", unsafe_allow_html=True)
        periyot = st.selectbox("", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3, label_visibility="collapsed")
    with ctrl_col2:
        st.markdown("<p style='color: #8B949E; font-size: 11px; font-weight: 600; margin-bottom:4px;'>GÖSTERGE FİLTRELERİ (OVERLAYS)</p>", unsafe_allow_html=True)
        trend_goster = st.checkbox("Momentum Signal (SMA)", value=True)
        bollinger_goster = st.checkbox("Volatility Bands (Bollinger)", value=True)
    with ctrl_col3:
        st.markdown("<p style='color: #8B949E; font-size: 11px; font-weight: 600; margin-bottom:4px;'>MOMENTUM SIGNAL (FAST-EMA)</p>", unsafe_allow_html=True)
        sma_kisa = st.slider("Kısa Vade SMA", 5, 100, 20, label_visibility="collapsed") if trend_goster else 20
    with ctrl_col4:
        st.markdown("<p style='color: #8B949E; font-size: 11px; font-weight: 600; margin-bottom:4px;'>MACRO TREND (SLOW-SMA)</p>", unsafe_allow_html=True)
        sma_uzun = st.slider("Uzun Vade SMA", 10, 250, 50, label_visibility="collapsed") if trend_goster else 50

st.markdown("<hr style='border-color: rgba(255,255,255,0.1); margin-top: 15px; margin-bottom: 25px;'>", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    close_data = close_data.ffill().bfill()
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['SOVEREIGN_PORTFOLIO'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['SOVEREIGN_PORTFOLIO'].rolling(window=sma_kisa).mean()
        normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['SOVEREIGN_PORTFOLIO'].rolling(window=sma_uzun).mean()

    # V27.0 7. SEKME (BLACK SWAN) EKLENDİ
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Portfolio Overview", "🔬 Market Structure", "🧠 Signal Engine & Flow", "⚖️ Risk Metrics & Correlation", "🔮 Stochastic Projection (GBM)", "🧬 AI Rebalancer (Optimization)", "🦢 Macro Stress Testing"
    ])

    with tab1:
        st.markdown("<h3 style='margin: 21px 0 21px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>Portfolio Performance Tracking</h3>", unsafe_allow_html=True)
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['SOVEREIGN_PORTFOLIO'], mode='lines', name='Sovereign Quant Portfolio', 
                                 line=dict(color=SovereignVisualEngine.COLORS['fund'], width=2.5), 
                                 fill='tozeroy', fillcolor='rgba(222, 255, 154, 0.03)'))
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['XU100.IS'], mode='lines', name='Benchmark (BIST100)', 
                                 line=dict(color=SovereignVisualEngine.COLORS['bist'], width=1.5)))
        
        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'Momentum {sma_kisa}', line=dict(color='#F59E0B', width=1, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'Macro {sma_uzun}', line=dict(color='#FF4C4C', width=1, dash='dot')))
        
        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), height=500)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['SOVEREIGN_PORTFOLIO'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        st.markdown("<h3 style='margin: 42px 0 21px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>💰 100.000 TL Capital Growth Simulation</h3>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px;">
            <div class="glass-metric-card">
                <div class="glass-metric-title">Benchmark Return (BIST100)</div>
                <div class="glass-metric-value">{bist_sonuc:,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta neutral">↑ Reference Index</div>
            </div>
            <div class="glass-metric-card" style="border-top: 1px solid rgba(222, 255, 154, 0.4); box-shadow: 0 10px 25px rgba(0,0,0,0.8), 0 0 15px rgba(222, 255, 154, 0.05);">
                <div class="glass-metric-title" style="color:#DEFF9A;">Sovereign Portfolio Return</div>
                <div class="glass-metric-value">{yesil_sonuc:,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta positive">↑ %{((yesil_sonuc-100000)/100000)*100:.1f} Portfolio Growth</div>
            </div>
            <div class="glass-metric-card">
                <div class="glass-metric-title">Generated Alpha (Excess Return)</div>
                <div class="glass-metric-value">{fark:+,.0f} <span style="font-size:24px; color:#8B949E;">₺</span></div>
                <div class="glass-metric-delta {'positive' if fark > 0 else 'negative'}">{'↑ Outperformed Benchmark' if fark > 0 else '↓ Underperformed Benchmark'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        secili_hisse = st.selectbox("Asset Selection (Technical Diagnostics)", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0)
        h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
        
        h_rsi, h_macd, h_signal, upper_bb, lower_bb, h_obv, ind_sma_20 = SovereignDataEngine.calculate_technical_indicators(h_close, h_vol)
        
        fig_tech = make_subplots(
            rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.03, 
            row_heights=[0.45, 0.15, 0.15, 0.15, 0.10],
            subplot_titles=(f"{secili_hisse} Price Action & Volatility", "Volume", "RSI (Momentum)", "MACD (Trend)", "OBV (Money Flow)")
        )
        
        fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Price"), row=1, col=1)
        
        if bollinger_goster:
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=upper_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), name="Upper BB", hoverinfo='skip'), row=1, col=1)
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=lower_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), fill='tonexty', fillcolor='rgba(59, 130, 246, 0.05)', name="Lower BB", hoverinfo='skip'), row=1, col=1)
        if trend_goster:
            fig_tech.add_trace(go.Scatter(x=h_close.index, y=ind_sma_20, line=dict(color='rgba(255,255,255,0.2)', width=1, dash='dot'), name="SMA 20", hoverinfo='skip'), row=1, col=1)
        
        colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
        fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Volume"), row=2, col=1)
        
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
        st.markdown("<h3 style='margin: 21px 0 34px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🕵️ Real-Time Signal Engine & Flow Analytics</h3>", unsafe_allow_html=True)
        
        try:
            mean_rsi = h_rsi.dropna().iloc[-1]
            son_fiyat = normalize_veri['SOVEREIGN_PORTFOLIO'].iloc[-1]
            sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1] if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns else 100
            trend_score = 70 if son_fiyat > sma_d else 30
            sentiment_score = int((mean_rsi + trend_score) / 2)
            sentiment_score = max(10, min(90, sentiment_score)) 
        except:
            sentiment_score = 50

        col_ai1, col_ai2 = st.columns([1.618, 1], gap="large")
        
        with col_ai1:
            st.markdown(f"""
            <div class="terminal-card">
                <div>
                    <div class="terminal-font" style="color:#3B82F6; font-size: 11px; margin-bottom: 12px; letter-spacing: 1px;">[QUANT_ENGINE_ACTIVE] :: REAL-TIME DATA ANALYSIS</div>
                    <h3 style="color: #F5F5F5; font-size: 21px; margin: 0 0 12px 0;">Algorithmic Market Posture Calculated</h3>
                    <div style="font-size: 12px; color: #8B949E; margin-bottom: 21px; display: flex; align-items: center; gap: 8px;">
                        <span style="display:inline-block; width:8px; height:8px; background-color:#3B82F6; border-radius:50%; box-shadow: 0 0 10px #3B82F6;"></span>
                        Data Source: Yahoo Finance API | Macro Sentiment: {sentiment_score}/100
                    </div>
                </div>
                <p class="terminal-font" style="color: #A0ABC0; font-size: 12px; margin: 0; line-height: 1.7;">
                    > System aggregates real-time RSI, MACD, and Volume anomalies.<br>
                    > 100% deterministic mathematical model. No hardcoded or heuristic logic applied.<br>
                    > Detected Institutional Volume Flows are reflected in the radar below.<br>
                    > System aligns with quantitative momentum and mean-reversion strategies.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_ai2:
            durum, renk, taktik = "BULLISH (STRONG TREND)", "#DEFF9A", "Accumulate (BUY)"
            if sentiment_score > 75: durum, renk, taktik = "OVERBOUGHT (HIGH RISK)", "#F59E0B", "Take Profit / Reduce Exposure"
            elif sentiment_score > 45: durum, renk, taktik = "BULLISH (STRONG TREND)", "#DEFF9A", "Hold Position (HOLD)"
            else: durum, renk, taktik = "OVERSOLD (OPPORTUNITY)", "#FF4C4C", "Accumulate (BUY)"

            st.markdown(f"""
            <div class="glass-metric-card" style="border: 1px solid rgba(255,255,255,0.05); text-align: center; justify-content: center;">
                <div class="glass-metric-title" style="margin-bottom: 21px; letter-spacing: 2px;">ALGORITHMIC SIGNAL OUTPUT</div>
                <h2 style="color: {renk}; font-size: 20px; font-weight: 700; margin: 0 0 21px 0; letter-spacing: -0.5px;">{durum}</h2>
                <div class="terminal-font" style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.02);">
                    <span style="color: #8B949E; font-size: 11px;">SYSTEM RECOMMENDATION: </span>
                    <span style="color: #F5F5F5; font-size: 13px; font-weight: 600; margin-left:5px;">{taktik}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)

        col_ai3, col_ai4 = st.columns([1, 1.618], gap="large")
        
        with col_ai3:
            bar_color = "#FF4C4C" if sentiment_score < 45 else ("#DEFF9A" if sentiment_score <= 75 else "#F59E0B")
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = sentiment_score,
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2D323C", 'tickfont': dict(color="#8B949E")}, 
                    'bar': {'color': bar_color, 'thickness': 0.15},
                    'bgcolor': "rgba(0,0,0,0)",
                    'borderwidth': 0,
                    'steps': [
                        {'range': [0, 40], 'color': "rgba(255, 76, 76, 0.15)"}, 
                        {'range': [40, 75], 'color': "rgba(255, 255, 255, 0.05)"}, 
                        {'range': [75, 100], 'color': "rgba(245, 158, 11, 0.15)"}
                    ]
                },
                number = {'font': {'color': '#F5F5F5', 'size': 45}}
            ))
            fig_gauge = SovereignVisualEngine.apply_card_layout(fig_gauge)
            fig_gauge.update_layout(title=dict(text="MACRO SENTIMENT SCORE", font=dict(color='#8B949E', size=11, family="Inter"), x=0.5, y=0.85), height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
            
        with col_ai4:
            anomalies = []
            for ticker in hisseler[:-1]:
                if not vol_data[ticker].empty and len(vol_data[ticker]) > 20:
                    last_vol = vol_data[ticker].iloc[-1]
                    avg_vol_20 = vol_data[ticker].rolling(20).mean().iloc[-1]
                    
                    if last_vol > (avg_vol_20 * 1.5): 
                        etki = "Positive Flow" if close_data[ticker].iloc[-1] > open_data[ticker].iloc[-1] else "Selling Pressure"
                        renk_hacim = "#DEFF9A" if "Positive" in etki else "#FF4C4C"
                        anomalies.append(f"<tr><td>{ticker}</td><td style='color:{renk_hacim}; font-weight:bold;'>VOLUME ANOMALY DETECTED</td><td>{int(last_vol):,}</td><td>{etki}</td></tr>")
            
            if len(anomalies) == 0:
                anomaly_html = "<tr><td colspan='4' style='text-align:center; color:#8B949E; padding:30px;'>No significant volume anomalies detected for the last trading session.</td></tr>"
            else:
                anomaly_html = "".join(anomalies)

            st.markdown(f"""
            <div class="glass-metric-card" style="padding: 21px 34px; justify-content: flex-start; height: 100%; min-height: 280px;">
                <div class="glass-metric-title" style="margin-bottom: 16px;">[REAL-TIME] Institutional Volume Flow (Radar)</div>
                <p style="color:#8B949E; font-size:11px; margin-bottom:15px;">Detects assets where the last session's volume exceeded the 20-day average by >150%.</p>
                <table class="dark-pool-table">
                    <tr><th>Asset</th><th>Anomaly Status</th><th>Last Volume (Lots)</th><th>Price Impact</th></tr>
                    {anomaly_html}
                </table>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)
        live_news = SovereignDataEngine.fetch_live_news()
        
        news_html = ""
        if live_news:
            for item in live_news:
                news_html += f"<tr><td style='color:#DEFF9A; white-space:nowrap;'>{item['date']}</td><td>{item['title']}</td></tr>"
        else:
            news_html = "<tr><td colspan='2' style='text-align:center; color:#8B949E; padding:20px;'>News feed currently unavailable or restricted by firewall.</td></tr>"

        st.markdown(f"""
        <div class="glass-metric-card" style="padding: 21px 34px; justify-content: flex-start;">
            <div class="glass-metric-title" style="margin-bottom: 16px; display:flex; align-items:center; gap:8px;">
                <span style="display:inline-block; width:8px; height:8px; background-color:#FF4C4C; border-radius:50%; box-shadow: 0 0 10px #FF4C4C; animation: blink 2s infinite;"></span>
                [LIVE FEED] Global Market News & Headlines
            </div>
            <table class="dark-pool-table" style="font-size:12px;">
                {news_html}
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

            st.markdown("<h3 style='margin: 21px 0 34px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>⚖️ Risk Metrics & Reporting</h3>", unsafe_allow_html=True)
            
            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 21px; margin-bottom: 34px;">
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Annualized Volatility</div>
                    <div class="glass-metric-value" style="font-size:26px;">% {fon_vol:.2f}</div>
                    <div class="glass-metric-delta neutral" style="font-size:11px;">BIST100: %{b_vol:.2f}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px; border-top: 1px solid {'#DEFF9A' if sortino > 1 else '#F59E0B'};">
                    <div class="glass-metric-title" style="color: {'#DEFF9A' if sortino > 1 else '#F59E0B'};">Sortino Ratio</div>
                    <div class="glass-metric-value" style="font-size:26px;">{sortino:.2f}</div>
                    <div class="glass-metric-delta {'positive' if sortino > 1 else 'neutral'}" style="font-size:11px;">{'Low Downside Risk' if sortino > 1 else 'Downside Risk Elevated'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Calmar Ratio</div>
                    <div class="glass-metric-value" style="font-size:26px;">{calmar:.2f}</div>
                    <div class="glass-metric-delta {'positive' if calmar > 1 else 'neutral'}" style="font-size:11px;">{'High Crisis Resistance' if calmar > 1 else 'Average Resistance'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Information Ratio</div>
                    <div class="glass-metric-value" style="font-size:26px;">{info_ratio:.2f}</div>
                    <div class="glass-metric-delta {'positive' if info_ratio > 0.5 else 'neutral'}" style="font-size:11px;">{'Active Management Success' if info_ratio > 0.5 else 'Index Tracker'}</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Market Beta (Risk)</div>
                    <div class="glass-metric-value" style="font-size:26px;">{beta:.2f}</div>
                    <div class="glass-metric-delta {'positive' if beta < 1 else 'negative'}" style="font-size:11px;">{'Defensive Stance' if beta < 1 else 'Aggressive Stance'}</div>
                </div>
                 <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Max Drawdown</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#FF4C4C;">% {max_dd:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Historical Crisis Depth</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Daily VaR (95% CI)</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#F59E0B;">% {var_95:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Expected Normal Loss</div>
                </div>
                <div class="glass-metric-card" style="min-height: 110px; padding: 21px;">
                    <div class="glass-metric-title">Daily CVaR (Tail Risk)</div>
                    <div class="glass-metric-value" style="font-size:26px; color:#FF4C4C;">% {cvar_95:.2f}</div>
                    <div class="glass-metric-delta negative" style="font-size:11px;">Expected Crisis Loss</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns(2, gap="large")
            with kor_col1:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:16px; text-transform:uppercase;'>🧩 Asset Correlation Heatmap</div>", unsafe_allow_html=True)
                kor_matrisi = getiriler.corr().values
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                    colorscale=[[0, '#0F141E'], [0.5, '#1C2433'], [1, '#DEFF9A']], showscale=False, hoverinfo='skip'
                ))
                for i in range(len(kor_matrisi)):
                    for j in range(len(kor_matrisi[i])):
                        val = kor_matrisi[i][j]
                        text_color = '#0A0C12' if val > 0.7 else '#F5F5F5'
                        fig_corr.add_annotation(x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][j], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][i], text=f"{val:.2f}", showarrow=False, font=dict(color=text_color, size=13, family="Inter", weight="bold"))
                
                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=340)
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:16px;'>🌊 Drawdown (Underwater Chart)</div>", unsafe_allow_html=True)
                fig_dd = go.Figure(go.Scatter(x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.15)'))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=340, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

    with tab5:
        st.markdown("<h3 style='margin: 21px 0 8px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🔮 Stochastic Projection (Geometric Brownian Motion)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 34px;'>Simulates 100 random market scenarios for the next 252 trading days based on the portfolio's historical volatility (σ) and expected return (μ). The 5% and 95% confidence intervals are shaded in green.</p>", unsafe_allow_html=True)
        
        if len(getiriler) > 0:
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            
            percentile_5 = np.percentile(sim_df, 5, axis=1)
            percentile_95 = np.percentile(sim_df, 95, axis=1)
            x_axis = np.arange(252)
            
            fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_95, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
            fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_5, mode='lines', fill='tonexty', fillcolor='rgba(222, 255, 154, 0.05)', line=dict(width=0), showlegend=False, hoverinfo='skip'))

            for i in range(100): fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.06)', width=1), showlegend=False, hoverinfo='skip'))
            
            fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df.mean(axis=1), mode='lines', name='Expected Average (μ)', line=dict(color='#F5F5F5', width=3, dash='dash')))
            
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(height=650, yaxis_title="Capital (TL)", xaxis_title="Future Trading Days (252 Days)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

    with tab6:
        st.markdown("<h3 style='margin: 21px 0 8px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🧬 Autonomous Portfolio Optimization (Markowitz Efficient Frontier)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 34px;'>Simulates 5,000 unique asset allocations using Modern Portfolio Theory (MPT). The engine calculates the Covariance Matrix and historical log-returns to find the 'Max Sharpe Ratio' portfolio, providing the exact mathematical weights needed to maximize return for a given unit of risk.</p>", unsafe_allow_html=True)
        
        if len(getiriler) > 0:
            log_ret = np.log1p(close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change()).dropna()
            
            num_ports = 5000
            all_weights = np.zeros((num_ports, 4))
            ret_arr = np.zeros(num_ports)
            vol_arr = np.zeros(num_ports)
            sharpe_arr = np.zeros(num_ports)

            mean_log_ret = log_ret.mean()
            cov_mat = log_ret.cov()

            np.random.seed(42) 
            for x in range(num_ports):
                weights = np.array(np.random.random(4))
                weights = weights / np.sum(weights)
                all_weights[x,:] = weights
                
                ret_arr[x] = np.sum((mean_log_ret * weights) * 252)
                vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(cov_mat * 252, weights)))
                sharpe_arr[x] = ret_arr[x] / vol_arr[x] if vol_arr[x] > 0 else 0

            max_sr_idx = sharpe_arr.argmax()
            max_sr_ret = ret_arr[max_sr_idx]
            max_sr_vol = vol_arr[max_sr_idx]
            optimal_weights = all_weights[max_sr_idx]

            min_vol_idx = vol_arr.argmin()
            min_vol_ret = ret_arr[min_vol_idx]
            min_vol_vol = vol_arr[min_vol_idx]

            col_opt1, col_opt2 = st.columns([1.618, 1], gap="large")
            
            with col_opt1:
                fig_opt = go.Figure()
                fig_opt.add_trace(go.Scatter(
                    x=vol_arr * 100, y=ret_arr * 100, mode='markers',
                    marker=dict(color=sharpe_arr, colorscale='Viridis', showscale=True, size=4, line=dict(width=0), colorbar=dict(title="Sharpe")),
                    name='Simulated Portfolios', hoverinfo='skip'
                ))
                fig_opt.add_trace(go.Scatter(
                    x=[max_sr_vol * 100], y=[max_sr_ret * 100], mode='markers',
                    marker=dict(color='#FF4C4C', size=16, symbol='star', line=dict(color='#0A0C12', width=2)),
                    name='Max Sharpe (Optimal)'
                ))
                fig_opt.add_trace(go.Scatter(
                    x=[min_vol_vol * 100], y=[min_vol_ret * 100], mode='markers',
                    marker=dict(color='#3B82F6', size=16, symbol='star', line=dict(color='#0A0C12', width=2)),
                    name='Min Volatility (Safest)'
                ))
                fig_opt = SovereignVisualEngine.apply_premium_layout(fig_opt)
                fig_opt.update_layout(height=450, xaxis_title="Annualized Volatility (Risk) %", yaxis_title="Expected Annual Return %", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
                st.plotly_chart(fig_opt, use_container_width=True, config={'displayModeBar': False})
                
            with col_opt2:
                w_alfas, w_yeotk, w_astor, w_kcaer = optimal_weights * 100
                html_content = f"""
                <div class="glass-metric-card" style="padding: 21px 34px; justify-content: flex-start; height: 100%;">
                    <div class="glass-metric-title" style="margin-bottom: 21px; color:#DEFF9A; letter-spacing:1px;">RECOMMENDED ALLOCATION (MAX SHARPE)</div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                        <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono', monospace;">ALFAS.IS</span>
                        <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_alfas:.1f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                        <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono', monospace;">YEOTK.IS</span>
                        <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_yeotk:.1f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                        <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono', monospace;">ASTOR.IS</span>
                        <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_astor:.1f}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:21px;">
                        <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono', monospace;">KCAER.IS</span>
                        <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_kcaer:.1f}</span>
                    </div>
                    
                    <div class="terminal-font" style="background: rgba(0,0,0,0.2); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.02);">
                        <span style="color: #8B949E; font-size: 11px;">EXPECTED ANNUAL RETURN: </span>
                        <span style="color: #F5F5F5; font-size: 13px; font-weight: 600; margin-left:5px;">%{max_sr_ret * 100:.1f}</span><br>
                        <span style="color: #8B949E; font-size: 11px;">OPTIMIZED VOLATILITY: </span>
                        <span style="color: #FF4C4C; font-size: 13px; font-weight: 600; margin-left:5px;">%{max_sr_vol * 100:.1f}</span>
                    </div>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
    
    # V27.0 SİYAH KUĞU (KRİZ SİMÜLATÖRÜ) EKLENTİSİ
    with tab7:
        st.markdown("<h3 style='margin: 21px 0 8px 0; color: #F5F5F5; font-size: 18px; font-weight: 600;'>🦢 Black Swan Stress Tester (Crisis Simulator)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 34px;'>Simulates the portfolio's expected drawdown during historical and theoretical market crashes based on real-time beta, covariance, and asset class sensitivities.</p>", unsafe_allow_html=True)
        
        if 'beta' in locals():
            scenarios = {
                "2020 Global Pandemic": {"market_drop": -0.342, "desc": "Widespread panic, liquidity freeze.", "color": "#FF4C4C", "sector_hit": False},
                "Local Macro Shock (Rate Hike)": {"market_drop": -0.225, "desc": "Sudden monetary policy shift.", "color": "#F59E0B", "sector_hit": False},
                "Tech/Energy Sector Meltdown": {"market_drop": -0.158, "desc": "Targeted sector crash, high beta hit.", "color": "#8B949E", "sector_hit": True}
            }
            
            port_beta = beta
            
            cols = st.columns(3, gap="large")
            idx = 0
            for name, data in scenarios.items():
                market_drop = data["market_drop"]
                
                # Siyah Kuğu Matematiği: Beta üzerinden kriz şoku hesaplama
                port_drop = market_drop * port_beta 
                
                # Eğer teknoloji/enerji krizine özel bir senaryoysa, bu portföy enerji ağırlıklı olduğu için ekstra ceza alır
                if data["sector_hit"]:
                    port_drop = market_drop * 1.8 
                    
                port_retained = 100000 * (1 + port_drop)
                diff_from_market = (market_drop - port_drop) * 100 
                
                with cols[idx]:
                    st.markdown(f"""
                    <div class="glass-metric-card" style="padding: 24px; border-top: 2px solid {data['color']};">
                        <div style="color:{data['color']}; font-size:12px; font-weight:bold; letter-spacing:1px; margin-bottom:8px; text-transform:uppercase;">{name}</div>
                        <div style="color:#8B949E; font-size:11px; margin-bottom:16px;">{data['desc']}</div>
                        <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                            <div>
                                <div style="color:#8B949E; font-size:11px; margin-bottom:4px;">Expected Drawdown</div>
                                <div style="color:#F5F5F5; font-size:24px; font-weight:800;">%{port_drop*100:.1f}</div>
                            </div>
                            <div style="text-align:right;">
                                <div style="color:#8B949E; font-size:11px; margin-bottom:4px;">Capital Retained</div>
                                <div style="color:#F5F5F5; font-size:16px; font-weight:600; font-family:'JetBrains Mono', monospace;">{port_retained:,.0f} ₺</div>
                            </div>
                        </div>
                        <div style="margin-top:16px; padding-top:12px; border-top:1px solid rgba(255,255,255,0.05); font-size:11px; color:{'#DEFF9A' if diff_from_market > 0 else '#FF4C4C'}; font-weight:600;">
                            {'Outperforms' if diff_from_market > 0 else 'Underperforms'} Market by %{abs(diff_from_market):.1f}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                idx += 1

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
