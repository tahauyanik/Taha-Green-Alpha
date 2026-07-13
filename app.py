import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="Sovereign Quant | V18.0 FIBONACCI", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Font ve Uzay Karanlığı Arka Planı */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp { 
    background: #05070A !important;
    background-image: radial-gradient(circle at 50% 0%, #0F141E 0%, #05070A 70%) !important;
}

/* ÇÖP TEMİZLİĞİ VE MENÜ KORUMASI */
[data-testid="stHeader"] { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; }
footer { display: none !important; }
a { pointer-events: none; cursor: default; } /* Kırmızı link ikonlarını öldürür */

/* MENÜ AÇMA TUŞUNU NEON YAP VE GÖRÜNÜR KIL */
[data-testid="collapsedControl"] {
    display: flex !important;
    color: #DEFF9A !important;
    background-color: rgba(15, 20, 30, 0.9) !important;
    border: 1px solid rgba(222, 255, 154, 0.3) !important;
    border-radius: 8px !important;
    box-shadow: 0px 0px 15px rgba(222, 255, 154, 0.1) !important;
    z-index: 99999 !important;
    transition: all 0.3s ease;
}
[data-testid="collapsedControl"]:hover {
    background-color: rgba(222, 255, 154, 0.1) !important;
    border: 1px solid #DEFF9A !important;
    box-shadow: 0px 0px 20px rgba(222, 255, 154, 0.4) !important;
}

/* SEKMELER (TABS) - KUSURSUZ GENTA/FIBONACCI ESTETİĞİ */
.stTabs [data-baseweb="tab-list"] {
    gap: 40px;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    padding-bottom: 0px;
}
.stTabs [data-baseweb="tab"] {
    height: 55px;
    background-color: transparent !important;
    padding: 0px 5px !important;
    color: #6B7280 !important;
    font-weight: 500 !important;
    font-size: 15px !important;
    border: none !important;
    transition: color 0.3s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #A0ABC0 !important;
    background-color: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: #DEFF9A !important;
    background-color: transparent !important; 
    font-weight: 700 !important;
}
/* KALINLAŞTIRILMIŞ VE YUVARLATILMIŞ NEON ALT ÇİZGİ */
div[data-baseweb="tab-highlight"] {
    background-color: #DEFF9A !important;
    height: 3px !important;
    border-radius: 3px 3px 0 0 !important;
}

/* 3D GLASSMORPHISM KARTLAR (TAM ALTIN ORAN: 42/26 = 1.61) */
.glass-metric-card {
    background: linear-gradient(160deg, rgba(20, 25, 35, 0.95) 0%, rgba(10, 12, 18, 0.98) 100%);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-top: 1px solid rgba(222, 255, 154, 0.3);
    border-radius: 16px;
    padding: 26px 42px; /* ALTIN ORAN PADDING */
    box-shadow: 0 15px 35px -10px rgba(0,0,0,0.8);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 150px;
    position: relative;
    overflow: hidden;
}
.glass-metric-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(222, 255, 154, 0.5), transparent);
}
.glass-metric-card:hover {
    transform: translateY(-5px);
    border-top: 1px solid rgba(222, 255, 154, 0.8);
    box-shadow: 0 20px 40px -5px rgba(222, 255, 154, 0.15);
}
.glass-metric-title {
    color: #8B949E;
    font-size: 11px;
    font-weight: 600; /* İNCE VE ZARİF */
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.glass-metric-value {
    color: #F5F5F5;
    font-size: 34px; /* ALTIN ORAN BÜYÜKLÜK */
    font-weight: 800; /* DOMİNANT VE KALIN */
    letter-spacing: -1px;
    margin: 12px 0;
}
.glass-metric-delta.positive { color: #A3FF00; font-size: 13px; font-weight: 600; }
.glass-metric-delta.negative { color: #FF4C4C; font-size: 13px; font-weight: 600; }
.glass-metric-delta.neutral { color: #A0ABC0; font-size: 13px; font-weight: 600; }

/* RÖNTGEN BEYAZ KUTU İMHASI (SELECTBOX) */
.stSelectbox div[data-baseweb="select"] > div {
    background-color: #0F141E !important;
    color: #DEFF9A !important;
    border: 1px solid rgba(222, 255, 154, 0.2) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
.stSelectbox div[data-baseweb="popover"] {
    background-color: #0F141E !important;
    border: 1px solid rgba(222, 255, 154, 0.2) !important;
}
.stSelectbox li {
    background-color: transparent !important;
    color: #F5F5F5 !important;
}
.stSelectbox li:hover {
    background-color: rgba(222, 255, 154, 0.1) !important;
    color: #DEFF9A !important;
}

/* Sidebar Ultra Premium */
[data-testid="stSidebar"] {
    background-color: rgba(8, 10, 15, 0.98) !important;
    border-right: 1px solid rgba(222, 255, 154, 0.05) !important;
}

/* Scrollbar ve Genel Renkler */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #05070A; }
::-webkit-scrollbar-thumb { background: #2D323C; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #DEFF9A; }
h1, h2, h3, h4, p, label, span { color: #F5F5F5; }
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
        histogram = macd - signal_line
        
        return rsi, macd, signal_line, histogram

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
        sharpe_ratio = (excess_returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        
        negative_returns = excess_returns[excess_returns < 0]
        downside_deviation = negative_returns.std() * np.sqrt(252)
        sortino_ratio = (excess_returns.mean() * 252) / downside_deviation if downside_deviation > 0 else 0
        
        cumulative = (1 + returns).cumprod()
        peak = cumulative.cummax()
        drawdown = ((cumulative - peak) / peak) * 100
        max_dd = drawdown.min()
        
        var_95 = np.percentile(returns.dropna() * 100, 5)
        
        return annual_volatility, bench_volatility, sharpe_ratio, sortino_ratio, max_dd, var_95, drawdown, alpha, beta

class SovereignVisualEngine:
    COLORS = {
        'bg': 'rgba(0,0,0,0)', 'grid': 'rgba(255,255,255,0.03)',
        'text': '#8B949E', 'fund': '#DEFF9A', 'bist': '#3B82F6',
        'red': '#FF4C4C', 'orange': '#F59E0B'
    }

    @classmethod
    def apply_premium_layout(cls, fig, title=""):
        fig.update_layout(
            title=dict(text=title, font=dict(color='#F5F5F5', size=15, family="Inter", weight="bold")),
            plot_bgcolor=cls.COLORS['bg'], paper_bgcolor=cls.COLORS['bg'],
            font=dict(color=cls.COLORS['text'], family="Inter"),
            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11, color='#6B7280')),
            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11, color='#6B7280')),
            margin=dict(l=10, r=10, t=40, b=20),
            hovermode='x unified',
            hoverlabel=dict(bgcolor="#0F141E", font_size=13, font_family="Inter", bordercolor="rgba(222,255,154,0.3)")
        )
        return fig

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=40)
st.sidebar.markdown("<h3 style='font-weight: 800; margin-bottom: 0;'>Kontrol Paneli</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 11px; margin-top: 0;'>V18.0 FIBONACCI ARCHITECTURE</p>", unsafe_allow_html=True)

st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600; margin-top:20px;'>Zaman Aralığı</p>", unsafe_allow_html=True)
periyot = st.sidebar.selectbox("", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3, label_visibility="collapsed")

st.sidebar.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #8B949E; font-size: 12px; font-weight: 600;'>🧠 Algoritmik Araçlar</p>", unsafe_allow_html=True)

if 'trend_goster' not in st.session_state: st.session_state.trend_goster = True

trend_goster = st.sidebar.checkbox("Trend Kalkanı (SMA)", value=st.session_state.trend_goster)

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA", 10, 250, 50)

st.markdown("<h1 style='font-size: 38px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px;'>🌍 Taha Uyanık <span style='color: #2D323C;'>|</span> <span style='color: #F5F5F5;'>Ultra Premium Quant Fund</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8B949E; font-size: 14px; margin-bottom: 30px;'>Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V18.0 SUPREMACY)</p>", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    
    if close_data.empty:
        st.error("Veri akışı sağlanamadı. Lütfen internet bağlantınızı kontrol edin.")
        st.stop()
        
    close_data = close_data.ffill().bfill()
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Algoritmik Terminal", 
        "🔬 Röntgen (Derin Analiz)", 
        "🧠 AI İstihbarat Sinyalleri", 
        "⚖️ Kuantum Risk Radarı",
        "🔮 Gelecek Simülasyonu"
    ])

    with tab1:
        st.markdown("<h3 style='margin-bottom: 15px; color: #F5F5F5; font-size: 22px; font-weight: 700;'>Fon Performans Kıyaslaması</h3>", unsafe_allow_html=True)

        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=normalize_veri.index, y=normalize_veri['TAHA_YESIL_FON'], 
            mode='lines', name='Sovereign Yeşil Fon', 
            line=dict(color=SovereignVisualEngine.COLORS['fund'], width=2.5),
            fill='tozeroy', fillcolor='rgba(222, 255, 154, 0.04)'
        ))
        
        fig.add_trace(go.Scatter(
            x=normalize_veri.index, y=normalize_veri['XU100.IS'], 
            mode='lines', name='BIST100 Endeksi', 
            line=dict(color=SovereignVisualEngine.COLORS['bist'], width=1.5)
        ))

        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa} (Hızlı)', line=dict(color=SovereignVisualEngine.COLORS['orange'], width=1, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index, y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun} (Ana)', line=dict(color=SovereignVisualEngine.COLORS['red'], width=1, dash='dot')))

        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), height=450)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        st.markdown("<br><h3 style='margin-bottom: 20px; color: #F5F5F5; font-size: 22px; font-weight: 700;'>💰 100.000 TL Performans Simülasyonu</h3>", unsafe_allow_html=True)
        
        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc
        fon_buyume = ((yesil_sonuc-100000)/100000)*100

        html_cards = f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 20px;">
            <div class="glass-metric-card">
                <div>
                    <div class="glass-metric-title">Klasik BIST100 Getirisi</div>
                    <div class="glass-metric-value">{bist_sonuc:,.0f} ₺</div>
                </div>
                <div class="glass-metric-delta neutral">↑ Referans Endeks</div>
            </div>
            <div class="glass-metric-card">
                <div>
                    <div class="glass-metric-title">Taha Yeşil Fon Getirisi</div>
                    <div class="glass-metric-value">{yesil_sonuc:,.0f} ₺</div>
                </div>
                <div class="glass-metric-delta positive">↑ %{fon_buyume:.1f} Fon Büyümesi</div>
            </div>
            <div class="glass-metric-card">
                <div>
                    <div class="glass-metric-title">Yaratılan ALFA (Ekstra Kâr)</div>
                    <div class="glass-metric-value">{fark:+,.0f} ₺</div>
                </div>
                <div class="glass-metric-delta {'positive' if fark > 0 else 'negative'}">
                    {'↑ Piyasayı Yendi (Alpha)' if fark > 0 else '↓ Piyasaya Yenildi'}
                </div>
            </div>
        </div>
        """
        st.markdown(html_cards, unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3 style='margin-bottom: 15px; color: #F5F5F5; font-size: 22px;'>Teknik Analiz ve İndikatör Röntgeni</h3>", unsafe_allow_html=True)
        secili_hisse = st.selectbox("İncelenecek Hisseyi Seçin", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0, label_visibility="collapsed")
        
        if secili_hisse:
            h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
            h_rsi, h_macd, h_signal, h_hist = SovereignDataEngine.calculate_technical_indicators(h_close)
            
            fig_tech = make_subplots(
                rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03, 
                row_heights=[0.55, 0.15, 0.15, 0.15],
                subplot_titles=(f"{secili_hisse} Fiyat Hareketi", "İşlem Hacmi", "RSI (Göreceli Güç)", "MACD")
            )
            
            for annotation in fig_tech['layout']['annotations']:
                annotation['font'] = dict(size=12, color='#8B949E', family='Inter', weight='bold')
            
            fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Fiyat"), row=1, col=1)
            colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
            fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Hacim"), row=2, col=1)
            
            fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=1.5), name="RSI"), row=3, col=1)
            fig_tech.add_hline(y=70, line_dash="dash", line_color="rgba(255, 76, 76, 0.5)", row=3, col=1)
            fig_tech.add_hline(y=30, line_dash="dash", line_color="rgba(222, 255, 154, 0.5)", row=3, col=1)
            
            fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A', width=1.5), name="MACD"), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C', width=1), name="Sinyal"), row=4, col=1)
            fig_tech.add_trace(go.Bar(x=h_hist.index, y=h_hist, marker_color=['rgba(222, 255, 154, 0.5)' if val >= 0 else 'rgba(255, 76, 76, 0.5)' for val in h_hist], name="Histogram"), row=4, col=1)
            
            fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
            fig_tech.update_layout(height=800, showlegend=False, xaxis_rangeslider_visible=False)
            st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("<h3 style='margin-bottom: 20px; color: #F5F5F5; font-size: 22px;'>🕵️‍♂️ NLP Haber Okuyucusu ve Karar Motoru</h3>", unsafe_allow_html=True)
        col_ai1, col_ai2 = st.columns([2, 1], gap="large")
        
        with col_ai1:
            st.markdown("<p style='color: #8B949E; font-weight: 700; font-size: 11px; letter-spacing: 1.5px;'>SEKTÖREL MAKRO TARAMA</p>", unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-metric-card" style="min-height: auto; padding: 26px 42px; margin-bottom: 20px; border-left: 3px solid #3B82F6;">
                <h4 style="color: #F5F5F5; margin: 0 0 10px 0; font-size: 18px;">Yeşil Enerji Regülasyonları Bekleniyor</h4>
                <div style="font-size: 12px; color: #8B949E; margin-bottom: 15px;">
                    Kaynak: Sovereign Macro AI | Analiz: <span style="background: rgba(59,130,246,0.15); color: #3B82F6; padding: 3px 10px; border-radius: 4px; font-weight: 600;">🔵 BEKLEMEDE (PENDING)</span>
                </div>
                <p style="color: #A0ABC0; font-size: 13px; margin: 0; line-height: 1.6;">Yapay zeka motorumuz spesifik hisse haberi bulamadığında otomatik olarak sektörel makro görünüme odaklanır. Yeşil enerji yatırımları uzun vadeli destek almaktadır.</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='color: #8B949E; font-weight: 700; font-size: 11px; letter-spacing: 1.5px; margin-top:30px;'>GLOBAL MAKRO PUAN (SOVEREIGN GAUGE)</p>", unsafe_allow_html=True)
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = 72, title = {'text': "Piyasa Hissiyatı (Sentiment)", 'font': {'color': '#8B949E', 'size': 13}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#2D323C"}, 
                    'bar': {'color': "#DEFF9A", 'thickness': 0.2},
                    'steps': [{'range': [0, 40], 'color': "rgba(255, 76, 76, 0.15)"}, {'range': [40, 60], 'color': "rgba(255, 255, 255, 0.03)"}, {'range': [60, 100], 'color': "rgba(222, 255, 154, 0.15)"}]
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5', family="Inter"))
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        with col_ai2:
            st.markdown("<p style='color: #8B949E; font-weight: 700; font-size: 11px; letter-spacing: 1.5px;'>ALGORİTMİK TAKTİK</p>", unsafe_allow_html=True)
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Pozisyonu Koru"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla"
            else:
                durum, renk, taktik = "ZIRH KAPALI", "#6B7280", "Trend Kalkanını Açın"

            st.markdown(f"""
            <div class="glass-metric-card" style="height: 100%; border-top: 2px solid {renk}; justify-content: center; text-align: center; min-height: 400px; padding: 42px;">
                <p style="color: #8B949E; font-size: 11px; font-weight: 600; letter-spacing: 2px;">SİSTEM DURUMU</p>
                <h2 style="color: {renk}; font-size: 28px; font-weight: 800; margin: 30px 0;">{durum}</h2>
                <hr style="border-color: rgba(255,255,255,0.05); margin: 40px 0;">
                <p style="color: #8B949E; font-size: 13px; font-weight: 600; margin-bottom: 10px;">Yapay Zeka Tavsiyesi:</p>
                <b style="color: #F5F5F5; font-size: 18px;">{taktik}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("<h3 style='margin-bottom: 20px; color: #F5F5F5; font-size: 22px;'>⚖️ Kantitatif Risk & Raporlama</h3>", unsafe_allow_html=True)
        getiriler = close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change().dropna()
        bist_getiri = close_data['XU100.IS'].pct_change().dropna()
        
        if len(getiriler) > 0:
            portfoy_getiri = getiriler.mean(axis=1)
            fon_vol, b_vol, sharpe, sortino, fon_dd, var_95, drawdown_serisi, alpha, beta = SovereignRiskEngine.calculate_metrics(portfoy_getiri, bist_getiri)

            risk_cards = f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; margin-bottom: 40px;">
                <div class="glass-metric-card">
                    <div>
                        <div class="glass-metric-title">Fon Yıllık Volatilite</div>
                        <div class="glass-metric-value">% {fon_vol:.2f}</div>
                    </div>
                    <div class="glass-metric-delta neutral">BIST100: %{b_vol:.2f}</div>
                </div>
                <div class="glass-metric-card">
                    <div>
                        <div class="glass-metric-title">Maks Düşüş (Drawdown)</div>
                        <div class="glass-metric-value" style="color: #FF4C4C;">{fon_dd:.2f}</div>
                    </div>
                    <div class="glass-metric-delta positive">Tarihsel Kriz Direnci</div>
                </div>
                <div class="glass-metric-card">
                    <div>
                        <div class="glass-metric-title">Piyasa Betası (Risk)</div>
                        <div class="glass-metric-value" style="color: {'#FF4C4C' if beta > 1 else '#F5F5F5'};">{beta:.2f}</div>
                    </div>
                    <div class="glass-metric-delta {'positive' if beta < 1 else 'negative'}">1.0 Altı Defansiftir</div>
                </div>
                <div class="glass-metric-card">
                    <div>
                        <div class="glass-metric-title">Yaratılan Yıllık Alpha</div>
                        <div class="glass-metric-value" style="color: {'#A3FF00' if alpha > 0 else '#FF4C4C'};">% {alpha:.2f}</div>
                    </div>
                    <div class="glass-metric-delta {'positive' if alpha > 0 else 'negative'}">Fon Yönetim Başarısı</div>
                </div>
            </div>
            """
            st.markdown(risk_cards, unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns(2, gap="large")
            with kor_col1:
                st.markdown("<p style='color: #8B949E; font-weight: 700; font-size: 12px; margin-bottom:15px;'>🧩 FON KORELASYON MATRİSİ (RİSK RADARI)</p>", unsafe_allow_html=True)
                kor_matrisi = getiriler.corr().values
                
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                    colorscale=[[0, '#0F141E'], [0.5, '#1C2433'], [1, '#DEFF9A']], 
                    showscale=False, hoverinfo='skip'
                ))
                
                for i in range(len(kor_matrisi)):
                    for j in range(len(kor_matrisi[i])):
                        val = kor_matrisi[i][j]
                        text_col = '#0F141E' if val > 0.7 else '#F5F5F5'
                        fig_corr.add_annotation(
                            x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][j], 
                            y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][i], 
                            text=f"{val:.2f}", showarrow=False, 
                            font=dict(color=text_col, size=13, family="Inter", weight="bold")
                        )

                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=20, l=10, r=10), height=320)
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<p style='color: #8B949E; font-weight: 700; font-size: 12px; margin-bottom:15px;'>🌊 KRİZ DİRENCİ (UNDERWATER / DRAWDOWN)</p>", unsafe_allow_html=True)
                fig_dd = go.Figure(go.Scatter(
                    x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', 
                    line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.15)'
                ))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=320, margin=dict(t=0, b=20, l=10, r=10))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

    with tab5:
        st.markdown("<h3 style='margin-bottom: 10px; color: #F5F5F5; font-size: 22px;'>🔮 Monte Carlo Gelecek Projeksiyonu (1 Yıl)</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 14px; margin-bottom: 30px; line-height: 1.6;'>Geometrik Brownian Hareketi (GBM) kullanılarak, fonun tarihsel volatilitesi (risk) üzerinden önümüzdeki 1 iş yılı (252 gün) için 100 farklı rastgele matematiksel senaryo hesaplanmıştır.</p>", unsafe_allow_html=True)
        
        if len(getiriler) > 0:
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            for i in range(100): 
                fig_mc.add_trace(go.Scatter(y=sim_df[:, i], mode='lines', line=dict(color='rgba(222, 255, 154, 0.1)', width=1), showlegend=False, hoverinfo='skip'))
            
            fig_mc.add_trace(go.Scatter(y=sim_df.mean(axis=1), mode='lines', name='Beklenen Ortalama', line=dict(color='#F5F5F5', width=3, dash='dash')))
            
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(height=600, xaxis_title="Gelecek Günler (1 İş Yılı)", yaxis_title="Sermaye (TL)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
