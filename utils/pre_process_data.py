
import yfinance as yf
import random

def create_ma_columns(df,column, lag):
    df[f"ma_{column.lower()}_{lag}"]= df[column].rolling(window = lag).mean()
    return df

def create_lagged_columns(df, column, lag):
    df[f"lag_{column.lower()}_{lag}"]= df[column].shift(lag)
    return df

def create_percentage_of_value(df, column, percentage:float = random.random()):
    df[f"percentage_{column.lower()}_{(round(percentage*100,))}"]= df[column]*percentage
    # df[f"percentage_{column.lower()}_{(percentage*100,)}"]= df[column]*percentage
    return df

def create_difference(df, column1:str = "low", column2:str = "high"):
    df[f"difference_{column1.lower()}_{column2.lower()}"]= df[column2]-df[column1]
    return df

def pre_process(df):
    """Remove nulls and columns from the DF."""
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
