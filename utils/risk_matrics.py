from performance_matrics import calculate_portfolio_metrics, calculate_benchmark_stock_metrics
import numpy as np

def calculate_returns(dataframe, timeframe, return_method):
    """
    Calculate returns based on the type of return and timeframe provided.

    :param dataframe: DataFrame containing the stock price data.
    :param timeframe: Timeframe for calculating returns (daily, weekly, monthly, etc.).
    :param return_method: Method for calculating returns ('simple' or 'log').
    :return: DataFrame with calculated returns.
    """
    # Dictionary mapping timeframes to pandas resample rule strings
    returns = None
    timeframe_rules = {
        'daily': 'D',
        'weekly': 'W',
        'bi-weekly': '2W',
        'monthly': 'M',
        'quarterly': 'Q',
        'semi-annually': '6M',
    }

    if timeframe not in timeframe_rules:
        raise ValueError("Invalid timeframe provided. Please provide a valid timeframe.")
    if return_method not in ['simple', 'log']:
        raise ValueError("Invalid return method provided. Please provide a valid return method.")

    # Resampling dataframe based on timeframe
    if timeframe == 'daily':
        resampled_df = dataframe
    else:
        resampled_df = dataframe.resample(timeframe_rules[timeframe]).ffill()

    # Calculating returns based on the return method
    if return_method == 'simple':
        returns = resampled_df.pct_change().dropna()
    elif return_method == 'log':
        returns = np.log(resampled_df / resampled_df.shift(1)).dropna()

    return returns


def risk_averse_method(portfolio_return, portfolio_volatility, metric, returns=None, risk_free_rate=0.02 / 252):
    """
    Calculate the risk-averse metric based on the metric provided.

    Supported metrics:
    - 'sharpe_ratio': Calculates the Sharpe Ratio.
    - 'sharpe_squared': Calculates the Sharpe Squared.
    - 'sortino': Calculates the Sortino Ratio (downside risk only).
    - 'omega': Calculates the Omega Ratio.

    :param portfolio_return: Portfolio return.
    :param portfolio_volatility: Portfolio volatility (standard deviation).
    :param metric: Selected metric for risk-adjusted return calculation.
    :param returns: Returns data needed for certain metrics (like Sortino and Omega).
    :param risk_free_rate: Risk-free rate (default: 0.01/252 for daily risk-free rate).
    :return: Calculated risk metric.
    """
    # Calculate Sharpe Ratio
    if metric == 'sharpe_ratio':
        return (portfolio_return - risk_free_rate) / portfolio_volatility

    # Calculate Sharpe Squared
    elif metric == 'sharpe_squared':
        return ((portfolio_return - risk_free_rate) / portfolio_volatility) ** 2

    # Calculate Sortino Ratio (using downside risk)
    elif metric == 'sortino':
        negative_returns = returns[returns < 0]
        downside_volatility = np.sqrt(np.mean(negative_returns ** 2))
        return (portfolio_return - risk_free_rate) / downside_volatility

    # Calculate Omega Ratio
    elif metric == 'omega':
        threshold = risk_free_rate
        excess_returns = returns - threshold
        gains = excess_returns[excess_returns > 0].sum()
        losses = -excess_returns[excess_returns < 0].sum()
        if losses != 0:
            return gains / losses
        else:
            return np.inf  # If no losses, Omega ratio is theoretically infinite.

    # More metrics like Calmar, Rachev, CVAR can be added here

    # If metric is not recognized
    else:
        raise ValueError("Invalid metric provided.")


def compare_portfolio_vs_benchmark(returns, weights, benchmark_returns, metric, risk_free_rate=0.02 / 252):
    """
    Compare the portfolio metrics against the benchmark returns using the selected metric.

    :param returns: DataFrame of portfolio returns.
    :param weights: Portfolio weights.
    :param benchmark_returns: Returns of the benchmark stock.
    :param metric: Selected performance metric (e.g., 'sharpe_ratio', 'sortino', 'omega').
    :param risk_free_rate: Risk-free rate for calculations (default 0.02 annualized).
    :return: Comparison results including the information ratio.
    """

    # Calculate portfolio metrics
    portfolio_return, portfolio_volatility = calculate_portfolio_metrics(returns, weights)
    portfolio_metric = risk_averse_method(portfolio_return, portfolio_volatility, metric, returns, risk_free_rate)

    # Calculate benchmark metrics
    benchmark_mean_return, benchmark_volatility = calculate_benchmark_stock_metrics(benchmark_returns)
    benchmark_metric = risk_averse_method(benchmark_mean_return, benchmark_volatility, metric, benchmark_returns,
                                          risk_free_rate)

    # Calculate excess return and excess volatility
    excess_return = portfolio_return - benchmark_mean_return
    excess_volatility = portfolio_volatility - benchmark_volatility

    # Calculate tracking error
    tracking_error = np.std(returns.mean() - benchmark_returns.mean())

    # Calculate information ratio
    if tracking_error != 0:
        information_ratio = excess_return / tracking_error
    else:
        information_ratio = np.inf  # Infinite information ratio if tracking error is zero

    return {
        'portfolio_return': portfolio_return,
        'portfolio_volatility': portfolio_volatility,
        'portfolio_metric': portfolio_metric,
        'benchmark_return': benchmark_mean_return,
        'benchmark_volatility': benchmark_volatility,
        'benchmark_metric': benchmark_metric,
        'excess_return': excess_return,
        'excess_volatility': excess_volatility,
        'tracking_error': tracking_error,
        'information_ratio': information_ratio
    }
