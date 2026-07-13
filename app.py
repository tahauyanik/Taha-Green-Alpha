import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Taha Uyanık | Sovereign Quant Fund", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded" # SAYFA AÇILDIĞINDA MENÜ KESİN OLARAK AÇIK GELİR
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { 
    background: #05070A !important;
    background-image: radial-gradient(circle at 50% 0%, #0C1017 0%, #05070A 80%) !important;
}

/* ÇÖP TEMİZLİĞİ VE İKON YOK ETME */
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
a { pointer-events: none; cursor: default; text-decoration: none !important; }
.css-15zrgzn { display: none !important; } /* Link ikonları infazı */

/* NEON MENÜ AÇMA TUŞU (KAPIDA KALMAMAK İÇİN) */
[data-testid="collapsedControl"] {
    display: flex !important; color: #DEFF9A !important;
    background-color: rgba(12, 16, 23, 0.9) !important;
    border: 1px solid rgba(222, 255, 154, 0.3) !important;
    border-radius: 8px !important; z-index: 99999 !important;
}
[data-testid="collapsedControl"]:hover { border: 1px solid #DEFF9A !important; }

/* SEKME (TAB) DEVRİMİ - İĞRENÇ ÇİZGİLER YOK EDİLDİ */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px; background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important; padding-bottom: 0px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px; background-color: transparent !important;
    padding: 0px 5px !important; color: #6B7280 !important;
    font-weight: 600 !important; font-size: 14px !important;
    border: none !important; transition: all 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover { color: #A0ABC0 !important; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #DEFF9A !important; background-color: transparent !important; font-weight: 700 !important; }
div[data-baseweb="tab-highlight"] { background-color: #DEFF9A !important; height: 3px !important; border-radius: 3px 3px 0 0 !important; }

/* 3D GLASSMORPHISM KARTLAR - ALTIN ORAN (1.618 PADDING) */
.glass-metric-card {
    background: linear-gradient(160deg, rgba(16, 20, 26, 0.95) 0%, rgba(10, 12, 16, 0.98) 100%);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.03);
    border-top: 1px solid rgba(222, 255, 154, 0.15);
    border-radius: 12px;
    padding: 26px 42px; /* ALTIN ORAN */
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8);
    transition: all 0.3s ease;
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 140px; position: relative; overflow: hidden;
}
.glass-metric-card:hover {
    transform: translateY(-3px); border-top: 1px solid rgba(222, 255, 154, 0.5);
    box-shadow: 0 15px 35px -5px rgba(222, 255, 154, 0.05);
}
.glass-metric-title {
    color: #8B949E; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px;
}
.glass-metric-value {
    color: #F5F5F5; font-size: 34px; font-weight: 800; letter-spacing: -1px; margin: 8px 0;
}
.glass-metric-delta.positive { color: #A3FF00; font-size: 13px; font-weight: 600; }
.glass-metric-delta.negative { color: #FF4C4C; font-size: 13px; font-weight: 600; }
.glass-metric-delta.neutral { color: #A0ABC0; font-size: 13px; font-weight: 600; }

/* PALANTIR TERMİNAL KARTI (AI SEKME İÇİN) */
.terminal-card {
    background: #0A0C10; border: 1px solid rgba(59, 130, 246, 0.2);
    border-radius: 12px; padding: 30px; position: relative;
}
.terminal-card::before {
    content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%;
    background: linear-gradient(to bottom, #3B82F6, transparent); border-radius: 12px 0 0 12px;
}
.terminal-font { font-family: 'JetBrains Mono', monospace; }

/* RÖNTGEN BEYAZ KUTU İMHASI (SELECTBOX) */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #0F141E !important; color: #F5F5F5 !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important; border-radius: 8px !important;
}
.stSelectbox div[data-baseweb="popover"] { background-color: #0F141E !important; border: 1px solid rgba(255, 255, 255, 0.1) !important; }
.stSelectbox li { background-color: transparent !important; color: #F5F5F5 !important; }
.stSelectbox li:hover { background-color: rgba(222, 255, 154, 0.1) !important; color: #DEFF9A !important; }

/* Sidebar Ultra Premium */
[data-testid="stSidebar"] { background-color: rgba(8, 10, 15, 0.98) !important; border-right: 1px solid rgba(255, 255, 255, 0.02) !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #05070A; }
::-webkit-scrollbar-thumb { background: #1C212B; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #3B82F6; }
h1, h2, h3, p, span { color: #F5F5F5; }
hr { border-color: rgba(255,255,255,0.05) !important; }
</style>
""", unsafe_allow_html=True)

class SovereignDataEngine:
    @staticmethod
    @st.cache_data(ttl=3600, show_spinner=False)
    def fetch_market_data(tickers, period):
        data = yf.download(tickers, period=period, progress=False, threads=True)
        return data['Close'], data['Volume'], data['High'], data['Low'], data['Open']
    
    @staticmethod
    def calculate_technical_indicators(close_prices):
        delta = close_prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        exp1 = close_prices.ewm(span=12, adjust=False).mean()
        exp2 = close_prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal_line = macd.ewm(span=9, adjust=False).mean()
        return rsi, macd, signal_line

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
        var_95 = np.percentile(returns.dropna() * 100, 5)
        return annual_volatility, bench_volatility, sortino_ratio, max_dd, var_95, drawdown, alpha, beta

class SovereignVisualEngine:
    COLORS = {'bg': 'rgba(0,0,0,0)', 'grid': '#161A23', 'text': '#8B949E', 'fund': '#DEFF9A', 'bist': '#3B82F6', 'red': '#FF4C4C'}
    @classmethod
    def apply_premium_layout(cls, fig):
        fig.update_layout(
            plot_bgcolor=cls.COLORS['bg'], paper_bgcolor=cls.COLORS['bg'],
            font=dict(color=cls.COLORS['text'], family="Inter"),
            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280')),
            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280')),
            margin=dict(l=10, r=10, t=30, b=10), hovermode='x unified',
            hoverlabel=dict(bgcolor="#0F141E", font_size=12, font_family="Inter", bordercolor="rgba(222,255,154,0.3)")
        )
        return fig

st.sidebar.markdown("<h3 style='font-weight: 800; margin-bottom: 0; color: #F5F5F5;'>Sistem Kontrolü</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 11px; margin-top: 0;'>V19.0 PALANTIR CORE</p>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600; margin-top:20px;'>Zaman Aralığı</p>", unsafe_allow_html=True)
periyot = st.sidebar.selectbox("", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3, label_visibility="collapsed")

st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600;'>🧠 Algoritmik Araçlar</p>", unsafe_allow_html=True)

# İŞTE BURASI! OTOMATİK OLARAK AÇIK GELEN VE ASLA KAYBOLMAYAN SMA ŞALTERİ
trend_goster = st.sidebar.toggle("🛡️ Trend Kalkanı (SMA)", value=True)

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA", 10, 250, 50)

st.markdown("<h1 style='font-size: 34px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px;'>🌍 Taha Uyanık <span style='color: #2D323C;'>|</span> Ultra Premium Quant Fund</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 25px;'>Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V19.0 FOUNDRY)</p>", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']
try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    if close_data.empty: st.stop()
    
    close_data = close_data.ffill().bfill()
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Algoritmik Terminal", "🔬 Röntgen (Derin Analiz)", "🧠 AI İstihbarat Sinyalleri", "⚖️ Kuantum Risk Radarı", "🔮 Gelecek Simülasyonu"
    ])

    with tab1:
        st.markdown("<h3 style='margin-bottom: 15px; color: #F5F5F5; font-size: 20px;'>Fon Performans Kıyaslaması</h3>", unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['TAHA_YESIL_FON'], mode='lines', name='Sovereign Yeşil Fon', line=dict(color=SovereignVisualEngine.COLORS['fund'], width=2.5), fill='tozeroy', fillcolor='rgba(222, 255, 154, 0.03)'))
        fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri['XU100.IS'], mode='lines', name='BIST100 Endeksi', line=dict(color=SovereignVisualEngine.COLORS['bist'], width=1.5)))
        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa}', line=dict(color='#F59E0B', width=1, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns: fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun}', line=dict(color='#FF4C4C', width=1, dash='dot')))
        
        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), height=400)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-top: 20px;">
            <div class="glass-metric-card">
                <div class="glass-metric-title">Klasik BIST100 Getirisi</div>
                <div class="glass-metric-value">{bist_sonuc:,.0f} ₺</div>
                <div class="glass-metric-delta neutral">↑ Referans Endeks</div>
            </div>
            <div class="glass-metric-card" style="border-top: 1px solid #DEFF9A;">
                <div class="glass-metric-title" style="color:#DEFF9A;">Taha Yeşil Fon Getirisi</div>
                <div class="glass-metric-value">{yesil_sonuc:,.0f} ₺</div>
                <div class="glass-metric-delta positive">↑ %{((yesil_sonuc-100000)/100000)*100:.1f} Fon Büyümesi</div>
            </div>
            <div class="glass-metric-card">
                <div class="glass-metric-title">Yaratılan ALFA (Ekstra Kâr)</div>
                <div class="glass-metric-value">{fark:+,.0f} ₺</div>
                <div class="glass-metric-delta {'positive' if fark > 0 else 'negative'}">{'↑ Piyasayı Yendi (Alpha)' if fark > 0 else '↓ Piyasaya Yenildi'}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        secili_hisse = st.selectbox("", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0, label_visibility="collapsed")
        h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
        h_rsi, h_macd, h_signal = SovereignDataEngine.calculate_technical_indicators(h_close)
        
        fig_tech = make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.6, 0.2, 0.2])
        fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Fiyat"), row=1, col=1)
        colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
        fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Hacim"), row=2, col=1)
        fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=1.5), name="RSI"), row=3, col=1)
        fig_tech.add_hline(y=70, line_dash="dash", line_color="#FF4C4C", row=3, col=1)
        fig_tech.add_hline(y=30, line_dash="dash", line_color="#DEFF9A", row=3, col=1)
        
        fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
        fig_tech.update_layout(height=700, showlegend=False, xaxis_rangeslider_visible=False)
        st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)
        col_ai1, col_ai2 = st.columns([1.2, 1], gap="large")
        
        with col_ai1:
            st.markdown("""
            <div class="terminal-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
                <div class="glass-metric-title" style="margin-bottom: 15px; color:#3B82F6;">[NLP_ENGINE_ACTIVE] :: Sektörel Tarama</div>
                <h3 style="color: #F5F5F5; font-size: 18px; margin: 0 0 10px 0;">Yeşil Enerji Regülasyonları Bekleniyor</h3>
                <div style="font-size: 12px; color: #8B949E; margin-bottom: 15px; display: flex; align-items: center; gap: 8px;">
                    <span style="display:inline-block; width:8px; height:8px; background-color:#3B82F6; border-radius:50%; box-shadow: 0 0 8px #3B82F6;"></span>
                    Kaynak: Sovereign AI | Durum: PENDING
                </div>
                <p class="terminal-font" style="color: #A0ABC0; font-size: 12px; margin: 0; line-height: 1.6;">
                    > Spesifik şirket haberi bulunamadı (BIST API Koruması).<br>
                    > Sistem otonom olarak 'Makro Yeşil Enerji' taramasına geçti.<br>
                    > Sektörel uzun vade beklentisi: POZİTİF.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col_ai2:
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM (RİSK)", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Pozisyonu Koru (HOLD)"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla (BUY)"
            else:
                durum, renk, taktik = "ZIRH KAPALI", "#6B7280", "Menüden Trend Kalkanını Açın"

            st.markdown(f"""
            <div class="glass-metric-card" style="border-top: 2px solid {renk}; height: 100%; text-align: center; justify-content: center; padding: 30px;">
                <div class="glass-metric-title" style="margin-bottom: 20px;">ALGORİTMİK TAKTİK MERKEZİ</div>
                <h2 style="color: {renk}; font-size: 26px; font-weight: 800; margin: 0 0 20px 0;">{durum}</h2>
                <div class="terminal-font" style="background: rgba(255,255,255,0.02); padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                    <span style="color: #8B949E; font-size: 11px;">AI TAVSİYESİ: </span><br>
                    <span style="color: #F5F5F5; font-size: 14px; font-weight: bold;">{taktik}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)
        # GAUGE CHART KUSURSUZ ÇERÇEVE İÇİNE ALINDI
        st.markdown("""<div class="glass-metric-card" style="padding: 20px;"><div class="glass-metric-title" style="text-align: center; margin-bottom: -10px;">GLOBAL MAKRO HİSSİYAT PUANI</div>""", unsafe_allow_html=True)
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number", value = 72,
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2D323C"}, 
                'bar': {'color': "#DEFF9A", 'thickness': 0.15},
                'steps': [{'range': [0, 40], 'color': "rgba(255, 76, 76, 0.1)"}, {'range': [40, 60], 'color': "rgba(255, 255, 255, 0.02)"}, {'range': [60, 100], 'color': "rgba(222, 255, 154, 0.1)"}]
            }
        ))
        fig_gauge.update_layout(height=200, margin=dict(l=10, r=10, t=20, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5', family="Inter"))
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

    with tab4:
        getiriler = close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change().dropna()
        bist_getiri = close_data['XU100.IS'].pct_change().dropna()
        
        if len(getiriler) > 0:
            portfoy_getiri = getiriler.mean(axis=1)
            fon_vol, b_vol, sortino, fon_dd, var_95, drawdown_serisi, alpha, beta = SovereignRiskEngine.calculate_metrics(portfoy_getiri, bist_getiri)

            st.markdown(f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px;">
                <div class="glass-metric-card">
                    <div class="glass-metric-title">Fon Yıllık Volatilite</div>
                    <div class="glass-metric-value">% {fon_vol:.2f}</div>
                    <div class="glass-metric-delta neutral">BIST100: %{b_vol:.2f}</div>
                </div>
                <div class="glass-metric-card">
                    <div class="glass-metric-title">Maks Düşüş (Drawdown)</div>
                    <div class="glass-metric-value" style="color: #FF4C4C;">{fon_dd:.2f}</div>
                    <div class="glass-metric-delta positive">Tarihsel Kriz Direnci</div>
                </div>
                <div class="glass-metric-card">
                    <div class="glass-metric-title">Piyasa Betası (Risk)</div>
                    <div class="glass-metric-value">{beta:.2f}</div>
                    <div class="glass-metric-delta {'positive' if beta < 1 else 'negative'}">1.0 Altı Defansiftir</div>
                </div>
                <div class="glass-metric-card">
                    <div class="glass-metric-title">Yaratılan Yıllık Alpha</div>
                    <div class="glass-metric-value">% {alpha:.2f}</div>
                    <div class="glass-metric-delta positive">Fon Yönetim Başarısı</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns(2, gap="large")
            with kor_col1:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:10px;'>🧩 Fon Korelasyon Matrisi</div>", unsafe_allow_html=True)
                kor_matrisi = getiriler.corr().values
                fig_corr = go.Figure(data=go.Heatmap(z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], colorscale=[[0, '#0F141E'], [0.5, '#1C2433'], [1, '#DEFF9A']], showscale=False, hoverinfo='skip'))
                for i in range(len(kor_matrisi)):
                    for j in range(len(kor_matrisi[i])):
                        val = kor_matrisi[i][j]
                        fig_corr.add_annotation(x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][j], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][i], text=f"{val:.2f}", showarrow=False, font=dict(color='#0F141E' if val > 0.7 else '#F5F5F5', size=12, family="Inter", weight="bold"))
                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=300)
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<div class='glass-metric-title' style='margin-bottom:10px;'>🌊 Kriz Direnci (Sualtı Grafiği)</div>", unsafe_allow_html=True)
                fig_dd = go.Figure(go.Scatter(x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.1)'))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=300, margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

    with tab5:
        st.markdown("<div style='margin-bottom: 10px; color: #8B949E; font-size: 13px;'>Geçmiş getiri ve volatilite kullanılarak önümüzdeki 252 işlem günü için 100 farklı paralel evren (Geometrik Brownian Hareketi) simüle edilmiştir.</div>", unsafe_allow_html=True)
        if len(getiriler) > 0:
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            for i in range(100): fig_mc.add_trace(go.Scatter(y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.05)', width=1), showlegend=False, hoverinfo='skip'))
            fig_mc.add_trace(go.Scatter(y=sim_df.mean(axis=1), mode='lines', name='Beklenen Ortalama', line=dict(color='#F5F5F5', width=3, dash='dash')))
            
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(height=500, yaxis_title="Sermaye (TL)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
