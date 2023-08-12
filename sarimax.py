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
                                        max_p=10,
                                        max_d=10,
                                        max_q=10,
                                        trend='c',
                                        seasonal=True,
                                        m=24,
                                        # add sarima modelling

                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore')

    print(results_auto_arima)


# Apply ARIMA and print results
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX

def sarimax_apply(df, pred_period, forecast_periods, cut_off=0, *args, **kwargs):
    df = df.iloc[:(len(df) - cut_off)]

    mod = SARIMAX(endog=df['Total'],
                  order=(4, 1, 1),
                  seasonal_order=(3, 0, 1, 24),
                  trend='c')

    results = mod.fit(maxiter=100)

    predicted = results.get_prediction(start=-pred_period)
    forecast = results.get_forecast(steps=forecast_periods)

    plt.plot(df.index[-pred_period:], df['Total'][-pred_period:], label='Actual (Historical and Forecasted)')
    plt.plot(predicted.predicted_mean.index, predicted.predicted_mean, label='Historical Predicted', linestyle='dashed')
    plt.plot(forecast.predicted_mean.index, forecast.predicted_mean, label='Forecasted', linestyle='dotted')

    plt.legend()
    plt.title('Actual vs Predicted vs Forecasted Values')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.show()

# Example usage
# sarimax_apply(df, pred_period=30, forecast_periods=10, cut_off=0)



df1 = pre_process(csv_data_file_path='./Data/Bill_Bryson_Data.csv', resample_period='H').iloc[:-300]

sarimax_apply(df=df1, actual=72,
              pred_period=72, forecast_periods=60, cut_off=72)
#find_parameters(df=df1, col='Total', cut_off=72)
