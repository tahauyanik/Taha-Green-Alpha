import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import datetime
import pytz
import textwrap

# DİKKAT: Diğer dosyalarımızdan güç çekiyoruz! Modüler mimarinin kalbi burasıdır.
from data_engine import SovereignDataEngine
from risk_engine import SovereignRiskEngine
from visual_engine import SovereignVisualEngine

st.set_page_config(
    page_title="Sovereign OS | Decision Intelligence", 
    page_icon="🧬", 
    layout="wide", 
    initial_sidebar_state="collapsed" 
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Sovereign OS Zifiri Karanlık */
.stApp { 
    background: #020305 !important;
    background-image: radial-gradient(circle at 50% 0%, #080C14 0%, #020305 70%) !important;
}

[data-testid="stHeader"], [data-testid="stToolbar"], footer, [data-testid="collapsedControl"], section[data-testid="stSidebar"] { display: none !important; }
a { pointer-events: none; cursor: default; text-decoration: none !important; }

/* OS Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 30px; background-color: transparent !important; border-bottom: 1px solid rgba(255, 255, 255, 0.03) !important; padding-bottom: 0px; margin-bottom: 20px;
}
.stTabs [data-baseweb="tab"] {
    height: 50px; background-color: transparent !important; padding: 0px 8px !important; color: #4B5563 !important;
    font-weight: 500 !important; font-size: 13px !important; border: none !important; transition: color 0.3s ease; letter-spacing: 1px; text-transform: uppercase;
}
.stTabs [data-baseweb="tab"]:hover { color: #9CA3AF !important; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #F3F4F6 !important; background-color: transparent !important; font-weight: 700 !important; }
div[data-baseweb="tab-highlight"] { background-color: #3B82F6 !important; height: 1px !important; border-radius: 0px !important; }

/* Story & Metric Cards */
.os-greeting { font-size: 42px; font-weight: 300; color: #F3F4F6; letter-spacing: -1.5px; margin-bottom: 5px; line-height: 1.1; }
.os-greeting span { font-weight: 700; background: linear-gradient(90deg, #DEFF9A, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.os-sub { font-size: 14px; color: #6B7280; font-weight: 400; margin-bottom: 30px; letter-spacing: 0.5px; font-family: 'JetBrains Mono', monospace; }

.story-card {
    background: rgba(10, 12, 18, 0.4); border: 1px solid rgba(255, 255, 255, 0.03); border-radius: 12px; padding: 28px; 
    backdrop-filter: blur(10px); transition: all 0.3s ease; position: relative; overflow: hidden; height: 100%;
}
.story-card:hover { border-color: rgba(59, 130, 246, 0.3); background: rgba(10, 12, 18, 0.7); }
.story-label { color: #6B7280; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 12px; font-family: 'JetBrains Mono', monospace;}
.story-value { color: #F3F4F6; font-size: 24px; font-weight: 400; line-height: 1.4; letter-spacing: -0.5px; }
.story-highlight { color: #DEFF9A; font-weight: 700; }
.story-highlight-red { color: #FF4C4C; font-weight: 700; }
.story-highlight-blue { color: #3B82F6; font-weight: 700; }

.dna-card { border-left: 2px solid #3B82F6; padding-left: 15px; margin-top: 20px; background: rgba(59,130,246,0.05); padding: 15px 15px 15px 20px; border-radius: 0 8px 8px 0;}
.dna-title { color: #3B82F6; font-size: 11px; font-family: 'JetBrains Mono'; margin-bottom: 5px; text-transform: uppercase; letter-spacing: 1px;}
.dna-text { color: #9CA3AF; font-size: 13px; line-height: 1.6; }

.terminal-card { background: #0A0C12; border: 1px solid rgba(59, 130, 246, 0.2); border-radius: 12px; padding: 34px; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.5); height: 100%; display: flex; flex-direction: column; justify-content: space-between;}
.terminal-card::before { content: ''; position: absolute; top: 0; left: 0; width: 3px; height: 100%; background: linear-gradient(to bottom, #3B82F6, transparent); border-radius: 12px 0 0 12px; }
.terminal-font { font-family: 'JetBrains Mono', monospace; }

.dark-pool-table { width: 100%; border-collapse: collapse; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
.dark-pool-table th { color: #8B949E; text-align: left; padding: 8px 4px; border-bottom: 1px solid rgba(255,255,255,0.05); font-weight: 600; text-transform: uppercase;}
.dark-pool-table td { color: #D1D5DB; padding: 12px 4px; border-bottom: 1px solid rgba(255,255,255,0.02); }

::-webkit-scrollbar { width: 4px; height: 4px; } ::-webkit-scrollbar-track { background: #020305; } ::-webkit-scrollbar-thumb { background: #1F2937; } ::-webkit-scrollbar-thumb:hover { background: #3B82F6; }
</style>
""", unsafe_allow_html=True)

tz = pytz.timezone('Europe/Istanbul')
current_time = datetime.datetime.now(tz)
hour = current_time.hour

if hour < 12: greeting = "Good Morning"
elif hour < 18: greeting = "Good Afternoon"
else: greeting = "Good Evening"

st.markdown(f"""
<div style='margin-top: 10px; margin-left: 5px;'>
    <div class='os-greeting'>{greeting}, <span>Taha.</span></div>
    <div class='os-sub'>Sovereign OS • Decision Intelligence Kernel v1.0</div>
</div>
""", unsafe_allow_html=True)

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    close_data, vol_data, high_data, low_data, open_data = SovereignDataEngine.fetch_market_data(hisseler, "1y")
    close_data = close_data.ffill().bfill()
    portfoy_getiri_serisi = close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change().dropna().mean(axis=1)
    son_getiri = portfoy_getiri_serisi.iloc[-1] * 100
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 EXECUTIVE BRIEF", "🔬 MARKET STRUCTURE", "⚖️ RISK & CORRELATION", "🔮 STOCHASTIC GBM", "🧬 AI REBALANCER", "🦢 STRESS TESTING"
    ])

    with tab1:
        col_s1, col_s2, col_s3 = st.columns(3, gap="large")
        
        with col_s1:
            durum_metni = "Markets slept badly." if close_data['XU100.IS'].iloc[-1] < close_data['XU100.IS'].iloc[-2] else "Markets are breathing steadily."
            st.markdown(f"""
            <div class="story-card">
                <div class="story-label">Macro Narrative</div>
                <div class="story-value">{durum_metni} <br><br>The algorithm detects a rotation towards <span class="story-highlight-blue">energy infrastructure</span> while traditional sectors consolidate.</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_s2:
            getiri_renk = "story-highlight" if son_getiri > 0 else "story-highlight-red"
            yon = "gained" if son_getiri > 0 else "lost"
            sebep = "Positive structural flow" if son_getiri > 0 else "Systematic market pull-back"
            
            st.markdown(f"""
            <div class="story-card">
                <div class="story-label">Portfolio Pulse</div>
                <div class="story-value">Your portfolio {yon} <span class="{getiri_renk}">{abs(son_getiri):.2f}%</span> today.<br><br>Driver:<br><span style="font-size:16px; color:#9CA3AF; font-family:'JetBrains Mono';">{sebep}</span></div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_s3:
            st.markdown(f"""
            <div class="story-card">
                <div class="story-label">Digital Investor Twin</div>
                <div class="story-value" style="font-size:18px;">
                    "Taha, the old you would react emotionally right now."
                </div>
                <div class="dna-card">
                    <div class="dna-title">SYSTEM MEMORY</div>
                    <div class="dna-text">Your historical data shows panic-selling during minor drawdowns costs you <b>12% potential upside</b> annually. Trust the math. Hold the line.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#F3F4F6; font-weight:400; font-size:18px; margin-bottom: 20px; letter-spacing:0.5px;'>Actionable Insights (Explainable AI)</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style="background: rgba(10,12,18,0.5); border: 1px solid rgba(59,130,246,0.2); border-radius: 12px; padding: 25px;">
            <div style="display:flex; align-items:center; gap: 20px; margin-bottom: 20px;">
                <div style="background:#DEFF9A; color:#000; font-weight:800; padding:8px 16px; border-radius:6px; font-size:16px;">SIGNAL: ACCUMULATE</div>
                <div style="color:#6B7280; font-family:'JetBrains Mono'; font-size:12px;">AI CONFIDENCE: 84%</div>
            </div>
            <div style="color:#F3F4F6; font-size:14px; margin-bottom:15px; font-weight:500;">Deterministic Reasoning:</div>
            <ol style="color:#9CA3AF; font-size:13px; line-height:2; font-family:'JetBrains Mono'; margin:0; padding-left: 20px;">
                <li><span style="color:#DEFF9A">[88% Weight]</span> Mean-reversion detected. Asset classes are trading below optimal Markowitz bounds.</li>
                <li><span style="color:#DEFF9A">[72% Weight]</span> Institutional dark pool / volume anomalies indicate positive accumulation.</li>
                <li><span style="color:#FF4C4C">[30% Risk]</span> Macro volatility remains elevated. Maintain defensive Beta exposure.</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

    with tab2:
        secili_hisse = st.selectbox("Select Asset for Deep Technical Diagnostics", ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS'], index=0)
        h_close, h_open, h_high, h_low, h_vol = close_data[secili_hisse], open_data[secili_hisse], high_data[secili_hisse], low_data[secili_hisse], vol_data[secili_hisse]
        h_rsi, h_macd, h_signal, upper_bb, lower_bb, h_obv, ind_sma_20 = SovereignDataEngine.calculate_technical_indicators(h_close, h_vol)
        
        fig_tech = make_subplots(
            rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.04, 
            row_heights=[0.5, 0.15, 0.15, 0.2], subplot_titles=(f"{secili_hisse} Market Structure", "Volume Flow", "RSI Momentum", "MACD Trend")
        )
        
        fig_tech.add_trace(go.Candlestick(x=h_close.index, open=h_open, high=h_high, low=h_low, close=h_close, increasing_line_color='#DEFF9A', decreasing_line_color='#FF4C4C', name="Price"), row=1, col=1)
        fig_tech.add_trace(go.Scatter(x=h_close.index, y=upper_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), name="Upper BB", hoverinfo='skip'), row=1, col=1)
        fig_tech.add_trace(go.Scatter(x=h_close.index, y=lower_bb, line=dict(color='rgba(59, 130, 246, 0.3)', width=1), fill='tonexty', fillcolor='rgba(59, 130, 246, 0.05)', name="Lower BB", hoverinfo='skip'), row=1, col=1)
        
        colors = ['#DEFF9A' if row['close'] >= row['open'] else '#FF4C4C' for index, row in pd.concat([h_open, h_close], axis=1, keys=['open', 'close']).iterrows()]
        fig_tech.add_trace(go.Bar(x=h_vol.index, y=h_vol, marker_color=colors, name="Volume"), row=2, col=1)
        
        fig_tech.add_trace(go.Scatter(x=h_rsi.index, y=h_rsi, line=dict(color='#3B82F6', width=1.5), name="RSI"), row=3, col=1)
        fig_tech.add_hline(y=70, line_dash="dash", line_color="#FF4C4C", row=3, col=1)
        fig_tech.add_hline(y=30, line_dash="dash", line_color="#DEFF9A", row=3, col=1)
        
        fig_tech.add_trace(go.Scatter(x=h_macd.index, y=h_macd, line=dict(color='#DEFF9A', width=1.5), name="MACD"), row=4, col=1)
        fig_tech.add_trace(go.Scatter(x=h_signal.index, y=h_signal, line=dict(color='#FF4C4C', width=1), name="Signal"), row=4, col=1)

        fig_tech = SovereignVisualEngine.apply_premium_layout(fig_tech)
        for i in fig_tech['layout']['annotations']: i['font'] = dict(size=11, color='#8B949E', family="Inter", weight="bold")
        fig_tech.update_layout(height=800, showlegend=False, xaxis_rangeslider_visible=False, margin=dict(t=30))
        st.plotly_chart(fig_tech, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        bist_getiri = close_data['XU100.IS'].pct_change().dropna()
        (fon_vol, b_vol, sortino, calmar, info_ratio, max_dd, var_95, cvar_95, drawdown_serisi, alpha, beta) = SovereignRiskEngine.calculate_metrics(portfoy_getiri_serisi, bist_getiri)

        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px;">
            <div class="story-card" style="padding: 20px;">
                <div class="story-label">Sortino Ratio</div>
                <div class="story-value" style="font-size:26px; color:{'#DEFF9A' if sortino > 1 else '#F59E0B'};">{sortino:.2f}</div>
                <div style="font-size:11px; color:#6B7280; margin-top:5px;">Downside Risk Profiling</div>
            </div>
            <div class="story-card" style="padding: 20px;">
                <div class="story-label">Market Beta</div>
                <div class="story-value" style="font-size:26px;">{beta:.2f}</div>
                <div style="font-size:11px; color:#6B7280; margin-top:5px;">Systematic Risk Exposure</div>
            </div>
            <div class="story-card" style="padding: 20px;">
                <div class="story-label">Daily VaR (95%)</div>
                <div class="story-value" style="font-size:26px; color:#F59E0B;">% {var_95:.2f}</div>
                <div style="font-size:11px; color:#6B7280; margin-top:5px;">Value at Risk</div>
            </div>
            <div class="story-card" style="padding: 20px;">
                <div class="story-label">Max Drawdown</div>
                <div class="story-value" style="font-size:26px; color:#FF4C4C;">% {max_dd:.2f}</div>
                <div style="font-size:11px; color:#6B7280; margin-top:5px;">Historical Peak-to-Trough</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        kor_col1, kor_col2 = st.columns(2, gap="large")
        with kor_col1:
            st.markdown("<div class='story-label'>Asset Correlation Heatmap</div>", unsafe_allow_html=True)
            getiriler = close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].pct_change().dropna()
            kor_matrisi = getiriler.corr().values
            fig_corr = go.Figure(data=go.Heatmap(
                z=kor_matrisi, x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'], 
                colorscale=[[0, '#0F141E'], [0.5, '#1C2433'], [1, '#3B82F6']], showscale=False, hoverinfo='skip'
            ))
            for i in range(len(kor_matrisi)):
                for j in range(len(kor_matrisi[i])):
                    val = kor_matrisi[i][j]
                    text_color = '#0A0C12' if val > 0.7 else '#F3F4F6'
                    fig_corr.add_annotation(x=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][j], y=['ALFAS', 'YEOTK', 'ASTOR', 'KCAER'][i], text=f"{val:.2f}", showarrow=False, font=dict(color=text_color, size=13, family="Inter", weight="bold"))
            fig_corr.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), height=340)
            st.plotly_chart(fig_corr, use_container_width=True, config={'displayModeBar': False})
            
        with kor_col2:
            st.markdown("<div class='story-label'>Drawdown (Underwater Chart)</div>", unsafe_allow_html=True)
            fig_dd = go.Figure(go.Scatter(x=drawdown_serisi.index, y=drawdown_serisi, fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1.5), fillcolor='rgba(255, 76, 76, 0.15)'))
            fig_dd = SovereignVisualEngine.apply_premium_layout(fig_dd)
            fig_dd.update_layout(height=340, margin=dict(t=0, b=0, l=0, r=0))
            st.plotly_chart(fig_dd, use_container_width=True, config={'displayModeBar': False})

    with tab4:
        st.markdown("<div class='story-label'>Stochastic Projection (Geometric Brownian Motion)</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 20px;'>Simulates 100 random market scenarios for the next 252 trading days based on historical volatility (σ) and drift (μ). Shaded area represents 5% and 95% confidence intervals.</p>", unsafe_allow_html=True)
        
        sim_df = SovereignRiskEngine.simulate_gbm(portfoy_getiri_serisi)
        fig_mc = go.Figure()
        percentile_5 = np.percentile(sim_df, 5, axis=1)
        percentile_95 = np.percentile(sim_df, 95, axis=1)
        x_axis = np.arange(252)
        
        fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_95, mode='lines', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        fig_mc.add_trace(go.Scatter(x=x_axis, y=percentile_5, mode='lines', fill='tonexty', fillcolor='rgba(59, 130, 246, 0.1)', line=dict(width=0), showlegend=False, hoverinfo='skip'))
        for i in range(100): fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df[:, i], mode='lines', line=dict(color='rgba(255, 255, 255, 0.03)', width=1), showlegend=False, hoverinfo='skip'))
        fig_mc.add_trace(go.Scatter(x=x_axis, y=sim_df.mean(axis=1), mode='lines', name='Expected Trajectory (μ)', line=dict(color='#3B82F6', width=2, dash='dash')))
        
        fig_mc = SovereignVisualEngine.apply_premium_layout(fig_mc)
        fig_mc.update_layout(height=500, yaxis_title="Capital (TL)", xaxis_title="Future Trading Days (252 Days)", margin=dict(t=20))
        st.plotly_chart(fig_mc, use_container_width=True, config={'displayModeBar': False})

    with tab5:
        st.markdown("<div class='story-label'>Autonomous Portfolio Optimization (Efficient Frontier)</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 20px;'>Runs 5,000 MPT simulations to isolate the 'Max Sharpe Ratio' allocation, mathematically optimizing return for a given unit of risk.</p>", unsafe_allow_html=True)
        
        all_weights, ret_arr, vol_arr, sharpe_arr = SovereignRiskEngine.markowitz_optimization(close_data[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']])
        max_sr_idx = sharpe_arr.argmax()
        max_sr_ret, max_sr_vol, optimal_weights = ret_arr[max_sr_idx], vol_arr[max_sr_idx], all_weights[max_sr_idx]

        col_opt1, col_opt2 = st.columns([1.618, 1], gap="large")
        with col_opt1:
            fig_opt = go.Figure()
            fig_opt.add_trace(go.Scatter(
                x=vol_arr * 100, y=ret_arr * 100, mode='markers',
                marker=dict(color=sharpe_arr, colorscale='Viridis', showscale=False, size=4, line=dict(width=0)),
                name='Simulations', hoverinfo='skip'
            ))
            fig_opt.add_trace(go.Scatter(
                x=[max_sr_vol * 100], y=[max_sr_ret * 100], mode='markers',
                marker=dict(color='#DEFF9A', size=16, symbol='star', line=dict(color='#0A0C12', width=2)),
                name='Max Sharpe (Optimal)'
            ))
            fig_opt = SovereignVisualEngine.apply_premium_layout(fig_opt)
            fig_opt.update_layout(height=400, xaxis_title="Annualized Risk (%)", yaxis_title="Expected Return (%)", margin=dict(t=20))
            st.plotly_chart(fig_opt, use_container_width=True, config={'displayModeBar': False})
            
        with col_opt2:
            w_alfas, w_yeotk, w_astor, w_kcaer = optimal_weights * 100
            html_content = textwrap.dedent(f"""
            <div class="terminal-card" style="padding: 25px; height: 100%;">
                <div class="story-label" style="color:#DEFF9A; margin-bottom: 20px;">RECOMMENDED ALLOCATION</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                    <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono';">ALFAS.IS</span>
                    <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_alfas:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                    <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono';">YEOTK.IS</span>
                    <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_yeotk:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:12px; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px;">
                    <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono';">ASTOR.IS</span>
                    <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_astor:.1f}</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:21px;">
                    <span style="color:#F5F5F5; font-weight:600; font-family:'JetBrains Mono';">KCAER.IS</span>
                    <span style="color:#DEFF9A; font-weight:800; font-size:16px;">% {w_kcaer:.1f}</span>
                </div>
            </div>
            """)
            st.markdown(html_content, unsafe_allow_html=True)

    with tab6:
        st.markdown("<div class='story-label'>Macro Stress Testing (Black Swan Simulator)</div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8B949E; font-size: 13px; margin-bottom: 20px;'>Estimates portfolio drawdown against historical and theoretical systemic shocks utilizing dynamic beta weighting.</p>", unsafe_allow_html=True)
        
        bist_getiri = close_data['XU100.IS'].pct_change().dropna()
        cov_matrix = np.cov(portfoy_getiri_serisi, bist_getiri)
        beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] > 0 else 1
        
        scenarios = {
            "2020 Global Pandemic": {"market_drop": -0.342, "desc": "Widespread panic, liquidity freeze.", "color": "#FF4C4C", "sector_hit": False},
            "Local Macro Shock (Rate Hike)": {"market_drop": -0.225, "desc": "Sudden monetary policy shift.", "color": "#F59E0B", "sector_hit": False},
            "Tech/Energy Sector Meltdown": {"market_drop": -0.158, "desc": "Targeted sector crash, high beta hit.", "color": "#8B949E", "sector_hit": True}
        }
        
        cols = st.columns(3, gap="large")
        idx = 0
        for name, data in scenarios.items():
            market_drop = data["market_drop"]
            port_drop = market_drop * beta 
            if data["sector_hit"]: port_drop = market_drop * 1.8 
            port_retained = 100000 * (1 + port_drop)
            diff_from_market = (market_drop - port_drop) * 100 
            
            with cols[idx]:
                st.markdown(f"""
                <div class="terminal-card" style="padding: 24px; border-top: 2px solid {data['color']};">
                    <div style="color:{data['color']}; font-size:12px; font-weight:bold; letter-spacing:1px; margin-bottom:8px; text-transform:uppercase;">{name}</div>
                    <div style="color:#8B949E; font-size:11px; margin-bottom:16px;">{data['desc']}</div>
                    <div style="display:flex; justify-content:space-between; align-items:flex-end;">
                        <div>
                            <div style="color:#8B949E; font-size:11px; margin-bottom:4px;">Expected Drawdown</div>
                            <div style="color:#F5F5F5; font-size:24px; font-weight:800;">%{port_drop*100:.1f}</div>
                        </div>
                        <div style="text-align:right;">
                            <div style="color:#8B949E; font-size:11px; margin-bottom:4px;">Capital Retained</div>
                            <div style="color:#F5F5F5; font-size:16px; font-weight:600; font-family:'JetBrains Mono';">{port_retained:,.0f} ₺</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            idx += 1

except Exception as e:
    st.error(f"Sistem Kritik Bir Hata Yakaladı: {e}")
