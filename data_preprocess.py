import pandas as pd
from statsmodels.tsa.stattools import adfuller, pacf, acf
import matplotlib.pyplot as plt
import numpy as np

def pre_process(csv_data_file_path, resample_period='H'):
    df = pd.read_csv(csv_data_file_path)
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
    df['Date'] = pd.to_datetime(df['Date'])
    # Will need to create a loop, as we have multiple within year
    # Exog
    #holidays = pd.date_range(start='2023-07-14', end='2023-08-01', freq='D')
    #terms = pd.date_range(start='2023-08-01', end='2023-08-07', freq='D')
    #df['Holiday'] = df['Date'].isin(holidays)
    #df['Term'] = df['Date'].isin(terms)
    #df['Weekend'] = df['Datetime'].apply(lambda x: 1 if x.weekday() >= 5 else 0).astype(int)

    df.set_index('Datetime', inplace=True)
    df.sort_index(ascending=True)
    df.drop(columns=['Date', 'Time'], inplace=True)

    agg_functions = {'Total': 'median'} # , 'Weekend': 'max', 'Holiday': 'max', 'Term': 'max'
    df_resample = df.resample(resample_period).agg(agg_functions).bfill()

    """for i in ['Weekend', 'Holiday', 'Term']:
        df_resample[i] = df_resample[i].astype(int)"""

    assert (df_resample['Total'].isna().sum() == 0)
    return df_resample



