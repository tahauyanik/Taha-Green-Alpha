{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyPNQ8XgAgLs3qr3+u2ypD29",
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
        "<a href=\"https://colab.research.google.com/github/tahauyanik/Taha-Green-Alpha/blob/main/visual_engine.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "3PzRUJvDJKAT"
      },
      "outputs": [],
      "source": [
        "import plotly.graph_objects as go\n",
        "\n",
        "class SovereignVisualEngine:\n",
        "    COLORS = {'bg': 'rgba(0,0,0,0)', 'card': '#0A0C12', 'grid': 'rgba(255,255,255,0.03)',\n",
        "              'text': '#8B949E', 'fund': '#DEFF9A', 'bist': '#3B82F6', 'red': '#FF4C4C'}\n",
        "\n",
        "    @classmethod\n",
        "    def apply_premium_layout(cls, fig):\n",
        "        fig.update_layout(\n",
        "            plot_bgcolor=cls.COLORS['bg'], paper_bgcolor=cls.COLORS['bg'],\n",
        "            font=dict(color=cls.COLORS['text'], family=\"Inter\"),\n",
        "            xaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280'), zeroline=False),\n",
        "            yaxis=dict(showgrid=True, gridcolor=cls.COLORS['grid'], tickfont=dict(size=10, color='#6B7280'), zeroline=False),\n",
        "            margin=dict(l=10, r=10, t=40, b=10), hovermode='x unified',\n",
        "            hoverlabel=dict(bgcolor=\"#0A0C12\", font_size=12, font_family=\"JetBrains Mono\", bordercolor=\"rgba(222,255,154,0.3)\")\n",
        "        )\n",
        "        return fig\n",
        "\n",
        "    @classmethod\n",
        "    def apply_card_layout(cls, fig):\n",
        "        fig = cls.apply_premium_layout(fig)\n",
        "        fig.update_layout(\n",
        "            paper_bgcolor=cls.COLORS['card'],\n",
        "            plot_bgcolor=cls.COLORS['card'],\n",
        "            margin=dict(l=30, r=30, t=60, b=30),\n",
        "            shapes=[dict(type=\"rect\", xref=\"paper\", yref=\"paper\", x0=0, y0=0, x1=1, y1=1,\n",
        "                        line=dict(color=\"rgba(255,255,255,0.05)\", width=1))]\n",
        "        )\n",
        "        return fig"
      ]
    }
  ]
}