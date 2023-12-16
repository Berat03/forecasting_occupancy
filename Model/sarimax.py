import pandas as pd
import pmdarima as pmd
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.eval_measures import rmse
from statsmodels.graphics.tsaplots import plot_pacf, plot_acf
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose



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
def find_parameters(df, col, exog_var=None, train=0.8, cut_off=0, m=24, seasonality=True):
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
                                        d= 0,
                                        D= 0,
                                        start_q=0,
                                        start_P=0,
                                        start_Q=0,
                                        trend='c',
                                        seasonal=seasonality,
                                        m=m,
                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore',
                                        njobs=-1,
                                        )

    print(results_auto_arima)


def sarimax_apply(df, pred_period, forecast_periods, order, seasonal_order, cut_off=0, *args, **kwargs):
    df = df.iloc[:(len(df) - cut_off)]

    mod = SARIMAX(endog=df['Total'],
                  exog=df['Weekend'],
                  order=order,  # 1, 0, 0
                  seasonal_order=seasonal_order,  # 1, 0, 0, 24
                  trend='c')

    results = mod.fit(maxiter=100)

    exog_forecast = df['Weekend'][-forecast_periods:].values.reshape(-1, 1)

    predicted = results.get_prediction(start=-pred_period, exog=df['Weekend'])
    forecast = results.get_forecast(steps=forecast_periods, exog=exog_forecast)

    predicted_mean_clipped = np.clip(predicted.predicted_mean, 0, 1800) # Occupancy [0, 1800]
    forecast_mean_clipped = np.clip(forecast.predicted_mean, 0, 1800)

    plt.plot(df.index[-pred_period:], df['Total'][-pred_period:], label='Actual')
    plt.plot(predicted.predicted_mean.index, predicted_mean_clipped, label='Predicted', linestyle='dotted')
    plt.plot(forecast.predicted_mean.index, forecast_mean_clipped, label='Forecasted', linestyle='dotted')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Occupancy')
    plt.show()

    print(rmse(predicted_mean_clipped, df['Total'][-pred_period:]))
def MSE(df, pred_period, predicted):
    actual_values = df['Total'][-pred_period:].dropna()
    predicted_mean = predicted.predicted_mean.dropna()
    mse = mean_squared_error(actual_values, predicted_mean)
    print("Mean Squared Error (MSE):", mse)

def acf_plots(df, col='Total', m=24):
    fig, axes = plt.subplots(3, 2, figsize=(12, 12))

    plot_acf(df[col], ax=axes[0, 0], title='ACF - Original')
    plot_pacf(df[col], ax=axes[0, 1], title='PACF - Original')

    df_diff = df.diff().dropna()
    plot_acf(df_diff[col], ax=axes[1, 0], title='ACF - Differenced')
    plot_pacf(df_diff[col], ax=axes[1, 1], title='PACF - Differenced')
    df_diff_season = df.diff(m).dropna()

    plot_acf(df_diff_season[col], ax=axes[2, 0], title='ACF - Seasonally Differenced')
    plot_pacf(df_diff_season[col], ax=axes[2, 1], title='PACF - Seasonal;y Differenced')
    plt.tight_layout()
    plt.show()
def seasonal_plot(df):
    fig = seasonal_decompose(df).plot()
    fig.set_size_inches((16, 9))
    fig.tight_layout()
    plt.show()