import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from data_preprocess import pre_process

"""Calculate Mean Squared Error (MSE)
actual_values = df['Total'][-pred_period:].dropna()
predicted_mean = predicted.predicted_mean.dropna()
mse = mean_squared_error(actual_values, predicted_mean)
print("Mean Squared Error (MSE):", mse)"""


# ARIMA model fitting
def find_parameters(df, col, train=0.8, cut_off=0):  # Need to make so can put df in
    df = df.iloc[:(len(df) - cut_off)]  # Getting rid of the mainly useless (empty) holiday data
    time_series_data_col = df[col].iloc[:int(len(df) * train)]
    results_auto_arima = pmd.auto_arima(time_series_data_col,
                                        start_p=0,
                                        start_d=0,
                                        start_q=0,
                                        start_P=0,
                                        start_Q=0,
                                        trend='c',
                                        seasonal=True,
                                        m=24,
                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore',
                                        njobs = -1,
                                        )

    print(results_auto_arima)


# Apply ARIMA and print results
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarimax_apply(df, pred_period, forecast_periods, cut_off=0, *args, **kwargs):
    df = df.iloc[:(len(df) - cut_off)]

    mod = SARIMAX(endog=df['Total'],
                  exog=df['Weekend'],
                  order=(4, 1, 1),
                  seasonal_order=(3, 0, 1, 24),
                  trend='c')

    results = mod.fit(maxiter=10)

    # For forecast, create an array of the same shape as forecast_periods
    exog_forecast = df['Weekend'][-forecast_periods:].values.reshape(-1, 1)

    predicted = results.get_prediction(start=-pred_period, exog=df['Weekend'])
    forecast = results.get_forecast(steps=forecast_periods, exog=exog_forecast)

    plt.plot(df.index[-pred_period:], df['Total'][-pred_period:], label='Actual (Historical and Forecasted)')
    plt.plot(predicted.predicted_mean.index, predicted.predicted_mean, label='Historical Predicted', linestyle='dashed')
    plt.plot(forecast.predicted_mean.index, forecast.predicted_mean, label='Forecasted', linestyle='dotted')

    plt.legend()
    plt.xlabel('Date')
    plt.ylabel('Occupancy')
    plt.show()

# Usage


# Example usage



df1 = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv', resample_period='H')
sarimax_apply(df=df1, pred_period=72, forecast_periods=72, cut_off=100)

#find_parameters(df=df1, col='Total', cut_off=0)
