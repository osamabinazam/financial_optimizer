import numpy as np
import pandas as pd


def calculate_returns(dataframe, timeframe, return_method):
    """
    Calculate returns based on the type of return and timeframe provided. Returns is calculated based on the formula:
    (current price - previous price) / previous price
    and then multiplied by 100 to get the percentage return.

    To calculate log returns, the formula is:
    log(current price / previous price)

    :param dataframe: Contains the stock price data
    :param timeframe: Contains the timeframe for which the returns are calculated (daily, weekly, bi-weekly, monthly, quarterly, semi-annually)
    :param return_method: Contains the method for calculating returns (simple or log)
    :return:
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

    # Calculating returns based on the method
    if return_method == 'simple':
        returns = resampled_df.pct_change().dropna()
    elif return_method == 'log':
        returns = np.log(resampled_df / resampled_df.shift(1)).dropna()
    return returns


def risk_averse_method(portfolio_return, portfolio_volatility, metric, risk_free_rate=0.01 / 252):
    """
    Calculate the risk-averse metric based on the metric provided. The method can be one of the following:
    - Sharpe Ratio
    - Sharpe Squared
    - Sortino Ratio
    - Omega
    - Calmar
    - Rachev
    - Information Ratio


    :param dataframe: Contains the stock price data
    :param metric: Contains the method for calculating risk-averse metrics
    :return:
    """

    if metric == 'sharpe_ratio':
        return portfolio_return - risk_free_rate / portfolio_volatility
    elif metric == 'sharpe_squared':
        return ((portfolio_return - risk_free_rate) / portfolio_volatility) ** 2
    elif metric == 'omega':
        threshold = risk_free_rate
        excess_returns = portfolio_return - threshold
        gains = excess_returns[excess_returns > 0].sum().sum()
        losses = -excess_returns[excess_returns < 0].sum().sum()
        if losses != 0:
            return gains / losses
        else:
            return 1
    else:
        return None
    # elif metric == 'sortino':
    #     negative_returns = portfolio_return[portfolio_return < 0]
    #     downside_volatility = np.sqrt(np.mean(negative_returns ** 2))
    #     return (portfolio_return - risk_free_rate) / downside_volatility


