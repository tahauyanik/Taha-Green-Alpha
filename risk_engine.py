{
  "nbformat": 4,
  "nbformat_minor": 0,
  "metadata": {
    "colab": {
      "provenance": [],
      "authorship_tag": "ABX9TyOu7ZmdMhCNdOtn8f7E6XwN",
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
        "<a href=\"https://colab.research.google.com/github/tahauyanik/Taha-Green-Alpha/blob/main/risk_engine.py\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": null,
      "metadata": {
        "id": "PHCqav-_I4T7"
      },
      "outputs": [],
      "source": [
        "import numpy as np\n",
        "\n",
        "class SovereignRiskEngine:\n",
        "    @staticmethod\n",
        "    def calculate_metrics(returns, benchmark_returns, risk_free_rate=0.40):\n",
        "        rf_daily = risk_free_rate / 252\n",
        "        annual_volatility = returns.std() * np.sqrt(252) * 100\n",
        "        bench_volatility = benchmark_returns.std() * np.sqrt(252) * 100\n",
        "\n",
        "        cov_matrix = np.cov(returns, benchmark_returns)\n",
        "        beta = cov_matrix[0, 1] / cov_matrix[1, 1] if cov_matrix[1, 1] > 0 else 1\n",
        "        port_ann_return = returns.mean() * 252\n",
        "        bench_ann_return = benchmark_returns.mean() * 252\n",
        "        alpha = (port_ann_return - (risk_free_rate + beta * (bench_ann_return - risk_free_rate))) * 100\n",
        "\n",
        "        excess_returns = returns - rf_daily\n",
        "        negative_returns = excess_returns[excess_returns < 0]\n",
        "        downside_deviation = negative_returns.std() * np.sqrt(252)\n",
        "        sortino_ratio = (excess_returns.mean() * 252) / downside_deviation if downside_deviation > 0 else 0\n",
        "\n",
        "        cumulative = (1 + returns).cumprod()\n",
        "        peak = cumulative.cummax()\n",
        "        drawdown = ((cumulative - peak) / peak) * 100\n",
        "        max_dd = drawdown.min()\n",
        "        calmar_ratio = (port_ann_return * 100) / abs(max_dd) if abs(max_dd) > 0 else 0\n",
        "\n",
        "        tracking_error = (returns - benchmark_returns).std() * np.sqrt(252)\n",
        "        info_ratio = (port_ann_return - bench_ann_return) / tracking_error if tracking_error > 0 else 0\n",
        "\n",
        "        var_95 = np.percentile(returns.dropna() * 100, 5)\n",
        "        cvar_95 = returns.dropna()[returns.dropna() * 100 <= var_95].mean() * 100\n",
        "\n",
        "        return (annual_volatility, bench_volatility, sortino_ratio, calmar_ratio, info_ratio,\n",
        "                max_dd, var_95, cvar_95, drawdown, alpha, beta)\n",
        "\n",
        "    @staticmethod\n",
        "    def simulate_gbm(portfolio_returns, days=252, simulations=100, initial_capital=100000):\n",
        "        mu = portfolio_returns.mean()\n",
        "        sigma = portfolio_returns.std()\n",
        "        sim_df = np.zeros((days, simulations))\n",
        "        sim_df[0] = initial_capital\n",
        "        for t in range(1, days):\n",
        "            sim_df[t] = sim_df[t-1] * (1 + np.random.normal(loc=mu, scale=sigma, size=simulations))\n",
        "        return sim_df\n",
        "\n",
        "    @staticmethod\n",
        "    def markowitz_optimization(close_data, num_ports=5000):\n",
        "        log_ret = np.log1p(close_data.pct_change()).dropna()\n",
        "        all_weights = np.zeros((num_ports, 4))\n",
        "        ret_arr = np.zeros(num_ports)\n",
        "        vol_arr = np.zeros(num_ports)\n",
        "        sharpe_arr = np.zeros(num_ports)\n",
        "\n",
        "        mean_log_ret = log_ret.mean()\n",
        "        cov_mat = log_ret.cov()\n",
        "\n",
        "        np.random.seed(42)\n",
        "        for x in range(num_ports):\n",
        "            weights = np.array(np.random.random(4))\n",
        "            weights = weights / np.sum(weights)\n",
        "            all_weights[x,:] = weights\n",
        "\n",
        "            ret_arr[x] = np.sum((mean_log_ret * weights) * 252)\n",
        "            vol_arr[x] = np.sqrt(np.dot(weights.T, np.dot(cov_mat * 252, weights)))\n",
        "            sharpe_arr[x] = ret_arr[x] / vol_arr[x] if vol_arr[x] > 0 else 0\n",
        "\n",
        "        return all_weights, ret_arr, vol_arr, sharpe_arr"
      ]
    }
  ]
}