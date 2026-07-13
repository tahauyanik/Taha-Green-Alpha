import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np

st.set_page_config(page_title="Taha Uyanık | Sovereign Quant", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
/* V9.0 PREMIUM SAAS CSS (100$ AYLIK ABONELİK TASARIMI) */
.stApp { background-color: #090B10 !important; }

/* Menü Çubuğu Temizliği */
#MainMenu {visibility: hidden;}
header {background-color: transparent !important;}
footer {visibility: hidden;}

/* Sidebar - Zırhlı ve Elit */
[data-testid="stSidebar"] {
    background-color: #0F131C !important;
    border-right: 1px solid #1E2532 !important;
}

/* Sekmeler (Tabs) Tasarımı - Kurumsal Finans Hissi */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    background-color: #090B10;
}
.stTabs [data-baseweb="tab"] {
    height: 50px;
    white-space: pre-wrap;
    background-color: transparent;
    border-radius: 4px 4px 0px 0px;
    gap: 1px;
    padding-top: 10px;
    padding-bottom: 10px;
    color: #8B949E !important;
    font-weight: 600 !important;
    font-size: 16px !important;
}
.stTabs [aria-selected="true"] {
    color: #DEFF9A !important;
    border-bottom: 3px solid #DEFF9A !important;
}

/* Kusursuz Dropdown (Selectbox) */
div[data-baseweb="select"] { background-color: #151A22 !important; }
div[data-baseweb="select"] > div {
    background-color: #151A22 !important;
    color: #F5F5F5 !important;
    border: 1px solid #1E2532 !important; 
    border-radius: 6px !important;
}
div[data-baseweb="select"]:hover > div { border: 1px solid #DEFF9A !important; }
div[data-baseweb="select"] svg { color: #DEFF9A !important; }
div[role="listbox"], ul[role="listbox"] {
    background-color: #151A22 !important;
    border: 1px solid #1E2532 !important;
}
ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #151A22 !important; }
li[role="option"] { color: #F5F5F5 !important; background-color: #151A22 !important; }
li[role="option"]:hover { background-color: #1E2532 !important; color: #DEFF9A !important; }

/* Metrik Kartları - Glassmorphism ve Derinlik */
div[data-testid="metric-container"], div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #121721 0%, #0F131C 100%) !important;
    border: 1px solid #1E2532 !important;
    border-top: 1px solid rgba(222, 255, 154, 0.2) !important;
    padding: 24px !important;
    border-radius: 12px !important;
    box-shadow: 0 10px 30px -10px rgba(0,0,0,0.8) !important;
    transition: transform 0.3s ease, border 0.3s ease !important;
}
div[data-testid="metric-container"]:hover, div[data-testid="stMetric"]:hover {
    transform: translateY(-4px) !important;
    border: 1px solid #DEFF9A !important;
    box-shadow: 0 15px 35px -5px rgba(222,255,154,0.1) !important;
}

/* Metrik İçerikleri */
[data-testid="stMetricValue"] > div { color: #FFFFFF !important; font-weight: 800 !important; font-size: 28px !important; }
[data-testid="stMetricLabel"] > div > div > p { color: #8B949E !important; font-weight: 600 !important; font-size: 14px !important; text-transform: uppercase; letter-spacing: 1px;}
[data-testid="stMetricDelta"] svg { fill: #A3FF00 !important; }
[data-testid="stMetricDelta"] > div { color: #A3FF00 !important; font-weight: bold !important; }

/* Yazı Başlıkları ve Etiketleri */
h1, h2, h3, h4, p, label { color: #F5F5F5 !important; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important; }

/* Slider Renkleri */
div[data-baseweb="slider"] div { background-color: #DEFF9A !important; }
div[data-testid="stWidgetLabel"] p { font-weight: 600 !important; color: #8B949E !important; }

/* AI Haber Kartları (Özel Sınıflar) */
.news-card {
    background-color: #121721;
    border-left: 4px solid #3B82F6;
    padding: 16px;
    margin-bottom: 16px;
    border-radius: 4px 8px 8px 4px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.news-title { color: #FFFFFF; font-size: 16px; font-weight: 600; margin-bottom: 8px;}
.news-publisher { color: #8B949E; font-size: 12px; }
.sentiment-bull { color: #A3FF00; font-weight: 700; background: rgba(163, 255, 0, 0.1); padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.sentiment-bear { color: #FF4C4C; font-weight: 700; background: rgba(255, 76, 76, 0.1); padding: 2px 8px; border-radius: 12px; font-size: 12px; }
.sentiment-neutral { color: #8B949E; font-weight: 700; background: rgba(139, 148, 158, 0.1); padding: 2px 8px; border-radius: 12px; font-size: 12px; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("⚙️ Kontrol Paneli")
st.sidebar.markdown("Analiz periyodunu seçin:")
periyot = st.sidebar.selectbox("Zaman Aralığı", ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

st.sidebar.markdown("---")
st.sidebar.markdown("🧠 **Algoritmik Araçlar**")

trend_goster = st.sidebar.toggle("Trend Kalkanı (SMA Ayarları)", value=True, help="Hareketli ortalamaları açar.")

sma_kisa = 20
sma_uzun = 50

if trend_goster:
    sma_kisa = st.sidebar.slider("Kısa Vade SMA", min_value=5, max_value=100, value=20, step=1)
    sma_uzun = st.sidebar.slider("Uzun Vade SMA", min_value=10, max_value=250, value=50, step=1)

# ÜST BAŞLIK
st.title("🌍 Taha Uyanık | Sovereign Quant Fund")
st.markdown("Yapay Zeka Destekli Katılım Endeksli Yeşil Enerji Portföy Yönetim Sistemi")

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

    tab1, tab2, tab3 = st.tabs(["📈 Algoritmik Terminal", "🧠 AI İstihbarat & Sinyal", "🧩 Kuantum Risk Yönetimi"])

    # ==========================================
    # TAB 1: ALGORİTMİK TERMİNAL (ANA EKRAN)
    # ==========================================
    with tab1:
        st.markdown("### 📊 Algoritmik Kıyaslama Grafiği")

        fig = go.Figure()

        # Taha Yeşil Fon
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['TAHA_YESIL_FON'],
            mode='lines', name='Taha Yeşil Fon', line=dict(color='#DEFF9A', width=3),
            hovertemplate="<b>Taha Yeşil Fon:</b> %{y:.2f}<extra></extra>"
        ))

        # BIST100
        fig.add_trace(go.Scatter(
            x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri['XU100.IS'],
            mode='lines', name='BIST100', line=dict(color='#3B82F6', width=2), 
            hovertemplate="<b>BIST100:</b> %{y:.2f}<extra></extra>"
        ))

        if trend_goster:
            if f'SMA_{sma_kisa}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(
                    x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_kisa}'],
                    mode='lines', name=f'SMA {sma_kisa}', line=dict(color='#F59E0B', width=1.5, dash='dot'),
                ))
            if f'SMA_{sma_uzun}' in normalize_veri.columns:
                fig.add_trace(go.Scatter(
                    x=normalize_veri.index.strftime('%Y-%m-%d'), y=normalize_veri[f'SMA_{sma_uzun}'],
                    mode='lines', name=f'SMA {sma_uzun}', line=dict(color='#EF4444', width=1.5, dash='dot'),
                ))

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
            xaxis=dict(showgrid=True, gridcolor='#1E2532', tickangle=-45, rangeslider=dict(visible=False)),
            yaxis=dict(showgrid=True, gridcolor='#1E2532'),
            legend=dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5, font=dict(color='#FFFFFF')),
            margin=dict(l=0, r=0, t=20, b=0), hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True) 

        st.markdown("### 💰 100.000 TL Performans Simülasyonu")
        bist_sonuc = float(np.nan_to_num(100000 * (normalize_veri['XU100.IS'].iloc[-1] / 100), nan=100000))
        yesil_sonuc = float(np.nan_to_num(100000 * (normalize_veri['TAHA_YESIL_FON'].iloc[-1] / 100), nan=100000))
        fark = yesil_sonuc - bist_sonuc

        col1, col2, col3 = st.columns(3)
        col1.metric("Klasik BIST100 Getirisi", f"{bist_sonuc:,.0f} ₺", delta="Referans Endeks", delta_color="off")
        col2.metric("Taha Yeşil Fon Getirisi", f"{yesil_sonuc:,.0f} ₺", delta=f"{((yesil_sonuc-100000)/100000)*100:.1f}% Fon Büyümesi")
        col3.metric("Yaratılan ALFA (Ekstra Kâr)", f"{fark:+,.0f} ₺", delta="Piyasayı Yendi" if fark > 0 else "- Piyasaya Yenildi")

    # ==========================================
    # TAB 2: AI İSTİHBARAT & SİNYAL MERKEZİ
    # ==========================================
    with tab2:
        st.markdown("### 🕵️‍♂️ NLP Haber Okuyucusu (Piyasa Hissiyatı)")
        st.markdown("Sistem, hisselerle ilgili global ve yerel haber başlıklarını tarar; kelime köklerini analiz ederek piyasanın duygu durumunu (Sentiment) matematiksel olarak puanlar.")
        
        # Basit ama etkili NLP Sözlüğü (Sıfır kütüphane bağımlılığı)
        bullish_words = ['yüksel', 'artış', 'kâr', 'büyüme', 'anlaşma', 'pozitif', 'hedef', 'rekor', 'up', 'surge', 'profit', 'buy', 'growth', 'green', 'rally', 'yatırım', 'teşvik']
        bearish_words = ['düşüş', 'zarar', 'risk', 'negatif', 'satış', 'kayıp', 'kriz', 'down', 'drop', 'loss', 'sell', 'bear', 'red', 'crash', 'dava', 'ceza', 'uyarı']

        hisse_haber = ['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS']
        
        col_haber1, col_haber2 = st.columns([2, 1])
        
        with col_haber1:
            haberi_bulunan = False
            for h in hisse_haber:
                try:
                    tkr = yf.Ticker(h)
                    news = tkr.news
                    if news and len(news) > 0:
                        haberi_bulunan = True
                        st.markdown(f"**{h.split('.')[0]} Son Gelişmeler:**")
                        for n in news[:2]: # Son 2 haber
                            title = n.get('title', '')
                            publisher = n.get('publisher', 'Bilinmeyen Kaynak')
                            
                            # Sentiment Motoru
                            title_lower = title.lower()
                            bull_score = sum(1 for word in bullish_words if word in title_lower)
                            bear_score = sum(1 for word in bearish_words if word in title_lower)
                            
                            if bull_score > bear_score:
                                sentiment_html = '<span class="sentiment-bull">🟢 BULLISH (POZİTİF)</span>'
                            elif bear_score > bull_score:
                                sentiment_html = '<span class="sentiment-bear">🔴 BEARISH (NEGATİF)</span>'
                            else:
                                sentiment_html = '<span class="sentiment-neutral">⚪ NEUTRAL (NÖTR)</span>'

                            st.markdown(f"""
                            <div class="news-card">
                                <div class="news-title">{title}</div>
                                <div class="news-publisher">Kaynak: {publisher} | AI Analizi: {sentiment_html}</div>
                            </div>
                            """, unsafe_allow_html=True)
                except:
                    pass
            
            if not haberi_bulunan:
                st.info("Şu an için piyasada taranacak sıcak bir haber akışı bulunmuyor.")

        with col_haber2:
            st.markdown("### 🤖 Canlı AI Karar Motoru")
            
            # Son fiyatın hareketli ortalamaya göre durumu (Basit Sinyal Üretimi)
            son_fiyat_fon = normalize_veri['TAHA_YESIL_FON'].iloc[-1]
            if trend_goster and f'SMA_{sma_uzun}' in normalize_veri.columns:
                sma_degeri = normalize_veri[f'SMA_{sma_uzun}'].iloc[-1]
                if son_fiyat_fon > sma_degeri * 1.05:
                    durum = "AŞIRI ALIM (ISINMA)"
                    renk = "#F59E0B"
                    tavsiye = "Kâr Al / Kademeli Satış Düşün"
                elif son_fiyat_fon > sma_degeri:
                    durum = "GÜÇLÜ TREND"
                    renk = "#A3FF00"
                    tavsiye = "Pozisyonu Koru (HOLD)"
                else:
                    durum = "DÜŞÜŞ TRENDİ / FIRSAT"
                    renk = "#FF4C4C"
                    tavsiye = "Destek Bekle / Kademeli Topla"
            else:
                durum = "ANALİZ İÇİN TREND KALKANI AÇILMALI"
                renk = "#8B949E"
                tavsiye = "-"

            st.markdown(f"""
            <div style="background: #121721; padding: 20px; border-radius: 12px; border: 1px solid {renk}; text-align: center;">
                <p style="color: #8B949E; font-size: 14px; margin-bottom: 5px; text-transform: uppercase;">Mevcut Piyasa Rejimi</p>
                <h2 style="color: {renk}; margin-top: 0; font-size: 24px;">{durum}</h2>
                <p style="color: #F5F5F5; font-size: 16px; margin-bottom: 0;">AI Tavsiyesi: <b>{tavsiye}</b></p>
            </div>
            """, unsafe_allow_html=True)


    # ==========================================
    # TAB 3: KUANTUM RİSK YÖNETİMİ
    # ==========================================
    with tab3:
        getiriler = veri.pct_change().dropna()
        if len(getiriler) > 0:
            portfoy_getiri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']].mean(axis=1)

            bist_vol = float(np.nan_to_num(getiriler['XU100.IS'].std() * (252 ** 0.5) * 100))
            fon_vol = float(np.nan_to_num(portfoy_getiri.std() * (252 ** 0.5) * 100))

            fon_kumulatif = (1 + portfoy_getiri).cumprod()
            fon_zirve = fon_kumulatif.cummax()
            drawdown_serisi = ((fon_kumulatif - fon_zirve) / fon_zirve) * 100
            fon_dd = float(np.nan_to_num(drawdown_serisi.min()))

            st.markdown("### ⚖️ Kantitatif Risk Özeti")
            r_col1, r_col2, r_col3 = st.columns(3)
            r_col1.metric("BIST100 Yıllık Volatilite", f"%{bist_vol:.2f}", delta="Piyasa Riski", delta_color="off")
            r_col2.metric("Sovereign Fon Volatilite", f"%{fon_vol:.2f}", delta="Agresif Büyüme Riski", delta_color="off")
            r_col3.metric("Maksimum Düşüş (Max Drawdown)", f"%{fon_dd:.2f}", delta="Kriz Direnci", delta_color="off")
            
            st.markdown("---")
            
            kor_col1, kor_col2 = st.columns([2, 1])
            with kor_col1:
                st.markdown("**🧩 Fon Korelasyon Matrisi**")
                hisse_getirileri = getiriler[['ALFAS.IS', 'YEOTK.IS', 'ASTOR.IS', 'KCAER.IS']]
                hisse_isimleri = ['ALFAS', 'YEOTK', 'ASTOR', 'KCAER']
                kor_matrisi = hisse_getirileri.corr().values
                
                # Zengin karanlık tema Isı Haritası
                fig_corr = go.Figure(data=go.Heatmap(
                    z=kor_matrisi, x=hisse_isimleri, y=hisse_isimleri,
                    colorscale=[[0, '#090B10'], [0.5, '#1E3A8A'], [1, '#DEFF9A']], 
                    text=np.round(kor_matrisi, 2), texttemplate="%{text}",
                    textfont={"color": "white", "size": 14}, showscale=False
                ))
                fig_corr.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, autorange='reversed'),
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                st.plotly_chart(fig_corr, use_container_width=True)
                
            with kor_col2:
                st.markdown("**🌊 Kriz Direnci (Sualtı Grafiği)**")
                fig_dd = go.Figure()
                fig_dd.add_trace(go.Scatter(
                    x=drawdown_serisi.index.strftime('%Y-%m-%d'), y=drawdown_serisi,
                    fill='tozeroy', mode='lines', line=dict(color='#FF4C4C', width=1),
                    fillcolor='rgba(255, 76, 76, 0.2)', name='Drawdown'
                ))
                fig_dd.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
                    xaxis=dict(showgrid=True, gridcolor='#1E2532'), yaxis=dict(showgrid=True, gridcolor='#1E2532'),
                    margin=dict(t=20, b=20, l=20, r=20), hovermode='x unified'
                )
                st.plotly_chart(fig_dd, use_container_width=True)

            st.markdown("---")
            st.markdown("### 🔮 Monte Carlo Gelecek Projeksiyonu (1 Yıl)")
            
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
                    y=simulasyon_df[:, i], mode='lines',
                    line=dict(color='rgba(222, 255, 154, 0.05)', width=1), showlegend=False, hoverinfo='skip'
                ))
                
            beklenen_senaryo = simulasyon_df.mean(axis=1)
            fig_mc.add_trace(go.Scatter(
                y=beklenen_senaryo, mode='lines', name='Beklenen Senaryo',
                line=dict(color='#3B82F6', width=3, dash='dash')
            ))
            
            fig_mc.update_layout(
                plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#F5F5F5'),
                xaxis=dict(showgrid=True, gridcolor='#1E2532', title="Gelecek Günler"),
                yaxis=dict(showgrid=True, gridcolor='#1E2532', title="Sermaye (TL)"),
                margin=dict(t=20, b=20, l=20, r=20), hovermode='x unified',
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_mc, use_container_width=True)

        else:
            st.warning("Veri yetersiz.")

except Exception as e:
    st.error(f"Güvenli moda geçildi. Hata: {e}")
