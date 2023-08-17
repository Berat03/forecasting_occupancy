import pandas as pd
import pmdarima as pmd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX


# Pre-processing data from CSV to pandas df
def pre_process(csv_data_file_path, resample_period='H'):
    df = pd.read_csv(csv_data_file_path, delimiter=',')
    df['Datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y-%m-%d %H:%M')
    df.dropna(inplace=True)
    # Exog variables
    holidays = pd.date_range(start='2023-07-14', end='2023-07-28', freq='D')
    terms = pd.date_range(start='2023-07-29', end='2023-08-12', freq='D')
    df['Holiday'] = pd.to_datetime(df['Datetime'].dt.date).isin(holidays).astype(int)
    df['Term'] = pd.to_datetime(df['Datetime'].dt.date).isin(terms).astype(int)
    df['Weekend'] = df['Datetime'].apply(lambda x: 1 if x.weekday() >= 5 else 0).astype(int)
    df.set_index('Datetime', inplace=True)
    df.sort_index(ascending=True, inplace=True)
    df.drop(columns=['Date', 'Time'], inplace=True)
    agg_functions = {'Total': 'median', 'Weekend': 'max', 'Holiday': 'max', 'Term': 'max'}  #
    df_resample = df.resample(resample_period).agg(agg_functions).bfill()

    assert (df_resample['Total'].isna().sum() == 0)
    return df_resample


# Finding parameters for SARIMAX
def find_parameters(df, col, exog_var=None, train=0.8, cut_off=0, m=24):
    df = df.iloc[:(len(df) - cut_off)]
    time_series_data_col = df[col].iloc[:int(len(df) * train)]

    if exog_var is not None:
        exog = df[exog_var].iloc[:int(len(df) * train)].values.reshape(-1, 1)
    else:
        exog = None

    results_auto_arima = pmd.auto_arima(y=time_series_data_col,
                                        exogenous=exog,
                                        start_p=0,
                                        start_d=0,
                                        start_q=0,
                                        start_P=0,
                                        start_Q=0,
                                        trend='c',
                                        seasonal=True,
                                        m=m,
                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore',
                                        njobs=-1,
                                        )

    print(results_auto_arima)


# Apply ARIMA and print results
"""
order=(4, 1, 1),
seasonal_order=(3, 0, 1, 24),
"""

def sarimax_apply(df, pred_period, forecast_periods, cut_off=0, *args, **kwargs):
    df = df.iloc[:(len(df) - cut_off)]

    mod = SARIMAX(endog=df['Total'],
                  exog=df['Weekend'],
                  order=(1, 0, 0),
                  seasonal_order=(1, 0, 0, 24),
                  trend='c')

    results = mod.fit(maxiter=50)

    exog_forecast = df['Weekend'][-forecast_periods:].values.reshape(-1, 1)

    predicted = results.get_prediction(start=-pred_period, exog=df['Weekend'])
    forecast = results.get_forecast(steps=forecast_periods, exog=exog_forecast)

    predicted_mean_clipped = np.clip(predicted.predicted_mean, 0, 1800)  # range currently [0,1800]
    forecast_mean_clipped = np.clip(forecast.predicted_mean, 0, 1800)

    plt.plot(df.index[-pred_period:], df['Total'][-pred_period:], label='Actual (Historical and Forecasted)')
    plt.plot(predicted.predicted_mean.index, predicted_mean_clipped, label='Historical Predicted', linestyle='dashed')
    plt.plot(forecast.predicted_mean.index, forecast_mean_clipped, label='Forecasted', linestyle='dotted')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Occupancy')
    plt.show()


def MSE(df, pred_period, predicted):
    actual_values = df['Total'][-pred_period:].dropna()
    predicted_mean = predicted.predicted_mean.dropna()
    mse = mean_squared_error(actual_values, predicted_mean)
    print("Mean Squared Error (MSE):", mse)
