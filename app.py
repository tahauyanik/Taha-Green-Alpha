import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime

st.set_page_config(
    page_title="Sovereign Quant | V14.0 GOD MODE", 
    page_icon="🌍", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Font ve Uzay Karanlığı Arka Planı */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}
.stApp { 
    background: #05070A !important;
    background-image: radial-gradient(circle at 50% 0%, #0F141E 0%, #05070A 70%) !important;
}

/* ÇÖP TEMİZLİĞİ: Header, Footer, Sağ Üst İkonlar, Başlık Zincirleri */
header { background-color: transparent !important; }
[data-testid="stToolbar"] { display: none !important; } 
footer { display: none !important; }
.css-1nhreja, .css-1e6lza2, a.css-1a22dnu { display: none !important; pointer-events: none !important; }
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a { display: none !important; }

/* SEKMELER (TABS) - KUSURSUZ ZIRH */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px;
    background-color: transparent !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    padding-bottom: 5px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    background-color: transparent !important;
    padding: 0px 10px;
    color: #6B7280 !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    border: none !important;
    transition: all 0.3s ease;
}
.stTabs [aria-selected="true"] {
    color: #DEFF9A !important;
    background-color: transparent !important; 
}
div[data-baseweb="tab-highlight"] {
    background-color: #DEFF9A !important;
    height: 3px !important;
    border-radius: 3px !important;
}

/* SAF HTML METRİK KARTLARI (STREAMLIT'İ DEVRE DIŞI BIRAKTIK) */
.glass-metric-card {
    background: rgba(15, 20, 30, 0.6);
    backdrop-filter: blur(15px);
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(222, 255, 154, 0.1);
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8);
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.glass-metric-card:hover {
    transform: translateY(-8px);
    border: 1px solid rgba(222, 255, 154, 0.4);
    box-shadow: 0 20px 40px -10px rgba(222, 255, 154, 0.15);
}
.glass-metric-title {
    color: #8B949E;
    font-size: 13px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}
.glass-metric-value {
    color: #F5F5F5;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 5px;
}
.glass-metric-delta.positive { color: #A3FF00; font-size: 15px; font-weight: 700; }
.glass-metric-delta.negative { color: #FF4C4C; font-size: 15px; font-weight: 700; }
.glass-metric-delta.neutral { color: #A0ABC0; font-size: 15px; font-weight: 700; }

/* BEYAZ SEÇİM KUTUSU İMHASI (SELECTBOX) */
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
    background-color: rgba(10, 13, 18, 0.95) !important;
    border-right: 1px solid rgba(222, 255, 154, 0.05) !important;
}

/* Scrollbar ve Genel Renkler */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #05070A; }
::-webkit-scrollbar-thumb { background: #2D323C; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #DEFF9A; }
h1, h2, h3, h4, p, label, span { color: #F5F5F5; }
hr { border-color: rgba(255,255,255,0.05) !important; }
</style>
""", unsafe_allow_html=True)

class SovereignDataEngine:
    """Piyasa verilerini çeken ve teknik indikatörleri hesaplayan motor."""
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
    """Gelişmiş hedge fund risk metriklerini hesaplar."""
    @staticmethod
    def calculate_metrics(returns, risk_free_rate=0.40):
        rf_daily = risk_free_rate / 252
        annual_volatility = returns.std() * np.sqrt(252) * 100
        
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
        
        return annual_volatility, sharpe_ratio, sortino_ratio, max_dd, var_95, drawdown

class SovereignVisualEngine:
    COLORS = {
        'bg': 'rgba(0,0,0,0)', 'grid': 'rgba(255,255,255,0.02)',
        'text': '#A0ABC0', 'fund': '#DEFF9A', 'bist': '#3B82F6',
        'red': '#FF4C4C', 'orange': '#F59E0B'
    }

    @classmethod
    def apply_premium_layout(cls, fig, title=""):
        fig.update_layout(
            title=dict(text=title, font=dict(color='#F5F5F5', size=18, family="Inter")),
            plot_bgcolor=cls.COLORS['bg'], paper_bgcolor=cls.COLORS['bg'],
            font=dict(color=cls.COLORS['text'], family="Inter"),
            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11)),
            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=11)),
            margin=dict(l=10, r=10, t=40, b=20),
            hovermode='x unified',
            hoverlabel=dict(bgcolor="#0F141E", font_size=13, font_family="Inter", bordercolor="rgba(222,255,154,0.3)")
        )
        return fig

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=50)
st.sidebar.markdown("<h2 style='font-weight: 800; margin-bottom: 0;'>Sovereign Terminal</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #6B7280; font-size: 12px; margin-top: 0;'>V14.0 GOD MODE ARCHITECTURE</p>", unsafe_allow_html=True)
st.sidebar.markdown("<hr>", unsafe_allow_html=True)

st.sidebar.markdown("### ⚙️ Zaman Makinesi")
periyot = st.sidebar.selectbox("Analiz Periyodu:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"], index=3)

st.sidebar.markdown("<hr>", unsafe_allow_html=True)

# Kaybolma krizini çözen Kırılmaz Checkbox Zırhı
trend_goster = st.sidebar.checkbox("🛡️ Algoritmik Zırh (SMA)", value=True)

sma_kisa, sma_uzun = 20, 50
if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA (Hızlı Trend)", 5, 100, 20)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA (Ana Trend)", 10, 250, 50)

st.markdown("<h1 style='font-size: 42px; letter-spacing: -1px;'>🌍 Taha Uyanık <span style='color: #2D323C;'>|</span> <span style='color: #DEFF9A;'>Ultra Premium Quant Fund</span></h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #8B949E; font-size: 16px; margin-bottom: 20px;'>Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi (V14.0 GOD MODE)</p>", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, periyot)
    
    if close_data.empty:
        st.error("Veri akışı sağlanamadı. Bağlantıyı kontrol edin.")
        st.stop()
        
    close_data = close_data.ffill().bfill()
    ilk_satir = close_data.iloc[0].replace(0, 0.0001)
    normalize_veri = (close_data / ilk_satir) * 100
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        if len(normalize_veri) >= sma_kisa: normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        if len(normalize_veri) >= sma_uzun: normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Algoritmik Terminal", 
        "🔬 Röntgen (Derin Analiz)", 
        "🧠 AI İstihbarat Sinyalleri", 
        "🧩 Kuantum Risk & Monte Carlo"
    ])

    with tab1:
        st.markdown("<h3 style='margin-bottom: 15px;'>📊 Fon Performans Kıyaslaması</h3>", unsafe_allow_html=True)

        fig = go.Figure()
        
        # Premium Area Chart (Altı Dolgulu)
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['TAHA_YESIL_FON'], 
            mode='lines', name='Sovereign Yeşil Fon', 
            line=dict(color=SovereignVisualEngine.COLORS['fund'], width=3),
            fill='tozeroy', fillcolor='rgba(222, 255, 154, 0.08)'
        ))
        
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['XU100.IS'], 
            mode='lines', name='BIST100 Endeksi', 
            line=dict(color=SovereignVisualEngine.COLORS['bist'], width=2)
        ))

        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'], mode='lines', name=f'SMA {sma_kisa}', line=dict(color=SovereignVisualEngine.COLORS['orange'], width=1.5, dash='dot')))
            if f'SMA_{sma_uzun}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'], mode='lines', name=f'SMA {sma_uzun}', line=dict(color=SovereignVisualEngine.COLORS['red'], width=1.5, dash='dot')))

        fig = SovereignVisualEngine.apply_premium_layout(fig)
        fig.update_layout(legend=dict(orientation="h", yanchor="top", y=-0.1, xanchor="center", x=0.5), height=450)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) 

        st.markdown("<br><h3 style='margin-bottom: 20px;'>💰 100.000 TL Performans Simülasyonu</h3>", unsafe_allow_html=True)
        
        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc
        fon_buyume = ((yesil_sonuc-100000)/100000)*100

        # GERÇEK HTML/CSS CAM KARTLAR (Streamlit metric çöpünü bıraktık)
        html_cards = f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px;">
            <div class="glass-metric-card">
                <div class="glass-metric-title">Klasik BIST100 Getirisi</div>
                <div class="glass-metric-value">{bist_sonuc:,.0f} ₺</div>
                <div class="glass-metric-delta neutral">↑ Referans Endeks</div>
            </div>
            <div class="glass-metric-card">
                <div class="glass-metric-title">Taha Yeşil Fon Getirisi</div>
                <div class="glass-metric-value" style="color: #DEFF9A;">{yesil_sonuc:,.0f} ₺</div>
                <div class="glass-metric-delta positive">↑ %{fon_buyume:.1f} Fon Büyümesi</div>
            </div>
            <div class="glass-metric-card">
                <div class="glass-metric-title">Yaratılan ALFA (Ekstra Kâr)</div>
                <div class="glass-metric-value">{fark:+,.0f} ₺</div>
                <div class="glass-metric-delta {'positive' if fark > 0 else 'negative'}">
                    {'↑ Piyasayı Yendi (Alpha)' if fark > 0 else '↓ Piyasaya Yenildi'}
                </div>
            </div>
        </div>
        """
        st.markdown(html_cards, unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3 style='margin-bottom: 15px;'>🔬 Teknik Analiz ve İndikatör Röntgeni</h3>", unsafe_allow_html=True)
        secili_hisse = st.selectbox("İncelenecek Hisseyi Seçin", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0)
        
        if secili_hisse:
            h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
            h_rsi, h_macd, h_signal, h_hist = SovereignDataEngine.calculate_technical_indicators(h_close)
            
            fig_tech = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.5, 0.15, 0.15, 0.2])
            
            # Candlestick
            fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Fiyat"), row=1, col=1)
            
            # Volume
            colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
            fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Hacim"), row=2, col=1)
            
            # RSI
            fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=2), name="RSI"), row=3, col=1)
            fig_tech.add_hline(y=70, line_dash="dash", line_color="rgba(255, 76, 76, 0.5)", row=3, col=1)
            fig_tech.add_hline(y=30, line_dash="dash", line_color="rgba(222, 255, 154, 0.5)", row=3, col=1)
            
            # MACD
            fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A', width=1.5), name="MACD"), row=4, col=1)
            fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C', width=1.5), name="Sinyal"), row=4, col=1)
            fig_tech.add_trace(go.Bar(x=h_hist.index, y=h_hist, marker_color=['rgba(222, 255, 154, 0.5)' if val >= 0 else 'rgba(255, 76, 76, 0.5)' for val in h_hist], name="Histogram"), row=4, col=1)
            
            fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
            fig_tech.update_layout(height=800, showlegend=False, xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=20, b=20))
            st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("<h3 style='margin-bottom: 20px;'>🕵️‍♂️ NLP Haber Okuyucusu ve Karar Motoru</h3>", unsafe_allow_html=True)
        col_ai1, col_ai2 = st.columns([2, 1])
        
        with col_ai1:
            st.markdown("<p style='color: #6B7280; font-weight: 600; font-size: 14px;'>Sektörel Makro Tarama</p>", unsafe_allow_html=True)
            st.markdown("""
            <div class="glass-metric-card" style="margin-bottom: 20px; border-left: 4px solid #3B82F6;">
                <h4 style="color: #F5F5F5; margin: 0 0 10px 0;">Yeşil Enerji Regülasyonları Bekleniyor</h4>
                <div style="font-size: 13px; color: #8B949E; margin-bottom: 10px;">
                    Kaynak: Sovereign Macro AI | Analiz: <span style="background: rgba(59,130,246,0.2); color: #3B82F6; padding: 3px 8px; border-radius: 12px; font-weight: bold;">🔵 BEKLEMEDE (PENDING)</span>
                </div>
                <p style="color: #A0ABC0; font-size: 14px; margin: 0;">Yapay zeka motorumuz spesifik hisse haberi bulamadığında (BIST API kısıtlamaları), otomatik olarak sektörel makro görünüme odaklanır.</p>
            </div>
            """, unsafe_allow_html=True)
            
            fig_gauge = go.Figure(go.Indicator(
                mode = "gauge+number", value = 72, title = {'text': "Piyasa Hissiyatı (Sentiment)", 'font': {'color': '#8B949E', 'size': 14}},
                gauge = {
                    'axis': {'range': [None, 100], 'tickcolor': "#2D323C"}, 
                    'bar': {'color': "#DEFF9A", 'thickness': 0.3},
                    'steps': [{'range': [0, 40], 'color': "rgba(255, 76, 76, 0.1)"}, {'range': [40, 60], 'color': "rgba(255, 255, 255, 0.02)"}, {'range': [60, 100], 'color': "rgba(222, 255, 154, 0.1)"}]
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=30, b=10), paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5', family="Inter"))
            st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False})

        with col_ai2:
            st.markdown("<p style='color: #6B7280; font-weight: 600; font-size: 14px;'>🤖 Algoritmik Taktik</p>", unsafe_allow_html=True)
            son_fiyat = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_d = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat > sma_d * 1.10: durum, renk, taktik = "AŞIRI ALIM (RİSK)", "#F59E0B", "Kâr Al / Nakite Geç"
                elif son_fiyat > sma_d: durum, renk, taktik = "GÜÇLÜ TREND", "#DEFF9A", "Pozisyonu Koru (Hold)"
                else: durum, renk, taktik = "DÜŞÜŞ FIRSATI", "#FF4C4C", "Kademeli Topla"
            else:
                durum, renk, taktik = "ZIRH KAPALI", "#6B7280", "Trend Kalkanını Açın"

            st.markdown(f"""
            <div class="glass-metric-card" style="height: 100%; border: 1px solid {renk}50; text-align: center; justify-content: center;">
                <p style="color: #8B949E; font-size: 11px; letter-spacing: 2px;">SİSTEM DURUMU</p>
                <h2 style="color: {renk}; font-size: 26px; font-weight: 800; margin: 15px 0;">{durum}</h2>
                <hr style="border-color: rgba(255,255,255,0.05); margin: 20px 0;">
                <p style="color: #6B7280; font-size: 13px; margin-bottom: 5px;">Yapay Zeka Tavsiyesi:</p>
                <b style="color: #F5F5F5; font-size: 16px;">{taktik}</b>
            </div>
            """, unsafe_allow_html=True)

    with tab4:
        st.markdown("<h3 style='margin-bottom: 20px;'>⚖️ Kantitatif Risk & Raporlama</h3>", unsafe_allow_html=True)
        getiriler = close_data.pct_change().dropna()
        
        if len(getiriler) > 0:
            portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)
            fon_vol, sharpe, sortino, fon_dd, var_95, drawdown_serisi = SovereignRiskEngine.calculate_metrics(portfoy_getiri)

            # Saf HTML Risk Kartları
            risk_cards = f"""
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px;">
                <div class="glass-metric-card" style="padding: 15px;">
                    <div class="glass-metric-title">Fon Yıllık Volatilite</div>
                    <div class="glass-metric-value" style="font-size: 24px;">%{fon_vol:.2f}</div>
                </div>
                <div class="glass-metric-card" style="padding: 15px;">
                    <div class="glass-metric-title">Sortino Oranı</div>
                    <div class="glass-metric-value" style="font-size: 24px; color: {'#DEFF9A' if sortino > 1 else '#F5F5F5'};">{sortino:.2f}</div>
                </div>
                <div class="glass-metric-card" style="padding: 15px;">
                    <div class="glass-metric-title">Maks Düşüş (Drawdown)</div>
                    <div class="glass-metric-value" style="font-size: 24px; color: #FF4C4C;">%{fon_dd:.2f}</div>
                </div>
                <div class="glass-metric-card" style="padding: 15px;">
                    <div class="glass-metric-title">Günlük VaR (%95)</div>
                    <div class="glass-metric-value" style="font-size: 24px; color: #F59E0B;">%{var_95:.2f}</div>
                </div>
            </div>
            """
            st.markdown(risk_cards, unsafe_allow_html=True)
            
            kor_col1, kor_col2 = st.columns([1, 1])
            with kor_col1:
                st.markdown("<p style='color: #F5F5F5; font-weight: 600;'>🧩 Fon Korelasyon Matrisi (Risk Radarı)</p>", unsafe_allow_html=True)
                kor_matrisi = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].corr().values
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                    colorscale=[[0, '#0F141E'], [0.5, '#1E3A8A'], [1, '#DEFF9A']], 
                    text=np.round(kor_matrisi, 2), texttemplate="%{text}", textfont={"color": "white", "size": 14}, showscale=False
                ))
                fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=10, b=10, l=10, r=10), height=300)
                st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
                
            with kor_col2:
                st.markdown("<p style='color: #F5F5F5; font-weight: 600;'>🌊 Kriz Direnci (Underwater / Drawdown)</p>", unsafe_allow_html=True)
                fig_dd = go.Figure(go.Scatter(
                    x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', 
                    line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.2)'
                ))
                fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
                fig_dd.update_layout(height=300, margin=dict(t=10, b=20, l=10, r=10))
                st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

            st.markdown("<h3 style='margin: 30px 0 10px 0;'>🔮 Monte Carlo Gelecek Projeksiyonu (1 Yıl)</h3>", unsafe_allow_html=True)
            mu, sigma = portfoy_getiri.mean(), portfoy_getiri.std()
            sim_df = np.zeros((252, 100))
            sim_df[0] = 100000
            for t in range(1, 252): sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=100))
                
            fig_mc = go.Figure()
            # Göz alıcı neon şeffaflık (0.04'ten 0.15'e çıkarıldı ve renk neon mavi/yeşile döndü)
            for i in range(100): 
                fig_mc.add_trace(go.Scatter(y=sim_df[:, i], mode='lines', line=dict(color='rgba(0, 255, 157, 0.12)', width=1), showlegend=False, hoverinfo='skip'))
            
            fig_mc.add_trace(go.Scatter(y=sim_df.mean(axis=1), mode='lines', name='Beklenen Ortalama', line=dict(color='#F5F5F5', width=3, dash='dash')))
            fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
            fig_mc.update_layout(height=500, xaxis_title="Gelecek Günler (1 İş Yılı)", yaxis_title="Sermaye (TL)", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
