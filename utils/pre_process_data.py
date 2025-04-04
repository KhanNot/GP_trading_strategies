"""
This module provides utility functions for preprocessing financial data and generating 
additional features for analysis. It includes functions to create moving average columns, 
lagged columns, percentage-based columns, and difference columns. Additionally, it provides 
a function to fetch historical data for a given ticker symbol and preprocess it by removing 
null values and unnecessary columns.
Functions:
----------
- create_ma_columns(df, column, lag):
    Adds a moving average column to the DataFrame for a specified column and lag.
- create_lagged_columns(df, column, lag):
    Adds a lagged column to the DataFrame for a specified column and lag.
- create_percentage_of_value(df, column, percentage=random.random()):
    Adds a column to the DataFrame representing a percentage of the specified column's value.
- create_difference(df, column1="low", column2="high"):
    Adds a column to the DataFrame representing the difference between two specified columns.
- pre_process(df):
    Removes rows with null values and drops unnecessary columns from the DataFrame.
- get_data(ticker="BTC-USD", start='2016-01-01', end='2024-06-30', ma_lags=50, lag_lags=50, pers_col_num=10):
    Fetches historical data for a given ticker symbol, generates additional features, 
    and preprocesses the data.
Usage:
------
This module is designed to be imported and used as part of a larger data analysis pipeline. 
The `get_data` function serves as the main entry point for fetching and preprocessing data.
"""
import yfinance as yf
import random

def create_ma_columns(df,column, lag):
    """
    Adds a moving average (MA) column to the given DataFrame based on the specified column and lag.
    Parameters:
        df (pandas.DataFrame): The input DataFrame containing the data.
        column (str): The name of the column in the DataFrame for which the moving average is calculated.
        lag (int): The window size (number of periods) for calculating the moving average.
    Returns:
        pandas.DataFrame: The DataFrame with the new moving average column added. 
                            The new column is named in the format "ma_<column>_<lag>".
    """
    df[f"ma_{column.lower()}_{lag}"]= df[column].rolling(window = lag).mean()
    return df

def create_lagged_columns(df, column, lag):
    """
    Creates lagged columns in a DataFrame for a specified column and lag value.
    Parameters:
        df (pandas.DataFrame): The input DataFrame.
        column (str): The name of the column to create lagged values for.
        lag (int): The number of periods to shift the column values.
    Returns:
        pandas.DataFrame: The DataFrame with the newly created lagged column added.
                        The new column is named in the format "lag_<column>_<lag>".
    """
    df[f"lag_{column.lower()}_{lag}"]= df[column].shift(lag)
    return df

def create_percentage_of_value(df, column, percentage:float = random.random()):
    """
    Creates a new column in the given DataFrame that represents a percentage of the values 
    in the specified column. The percentage is either provided as an argument or randomly 
    generated if not specified.
    Args:
        df (pd.DataFrame): The input DataFrame.
        column (str): The name of the column in the DataFrame to calculate the percentage of.
        percentage (float, optional): The percentage to apply to the column values. 
                                        Defaults to a random float between 0 and 1.
    Returns:
        pd.DataFrame: The DataFrame with the new column added. The new column is named 
                        using the format "percentage_<column_name>_<percentage_value>".
    """
    df[f"percentage_{column.lower()}_{(round(percentage*100,))}"]= df[column]*percentage
    # df[f"percentage_{column.lower()}_{(percentage*100,)}"]= df[column]*percentage
    return df

def create_difference(df, column1:str = "low", column2:str = "high"):
    """
    Creates a new column in the given DataFrame that represents the difference 
    between two specified columns.
    Parameters:
        df (pd.DataFrame): The input DataFrame containing the data.
        column1 (str): The name of the first column (default is "low").
        column2 (str): The name of the second column (default is "high").
    Returns:
        pd.DataFrame: The modified DataFrame with a new column named 
                        'difference_<column1>_<column2>' containing the differences.
    """
    df[f"difference_{column1.lower()}_{column2.lower()}"]= df[column2]-df[column1]
    return df

def pre_process(df):
    """
    Pre-processes the given DataFrame by performing the following steps:
    1. Identifies and removes rows with any missing values.
    2. Drops the columns 'Dividends' and 'Stock Splits' from the DataFrame.
    Parameters:
        df (pandas.DataFrame): The input DataFrame to be pre-processed.
    Returns:
        pandas.DataFrame: The cleaned DataFrame with rows containing missing values removed 
                        and specified columns dropped.
    """
    
    null_rows = df.isna().sum(axis=1)[df.isna().sum(axis=1)!=0]
    null_row_indices = list(null_rows.index)
    df.drop(null_row_indices,inplace=True)
    # sum(df.isna().sum(axis=1))
    df.drop(['Dividends','Stock Splits'], axis=1,inplace = True)
    return df

def get_data(
        ticker = "BTC-USD", 
        start='2016-01-01', 
        end='2024-06-30',
        ma_lags = 50,
        lag_lags = 50,
        pers_col_num = 10
    ):
    """
    Fetches historical stock or cryptocurrency data for a given ticker symbol, 
    processes the data by adding moving average, lagged, and percentage-based 
    columns, and returns the pre-processed DataFrame.
    Parameters:
        ticker (str): The ticker symbol of the asset to fetch data for. 
                    Default is "BTC-USD".
        start (str): The start date for fetching historical data in 'YYYY-MM-DD' format. 
                    Default is '2016-01-01'.
        end (str): The end date for fetching historical data in 'YYYY-MM-DD' format. 
                Default is '2024-06-30'.
        ma_lags (int): The number of moving average lag columns to create for each base column. 
                    Default is 50.
        lag_lags (int): The number of lagged columns to create for each base column. 
                Default is 50.
        pers_col_num (int): The number of percentage-based columns to create for each base column. 
                    Default is 10.
    Returns:
        pandas.DataFrame: A pre-processed DataFrame containing the original data 
                    along with the generated moving average, lagged, and 
                    percentage-based columns.
    """
    df = yf.Ticker(ticker).history(start=start, end=end)

    #Add in columns:
    base_columns_list = ['Open', 'High', 'Low', 'Close', 'Volume']
    for column in base_columns_list:
        for lag in range(2,ma_lags):
            create_ma_columns(df = df,column=column, lag = lag)
        for lag in range(1,lag_lags):
            create_lagged_columns(df = df,column=column, lag = lag)
        for i in range(pers_col_num):
            create_percentage_of_value(df = df,column=column)
        create_percentage_of_value(df = df,column=column , percentage=0.37)
        create_percentage_of_value(df = df,column=column , percentage=0.57)
        create_percentage_of_value(df = df,column=column , percentage=0.60)
        create_percentage_of_value(df = df,column=column , percentage=0.68)

    return pre_process(df)

if __name__ =='__main__':
    pass
