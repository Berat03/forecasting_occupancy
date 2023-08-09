import pandas as pd
import pmdarima as pmd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
from data_preprocessing import pre_process


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
def sarimax_apply(df, actual, pred_period):
    # using result from auto.arima
    mod = SARIMAX(endog=df,
                  order=(2, 0, 0),
                  trend='c')
    results_manual_sarima = mod.fit()

    plt.plot(df[-actual:], label='Actual')
    predicted = results_manual_sarima.get_prediction(start=-(pred_period))  # Predictions for the last 100 time units
    plt.plot(predicted.predicted_mean, label='Predicted', linestyle='dashed')
    plt.legend()
    plt.show()

    actual_values = df[-pred_period:].dropna()
    predicted_mean = predicted.predicted_mean.dropna()

    # Calculate Mean Squared Error (MSE)
    mse = mean_squared_error(actual_values, predicted_mean)
    print("Mean Squared Error (MSE):", mse)


df_resampled = pre_process(csv_data_file_path="./Data/bbtable_data.csv", resample_period='H')

df_resampled = df_resampled.iloc[:(len(df_resampled) - 450)] # Getting rid of the mainly useless (empty)  holiday data


sarimax_apply(df_resampled, 200, 150)

df_resampled = pre_process(csv_data_file_path="./Data/Bill_Bryson_Data.csv", resample_period='30T')

sarimax_apply(df_resampled, 300, 200)
