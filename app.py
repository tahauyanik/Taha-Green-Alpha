import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Taha Uyanık | Green Alpha Quant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Karanlık Tema ve Ana Arka Plan */
.stApp { background-color: #0B0E14 !important; } /* Daha derin bir uzay siyahı */

/* Üstteki Streamlit Menü Çubuğunu ve Footer'ı Gizle */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Sidebar Arka Planı ve Çizgisi */
[data-testid="stSidebar"] {
    background-color: #10131A !important;
    border-right: 1px solid #1E222A !important;
}

/* Kusursuz Selectbox (Beyaz Kutu İmhasi) */
div[data-baseweb="select"] { background-color: transparent !important; }
div[data-baseweb="select"] > div {
    background-color: rgba(22, 26, 34, 0.7) !important; /* Yarı Şeffaf Menü */
    color: #F5F5F5 !important;
    border: 1px solid #2D323C !important; 
    border-radius: 8px !important;
    backdrop-filter: blur(5px) !important;
}
div[data-baseweb="select"] > div:hover { border: 1px solid #DEFF9A !important; }
div[data-baseweb="select"] svg { color: #DEFF9A !important; }
div[role="listbox"], ul[role="listbox"] {
    background-color: #161A22 !important;
    border: 1px solid #2D323C !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #161A22 !important; }
li[role="option"] { color: #F5F5F5 !important; background-color: #161A22 !important; }
li[role="option"]:hover { background-color: #2D323C !important; color: #DEFF9A !important; }

/* V7.0 LINKEDIN ŞOVU: CAM EFEKTİ (GLASSMORPHISM) METRİK KARTLARI */
div[data-testid="metric-container"], div[data-testid="stMetric"] {
    background-color: rgba(22, 26, 34, 0.4) !important; /* Şeffaf arka plan */
    backdrop-filter: blur(10px) !important; /* Cam buğusu */
    -webkit-backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(222, 255, 154, 0.2) !important; /* İncecik neon sınır */
    padding: 24px !important;
    border-radius: 16px !important; /* Daha oval köşeler */
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important; /* Sıçrama animasyonu */
}

div[data-testid="metric-container"]:hover, div[data-testid="stMetric"]:hover {
    transform: translateY(-8px) scale(1.02) !important;
    box-shadow: 0 15px 40px rgba(222, 255, 154, 0.15) !important;
    border: 1px solid #DEFF9A !important;
    background-color: rgba(22, 26, 34, 0.8) !important;
}

/* Rakamların Rengi (Neon Yeşil Vurgu) */
[data-testid="stMetricValue"] > div { color: #DEFF9A !important; font-weight: 900 !important; letter-spacing: 1px !important;}

/* Alt Başlıklar (Okunabilirlik için gümüş/beyaz) */
[data-testid="stMetricLabel"] > div > div > p { color: #8B949E !important; font-weight: 600 !important; font-size: 15px !important; text-transform: uppercase !important; letter-spacing: 0.5px !important;}

/* Delta (Artış/Azalış) Renkleri */
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }
[data-testid="stMetricDelta"] > div { color: #A3FF00 !important; font-weight: bold !important; }

/* Yazı Başlıkları ve Etiketleri */
h1, h2, h3, p, label { color: #F5F5F5 !important; font-family: 'Inter', sans-serif !important;}

/* Slider Renkleri */
div[data-baseweb="slider"] div { background-color: #DEFF9A !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **Algoritmik Araçlar**")

# Trend Kalkanı (Kullanıcı Seçimi)
trend_goster = st.sidebar.toggle("Trend Kalkanı (SMA Ayarları)", value=False, help="Kendi belirlediğin hareketli ortalamaları açar.")

sma_kisa = 20
sma_uzun = 50

if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA", min_value=5, max_value=100, value=20, step=1)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA", min_value=10, max_value=250, value=50, step=1)

# YENİ AGRESİF BAŞLIK
st.title("🌍 Taha Uyanık | Green Alpha Quant Fund")
st.markdown("*BIST100 vs. Katılım Endeksli Yeşil Enerji Algoritması (Volatilite ve Alfa Analizi)*")

# GERÇEK MERMİLER (Katılım + Yeşil Enerji Filtresi)
hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    veri = yf.download(hisseler, period=periyot, progress=False, threads=False)['Close']
    
    if veri.empty:
        st.error("Piyasa verisi çekilemiyor. Lütfen farklı bir zaman aralığı seçin.")
        st.stop()
        
    veri = veri.ffill().bfill() 
    
    # 0'a bölme kalkanı
    ilk_satir = veri.iloc[0].replace(0, 0.0001)
    normalize_veri = (veri / ilk_satir) * 100
    
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
        # Dinamik SMA hesaplaması
        if len(normalize_veri) >= sma_kisa:
            normalize_veri[f'SMA_{sma_kisa}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_kisa).mean()
        if len(normalize_veri) >= sma_uzun:
            normalize_veri[f'SMA_{sma_uzun}'] = normalize_veri['TAHA_YESIL_FON'].rolling(window=sma_uzun).mean()

    st.subheader(f"📊 Algoritmik Kıyaslama ({periyot})")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=normalize_veri.index.strftime('%Y-%m-%d'), 
        y=normalize_veri['TAHA_YESIL_FON'],
        mode='lines', name='Taha Yeşil Fon',
        line=dict(color='#DEFF9A', width=3),
        hovertemplate="<b>Tarih:</b> %{x}<br><b>Taha Yeşil Fon:</b> %{y:.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=normalize_veri.index.strftime('%Y-%m-%d'), 
        y=normalize_veri['XU100.IS'],
        mode='lines', name='BIST100',
        line=dict(color='#64748B', width=2), 
        hovertemplate="<b>Tarih:</b> %{x}<br><b>BIST100:</b> %{y:.2f}<extra></extra>"
    ))

    if trend_goster:
        if f'SMA_{sma_kisa}' in normalize_veri.columns:
            fig.add_trace(go.Scatter(
                x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'],
                mode='lines', name=f'SMA {sma_kisa} (Hızlı Trend)',
                line=dict(color='#FFA500', width=1.5, dash='dot'),
                hovertemplate=f"SMA {sma_kisa}: %{{y:.2f}}<extra></extra>"
            ))
        if f'SMA_{sma_uzun}' in normalize_veri.columns:
            fig.add_trace(go.Scatter(
                x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'],
                mode='lines', name=f'SMA {sma_uzun} (Ana Trend)',
                line=dict(color='#FF1493', width=1.5, dash='dot'),
                hovertemplate=f"SMA {sma_uzun}: %{{y:.2f}}<extra></extra>"
            ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickangle=-45, rangeslider=dict(visible=False)),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        legend=dict(bgcolor='rgba(11, 14, 20, 0.8)', bordercolor='#2D323C', borderwidth=1, orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5, font=dict(color='#FFFFFF', size=13)),
        margin=dict(l=0, r=0, t=20, b=80), hovermode='x unified',
        hoverlabel=dict(bgcolor="#161A22", font_size=14, font_family="Arial", font_color="#FFFFFF", bordercolor="#DEFF9A")
    )
    
    st.plotly_chart(fig, use_container_width=True) 

    st.markdown("### 💰 100.000 TL Simülasyon Sonuçları")
    
    bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
    yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
    fark = yesil_sonuc - bist_sonuc

    col1, col2, col3 = st.columns(3)
    col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} TL", delta="Referans Endeks", delta_color="off")
    col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} TL", delta=f"{((yesil_sonuc-100000)/100000)*100:.1f}% Fon Büyümesi")
    col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} TL", delta="Piyasayı Yendi" if fark > 0 else "- Piyasaya Yenildi")

    getiriler = veri.pct_change().dropna()
    
    if len(getiriler) > 0:
        portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

        bist_vol = float(np.nan_to_num(getiriler['XU100.IS'].std() * (252 ** 0.5) * 100))
        fon_vol = float(np.nan_to_num(portfoy_getiri.std() * (252 ** 0.5) * 100))

        fon_kumulatif = (1 + portfoy_getiri).cumprod()
        fon_zirve = fon_kumulatif.cummax()
        drawdown_serisi = ((fon_kumulatif - fon_zirve) / fon_zirve) * 100
        fon_dd = float(np.nan_to_num(drawdown_serisi.min()))

        st.markdown("### ⚖️ Kantitatif Risk Analizi")
        r_col1, r_col2, r_col3 = st.columns(3)
        r_col1.metric("BIST100 Yıllık Volatilite", f"%{bist_vol:.2f}", delta="Risk Endeksi", delta_color="off")
        r_col2.metric("Taha Yeşil Fon Volatilite", f"%{fon_vol:.2f}", delta="Agresif Büyüme Riski", delta_color="off")
        r_col3.metric("Maksimum Düşüş (Max Drawdown)", f"%{fon_dd:.2f}", delta="Kriz Direnci", delta_color="off")
        
        st.markdown("---")
        st.markdown("### 🔬 Kaputun Altı: Portföy DNA'sı ve Kriz Şeffaflığı")
        
        grafik_col1, grafik_col2 = st.columns(2)
        
        with grafik_col1:
            st.markdown("**Fon Dağılım Modeli (Eşit Ağırlıklı)**")
            labels = ['ALFAS', 'YEOTK', 'ASTOR', 'KCAER']
            values = [25, 25, 25, 25] 
            colors = ['#DEFF9A', '#A3FF00', '#2E8B57', '#00FA9A']
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.6, marker=dict(colors=colors, line=dict(color='#0B0E14', width=2)))])
            fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', # V7.0 JİLET GİBİ ŞEFFAFLIK
                font=dict(color='#F5F5F5'), margin=dict(t=20, b=20, l=20, r=20),
                showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5, font=dict(color='#FFFFFF'))
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with grafik_col2:
            st.markdown("**Sualtı Grafiği (Underwater / Drawdown)**")
            fig_dd = go.Figure()
            fig_dd.add_trace(go.Scatter(
                x=drawdown_serisi.index.strftime('%Y-%m-%d'), 
                y=drawdown_serisi,
                fill='tozeroy', mode='lines',
                line=dict(color='#FF4C4C', width=1.5),
                fillcolor='rgba(255, 76, 76, 0.15)',
                name='Düşüş (Drawdown)',
                hovertemplate="Tarih: %{x}<br>Düşüş: %{y:.2f}%<extra></extra>"
            ))
            fig_dd.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
                xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickangle=-45),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="% Düşüş"),
                margin=dict(t=20, b=20, l=20, r=20), hovermode='x unified',
                legend=dict(font=dict(color='#FFFFFF'))
            )
            st.plotly_chart(fig_dd, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔮 Yapay Zeka Monte Carlo Simülasyonu (1 Yıllık Gelecek Projeksiyonu)")
        st.markdown("Geçmiş volatilite ve getiri metrikleri kullanılarak **önümüzdeki 252 işlem günü (1 Yıl)** için 100 farklı rastgele piyasa senaryosu simüle edilmiştir. Başlangıç: **100.000 TL**")
        
        gun_sayisi = 252
        simulasyon_sayisi = 100
        baslangic_sermayesi = 100000
        
        mu = portfoy_getiri.mean()
        sigma = portfoy_getiri.std()
        
        simulasyon_df = np.zeros((gun_sayisi, simulasyon_sayisi))
        simulasyon_df[0] = baslangic_sermayesi
        
        for t in range(1, gun_sayisi):
            rassal_sok = np.random.normal(loc=mu, scale=sigma, size=simulasyon_sayisi)
            simulasyon_df[t] = simulasyon_df[t-1] * (1 + rassal_sok)
            
        fig_mc = go.Figure()
        
        for i in range(simulasyon_sayisi):
            fig_mc.add_trace(go.Scatter(
                y=simulasyon_df[:, i],
                mode='lines',
                line=dict(color='rgba(222, 255, 154, 0.08)', width=1), # Neon Yeşil Şeffaf Çizgiler
                showlegend=False,
                hoverinfo='skip'
            ))
            
        beklenen_senaryo = simulasyon_df.mean(axis=1)
        fig_mc.add_trace(go.Scatter(
            y=beklenen_senaryo,
            mode='lines',
            name='Beklenen Senaryo (Ortalama)',
            line=dict(color='#FF1493', width=3, dash='dash'), 
        ))
        
        # V7.0: MONTE CARLO UX OVERHAUL (Şeffaf Zemin, Okunabilir Eksenler)
        fig_mc.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
            xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Gelecek Günler (1 Yıl)"),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Sermaye Büyüklüğü (TL)", tickformat=",.0f"),
            margin=dict(t=20, b=20, l=20, r=20), hovermode='x unified',
            legend=dict(
                bgcolor='rgba(11, 14, 20, 0.8)', 
                bordercolor='#2D323C', 
                borderwidth=1, 
                orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                font=dict(color='#FFFFFF') 
            )
        )
        st.plotly_chart(fig_mc, use_container_width=True)
        
        en_kotu = np.percentile(simulasyon_df[-1, :], 5) 
        beklenen = beklenen_senaryo[-1]
        en_iyi = np.percentile(simulasyon_df[-1, :], 95) 
        
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        mc_col1.metric("Karamsar Senaryo (%5 Olasılık)", f"{en_kotu:,.0f} TL", delta=f"{((en_kotu-100000)/100000)*100:.1f}%", delta_color="normal")
        mc_col2.metric("Beklenen Senaryo (Ortalama)", f"{beklenen:,.0f} TL", delta=f"{((beklenen-100000)/100000)*100:.1f}%", delta_color="normal")
        mc_col3.metric("İyimser Senaryo (%95 Olasılık)", f"{en_iyi:,.0f} TL", delta=f"{((en_iyi-100000)/100000)*100:.1f}%", delta_color="normal")

    else:
        st.warning("Seçilen periyotta risk metriklerini hesaplayacak kadar veri yok.")

except Exception as e:
    st.error(f"Sistem bir anormallik tespit etti ve güvenli moda geçti. Hata: {e}")
