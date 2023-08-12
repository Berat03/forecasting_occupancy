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
def find_parameters(df, col, train=0.8): # Need to make so can put df in
    time_series_data_col = df[col].iloc[:int(len(df) *train)]
    results_auto_arima = pmd.auto_arima(time_series_data_col,
                                        start_p=0,
                                        start_d=0,
                                        start_q=0,
                                        max_p=10,
                                        max_d=10,
                                        max_q=10,
                                        trend='c',
                                        # add sarima modelling

                                        information_criterion='aic',
                                        trace=True,
                                        error_action='ignore')

    print(results_auto_arima)

# Apply ARIMA and print results
def sarimax_apply(df, actual, pred_period, forecast_periods, cut_off=0):
    df = df.iloc[:(len(df) - cut_off)]  # Getting rid of the mainly useless (empty) holiday data

    # using result from auto.arima
    mod = SARIMAX(endog=df['Total'],
                  order=(7, 1, 4),
                  trend='c', )

    # Fit the SARIMAX model
    results = mod.fit()

    # Get predictions for historical data and forecasted data
    predicted = results.get_prediction(start=-pred_period)
    forecast = results.get_forecast(steps=forecast_periods)

    # Plot historical and forecasted values
    plt.plot(df.index[-actual:], df['Total'][-actual:], label='Historical Actual')
    plt.plot(predicted.predicted_mean.index, predicted.predicted_mean, label='Historical Predicted', linestyle='dashed')
    plt.plot(forecast.predicted_mean.index, forecast.predicted_mean, label='Forecasted', linestyle='dotted')
    plt.legend()
    plt.title('Actual vs Predicted vs Forecasted Values')
    plt.xlabel('Time')
    plt.ylabel('Value')
    plt.show()


#sarimax_apply(df = pre_process(csv_data_file_path='./Data/bbtable_data.csv',resample_period='H'), actual=300,
              #pred_period=120, forecast_periods=100, cut_off=1300)
#find_parameters(df = pre_process(csv_data_file_path='./Data/bbtable_data.csv', resample_period='H'), col= 'Total' )



