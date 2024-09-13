import numpy as np


def calculate_portfolio_metrics(returns, weights, risk_free_rate=0.02 / 252):
    """
    Calculates portfolio metrics: mean return, volatility, Sharpe Ratio.

    """
    portfolio_return = np.dot(weights, returns.mean())
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov(), weights)))
    sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_volatility
    return portfolio_return, portfolio_volatility, sharpe_ratio


def calculate_benchmark_stock_metrics(stock_returns, risk_free_rate=0.02 / 252):
    """Calculates metrics for a single stock."""
    stock_mean_return = stock_returns.mean()
    stock_volatility = stock_returns.std()
    stock_sharpe_ratio = (stock_mean_return - risk_free_rate) / stock_volatility
    return stock_mean_return, stock_volatility, stock_sharpe_ratio
