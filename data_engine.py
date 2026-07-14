{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPfEabci6ElkpD2RS5W1fba",
      "include_colab_link": true
    },
    "kernelspec": {
      "name": "python3",
      "display_name": "Python 3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "view-in-github",
        "colab_type": "text"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/tahauyanik/Taha-Green-Alpha/blob/main/data_engine.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 384
        },
        "id": "hrF_HlE1Hhic",
        "outputId": "0e24053a-fa36-4a64-d52e-5982b93adf37"
      },
      "outputs": [
        {
          "output_type": "error",
          "ename": "ModuleNotFoundError",
          "evalue": "No module named 'streamlit'",
          "traceback": [
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
            "\u001b[0;31mModuleNotFoundError\u001b[0m                       Traceback (most recent call last)",
            "\u001b[0;32m/tmp/ipykernel_1770/1717106568.py\u001b[0m in \u001b[0;36m<cell line: 0>\u001b[0;34m()\u001b[0m\n\u001b[1;32m      4\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mrequests\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      5\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mxml\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0metree\u001b[0m\u001b[0;34m.\u001b[0m\u001b[0mElementTree\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mET\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0;32m----> 6\u001b[0;31m \u001b[0;32mimport\u001b[0m \u001b[0mstreamlit\u001b[0m \u001b[0;32mas\u001b[0m \u001b[0mst\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[0m\u001b[1;32m      7\u001b[0m \u001b[0;32mimport\u001b[0m \u001b[0mtime\u001b[0m\u001b[0;34m\u001b[0m\u001b[0;34m\u001b[0m\u001b[0m\n\u001b[1;32m      8\u001b[0m \u001b[0;34m\u001b[0m\u001b[0m\n",
            "\u001b[0;31mModuleNotFoundError\u001b[0m: No module named 'streamlit'",
            "",
            "\u001b[0;31m---------------------------------------------------------------------------\u001b[0;32m\nNOTE: If your import is failing due to a missing package, you can\nmanually install dependencies using either !pip or !apt.\n\nTo view examples of installing some common dependencies, click the\n\"Open Examples\" button below.\n\u001b[0;31m---------------------------------------------------------------------------\u001b[0m\n"
          ],
          "errorDetails": {
            "actions": [
              {
                "action": "open_url",
                "actionText": "Open Examples",
                "url": "/notebooks/snippets/importing_libraries.ipynb"
              }
            ]
          }
        }
      ],
      "source": [
        "import yfinance as yf\n",
        "import pandas as pd\n",
        "import numpy as np\n",
        "import requests\n",
        "import xml.etree.ElementTree as ET\n",
        "import streamlit as st\n",
        "import time\n",
        "\n",
        "class SovereignDataEngine:\n",
        "    @staticmethod\n",
        "    @st.cache_data(ttl=1800, show_spinner=False)\n",
        "    def fetch_market_data(tickers, period):\n",
        "        data = yf.download(tickers, period=period, progress=False, threads=True)\n",
        "        if data.empty:\n",
        "            raise ValueError(\"API Kritik Hatası: Veri çekilemedi.\")\n",
        "        return data['Close'], data['Volume'], data['High'], data['Low'], data['Open']\n",
        "\n",
        "    @staticmethod\n",
        "    def calculate_technical_indicators(close_prices, volume):\n",
        "        delta = close_prices.diff()\n",
        "        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()\n",
        "        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()\n",
        "        rs = gain / loss\n",
        "        rsi = 100 - (100 / (1 + rs))\n",
        "\n",
        "        exp1 = close_prices.ewm(span=12, adjust=False).mean()\n",
        "        exp2 = close_prices.ewm(span=26, adjust=False).mean()\n",
        "        macd = exp1 - exp2\n",
        "        signal_line = macd.ewm(span=9, adjust=False).mean()\n",
        "\n",
        "        obv = (np.sign(delta) * volume).fillna(0).cumsum()\n",
        "\n",
        "        sma_20 = close_prices.rolling(window=20).mean()\n",
        "        std_20 = close_prices.rolling(window=20).std()\n",
        "        upper_band = sma_20 + (std_20 * 2.1)\n",
        "        lower_band = sma_20 - (std_20 * 2.1)\n",
        "\n",
        "        return rsi, macd, signal_line, upper_band, lower_band, obv, sma_20\n",
        "\n",
        "    @staticmethod\n",
        "    @st.cache_data(ttl=600, show_spinner=False)\n",
        "    def fetch_live_news():\n",
        "        try:\n",
        "            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}\n",
        "            url = \"https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664\"\n",
        "            response = requests.get(url, headers=headers, timeout=5)\n",
        "            root = ET.fromstring(response.content)\n",
        "            news_items = []\n",
        "            for item in root.findall('./channel/item')[:4]:\n",
        "                title = item.find('title').text\n",
        "                pub_date = item.find('pubDate').text[:16]\n",
        "                news_items.append({'title': title, 'date': pub_date})\n",
        "            return news_items\n",
        "        except Exception:\n",
        "            return []\n",
        "\n",
        "    @staticmethod\n",
        "    def generate_ai_report(port_returns, max_dd, sortino, optimal_weights, tickers):\n",
        "        time.sleep(1.5) # API gecikmesini simüle et\n",
        "\n",
        "        annual_ret = port_returns.mean() * 252 * 100\n",
        "        volatility = port_returns.std() * np.sqrt(252) * 100\n",
        "\n",
        "        max_weight_idx = np.argmax(optimal_weights)\n",
        "        top_asset = tickers[max_weight_idx].replace('.IS', '')\n",
        "        top_weight = optimal_weights[max_weight_idx] * 100\n",
        "\n",
        "        stance = \"Aggressive Growth\" if annual_ret > 50 else \"Defensive Value\"\n",
        "        risk_profile = \"Elevated\" if max_dd < -20 else \"Controlled\"\n",
        "\n",
        "        report = f\"\"\"\n",
        "        **Sovereign Otonom Danışman Raporu (LLM Model: Quant-Alpha-v1)**\n",
        "\n",
        "        Portföy analiziniz başarıyla tamamlandı. Sistemin tespitleri aşağıdadır:\n",
        "\n",
        "        **1. Performans ve Risk Karakteri:** Fonunuz şu anda %{annual_ret:.1f} seviyesinde yıllıklandırılmış bir getiri hızıyla {stance} karakteri sergiliyor. Ancak, %{volatility:.1f} seviyesindeki volatilite ve %{max_dd:.1f} Maksimum Düşüş (Drawdown), risk profilinizin '{risk_profile}' olduğuna işaret ediyor.\n",
        "\n",
        "        **2. Optimizasyon Önerisi (Markowitz):**\n",
        "        Sharpe oranınızı maksimize etmek için algoritma, portföy sermayesinin **%{top_weight:.1f}'sini {top_asset}** varlığına kaydırmanızı şiddetle tavsiye etmektedir. Bu hamle, fonun Sortino (Aşağı yön riski) korumasını güçlendirecektir.\n",
        "\n",
        "        **3. Taktiksel Görünüm:**\n",
        "        Aşağı yönlü korumanız (Sortino: {sortino:.2f}) {'oldukça güçlü, piyasa şoklarına karşı dayanıklısınız.' if sortino > 1 else 'zayıf. Daha fazla nakit pozisyonu veya düşük betalı varlık eklemeniz önerilir.'}\n",
        "        \"\"\"\n",
        "        return report"
      ]
    }
  ]
}