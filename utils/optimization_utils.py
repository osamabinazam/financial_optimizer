import pandas as pd
def calculate_return(data, start_date, end_date, initial_investment):
    """
    Calculate the return of an investment in a stock between two dates.

    Args:
    data (pd.DataFrame): The stock price data
    start_date (str): The start date of the investment
    end_date (str): The end date of the investment
    initial_investment (float): The initial investment amount

    Returns:
    float: The return on investment
    """

    # Filter the data for the given date range
    filtered_data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Calculate the return on investment
    start_price = filtered_data.iloc[0]['Close']
    end_price = filtered_data.iloc[-1]['Close']
    shares_purchased = initial_investment / start_price
    final_value = shares_purchased * end_price
    return_on_investment = (final_value - initial_investment) / initial_investment * 100

    return return_on_investment
