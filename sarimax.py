import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from data_query_and_preprocessing import pre_process


# ARIMA model fitting
def find_parameters(time_series_data_col):
    results_auto_arima = pmd.auto_arima(time_series_data_col,
                                        start_p=0,
                                        start_d=0,
                                        start_q=0,
                                        max_p=2,
                                        max_d=2,
                                        max_q=2,
                                        trend='c',
                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore')

    print(results_auto_arima)


# Apply ARIMA and print results
def sarimax_apply(csv_data_file_path, resample_period, actual, pred_period, cut_off=0):
    df = pre_process(csv_data_file_path=csv_data_file_path, resample_period=resample_period)
    df = df.iloc[:(len(df) - cut_off)]  # Getting rid of the mainly useless (empty)  holiday data

    # using result from auto.arima
    mod = SARIMAX(endog=df['Total'],
                  order=(2, 0, 0),
                  trend='c')
    results_manual_sarima = mod.fit()

    plt.plot(df['Total'][-actual:], label='Actual')
    predicted = results_manual_sarima.get_prediction(start=-(pred_period))  # Predictions for the last 100 time units
    plt.plot(predicted.predicted_mean, label='Predicted', linestyle='dashed')
    plt.legend()
    plt.show()

    actual_values = df['Total'][-pred_period:].dropna()
    predicted_mean = predicted.predicted_mean.dropna()

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(actual_values, predicted_mean)
    print("Mean Squared Error (MSE):", mse)


sarimax_apply(csv_data_file_path='./Data/Bill_Bryson_Data.csv',
              resample_period='30T', actual=300, pred_period=200, cut_off=100)
sarimax_apply(csv_data_file_path='./Data/bbtable_data.csv',
              resample_period='H', actual=200, pred_period=150, cut_off=400)
