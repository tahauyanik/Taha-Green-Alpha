import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Taha Uyanık | Green Alpha Quant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* Karanlık Tema ve Ana Arka Plan */
.stApp { background-color: #0E1117 !important; }

/* V5.5 SAAS TEMİZLİĞİ: Ucuz İkonları ve Linkleri Yokediyoruz */
[data-testid="stToolbar"] { visibility: hidden !important; } /* Sağ üstteki Share/Github ikonları GİTTİ */
header { background-color: transparent !important; }
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
a.anchor { display: none !important; } /* Başlıkların yanındaki çirkin zincir ikonu GİTTİ */

/* Sidebar Arka Planı ve Çizgisi */
[data-testid="stSidebar"] {
    background-color: #12151B !important;
    border-right: 1px solid #2D323C !important;
}

/* V5.5 KUSURSUZ DROPDOWN: Karanlıkta Kaybolan Yazılar ve Çirkin Kutu Tamiri */
div[data-baseweb="select"] > div {
    background-color: #161A22 !important;
    color: #F5F5F5 !important;
    border: 1px solid #2D323C !important; 
    border-radius: 8px !important;
}
div[data-baseweb="select"] > div:hover {
    border: 1px solid #DEFF9A !important; 
}
div[data-baseweb="select"] svg { color: #DEFF9A !important; }

div[data-baseweb="popover"] > div {
    background-color: #161A22 !important;
    border: 1px solid #2D323C !important;
    border-radius: 8px !important;
}
ul[role="listbox"] li {
    background-color: #161A22 !important;
    color: #FFFFFF !important; /* YAZILAR ARTIK BEMBEYAZ VE OKUNABİLİR */
    font-size: 15px !important;
}
ul[role="listbox"] li:hover, ul[role="listbox"] li:active, ul[role="listbox"] li[aria-selected="true"] {
    background-color: #2D323C !important; 
    color: #DEFF9A !important; /* Seçilen/Hover olan Neon Yeşil */
}

/* V5.4 KESİN ÇÖZÜM: METRİK KUTULARI (stMetric doğrudan hedeflendi) */
[data-testid="stMetric"] {
    background-color: #161A22 !important;
    border: 1px solid #2D323C !important; 
    padding: 20px !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5) !important;
    transition: all 0.3s ease-in-out !important;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 8px 20px rgba(222, 255, 154, 0.15) !important;
    border: 1px solid #DEFF9A !important;
}

/* Rakamların Rengi (Neon Yeşil Vurgu) */
[data-testid="stMetricValue"] { color: #F5F5F5 !important; font-weight: 800 !important; }

/* Delta (Artış/Azalış) Renkleri */
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }
[data-testid="stMetricDelta"] { color: #A3FF00 !important; }

/* Yazı Başlıkları ve Etiketleri */
h1, h2, h3, p, label { color: #F5F5F5 !important; }

/* Slider Renkleri ve Toggle Rengi */
div[data-baseweb="slider"] div { background-color: #DEFF9A !important; }
div[data-testid="stToggle"] div[data-baseweb="checkbox"] > div:first-child { background-color: #2D323C !important; }
div[data-testid="stToggle"] input:checked + div > div:first-child { background-color: #A3FF00 !important; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=2)

st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **Algoritmik Araçlar**")

trend_goster = st.sidebar.toggle("Trend Kalkanı (SMA Ayarları)", value=False, help="Kendi belirlediğin hareketli ortalamaları açar.")

sma_kisa = 20
sma_uzun = 50

if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA", min_value=5, max_value=100, value=20, step=1)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA", min_value=10, max_value=250, value=50, step=1)

st.title("🌍 Taha Uyanık | Green Alpha Quant Fund")
st.markdown("BIST100 vs. Katılım Endeksli Yeşil Enerji Algoritması (Volatilite ve Alfa Analizi)")

hisseler = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS', 'XU100.IS']

try:
    veri = yf.download(hisseler, period=periyot, progress=False, threads=False)['Close']
    
    if veri.empty:
        st.error("Piyasa verisi çekilemiyor. Lütfen farklı bir zaman aralığı seçin.")
        st.stop()
        
    veri = veri.ffill().bfill() 
    
    ilk_satir = veri.iloc[0].replace(0, 0.0001)
    normalize_veri = (veri / ilk_satir) * 100
    
    normalize_veri['TAHA_YESIL_FON'] = normalize_veri[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

    if trend_goster:
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
        hovertemplate="<b>Taha Yeşil Fon:</b> %{y:.2f}<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=normalize_veri.index.strftime('%Y-%m-%d'), 
        y=normalize_veri['XU100.IS'],
        mode='lines', name='BIST100',
        line=dict(color='#64748B', width=2), 
        hovertemplate="<b>BIST100:</b> %{y:.2f}<extra></extra>"
    ))

    if trend_goster:
        if f'SMA_{sma_kisa}' in normalize_veri.columns:
            fig.add_trace(go.Scatter(
                x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'],
                mode='lines', name=f'SMA {sma_kisa} (Hızlı)',
                line=dict(color='#FFA500', width=1.5, dash='dot'),
                hovertemplate=f"SMA {sma_kisa}: %{{y:.2f}}<extra></extra>"
            ))
        if f'SMA_{sma_uzun}' in normalize_veri.columns:
            fig.add_trace(go.Scatter(
                x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'],
                mode='lines', name=f'SMA {sma_uzun} (Ana)',
                line=dict(color='#FF1493', width=1.5, dash='dot'),
                hovertemplate=f"SMA {sma_uzun}: %{{y:.2f}}<extra></extra>"
            ))

    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
        xaxis=dict(showgrid=True, gridcolor='#1E222A', tickangle=-45, rangeslider=dict(visible=False)),
        yaxis=dict(showgrid=True, gridcolor='#1E222A'),
        legend=dict(
            bgcolor='rgba(22, 26, 34, 0.9)', 
            bordercolor='#DEFF9A', 
            borderwidth=1, 
            orientation="h", 
            yanchor="top", y=-0.35, # V5.4 KESİN ÇÖZÜM: X ekseni tarihleriyle çakışmaması için daha aşağı alındı
            xanchor="center", x=0.5,
            font=dict(color='#FFFFFF', size=12)
        ),
        margin=dict(l=0, r=0, t=50, b=90), # Alt boşluk genişletildi ki legend sığsın
        hovermode='x unified',
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

            # Drawdown'da Zoom Geri Geldi!
            st.plotly_chart(fig_dd, use_container_width=True)

        st.markdown("---")
        st.markdown("### 🔮 Yapay Zeka Monte Carlo Simülasyonu (1 Yıllık Gelecek Projeksiyonu)")
        st.markdown("Geçmiş volatilite ve getiri metrikleri (Geometric Brownian Motion) kullanılarak **önümüzdeki 252 işlem günü (1 Yıl)** için 100 farklı rastgele piyasa senaryosu simüle edilmiştir. Başlangıç sermayesi: **100.000 TL**")
        
        gun_sayisi = 252
        simulasyon_sayisi = 100
        baslangic_sermayesi = 100000
        
        # Günlük logaritmik getiri ortalaması ve standart sapması (Sürüklenme ve Volatilite)
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
                line=dict(color='rgba(222, 255, 154, 0.05)', width=1), # Çok şeffaf neon yeşil senaryolar
                showlegend=False,
                hoverinfo='skip'
            ))
            
        beklenen_senaryo = simulasyon_df.mean(axis=1)
        fig_mc.add_trace(go.Scatter(
            y=beklenen_senaryo,
            mode='lines',
            name='Beklenen Senaryo (Medyan)',
            line=dict(color='#FF1493', width=3, dash='dash'), # Derin pembe ortalama hedef
        ))
        
        fig_mc.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
            xaxis=dict(showgrid=True, gridcolor='#1E222A', title="Gelecek Günler (1 Yıl)"),
            yaxis=dict(showgrid=True, gridcolor='#1E222A', title="Sermaye Büyüklüğü (TL)", tickformat=",.0f"),
            margin=dict(t=20, b=20, l=20, r=20), hovermode='x unified',
            legend=dict(bgcolor='rgba(22, 26, 34, 0.9)', bordercolor='#DEFF9A', borderwidth=1, orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_mc, use_container_width=True)
        
        en_kotu = np.percentile(simulasyon_df[-1, :], 5) # %5'lik en kötü senaryo
        beklenen = beklenen_senaryo[-1]
        en_iyi = np.percentile(simulasyon_df[-1, :], 95) # %95'lik en iyi senaryo
        
        mc_col1, mc_col2, mc_col3 = st.columns(3)
        mc_col1.metric("Karamsar Senaryo (%5 Olasılık)", f"{en_kotu:,.0f} TL", delta=f"{((en_kotu-100000)/100000)*100:.1f}%", delta_color="normal")
        mc_col2.metric("Beklenen Senaryo (Ortalama)", f"{beklenen:,.0f} TL", delta=f"{((beklenen-100000)/100000)*100:.1f}%", delta_color="normal")
        mc_col3.metric("İyimser Senaryo (%95 Olasılık)", f"{en_iyi:,.0f} TL", delta=f"{((en_iyi-100000)/100000)*100:.1f}%", delta_color="normal")

    else:
        st.warning("Seçilen periyotta risk metriklerini hesaplayacak kadar veri yok.")

except Exception as e:
    st.error(f"Sistem bir anormallik tespit etti ve güvenli moda geçti. Hata: {e}")
